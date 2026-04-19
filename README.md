# 📊 AI Market Intelligence & Strategic Research Agent

> Automated market research powered by LLMs — from raw news to structured business intelligence in seconds.

---

## 🚀 Overview

This project is an autonomous AI agent designed to **collect, analyze, and transform unstructured news data into actionable market intelligence**.

Unlike traditional aggregators that rely on headlines or summaries, this system performs **deep content extraction** and applies LLM-based reasoning to generate structured insights for business decision-making.

---

## 🧠 What It Does

* Crawls and collects real-time news data from external sources
* Extracts full article content (not just headlines)
* Processes data using LLMs to generate structured intelligence
* Outputs both **business-ready reports** and **machine-readable data**

---

## ⚙️ Core Features

### 🔍 Deep Content Extraction

* Scrapes full article bodies using `newspaper3k`
* Avoids shallow analysis based on headlines or snippets

### 🧾 Structured Intelligence (JSON Mode)

* Uses OpenAI structured outputs for consistent, reliable data mapping
* Enables downstream integrations and automation pipelines

### 📉 Risk & Sentiment Scoring

* Classifies market sentiment (Bullish / Bearish / Neutral)
* Identifies and extracts potential risk factors from text

### 📊 Dual Output System

* **Excel Reports** → for business stakeholders
* **Raw JSON Files** → for technical integrations and pipelines

---

## 🧪 Output Data Model

Each processed article generates:

* **Credibility Score** → evaluation of source quality and depth
* **Market Sentiment** → directional signal (Bullish / Bearish / Neutral)
* **Strategic Outlook** → long-term implications and trend analysis
* **Risk Factors** → extracted threats and downside scenarios
* **Executive Summary** → concise, decision-ready brief

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **AI Engine:** OpenAI GPT-4o (structured outputs / JSON mode)
* **Data Processing:** pandas
* **Scraping:** newspaper3k
* **APIs:** requests (NewsAPI integration)
* **Reporting:** openpyxl (Excel generation)
* **Architecture:** Object-Oriented Design (modular & scalable)

---

## ⚡ How It Works

1. Fetches news articles via API
2. Extracts full article content
3. Processes text using LLM (structured output mode)
4. Generates:

   * structured JSON data
   * formatted Excel reports

---

## ▶️ Getting Started

### Install dependencies

```bash id="g1k8ap"
pip install openai requests pandas openpyxl newspaper3k lxml_html_clean
```

### Configure API keys

```python id="z8h2nr"
OPENAI_KEY = "your_openai_key_here"
NEWS_API_KEY = "your_news_api_key_here"
```

### Run the agent

```bash id="y7k3lm"
python3 market_intelligence.py
```

---

## 📈 Why This Matters

Most market analysis tools:

* rely on surface-level summaries
* lack structured outputs
* require manual interpretation

This system:

* **automates the full research pipeline**
* produces **decision-ready intelligence**
* enables **integration into larger data systems**

---

## 🔮 Future Improvements

* Real-time streaming pipeline (instead of batch processing)
* Multi-source aggregation beyond NewsAPI
* Historical trend analysis & time-series tracking
* Dashboard integration (Power BI / Streamlit)
* Evaluation benchmarks vs manual research workflows

---

## 👤 Author

**Luca Craciun**
AI Automation Engineer

GitHub: https://github.com/lucaomul
LinkedIn: https://www.linkedin.com/in/gabriel-luca-craciun-25ba95295

---

## ⭐ If you find this useful

Star the repo or fork it to build your own intelligence pipelines.
