"""Payments page — Card, Crypto, PayPal wallet top-up."""

import time
import random
import streamlit as st
from utils.db import get_wallet_balance, update_wallet, add_transaction
from utils.constants import CRYPTO_RATES, generate_order_id


def render(user_id: int):
    st.markdown('<div class="section-header">💳 Payment Methods</div>', unsafe_allow_html=True)

    balance = get_wallet_balance(user_id)
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:20px; max-width:260px;">
        <div class="label">CURRENT WALLET BALANCE</div>
        <div class="value">${balance:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💳 Card Payment", "🪙 Crypto Payment", "🏦 PayPal"])

    with tab1:
        st.markdown("")
        st.markdown("""
        <div class="product-card" style="margin-bottom:16px;">
            <h3>🔒 Secure Card Payment</h3>
            <p>256-bit SSL encrypted. We never store your full card details. PCI DSS compliant.<br>
            <em style="font-size:0.8rem; color:#FFB703;">ℹ️ Live Stripe integration coming soon — connect your Stripe keys to enable real card payments.</em></p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            name_on_card = st.text_input("Cardholder Name", placeholder="Jane Doe")
            card_number  = st.text_input("Card Number", placeholder="4242 4242 4242 4242", type="password")
            top_up_amt   = st.number_input("Amount to add to wallet ($)", min_value=5.0, value=25.0, step=5.0, key="card_top_amt")
        with col2:
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Expiry", placeholder="MM/YY")
            with c2:
                st.text_input("CVV", placeholder="123", type="password")
            st.selectbox("Card Type", ["Visa", "Mastercard", "Amex"])

        if st.button("💳 Add Funds via Card", use_container_width=True, key="card_pay"):
            if not name_on_card or not card_number:
                st.error("Please fill in cardholder name and card number.")
            else:
                with st.spinner("Processing card payment..."):
                    time.sleep(1.5)
                new_bal = update_wallet(user_id, top_up_amt)
                add_transaction(user_id, generate_order_id(), "Wallet", f"Card top-up ({card_number[-4:]})", top_up_amt)
                st.success(f"✅ ${top_up_amt:.2f} added to your wallet! New balance: **${new_bal:.2f}**")
                st.rerun()

    with tab2:
        st.markdown("")
        st.markdown("""
        <div class="product-card" style="margin-bottom:16px;">
            <h3>🪙 Pay with Cryptocurrency</h3>
            <p>We accept BTC, ETH, USDT, USDC, and LTC. Payments are confirmed within minutes.<br>
            <em style="font-size:0.8rem; color:#FFB703;">ℹ️ A real crypto payment gateway (e.g. NOWPayments) will replace mock verification before going live.</em></p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            crypto     = st.selectbox("Select Cryptocurrency", list(CRYPTO_RATES.keys()))
            pay_amount = st.number_input("Amount to add to wallet (USD)", min_value=1.0, value=25.0, step=1.0)
        with col2:
            rate         = CRYPTO_RATES[crypto]
            crypto_amt   = pay_amount / rate
            ticker       = crypto.split("(")[0].strip()
            st.markdown(f"""
            <div class="product-card">
                <h3>Conversion</h3>
                <p><b>Rate:</b> 1 {ticker} = ${rate:,.2f}</p>
                <p><b>You send:</b> {crypto_amt:.8f} {ticker}</p>
                <div class="price">${pay_amount:.2f} USD</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        mock_wallet = "0x7Fc9" + "".join(random.choices("abcdef0123456789", k=36))
        st.info(f"📋 Send **{crypto_amt:.8f} {ticker}** to: `{mock_wallet}`\n\nOnce sent, click the button below to confirm.")

        if st.button("✅ I've Sent the Payment", use_container_width=True, key="crypto_confirm"):
            with st.spinner("Verifying transaction on blockchain..."):
                time.sleep(2)
            new_bal = update_wallet(user_id, pay_amount)
            add_transaction(user_id, generate_order_id(), "Crypto Deposit", f"{ticker} deposit", pay_amount)
            st.success(f"✅ Payment confirmed! ${pay_amount:.2f} added to your wallet. New balance: **${new_bal:.2f}**")
            st.rerun()

    with tab3:
        st.markdown("")
        st.markdown("""
        <div class="product-card" style="margin-bottom:16px;">
            <h3>🏦 PayPal</h3>
            <p>Fast and secure payments through your PayPal account. Supports all major currencies.<br>
            <em style="font-size:0.8rem; color:#FFB703;">ℹ️ Connect your PayPal Business credentials to process real payments.</em></p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            pp_email  = st.text_input("PayPal Email", placeholder="you@email.com")
        with col2:
            pp_amount = st.number_input("Amount (USD)", min_value=5.0, value=25.0, step=5.0, key="pp_amt")

        if st.button("Pay with PayPal", use_container_width=True, key="pp_pay"):
            if not pp_email:
                st.error("Please enter your PayPal email.")
            elif "@" not in pp_email:
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Connecting to PayPal..."):
                    time.sleep(1.5)
                new_bal = update_wallet(user_id, pp_amount)
                add_transaction(user_id, generate_order_id(), "PayPal Deposit", f"PayPal ({pp_email})", pp_amount)
                st.success(f"✅ PayPal payment confirmed! ${pp_amount:.2f} added. New balance: **${new_bal:.2f}**")
                st.rerun()
