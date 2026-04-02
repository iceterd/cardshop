"""Cardshop — Authentication helpers
Bcrypt password hashing + session state management.
"""
import re
import streamlit as st
import bcrypt
from utils.db import create_user, get_user_by_email

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def _valid_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email.strip()))


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def is_logged_in() -> bool:
    return st.session_state.get("user_id") is not None


def get_current_user() -> dict | None:
    if not is_logged_in():
        return None
    return {
        "id": st.session_state["user_id"],
        "email": st.session_state["user_email"],
        "full_name": st.session_state["user_name"],
    }


def login_user(user_row):
    st.session_state["user_id"] = user_row["id"]
    st.session_state["user_email"] = user_row["email"]
    st.session_state["user_name"] = user_row["full_name"]


def logout_user():
    for key in ["user_id", "user_email", "user_name"]:
        st.session_state.pop(key, None)


def render_auth_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;500;700&family=Space+Mono:wght@400;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
        font-family: 'DM Sans', sans-serif;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .auth-card {
        max-width: 440px;
        margin: 60px auto 0 auto;
        background: linear-gradient(145deg, #16213E, #1A1A2E);
        border: 1px solid rgba(255,107,53,0.2);
        border-radius: 20px;
        padding: 40px 36px;
    }
    .auth-logo {
        font-family: 'Space Mono', monospace;
        color: #FF6B35;
        font-size: 2rem;
        text-align: center;
        margin-bottom: 4px;
    }
    .auth-sub {
        color: #8D99AE;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 28px;
    }
    .stTextInput label { color: #8D99AE !important; font-size: 0.85rem !important; }
    .stTextInput > div > div > input {
        background: #0F3460 !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #E85A2A) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-logo">🛒 Cardshop</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Airtime · Gift Cards · Crypto Payments</div>', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email address", placeholder="you@email.com")
            password = st.text_input("Password", type="password", placeholder="Your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                email = email.strip().lower()
                if not email or not password:
                    st.error("Please fill in both fields.")
                elif not _valid_email(email):
                    st.error("Please enter a valid email address.")
                else:
                    user = get_user_by_email(email)
                    if user and verify_password(password, user["password_hash"]):
                        login_user(user)
                        st.success(f"Welcome back, {user['full_name'].split()[0]}! 👋")
                        st.rerun()
                    else:
                        st.error("Incorrect email or password.")

    with tab_signup:
        with st.form("signup_form"):
            name = st.text_input("Full name", placeholder="Jane Doe")
            email_s = st.text_input("Email address", placeholder="you@email.com", key="su_email")
            pwd1 = st.text_input("Password", type="password", placeholder="Min. 8 characters", key="su_pwd1")
            pwd2 = st.text_input("Confirm password", type="password", placeholder="Repeat password", key="su_pwd2")
            submitted_s = st.form_submit_button("Create Account", use_container_width=True)
            if submitted_s:
                email_s = email_s.strip().lower()
                name = name.strip()
                if not all([name, email_s, pwd1, pwd2]):
                    st.error("Please fill in all fields.")
                elif not _valid_email(email_s):
                    st.error("Please enter a valid email address.")
                elif len(pwd1) < 8:
                    st.error("Password must be at least 8 characters.")
                elif pwd1 != pwd2:
                    st.error("Passwords don't match.")
                else:
                    hashed = hash_password(pwd1)
                    user_id = create_user(email_s, hashed, name)
                    if user_id:
                        user = get_user_by_email(email_s)
                        login_user(user)
                        st.success(f"Account created! Welcome, {name.split()[0]}! 🎉")
                        st.rerun()
                    else:
                        st.error("An account with that email already exists.")

    st.markdown('</div>', unsafe_allow_html=True)
    return is_logged_in()
