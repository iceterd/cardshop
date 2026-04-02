"""My Orders page — persistent transaction history from the database."""

import streamlit as st
from utils.db import get_transactions, get_transaction_stats
from utils.constants import TXN_ICONS


def render(user_id: int):
    st.markdown('<div class="section-header">📊 Order History</div>', unsafe_allow_html=True)

    transactions = get_transactions(user_id)

    if not transactions:
        st.markdown("""
        <div class="product-card" style="text-align:center; padding:40px;">
            <div class="card-icon">💭</div>
            <h3>No transactions yet</h3>
            <p>Your order history will appear here once you make your first purchase.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    stats = get_transaction_stats(user_id)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{stats['total_transactions']}</div>
            <div class="label">Total Transactions</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{stats['total_orders']}</div>
            <div class="label">Orders Placed</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">${stats['total_spent']:.2f}</div>
            <div class="label">Total Spent</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        txn_types   = ["All"] + sorted(set(t["type"] for t in transactions))
        filter_type = st.selectbox("Filter by type", txn_types, key="ord_filter")
    with col_f2:
        filter_status = st.selectbox("Status", ["All", "Completed", "Pending", "Failed"], key="ord_status")

    filtered = transactions
    if filter_type != "All":
        filtered = [t for t in filtered if t["type"] == filter_type]
    if filter_status != "All":
        filtered = [t for t in filtered if t["status"] == filter_status]

    if not filtered:
        st.info("No transactions match the selected filters.")
        return

    for txn in filtered:
        status_class = {
            "Completed": "status-success",
            "Pending":   "status-pending",
            "Failed":    "status-failed",
        }.get(txn["status"], "status-pending")

        icon = TXN_ICONS.get(txn["type"], "📄")
        date_str = txn["created_at"][:16] if txn["created_at"] else "—"

        is_deposit = txn["type"] in ("Wallet", "Crypto Deposit", "PayPal Deposit")
        amount_color = "#2DC653" if is_deposit else "#FF6B35"
        amount_prefix = "+" if is_deposit else "-"

        st.markdown(f"""
        <div class="txn-row">
            <div class="txn-info">
                <h4>{icon} {txn['description']}</h4>
                <p>{txn['order_id']} · {date_str}</p>
            </div>
            <div style="text-align:right;">
                <span class="status-badge {status_class}">{txn['status']}</span>
                <div style="font-family:'Space Mono',monospace; color:{amount_color}; font-weight:700; margin-top:4px;">
                    {amount_prefix}${txn['amount']:.2f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
