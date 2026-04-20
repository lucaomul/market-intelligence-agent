import streamlit as st
import openai
import requests
import pandas as pd
import json
import io
from newspaper import Article
from datetime import datetime
from typing import Optional

# ── CONFIGURAȚIE PAGINĂ ──────────────────────────────────────────
st.set_page_config(
    page_title="MIA | Market Intelligence Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS PENTRU MIA (SIDEBAR NATIV & TEXT LIZIBIL) ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

/* Fundalul general */
.stApp {
    background-color: #0a0a0f !important;
    color: #e2e2e2;
    font-family: 'IBM Plex Sans', sans-serif;
}

/* SIDEBAR NATIV - MIA THEME */
[data-testid="stSidebar"] {
    background-color: #0d0d16 !important;
    border-right: 1px solid #1a1a2e;
}

/* LOGO & VERSION */
.sidebar-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #00ff88;
    letter-spacing: 0.3em;
    margin-bottom: 0.2rem;
}
.sidebar-version {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #555577;
    margin-bottom: 2rem;
}

/* TITLURI SECȚIUNI SIDEBAR */
.sidebar-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #ffffff !important;
    font-weight: 600;
    text-transform: uppercase;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    border-left: 3px solid #00ff88;
    padding-left: 10px;
}

/* INPUT LABELS */
label p {
    color: #aaaacc !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* BUTON EXECUTE */
.stButton > button {
    background: #00ff88 !important;
    color: #0a0a0f !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    letter-spacing: 1px !important;
}

/* FOOTER SIDEBAR */
.sidebar-footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #1a1a2e;
    font-family: 'IBM Plex Mono', monospace;
}
.empowered-text {
    font-size: 0.75rem;
    color: #8888aa;
    margin-bottom: 10px;
}
.social-link {
    display: block;
    font-size: 0.7rem;
    color: #00ff88;
    text-decoration: none;
    margin-bottom: 5px;
}
.social-link:hover {
    text-decoration: underline;
}

/* CARDURI REZULTATE */
.article-card {
    background: #11111d;
    border: 1px solid #1a1a2e;
    border-left: 5px solid #00ff88;
    padding: 25px;
    margin-bottom: 20px;
    border-radius: 8px;
}
.article-card.bearish { border-left-color: #ff4466; }
.article-card.neutral { border-left-color: #ffaa00; }

.risk-tag {
    display: inline-block;
    background: rgba(255, 68, 102, 0.1);
    border: 1px solid #ff4466;
    color: #ff4466;
    font-size: 0.65rem;
    padding: 2px 8px;
    margin-right: 6px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
}

.main-title {
    font-family: 'IBM Plex Mono', monospace;
    color: #00ff88;
    font-size: 1.3rem;
    letter-spacing: 2px;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ── LOGICA MIA ───────────────────────────────────────────────────
class MarketIntelligenceAgent:
    def __init__(self, openai_key: str, news_api_key: str):
        self.client = openai.OpenAI(api_key=openai_key)
        self.news_api_key = news_api_key

    def fetch_news(self, query: str, n: int = 5):
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize={n}&apiKey={self.news_api_key}"
        try:
            r = requests.get(url, timeout=10).json()
            return r.get("articles", [])
        except: return []

    def scrape_and_analyze(self, art):
        try:
            content = art.get('description', '')
            try:
                scr = Article(art['url'])
                scr.download(); scr.parse()
                if len(scr.text) > 200: content = scr.text
            except: pass

            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Analyze market news. Return JSON only."},
                    {"role": "user", "content": f"Analyze: {content[:4000]}"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(resp.choices[0].message.content)
        except: return None

# ── SESSION & HELPERS ───────────────────────────────────────────
if "results" not in st.session_state: st.session_state.results = []

def to_excel(data):
    df = pd.DataFrame(data)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as w:
        df.to_excel(w, index=False)
    return buf.getvalue()

# ── SIDEBAR (CONTROALE MIA) ──────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">⬡ MIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-version">MARKET INTEL AGENT v2.0</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">Auth Tokens</div>', unsafe_allow_html=True)
    o_key = st.text_input("OpenAI Key", type="password")
    n_key = st.text_input("NewsAPI Key", type="password")
    
    st.markdown('<div class="sidebar-section">Target Parameters</div>', unsafe_allow_html=True)
    q = st.text_input("Search Topic", placeholder="Tesla, AI Trends...")
    n = st.number_input("Source Depth", 1, 10, 5)
    
    # MODIFICARE: Butonul se numește acum doar EXECUTE
    if st.button("▶ EXECUTE", use_container_width=True):
        if o_key and n_key and q:
            with st.status("Gathering Intelligence...") as status:
                agent = MarketIntelligenceAgent(o_key, n_key)
                articles = agent.fetch_news(q, n)
                results = []
                for a in articles:
                    analysis = agent.scrape_and_analyze(a)
                    if analysis: results.append({**a, **analysis})
                st.session_state.results = results
                status.update(label="Complete!", state="complete")
                st.rerun()
        else:
            st.error("Missing credentials.")

    if st.session_state.results:
        st.markdown('<div class="sidebar-section">Data Export</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download Report (.xlsx)", data=to_excel(st.session_state.results), file_name="MIA_Report.xlsx", use_container_width=True)

    # MODIFICARE: Footer cu credite și link-uri
    st.markdown(f"""
    <div class="sidebar-footer">
        <div class="empowered-text">Empowered by Luca Crăciun</div>
        <a href="https://github.com/lucaomul" target="_blank" class="social-link"> GitHub</a>
        <a href="https://www.linkedin.com/in/gabriel-luca-craciun-25ba95295" target="_blank" class="social-link"> LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN TERMINAL ────────────────────────────────────────────────
st.markdown('<div class="main-title">INTEL TERMINAL [MIA]</div>', unsafe_allow_html=True)

if not st.session_state.results:
    st.info("System Standby. Awaiting parameters from the sidebar to begin analysis.")
else:
    for r in st.session_state.results:
        sentiment = r.get('market_sentiment', 'Neutral')
        cls = sentiment.lower()
        color = "#00ff88" if cls == "bullish" else "#ff4466" if cls == "bearish" else "#ffaa00"
        
        st.markdown(f"""
        <div class="article-card {cls}">
            <div style="font-size:1.2rem; font-weight:600; color:#ffffff; margin-bottom:10px;">{r['title']}</div>
            <div style="font-family:IBM Plex Mono; font-size:0.75rem; color:#8888aa; margin-bottom:15px;">
                {r.get('source', {}).get('name', 'Unknown')} &nbsp;·&nbsp; 
                SENTIMENT: <span style="color:{color}">{sentiment.upper()}</span>
            </div>
            <p style="color:#9999bb; font-size:0.95rem; line-height:1.6;">{r.get('executive_summary', '')}</p>
            <div style="margin-top:10px;">
                {" ".join([f'<span class="risk-tag">{risk}</span>' for risk in r.get('risk_factors', [])])}
            </div>
        </div>
        """, unsafe_allow_html=True)