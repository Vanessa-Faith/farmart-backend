import base64
import os
from datetime import datetime
import requests
from flask import current_app


class MpesaError(Exception):
    """Raised when M-Pesa API calls fail"""


def _get_base_url():
    env = (os.getenv("MPESA_ENV") or current_app.config.get("MPESA_ENV") or "sandbox").lower()
    if env == "sandbox":
        return "https://sandbox.safaricom.co.ke"
    return "https://api.safaricom.co.ke"


def generate_access_token():
    """Generate Daraja access token using consumer key/secret."""
    consumer_key = os.getenv("MPESA_CONSUMER_KEY") or current_app.config.get("MPESA_CONSUMER_KEY")
    consumer_secret = (
        os.getenv("MPESA_CONSUMER_SECRET")
        or os.getenv("MPESA_SECRET")
        or current_app.config.get("MPESA_CONSUMER_SECRET")
    )
    if not consumer_key or not consumer_secret:
        raise MpesaError("Missing MPESA_CONSUMER_KEY or MPESA_CONSUMER_SECRET")

    auth_string = f"{consumer_key}:{consumer_secret}".encode("utf-8")
    auth_b64 = base64.b64encode(auth_string).decode("utf-8")

    url = f"{_get_base_url()}/oauth/v1/generate?grant_type=client_credentials"
    headers = {"Authorization": f"Basic {auth_b64}"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise MpesaError(f"Failed to fetch access token: {exc}") from exc

    data = response.json()
    token = data.get("access_token")
    if not token:
        raise MpesaError("Access token missing in response")
    return token


def _generate_password(shortcode, passkey, timestamp):
    raw = f"{shortcode}{passkey}{timestamp}".encode("utf-8")
    return base64.b64encode(raw).decode("utf-8")


def send_stk_push(amount, phone_number, account_reference, transaction_desc):
    """Send STK Push request to Daraja."""
    shortcode = os.getenv("MPESA_SHORTCODE") or current_app.config.get("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY") or current_app.config.get("MPESA_PASSKEY")
    callback_url = os.getenv("MPESA_CALLBACK_URL") or current_app.config.get("MPESA_CALLBACK_URL")

    if not shortcode or not passkey or not callback_url:
        raise MpesaError("Missing MPESA_SHORTCODE, MPESA_PASSKEY, or MPESA_CALLBACK_URL")

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    password = _generate_password(shortcode, passkey, timestamp)

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }

    token = generate_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = f"{_get_base_url()}/mpesa/stkpush/v1/processrequest"
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise MpesaError(f"STK Push request failed: {exc}") from exc

    return response.json()
