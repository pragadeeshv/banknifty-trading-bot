import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from auth.token_manager import save_access_token

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

if not API_KEY or not API_SECRET:
    raise SystemExit("Please set API_KEY and API_SECRET in your .env")

kite = KiteConnect(api_key=API_KEY)
print("Login URL:")
print(kite.login_url())

request_token = input("Paste request_token from redirect URL: ").strip()
data = kite.generate_session(request_token, api_secret=API_SECRET)
access_token = data["access_token"]
kite.set_access_token(access_token)
save_access_token(access_token)
print("✅ Access token saved to auth/access_token.json")
