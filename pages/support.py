"""Support page — AI chat, WhatsApp, email form."""

import time
import streamlit as st
from utils.constants import get_bot_response


def render(user_id: int):
    st.markdown('<div class="section-header">💬 Customer Support</div>', unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "bot", "text": "Hi! I'm the Cardshop assistant. How can I help you today?"}
        ]

    tab1, tab2, tab3 = st.tabs(["🤖 AI Chat", "💬 WhatsApp", "📧 Email Support"])

    with tab1:
        st.markdown("")

        chat_html = ""
        for msg in st.session_state.chat_messages:
            css_class = "chat-bot" if msg["role"] == "bot" else "chat-user"
            prefix    = "🤖 " if msg["role"] == "bot" else "You: "
            text = msg["text"].replace("\n", "<br>")
            chat_html += f'<div class="chat-msg {css_class}">{prefix}{text}</div>'

        st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)

        st.components.v1.html("""
        <script>
        window.parent.document.querySelectorAll('.chat-container').forEach(el => {
            el.scrollTop = el.scrollHeight;
        });
        </script>
        """, height=0)

        col1, col2 = st.columns([5, 1])
        with col1:
            user_msg = st.text_input(
                "Type your message...",
                key="chat_input",
                label_visibility="collapsed",
                placeholder="Ask about orders, payments, gift cards...",
            )
        with col2:
            send = st.button("Send", use_container_width=True, key="chat_send")

        if send and user_msg:
            st.session_state.chat_messages.append({"role": "user", "text": user_msg})
            st.session_state.chat_messages.append({"role": "bot", "text": get_bot_response(user_msg)})
            st.rerun()

        st.markdown("")
        st.caption("Quick questions:")
        qcol1, qcol2, qcol3, qcol4 = st.columns(4)

        def _quick(key, user_text, bot_text):
            if st.button(user_text, use_container_width=True, key=key):
                st.session_state.chat_messages.append({"role": "user",  "text": user_text})
                st.session_state.chat_messages.append({"role": "bot",   "text": bot_text})
                st.rerun()

        with qcol1:
            _quick("q1", "Track my order", get_bot_response("order"))
        with qcol2:
            _quick("q2", "Refund request", get_bot_response("refund"))
        with qcol3:
            _quick("q3", "Payment methods", get_bot_response("payment"))
        with qcol4:
            _quick(
                "q4",
                "Talk to human",
                "Absolutely! You can reach our human support team via:\n\n"
                "💬 WhatsApp: +1 (234) 567-890\n"
                "📧 Email: support@cardshop.com\n\n"
                "Average response time: under 5 minutes.",
            )

    with tab2:
        st.markdown("")
        st.markdown("""
        <div class="product-card" style="text-align:center; padding:40px;">
            <div class="card-icon">💬</div>
            <h3>WhatsApp Support</h3>
            <p>Chat with our support team directly on WhatsApp. We typically respond within 2–5 minutes.</p>
            <br>
            <a href="https://wa.me/1234567890" target="_blank" class="whatsapp-btn">
                💬 Open WhatsApp Chat
            </a>
            <br><br>
            <p style="font-size:0.8rem; color:#8D99AE;">Available 24/7 · English, French, Swahili, Hausa</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("""
        <div class="product-card">
            <h3>What you can ask on WhatsApp:</h3>
            <p>
            • Order tracking & status updates<br>
            • Refund requests & disputes<br>
            • Gift card activation help<br>
            • Airtime delivery issues<br>
            • Payment troubleshooting<br>
            • Account questions
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("")

        col1, col2 = st.columns(2)
        with col1:
            email_name    = st.text_input("Your Name",  placeholder="Jane Doe")
            email_addr    = st.text_input("Your Email", placeholder="jane@email.com")
            email_subject = st.selectbox("Subject", [
                "Order Issue",
                "Payment Problem",
                "Gift Card Not Working",
                "Airtime Not Received",
                "Refund Request",
                "Account Issue",
                "General Inquiry",
                "Partnership / Business",
            ])
        with col2:
            email_order = st.text_input("Order ID (optional)", placeholder="CS-XXXXXX")
            email_body  = st.text_area("Message", placeholder="Describe your issue in detail...", height=150)

        if st.button("📧 Send Message", use_container_width=True, key="send_email"):
            if not email_name or not email_addr or not email_body:
                st.error("Please fill in your name, email, and message.")
            elif "@" not in email_addr:
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Sending your message..."):
                    time.sleep(1)
                order_ref = f" (Order: {email_order})" if email_order else ""
                st.success(
                    f"✅ Message sent! A ticket has been created for **{email_subject}{order_ref}**. "
                    f"We'll reply to **{email_addr}** within 24 hours."
                )
