"""
Airtime & Data page.
Uses Reloadly for live operators/bundles when configured;
falls back to static mock data otherwise.
"""

import time
import streamlit as st
from utils.db import get_wallet_balance, update_wallet, add_transaction
from utils.constants import (
    COUNTRIES, AIRTIME_AMOUNTS, FALLBACK_OPERATORS,
    FALLBACK_DATA_PLANS, generate_order_id,
)
from utils.reloadly import (
    IS_CONFIGURED, get_operators, get_data_bundles,
    send_airtime, send_data_bundle,
)


def _validate_phone(phone: str, country_code: str) -> bool:
    """Basic phone validation: digits only, reasonable length."""
    digits = phone.replace("+", "").replace(" ", "").replace("-", "")
    return digits.isdigit() and 7 <= len(digits) <= 15


def render(user_id: int):
    st.markdown('<div class="section-header">📱 Airtime & Data Top-Up</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📞 Airtime", "📶 Data Bundle"])

    with tab1:
        st.markdown("")
        col1, col2 = st.columns(2)

        with col1:
            country_label = st.selectbox("Select Country", list(COUNTRIES.keys()), key="air_country")
            country_info  = COUNTRIES[country_label]
            iso           = country_info["iso"]

            if IS_CONFIGURED:
                with st.spinner("Loading operators..."):
                    ops_raw = get_operators(iso)
                operators = [{"id": op["operatorId"], "name": op["name"]} for op in ops_raw] if ops_raw else FALLBACK_OPERATORS.get(iso, [])
            else:
                operators = FALLBACK_OPERATORS.get(iso, [])

            op_names     = [op["name"] for op in operators]
            op_label     = st.selectbox("Select Operator", op_names, key="air_op")
            selected_op  = next((op for op in operators if op["name"] == op_label), None)

            phone = st.text_input(
                "Recipient Phone Number",
                placeholder=f"{country_info['code']} XXX XXX XXXX",
                key="air_phone",
            )

        with col2:
            amount = st.selectbox("Airtime Amount (USD)", AIRTIME_AMOUNTS, key="air_amount")
            balance = get_wallet_balance(user_id)
            payment_method = st.selectbox(
                "Payment Method",
                ["Wallet Balance", "Card (Visa/MC)", "PayPal", "Crypto (USDT)"],
                key="air_pay",
            )

            wallet_warning = ""
            if payment_method == "Wallet Balance" and balance < amount:
                wallet_warning = f'<p style="color:#FF5050; font-size:0.8rem;">⚠️ Insufficient wallet balance (${balance:.2f})</p>'

            st.markdown(f"""
            <div class="product-card" style="margin-top:10px;">
                <h3>Order Summary</h3>
                <p><b>Operator:</b> {op_label}</p>
                <p><b>Recipient:</b> {phone or '—'}</p>
                <p><b>Amount:</b> ${amount} USD</p>
                <p><b>Fee:</b> $0.00</p>
                {wallet_warning}
                <div class="price">Total: ${amount}.00</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("⚡ Send Airtime", use_container_width=True, key="send_airtime"):
            if not phone:
                st.error("Please enter a phone number.")
            elif not _validate_phone(phone, country_info["code"]):
                st.error("Please enter a valid phone number (digits only, 7–15 characters).")
            elif payment_method == "Wallet Balance" and balance < amount:
                st.error(f"Insufficient wallet balance. You have ${balance:.2f}.")
            else:
                with st.spinner("Processing your airtime top-up..."):
                    if IS_CONFIGURED and selected_op:
                        result = send_airtime(
                            operator_id=selected_op["id"],
                            phone=phone.replace(" ", "").replace("-", ""),
                            country_iso=iso,
                            amount=amount,
                        )
                    else:
                        time.sleep(1)
                        result = {"success": True, "order_id": generate_order_id(), "message": "Airtime sent (mock)."}

                if result["success"]:
                    order_id = result["order_id"] or generate_order_id()
                    if payment_method == "Wallet Balance":
                        update_wallet(user_id, -amount)
                    add_transaction(user_id, order_id, "Airtime", f"{op_label} airtime to {phone}", amount)
                    st.success(f"✅ Airtime sent successfully! Order ID: **{order_id}**")
                    st.balloons()
                else:
                    st.error(f"❌ {result['message']}")

    with tab2:
        st.markdown("")
        col1, col2 = st.columns(2)

        with col1:
            d_country_label = st.selectbox("Select Country", list(COUNTRIES.keys()), key="dat_country")
            d_country_info  = COUNTRIES[d_country_label]
            d_iso           = d_country_info["iso"]

            if IS_CONFIGURED:
                with st.spinner("Loading operators..."):
                    d_ops_raw = get_operators(d_iso)
                d_operators = [{"id": op["operatorId"], "name": op["name"]} for op in d_ops_raw] if d_ops_raw else FALLBACK_OPERATORS.get(d_iso, [])
            else:
                d_operators = FALLBACK_OPERATORS.get(d_iso, [])

            d_op_names    = [op["name"] for op in d_operators]
            d_op_label    = st.selectbox("Select Operator", d_op_names, key="dat_op")
            d_selected_op = next((op for op in d_operators if op["name"] == d_op_label), None)

            d_phone = st.text_input(
                "Recipient Phone Number",
                placeholder=f"{d_country_info['code']} XXX XXX XXXX",
                key="dat_phone",
            )

        with col2:
            if IS_CONFIGURED and d_selected_op:
                with st.spinner("Loading data plans..."):
                    live_bundles = get_data_bundles(d_selected_op["id"])
                if live_bundles:
                    bundle_options = [
                        {
                            "id": str(b.get("id") or b.get("bundleId", "")),
                            "description": b.get("description", "Unknown plan"),
                            "price": float(b.get("price", 0)),
                        }
                        for b in live_bundles
                    ]
                else:
                    bundle_options = FALLBACK_DATA_PLANS
            else:
                bundle_options = FALLBACK_DATA_PLANS

            bundle_labels = [f"{b['description']} — ${b['price']:.2f}" for b in bundle_options]
            d_bundle_label = st.selectbox("Data Plan", bundle_labels, key="dat_plan")
            d_bundle_idx   = bundle_labels.index(d_bundle_label)
            d_bundle       = bundle_options[d_bundle_idx]

            d_balance = get_wallet_balance(user_id)
            d_payment = st.selectbox(
                "Payment Method",
                ["Wallet Balance", "Card (Visa/MC)", "PayPal", "Crypto (USDT)"],
                key="dat_pay",
            )

            d_wallet_warning = ""
            if d_payment == "Wallet Balance" and d_balance < d_bundle["price"]:
                d_wallet_warning = f'<p style="color:#FF5050; font-size:0.8rem;">⚠️ Insufficient wallet balance (${d_balance:.2f})</p>'

            st.markdown(f"""
            <div class="product-card" style="margin-top:10px;">
                <h3>Order Summary</h3>
                <p><b>Plan:</b> {d_bundle['description']}</p>
                <p><b>Operator:</b> {d_op_label}</p>
                <p><b>Fee:</b> $0.00</p>
                {d_wallet_warning}
                <div class="price">Total: ${d_bundle['price']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("⚡ Buy Data Plan", use_container_width=True, key="buy_data"):
            if not d_phone:
                st.error("Please enter a phone number.")
            elif not _validate_phone(d_phone, d_country_info["code"]):
                st.error("Please enter a valid phone number.")
            elif d_payment == "Wallet Balance" and d_balance < d_bundle["price"]:
                st.error(f"Insufficient wallet balance. You have ${d_balance:.2f}.")
            else:
                with st.spinner("Processing your data bundle..."):
                    if IS_CONFIGURED and d_selected_op and d_bundle["id"] not in [b["id"] for b in FALLBACK_DATA_PLANS]:
                        result = send_data_bundle(
                            operator_id=d_selected_op["id"],
                            bundle_id=d_bundle["id"],
                            phone=d_phone.replace(" ", "").replace("-", ""),
                            country_iso=d_iso,
                        )
                    else:
                        time.sleep(1)
                        result = {"success": True, "order_id": generate_order_id(), "message": "Data bundle activated (mock)."}

                if result["success"]:
                    order_id = result["order_id"] or generate_order_id()
                    if d_payment == "Wallet Balance":
                        update_wallet(user_id, -d_bundle["price"])
                    add_transaction(user_id, order_id, "Data", f"{d_op_label} {d_bundle['description']} to {d_phone}", d_bundle["price"])
                    st.success(f"✅ Data bundle activated! Order ID: **{order_id}**")
                    st.balloons()
                else:
                    st.error(f"❌ {result['message']}")
