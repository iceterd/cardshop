"""Gift Cards marketplace page."""

import random
import time
import streamlit as st
from utils.db import get_wallet_balance, update_wallet, add_transaction
from utils.constants import GIFT_CARDS, generate_order_id


def render(user_id: int):
    st.markdown('<div class="section-header">🎁 Gift Card Marketplace</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search = st.text_input("🔍 Search gift cards", placeholder="e.g. Steam, Netflix, Amazon...")
    with col2:
        categories = ["All"] + sorted(set(gc["category"] for gc in GIFT_CARDS))
        selected_cat = st.selectbox("Category", categories)
    with col3:
        sort_by = st.selectbox("Sort", ["Popular", "A-Z", "Price ↑", "Price ↓"])

    filtered = GIFT_CARDS.copy()
    if search:
        filtered = [gc for gc in filtered if search.lower() in gc["name"].lower()]
    if selected_cat != "All":
        filtered = [gc for gc in filtered if gc["category"] == selected_cat]
    if sort_by == "A-Z":
        filtered.sort(key=lambda x: x["name"])
    elif sort_by == "Price ↑":
        filtered.sort(key=lambda x: min(x["denominations"]))
    elif sort_by == "Price ↓":
        filtered.sort(key=lambda x: min(x["denominations"]), reverse=True)
    elif sort_by == "Popular":
        filtered.sort(key=lambda x: x["popular"], reverse=True)

    if not filtered:
        st.info("No gift cards match your search. Try a different term.")
        return

    balance = get_wallet_balance(user_id)

    cols = st.columns(3)
    for idx, gc in enumerate(filtered):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <div class="card-icon">{gc['icon']}</div>
                <h3>{gc['name']}</h3>
                <p>{gc['category']}</p>
                <div class="price">From ${min(gc['denominations'])}</div>
            </div>
            """, unsafe_allow_html=True)

            denom = st.selectbox(
                "Amount",
                gc["denominations"],
                format_func=lambda x: f"${x}",
                key=f"gc_{gc['name']}",
            )

            gc_payment = st.selectbox(
                "Pay with",
                ["Wallet", "Card", "PayPal", "Crypto"],
                key=f"pay_{gc['name']}",
            )

            if st.button(f"Buy ${denom} card", key=f"buy_{gc['name']}", use_container_width=True):
                if gc_payment == "Wallet" and balance < denom:
                    st.error(f"Insufficient wallet (${balance:.2f}). Fund your wallet first.")
                else:
                    with st.spinner(f"Processing {gc['name']} gift card..."):
                        time.sleep(1)
                    mock_code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
                    order_id  = generate_order_id()

                    if gc_payment == "Wallet":
                        update_wallet(user_id, -denom)
                        balance = balance - denom

                    add_transaction(user_id, order_id, "Gift Card", f"{gc['name']} ${denom}", denom)
                    st.success(f"✅ {gc['name']} ${denom} purchased! Order: **{order_id}**")
                    st.code(f"Gift card code: {mock_code}", language=None)
                    st.caption("Code also sent to your email address on file.")

            st.markdown("")
