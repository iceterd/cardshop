"""Shared CSS injected on every page."""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700;1,9..40,400&family=Space+Mono:wght@400;700&display=swap');

:root {
    --primary: #FF6B35;
    --primary-dark: #E85A2A;
    --secondary: #004E89;
    --accent: #00B4D8;
    --success: #2DC653;
    --warning: #FFB703;
    --dark: #1A1A2E;
    --dark-card: #16213E;
    --dark-surface: #0F3460;
    --light-text: #E8E8E8;
    --muted: #8D99AE;
}

.stApp {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
    font-family: 'DM Sans', sans-serif;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F3460 0%, #1A1A2E 100%);
    border-right: 1px solid rgba(255, 107, 53, 0.2);
}

.hero-banner {
    background: linear-gradient(135deg, #FF6B35 0%, #E85A2A 40%, #004E89 100%);
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 30px;
}
.hero-banner h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    color: white;
    margin: 0;
    line-height: 1.1;
}
.hero-banner p { color: rgba(255,255,255,0.85); font-size: 1.15rem; margin-top: 12px; }

.product-card {
    background: linear-gradient(145deg, #16213E, #1A1A2E);
    border: 1px solid rgba(255, 107, 53, 0.15);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
    height: 100%;
}
.product-card:hover {
    border-color: var(--primary);
    box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
    transform: translateY(-2px);
}
.product-card .card-icon  { font-size: 2.5rem; margin-bottom: 12px; }
.product-card h3 { color: white; font-family: 'Space Mono', monospace; font-size: 1.1rem; margin: 8px 0; }
.product-card p  { color: var(--muted); font-size: 0.9rem; line-height: 1.5; }
.product-card .price {
    color: var(--primary);
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    margin-top: 12px;
}

.metric-card {
    background: linear-gradient(145deg, #16213E, #1A1A2E);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-card .value { font-family: 'Space Mono', monospace; font-size: 1.8rem; color: var(--primary); font-weight: 700; }
.metric-card .label { color: var(--muted); font-size: 0.85rem; margin-top: 4px; }

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.status-success { background: rgba(45,198,83,0.15); color: #2DC653; border: 1px solid rgba(45,198,83,0.3); }
.status-pending { background: rgba(255,183,3,0.15); color: #FFB703; border: 1px solid rgba(255,183,3,0.3); }
.status-failed  { background: rgba(255,80,80,0.15); color: #FF5050; border: 1px solid rgba(255,80,80,0.3); }

.section-header {
    font-family: 'Space Mono', monospace;
    color: white;
    font-size: 1.5rem;
    margin: 30px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--primary);
    display: inline-block;
}

.txn-row {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.txn-row .txn-info h4 { color: white; margin: 0; font-size: 0.95rem; }
.txn-row .txn-info p  { color: var(--muted); margin: 2px 0 0 0; font-size: 0.8rem; }

.stButton > button {
    background: linear-gradient(135deg, #FF6B35, #E85A2A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: var(--muted) !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #16213E !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}
.stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label {
    color: var(--muted) !important;
}

.stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    color: var(--muted);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35, #E85A2A) !important;
    color: white !important;
    border-color: transparent !important;
}

.chat-container {
    background: linear-gradient(145deg, #16213E, #1A1A2E);
    border: 1px solid rgba(0,180,216,0.2);
    border-radius: 16px;
    padding: 20px;
    max-height: 420px;
    overflow-y: auto;
}
.chat-msg { padding: 10px 16px; border-radius: 12px; margin: 8px 0; max-width: 80%; font-size: 0.9rem; line-height: 1.5; }
.chat-bot  { background: rgba(0,180,216,0.1); border: 1px solid rgba(0,180,216,0.2); color: var(--light-text); margin-right: auto; }
.chat-user { background: rgba(255,107,53,0.15); border: 1px solid rgba(255,107,53,0.2); color: var(--light-text); margin-left: auto; text-align: right; }

.whatsapp-btn {
    display: inline-block;
    background: #25D366;
    color: white !important;
    padding: 12px 28px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
}

.wallet-card {
    background: linear-gradient(135deg, #FF6B35, #E85A2A);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    text-align: center;
}
.wallet-label  { color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
.wallet-amount { font-family: 'Space Mono', monospace; font-size: 1.8rem; color: white; font-weight: 700; }

.app-footer {
    text-align: center;
    padding: 30px 0 10px 0;
    color: var(--muted);
    font-size: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 40px;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
