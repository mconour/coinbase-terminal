# src/coinbase_client.py
import time
import hmac
import hashlib
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COINBASE_API_KEY")
API_SECRET = os.getenv("COINBASE_API_SECRET")
API_BASE_URL = "https://api.coinbase.com"

def get_headers(request_path, method="GET", body=""):
    timestamp = str(int(time.time()))
    message = timestamp + method + request_path + body
    signature = hmac.new(
        base64.b64decode(API_SECRET),
        message.encode("utf-8"),
        hashlib.sha256
    )
    signature_b64 = base64.b64encode(signature.digest()).decode("utf-8")

    return {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": signature_b64,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-VERSION": "2023-10-05",  # Use latest version date
    }

def get_accounts():
    path = "/v2/accounts"
    url = API_BASE_URL + path
    headers = get_headers(path)
    response = requests.get(url, headers=headers)
    return response.json()
