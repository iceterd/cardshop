"""Shared data constants used across pages."""

import random

COUNTRIES = {
    "🇳🇬 Nigeria":       {"iso": "NG", "code": "+234", "currency": "NGN"},
    "🇬🇭 Ghana":         {"iso": "GH", "code": "+233", "currency": "GHS"},
    "🇰🇪 Kenya":         {"iso": "KE", "code": "+254", "currency": "KES"},
    "🇿🇦 South Africa":  {"iso": "ZA", "code": "+27",  "currency": "ZAR"},
    "🇨🇲 Cameroon":      {"iso": "CM", "code": "+237", "currency": "XAF"},
    "🇹🇿 Tanzania":      {"iso": "TZ", "code": "+255", "currency": "TZS"},
    "🇺🇬 Uganda":        {"iso": "UG", "code": "+256", "currency": "UGX"},
    "🇪🇬 Egypt":         {"iso": "EG", "code": "+20",  "currency": "EGP"},
}

FALLBACK_OPERATORS = {
    "NG": [{"id": 341, "name": "MTN Nigeria"}, {"id": 342, "name": "Airtel Nigeria"}, {"id": 343, "name": "Glo Nigeria"}, {"id": 344, "name": "9Mobile Nigeria"}],
    "GH": [{"id": 345, "name": "MTN Ghana"}, {"id": 346, "name": "Vodafone Ghana"}, {"id": 347, "name": "AirtelTigo Ghana"}],
    "KE": [{"id": 348, "name": "Safaricom Kenya"}, {"id": 349, "name": "Airtel Kenya"}, {"id": 350, "name": "Telkom Kenya"}],
    "ZA": [{"id": 351, "name": "Vodacom South Africa"}, {"id": 352, "name": "MTN South Africa"}, {"id": 353, "name": "Cell C"}, {"id": 354, "name": "Telkom SA"}],
    "CM": [{"id": 355, "name": "MTN Cameroon"}, {"id": 356, "name": "Orange Cameroon"}, {"id": 357, "name": "Nexttel Cameroon"}],
    "TZ": [{"id": 358, "name": "Vodacom Tanzania"}, {"id": 359, "name": "Airtel Tanzania"}, {"id": 360, "name": "Tigo Tanzania"}],
    "UG": [{"id": 361, "name": "MTN Uganda"}, {"id": 362, "name": "Airtel Uganda"}, {"id": 363, "name": "Africell Uganda"}],
    "EG": [{"id": 364, "name": "Vodafone Egypt"}, {"id": 365, "name": "Orange Egypt"}, {"id": 366, "name": "Etisalat Egypt"}, {"id": 367, "name": "WE Egypt"}],
}

AIRTIME_AMOUNTS = [1, 2, 5, 10, 15, 20, 25, 50, 100]

FALLBACK_DATA_PLANS = [
    {"id": "1gb_1d",   "description": "1GB — 1 Day",        "price": 1.50},
    {"id": "2gb_3d",   "description": "2GB — 3 Days",       "price": 2.50},
    {"id": "5gb_7d",   "description": "5GB — 7 Days",       "price": 5.00},
    {"id": "10gb_30d", "description": "10GB — 30 Days",     "price": 9.00},
    {"id": "20gb_30d", "description": "20GB — 30 Days",     "price": 15.00},
    {"id": "50gb_30d", "description": "50GB — 30 Days",     "price": 30.00},
    {"id": "unl_1d",   "description": "Unlimited — 1 Day",  "price": 3.00},
    {"id": "unl_7d",   "description": "Unlimited — 7 Days", "price": 12.00},
]

GIFT_CARDS = [
    {"name": "Apple / iTunes",   "icon": "🍎", "denominations": [10, 15, 25, 50, 100, 200], "category": "Entertainment", "popular": True},
    {"name": "Google Play",      "icon": "▶️", "denominations": [10, 15, 25, 50, 100],       "category": "Entertainment", "popular": True},
    {"name": "Amazon",           "icon": "📦", "denominations": [10, 25, 50, 100, 200, 500], "category": "Shopping",      "popular": True},
    {"name": "Steam",            "icon": "🎮", "denominations": [10, 20, 50, 100],           "category": "Gaming",        "popular": True},
    {"name": "PlayStation",      "icon": "🎯", "denominations": [10, 25, 50, 100],           "category": "Gaming",        "popular": False},
    {"name": "Xbox",             "icon": "🟢", "denominations": [10, 25, 50, 100],           "category": "Gaming",        "popular": False},
    {"name": "Netflix",          "icon": "🎦", "denominations": [15, 25, 50, 100],           "category": "Streaming",     "popular": True},
    {"name": "Spotify",          "icon": "🎧", "denominations": [10, 30, 60],                "category": "Streaming",     "popular": False},
    {"name": "Uber",             "icon": "🚗", "denominations": [15, 25, 50, 100],           "category": "Transport",     "popular": False},
    {"name": "Visa Prepaid",     "icon": "💳", "denominations": [25, 50, 100, 200, 500],     "category": "Finance",       "popular": True},
    {"name": "eBay",             "icon": "🏷️", "denominations": [10, 25, 50, 100, 200],  "category": "Shopping",      "popular": False},
    {"name": "Roblox",           "icon": "🧣", "denominations": [10, 25, 50],                "category": "Gaming",        "popular": False},
    {"name": "Nintendo eShop",   "icon": "🕹️", "denominations": [10, 20, 35, 50, 70],    "category": "Gaming",        "popular": False},
    {"name": "Hulu",             "icon": "📺", "denominations": [25, 50, 100],               "category": "Streaming",     "popular": False},
    {"name": "Sling TV",         "icon": "📡", "denominations": [25, 50],                    "category": "Streaming",     "popular": False},
    {"name": "DoorDash",         "icon": "🍔", "denominations": [15, 25, 50, 100],           "category": "Food",          "popular": False},
]

CRYPTO_RATES = {
    "BTC (Bitcoin)":   67234.50,
    "ETH (Ethereum)":  3521.80,
    "USDT (Tether)":   1.00,
    "USDC (USD Coin)": 1.00,
    "LTC (Litecoin)":  84.25,
}

BOT_RESPONSES = {
    "hello":   "Hi there! 👋 Welcome to Cardshop. I can help you with airtime top-ups, gift cards, payments, or any account questions. What do you need?",
    "help":    "I'm here for you! I can assist with:\n• Buying airtime or data\n• Finding the right gift card\n• Payment issues\n• Order tracking\n• Account questions\n\nJust tell me what you need!",
    "refund":  "I understand refund requests can be stressful. Please share your order ID and I'll check the status right away. If eligible, refunds are processed within 24 hours.",
    "order":   "I'd be happy to look into your order! Could you share your order ID or the email address you used? I'll pull up the details for you.",
    "payment": "We accept credit/debit cards (Visa, Mastercard), PayPal, and crypto (BTC, ETH, USDT, USDC, LTC). All transactions are encrypted and secure.",
    "default": "Thanks for reaching out! Let me connect you with the right support. Could you tell me a bit more about what you need help with?",
}

TXN_ICONS = {
    "Airtime":        "📞",
    "Data":           "📶",
    "Gift Card":      "🎁",
    "Wallet":         "💰",
    "Crypto Deposit": "🪙",
    "PayPal Deposit": "🏦",
}


def generate_order_id() -> str:
    return f"CS-{random.randint(100000, 999999)}"


def get_bot_response(msg: str) -> str:
    msg_lower = msg.lower()
    for key in BOT_RESPONSES:
        if key in msg_lower:
            return BOT_RESPONSES[key]
    return BOT_RESPONSES["default"]
