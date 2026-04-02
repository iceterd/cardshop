"""
Cardshop — Reloadly API integration
Covers: OAuth2 token fetch, operator lookup, airtime top-up, data bundles.

Env vars required:
    RELOADLY_CLIENT_ID      — from Reloadly dashboard
    RELOADLY_CLIENT_SECRET  — from Reloadly dashboard
    RELOADLY_ENV            — "sandbox" (default) or "production"
"""

import os
import time
import requests
import streamlit as st

CLIENT_ID     = os.environ.get("RELOADLY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("RELOADLY_CLIENT_SECRET", "")
ENV           = os.environ.get("RELOADLY_ENV", "sandbox").lower()

AUTH_URL  = "https://auth.reloadly.com/oauth/token"
BASE_URL  = (
    "https://topups.reloadly.com"
    if ENV == "production"
    else "https://topups-sandbox.reloadly.com"
)
AUDIENCE  = BASE_URL

IS_CONFIGURED = bool(CLIENT_ID and CLIENT_SECRET)


def _get_token() -> str | None:
    if not IS_CONFIGURED:
        return None
    now = time.time()
    cached_token  = st.session_state.get("_reloadly_token")
    cached_expiry = st.session_state.get("_reloadly_token_expiry", 0)
    if cached_token and now < cached_expiry - 60:
        return cached_token
    try:
        resp = requests.post(
            AUTH_URL,
            json={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "client_credentials",
                "audience": AUDIENCE,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        token = data["access_token"]
        expires_in = data.get("expires_in", 3600)
        st.session_state["_reloadly_token"]        = token
        st.session_state["_reloadly_token_expiry"] = now + expires_in
        return token
    except Exception:
        st.session_state.pop("_reloadly_token", None)
        return None


def _headers() -> dict:
    token = _get_token()
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/com.reloadly.topups-v1+json",
    }


def get_operators(country_iso: str) -> list[dict]:
    if not IS_CONFIGURED:
        return []
    try:
        resp = requests.get(
            f"{BASE_URL}/operators/countries/{country_iso}",
            headers=_headers(),
            params={"includeBundles": True, "includeData": True, "includePin": False},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


def get_operator_by_phone(phone: str, country_iso: str) -> dict | None:
    if not IS_CONFIGURED:
        return None
    try:
        resp = requests.get(
            f"{BASE_URL}/operators/auto-detect/phone/{phone}/countries/{country_iso}",
            headers=_headers(),
            params={"suggestedAmountsMap": False, "suggestedAmounts": False},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def send_airtime(operator_id: int, phone: str, country_iso: str, amount: float, use_local_amount: bool = False) -> dict:
    if not IS_CONFIGURED:
        return {"success": False, "order_id": None, "message": "Reloadly not configured."}
    payload = {
        "recipientPhone": {"countryCode": country_iso, "number": phone},
        "senderPhone":    {"countryCode": country_iso, "number": phone},
        "operatorId":     operator_id,
        "useLocalAmount": use_local_amount,
        "amount":         amount,
        "customIdentifier": f"cardshop-{int(time.time())}",
    }
    try:
        resp = requests.post(f"{BASE_URL}/topups", headers=_headers(), json=payload, timeout=15)
        data = resp.json()
        if resp.status_code in (200, 201) and data.get("transactionId"):
            return {"success": True, "order_id": str(data["transactionId"]), "message": "Airtime sent successfully.", "raw": data}
        error_msg = data.get("message") or data.get("developerMessage") or "Top-up failed."
        return {"success": False, "order_id": None, "message": error_msg}
    except Exception as e:
        return {"success": False, "order_id": None, "message": str(e)}


def get_data_bundles(operator_id: int) -> list[dict]:
    if not IS_CONFIGURED:
        return []
    try:
        resp = requests.get(f"{BASE_URL}/operators/{operator_id}/data-bundles", headers=_headers(), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


def send_data_bundle(operator_id: int, bundle_id: str, phone: str, country_iso: str) -> dict:
    if not IS_CONFIGURED:
        return {"success": False, "order_id": None, "message": "Reloadly not configured."}
    payload = {
        "recipientPhone": {"countryCode": country_iso, "number": phone},
        "operatorId":     operator_id,
        "dataBundleId":   bundle_id,
        "customIdentifier": f"cardshop-data-{int(time.time())}",
    }
    try:
        resp = requests.post(f"{BASE_URL}/data-topups", headers=_headers(), json=payload, timeout=15)
        data = resp.json()
        if resp.status_code in (200, 201) and data.get("transactionId"):
            return {"success": True, "order_id": str(data["transactionId"]), "message": "Data bundle activated.", "raw": data}
        error_msg = data.get("message") or data.get("developerMessage") or "Data top-up failed."
        return {"success": False, "order_id": None, "message": error_msg}
    except Exception:
        return {"success": False, "order_id": None, "message": "Request failed."}


def reloadly_status() -> dict:
    if not IS_CONFIGURED:
        return {"connected": False, "env": ENV, "message": "API credentials not set"}
    token = _get_token()
    if token:
        return {"connected": True, "env": ENV, "message": f"Connected ({ENV})"}
    return {"connected": False, "env": ENV, "message": "Auth failed — check credentials"}
