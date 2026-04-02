"""Home page — hero, stats, popular gift cards, value props."""

import streamlit as st
from utils.db import get_transaction_stats
from utils.constants import GIFT_CARDS


def render(user_id: int, user: dict):
    first_name = user["full_name"].split()[0]

    st.markdown(f"""
    <div class="hero-banner">
        <h1>Welcome back,<br>{first_name}! 👋</h1>
        <p>Airtime top-ups, gift cards & crypto payments — delivered instantly, supported always.</p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_transaction_stats(user_id)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{stats['total_orders']}</div>
            <div class="label">Orders Placed</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">${stats['total_spent']:.0f}</div>
            <div class="label">Total Spent</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="value">8</div>
            <div class="label">Countries Supported</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="value">24/7</div>
            <div class="label">Live Support</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔥 Popular Gift Cards</div>', unsafe_allow_html=True)
    popular = [gc for gc in GIFT_CARDS if gc["popular"]]
    cols = st.columns(4)
    for idx, gc in enumerate(popular[:8]):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="product-card">
                <div class="card-icon">{gc['icon']}</div>
                <h3>{gc['name']}</h3>
                <p>{gc['category']}</p>
                <div class="price">From ${min(gc['denominations'])}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Why Cardshop?</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="product-card">
            <div class="card-icon">⚡</div>
            <h3>Instant Delivery</h3>
            <p>Get your codes and top-ups within seconds of payment confirmation. No waiting, no delays.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="product-card">
            <div class="card-icon">🛡️</div>
            <h3>Secure & Trusted</h3>
            <p>Encrypted transactions, verified codes, and a money-back guarantee on every purchase.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="product-card">
            <div class="card-icon">🤝</div>
            <h3>Real Human Support</h3>
            <p>Live chat, WhatsApp, and AI assistant — we're here 24/7. No bots that go in circles.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="app-footer">
        © 2026 Cardshop · Airtime · Gift Cards · Crypto Payments
    </div>
    """, unsafe_allow_html=True)
