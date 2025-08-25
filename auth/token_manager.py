import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN_PATH = os.path.join(os.path.dirname(__file__), "access_token.json")

def save_access_token(access_token: str):
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    payload = {"access_token": access_token, "saved_at": datetime.now().isoformat()}
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return TOKEN_PATH

def load_access_token() -> str | None:
    if not os.path.exists(TOKEN_PATH):
        return None
    try:
        with open(TOKEN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("access_token")
    except Exception:
        return None
