#  News Navigator

**Live Demo:** [https://et-news-navigator.vercel.app](https://et-news-navigator.vercel.app)

News Navigator is an intelligent, multi-agent news platform built for the ET GenAI Hackathon 2026. It replaces traditional doom-scrolling with an AI-native news experience. By leveraging Google Gemini 2.5 Flash, it autonomously fetches live breaking news, extracts key geopolitical and financial entities, analyzes market sentiment (Bullish/Bearish), and translates complex global events into a personalized intelligence briefing.

##  Key Features
* **Live Data Streams:** Real-time ingestion of global news across Finance, Tech, Sports, and Health via NewsAPI.
* **Cognitive Analysis:** Uses Gemini 2.5 Flash to generate custom intelligence briefings rather than basic summaries.
* **Interactive AI Copilot:** A built-in query interface that allows users to chat directly with the agent to ask follow-up questions and dive deeper into specific news events.
* **Multilingual Translation:** Breaking news doesn't just stay in English; the agent can culturally translate and adapt summaries into the user's preferred vernacular.
* **Story Arc Tracker:** Contextualizes breaking news by tracking how specific entities and events evolve over time.
* **Engagement Memory:** Features an upvote system that tracks user affinities via local storage to quietly retune the feed to their preferences.
* **Market Sentiment Tracking:** Automatically tags articles with Bullish, Bearish, or Neutral financial indicators.
* **Entity Extraction:** Highlights key market movers, organizations, and geopolitical figures.

##  Tech Stack
* **Frontend:** Vanilla JavaScript, HTML5, Tailwind CSS (Hosted on Vercel)
* **Backend:** Python, Flask, Flask-CORS (Hosted on Render)
* **AI Agent:** Google Gemini 2.5 Flash (via Google GenAI SDK)
* **Data Provider:** NewsAPI

##  Local Setup Instructions

To run this project locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/Dynamic3728k/et-news-navigator.git](https://github.com/Dynamic3728k/et-news-navigator.git)
cd et-news-navigator
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add your secure API keys. **(Never commit your actual keys to GitHub!)**
```text
GEMINI_API_KEY=your_google_gemini_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### 3. Install Backend Dependencies
Ensure you have Python 3 installed, then run:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask backend server:
```bash
python app.py
```
*The backend will start running on `http://127.0.0.1:5000`.*

Finally, open the `index.html` file in your preferred web browser (or use a Live Server extension) to view the frontend interface.
