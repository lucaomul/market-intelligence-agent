AI Market Intelligence & Strategic Research Agent
An autonomous research agent designed to crawl, scrape, and analyze market trends using LLMs. Unlike simple news aggregators, this tool performs deep content extraction to provide structured business intelligence.

Core Features
Deep Scraping: Instead of analyzing just headlines or snippets, the agent visits the source URL to extract the full article body.

Structured Intelligence: Utilizes OpenAI's JSON mode for consistent data mapping and reliable output.

Risk & Sentiment Scoring: Quantifies market sentiment and identifies potential risks for business stakeholders.

Dual Reporting: Generates professional Excel reports for end-users and raw JSON files for technical integrations.

Technical Stack
Language: Python 3.12 (Optimized for M4 Apple Silicon)

AI Engine: OpenAI GPT-4o API

Libraries: newspaper3k, pandas, requests, openpyxl

Architecture: Object-Oriented (OOP) for scalability.

Installation & Setup
1. Install Dependencies

pip install openai requests pandas openpyxl newspaper3k lxml_html_clean

2. Configuration

Open market_intelligence.py and provide your API credentials:
OPENAI_KEY = "your_openai_key_here"
NEWS_API_KEY = "your_news_api_key_here"

3. Run the Agent

python3 market_intelligence.py

Output Data Points
The agent populates the following fields in the generated reports:

Credibility Score: AI's evaluation of the source content and depth.

Market Sentiment: Bullish, Bearish, or Neutral assessment.

Strategic Outlook: Long-term perspective and trend predictions.

Risk Factors: Potential threats or downsides identified in the text.

Executive Summary: A concise brief designed for high-level decision-makers.

Maintained by Luca Craciun.