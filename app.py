from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import requests
import json
import os # NEW: We need this to parse the Agent's structured output
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- API KEYS ---
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# 1. Fetch Live News (Unchanged)
@app.route('/api/news', methods=['GET'])
def get_live_news():
    try:
        category = request.args.get('category', 'business')
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        return jsonify(response.json().get('articles', []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. THE NEW AGENTIC PIPELINE (With Engagement Retuning)
@app.route('/api/briefing', methods=['POST'])
def generate_briefing():
    try:
        data = request.json
        article_text = data.get('message')
        language = data.get('language', 'English')
        user_topics = data.get('user_topics', 'General')
        user_affinities = data.get('user_affinities', []) # NEW: Catch the user's hidden interests
        
        # Build a dynamic prompt addition based on past engagement
        affinity_prompt = ""
        if user_affinities:
            affinity_prompt = f"""
            - CRITICAL ENGAGEMENT RETUNING: The user has shown high interest in these specific entities/topics recently: {', '.join(user_affinities[:10])}. 
            If any of these are relevant to the article, heavily emphasize them in your summary and impact points.
            """

        system_prompt = f"""
        You are an autonomous AI News Agent. Process the following news article through a 3-step transformation pipeline.
        
        Step 1 (Entity Extraction): Identify 3 to 5 key companies, people, or sectors.
        Step 2 (Sentiment Tagging): Classify the overall market sentiment strictly as Bullish, Bearish, or Neutral.
        Step 3 (Personalized Output & Vernacular Translation): Write a 2-sentence summary and exactly 3 bullet points on market impact.
        - Tailor the focus towards a user interested in: {user_topics}. {affinity_prompt}
        - Translate ONLY the summary and bullet points into: {language}. Ensure it is culturally adapted, not just literal.
        - IMPORTANT: Do NOT use asterisks (**) or markdown bolding in the bullet points. Use pure, plain text only.
        
        Return the output EXACTLY as a valid JSON object with these exact keys:
        "entities": (list of strings)
        "sentiment": (string)
        "summary": (string)
        "impact": (list of 3 strings)
        
        Article Text: {article_text}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=system_prompt
        )
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        parsed_json = json.loads(raw_text)
        return jsonify(parsed_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        # Clean up the output to ensure it is perfect JSON
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        parsed_json = json.loads(raw_text)
        return jsonify(parsed_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Multilingual Chat
@app.route('/api/chat', methods=['POST'])
def chat_with_article():
    try:
        data = request.json
        original_article = data.get('article')
        user_question = data.get('question')
        language = data.get('language', 'English') # Pass the language to chat too!
        
        system_prompt = f"""
        You are a helpful financial AI assistant. Read the news article provided below.
        Answer the user's question based STRICTLY on the facts in the article. 
        Respond entirely in the following language: {language}.
        
        Article Context: {original_article}
        User Question: {user_question}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=system_prompt
        )
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# 4. NEW: The Story Arc Tracker
@app.route('/api/storyarc', methods=['POST'])
def generate_story_arc():
    try:
        data = request.json
        article_text = data.get('article')
        
        system_prompt = f"""
        You are an expert News Historian and Analyst. Analyze the following news article and build a "Story Arc" JSON object.
        You must infer the broader context and history of this story.
        
        Return EXACTLY a valid JSON object with these keys:
        "timeline": (list of 3 objects, each with "date" (e.g., 'Past Month', '2023') and "event" (1 sentence))
        "contrarian": (1 short sentence explaining the opposing viewpoint or hidden risk)
        "prediction": (1 short sentence explaining what to watch for next)
        
        Article: {article_text}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=system_prompt
        )
        
        # Clean up JSON
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        parsed_json = json.loads(raw_text)
        return jsonify(parsed_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)