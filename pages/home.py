"""Home page — hero, stats, popular gift cards, value props."""
import os
import streamlit as st
from utils.db import get_transaction_stats
from utils.constants import GIFT_CARDS


def render(user_id: int, user: dict):
    first_name = user["full_name"].split()[0]

    # —— Sandbox / demo-mode notice ———————————————————————————————————————
    if not os.environ.get("RELOADLY_CLIENT_ID"):
        st.info(
            "🚧 **Demo mode** — Reloadly API credentials are not configured. "
            "Airtime top-ups and gift card purchases are disabled. "
            "Add `RELOADLY_CLIENT_ID` and `RELOADLY_CLIENT_SECRET` env vars to enable live transactions.",
            icon="⚠️",
        )

    st.markdown(f"""
    <div class="hero-banner">
      <h1>Welcome back,<br>{first_name}! U0001F44B</h1>
      <p>Airtime top-ups, gift cards &amp; crypto payments — delivered instantly, supported always.</p>
    </div>
    """, unsafe_allow_html=True)

    # —— Quick-action buttons ———————————————————————————————————————
    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        if st.button("U0001F4F1 Top Up Airtime", use_container_width=True):
            st.session_state["page"] = "U0001F4F1 Airtime & Data"
            st.rerun()
    with qa_col2:
        if st.button("U0001F381 Buy Gift Card", use_container_width=True):
            st.session_state["page"] = "U0001F381 Gift Cards"
            st.rerun()
    with qa_col3:
        if st.button("U0001F4B0 Pay with Crypto", use_container_width=True):
            st.session_state["page"] = "U0001F4B0 Payments"
            st.rerun()

    st.divider()

    # —— Stat cards —————————————————————————————————————————————
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
        country_count = len({gc["country"] for gc in GIFT_CARDS if gc.get("country")})
        display_count = country_count if country_count > 0 else 8
        st.markdown(f"""
    <div class="metric-card">
      <div class="value">{display_count}</div>
      <div class="label">Countries Supported</div>
    </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
    <div class="metric-card">
      <div class="value">24/7</div>
      <div class="label">Live Support</div>
    </div>""", unsafe_allow_html=True)

    # —— Popular gift cards —————————————————————————————————————
    st.markdown('<div class="section-header">U0001F525 Popular Gift Cards</div>', unsafe_allow_html=True)
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

    # —— Value props —————————————————————————————————————————————
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
      <div class="card-icon">U0001F6E1️</div>
      <h3>Secure &amp; Trusted</h3>
      <p>Encrypted transactions, verified codes, and a money-back guarantee on every purchase.</p>
    </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
    <div class="product-card">
      <div class="card-icon">U0001F91D</div>
      <h3>Real Human Support</h3>
      <p>Live chat, WhatsApp, and AI assistant — we're here 24/7. No bots that go in circles.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="app-footer">
      © 2026 Cardshop · Airtime · Gift Cards · Crypto Payments
    </div>
    """, unsafe_allow_html=True)
