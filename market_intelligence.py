import openai
import requests
import pandas as pd
import json
from newspaper import Article
from datetime import datetime

# ==========================================================
# AI STRATEGIC RESEARCH AGENT (v3.0)
# Professional Edition | Focus: Deep Data Extraction
# ==========================================================

# Configuration
OPENAI_KEY = "your_openai_key_here"
NEWS_API_KEY = "your_news_api_key_here"

client = openai.OpenAI(api_key=OPENAI_KEY)

class StrategicResearchAgent:
    """An autonomous agent that scrapes full web articles and performs 
    deep C-suite level business analysis."""
    
    def __init__(self, search_query):
        self.search_query = search_query
        self.research_results = []

    def fetch_trending_news(self):
        """Retrieves high-relevancy news links via API."""
        print(f"[*] Initiating global search for: {self.search_query}...")
        url = f"https://newsapi.org/v2/everything?q={self.search_query}&language=en&sortBy=relevancy&pageSize=5&apiKey={NEWS_API_KEY}"
        try:
            response = requests.get(url).json()
            return response.get('articles', [])
        except Exception as e:
            print(f"[!] API Connection Error: {e}")
            return []

    def scrape_full_content(self, url):
        """Bypasses snippets to extract the full body text of the article."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception:
            return None

    def perform_deep_analysis(self, full_text, title):
        """Uses GPT-4o to analyze full-text content for strategic insights."""
        print(f" -> Agent performing deep dive on: {title[:50]}...")
        
        prompt = f"""
        ROLE: Senior Strategic Investment Analyst.
        INPUT: Full article text provided below.
        
        TASK: Conduct a comprehensive business impact analysis.
        
        ARTICLE CONTENT: {full_text[:6000]} 
        
        OUTPUT REQUIREMENT: Return ONLY a valid JSON object with these keys:
        {{
            "credibility_rating": "1-10",
            "market_sentiment": "Bullish/Bearish/Neutral",
            "immediate_impact": "Short-term business consequence",
            "strategic_outlook": "Long-term trend prediction",
            "risk_factors": ["risk1", "risk2"],
            "executive_summary": "High-level summary for CEO/Board"
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional research engine that outputs structured JSON data."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"    [!] AI Analysis failed for: {title[:20]} - {e}")
            return None

    def execute_workflow(self):
        """Coordinates the end-to-end research pipeline."""
        articles = self.fetch_trending_news()
        
        if not articles:
            print("[-] No news data found. Pipeline aborted.")
            return

        for entry in articles:
            # Step 1: Get the full story
            content = self.scrape_full_content(entry['url'])
            
            # Step 2: Fallback to description if scraping is blocked
            text_to_process = content if content and len(content) > 300 else entry['description']
            
            if text_to_process:
                analysis = self.perform_deep_analysis(text_to_process, entry['title'])
                if analysis:
                    self.research_results.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Headline": entry['title'],
                        "URL": entry['url'],
                        **analysis
                    })
        
        self.export_results()

    def export_results(self):
        """Saves findings into professional formats."""
        if not self.research_results:
            return

        df = pd.DataFrame(self.research_results)
        file_id = datetime.now().strftime("%H%M")
        excel_name = f"Strategic_Report_{file_id}.xlsx"
        
        df.to_excel(excel_name, index=False)
        
        with open("research_data.json", "w") as f:
            json.dump(self.research_results, f, indent=4)
            
        print(f"\n" + "="*60)
        print(f"[SUCCESS] Research Mission Completed.")
        print(f"-> Strategic Excel Report: {excel_name}")
        print(f"-> Developer JSON Export: research_data.json")
        print("="*60)

if __name__ == "__main__":
    # You can customize your target market query here
    research_agent = StrategicResearchAgent(search_query="Future of AI in Finance")
    research_agent.execute_workflow()