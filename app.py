"""
Cardshop — Main entry point
Handles auth gate, sidebar navigation, and page routing.
"""

import streamlit as st
from utils.db import init_db, get_wallet_balance, update_wallet, add_transaction
from utils.auth import render_auth_page, is_logged_in, get_current_user, logout_user
from utils.styles import inject_css
from utils.constants import generate_order_id
from utils.reloadly import reloadly_status

# ── Page config (must be first Streamlit call) ────────────────────────────────────
st.set_page_config(
    page_title="Cardshop",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialise DB & CSS ─────────────────────────────────────────────────────
if "db_initialised" not in st.session_state:
    init_db()
    st.session_state["db_initialised"] = True
inject_css()

# ── Auth gate ───────────────────────────────────────────────────────────────
if not is_logged_in():
    render_auth_page()
    st.stop()

user = get_current_user()
user_id = user["id"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <h1 style='font-size:2rem; margin:0;'>🛒</h1>
        <h2 style='font-size:1.2rem; margin:0; color:#FF6B35;'>Cardshop</h2>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Live wallet balance
    wallet_bal = get_wallet_balance(user_id)
    st.markdown(f"""
    <div class='wallet-card'>
        <div class='wallet-label'>Wallet Balance</div>
        <div class='wallet-amount'>${wallet_bal:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡ Fund Wallet", use_container_width=True, key="sidebar_fund"):
        st.session_state["active_page"] = "💳 Payments"
        st.rerun()
    st.divider()

    pages = [
        ("🏠 Home",            "🏠 Home"),
        ("📱 Airtime & Data", "📱 Airtime & Data"),
        ("🎁 Gift Cards",     "🎁 Gift Cards"),
        ("💳 Payments",       "💳 Payments"),
        ("📊 My Orders",      "📊 My Orders"),
        ("💬 Support",        "💬 Support"),
    ]
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "🏠 Home"

    for label, page_key in pages:
        active = st.session_state["active_page"] == page_key
        btn_type = "primary" if active else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
            st.session_state["active_page"] = page_key
            st.rerun()

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.8rem; color:#888; text-align:center;'>
        👤 {user['full_name']}<br>
        <span style='font-size:0.7rem;'>{user['email']}</span>
    </div>
    """, unsafe_allow_html=True)

    status = reloadly_status()
    colour = "#4CAF50" if status["connected"] else "#FF9800"
    st.markdown(f"""
    <div style='font-size:0.75rem; color:{colour}; text-align:center; margin-top:0.5rem;'>
        ● Reloadly: {status['message']}
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
        logout_user()
        st.rerun()

# ── Page routing ─────────────────────────────────────────────────────────────────
page = st.session_state.get("active_page", "🏠 Home")

if page == "🏠 Home":
    from pages.home import render
    render(user_id, user)

elif page == "📱 Airtime & Data":
    from pages.airtime import render
    render(user_id)

elif page == "🎁 Gift Cards":
    from pages.gift_cards import render
    render(user_id)

elif page == "💳 Payments":
    from pages.payments import render
    render(user_id)

elif page == "📊 My Orders":
    from pages.orders import render
    render(user_id)

elif page == "💬 Support":
    from pages.support import render
    render(user_id)

else:
    from pages.home import render
    render(user_id, user)
