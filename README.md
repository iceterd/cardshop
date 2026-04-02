# 🛒 Cardshop

**Your Digital Marketplace — Airtime · Gift Cards · Crypto Payments**

Cardshop is a Streamlit-based digital utilities platform offering instant airtime/data top-ups, gift card purchases, and multi-method payments with 24/7 customer support.

## Features

### 📱 Airtime & Data Top-Up
- 8 African countries supported (Nigeria, Ghana, Kenya, South Africa, Cameroon, Tanzania, Uganda, Egypt)
- All major operators (MTN, Airtel, Safaricom, Vodacom, etc.)
- Instant delivery with order confirmation
- Flexible data plans (1GB to Unlimited)

### 🎁 Gift Card Marketplace
- 16+ brands (Apple, Google Play, Amazon, Steam, Netflix, PlayStation, Xbox, etc.)
- Multiple denominations per card
- Searchable & filterable catalog
- Instant code delivery with email confirmation

### 💳 Multi-Payment Support
- Credit/Debit cards (Visa, Mastercard, Amex)
- PayPal integration
- Crypto payments (BTC, ETH, USDT, USDC, LTC)
- In-app wallet system

### 💬 24/7 Customer Support
- **AI Chatbot** — Instant answers with quick-action buttons
- **WhatsApp Integration** — Direct chat link for real-time human support
- **Email Support** — Ticketed system with order ID tracking
- **Escalation** — AI-to-human handoff built in

### 📊 Order Management
- Full transaction history
- Order tracking with status badges
- Spending analytics

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect repo at [share.streamlit.io](https://share.streamlit.io)
3. Deploy

### VPS (Ubuntu)
```bash
git clone <your-repo>
cd cardshop
pip install -r requirements.txt
nohup streamlit run app.py --server.port 8501 &
```

## Roadmap

- [ ] Connect live airtime API (Reloadly / DingConnect)
- [ ] Connect gift card supplier API
- [ ] Stripe / Flutterwave payment integration
- [ ] User authentication & accounts
- [ ] SMS/email notification system
- [ ] Admin dashboard
- [ ] Mobile PWA wrapper
- [ ] Referral & loyalty program

## Tech Stack

- **Frontend:** Streamlit + Custom CSS
- **Backend:** Python (mock APIs, ready for live integration)
- **Payments:** Mock (ready for Stripe, Flutterwave, crypto gateway)

## License

Proprietary — © 2026 Cardshop
