import io
import os
import requests
import pandas as pd
from datetime import datetime

KITE_INSTRUMENTS_URL = "https://api.kite.trade/instruments"

def download_instruments_csv() -> pd.DataFrame:
    # Zerodha instruments dump (CSV). Public.
    headers = {"X-Kite-Version": "3"}
    resp = requests.get(KITE_INSTRUMENTS_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return pd.read_csv(io.StringIO(resp.text))

def get_banknifty_current_month_fut_token(df: pd.DataFrame) -> int | None:
    # Filter current-month BANKNIFTY futures (FUT)
    now = datetime.now()
    # Zerodha uses actual expiry date; pick nearest future expiry for BANKNIFTY
    bn = df[(df["name"] == "BANKNIFTY") & (df["segment"] == "NFO-FUT")]
    if bn.empty:
        return None
    # Choose the nearest expiry in the future
    bn = bn.copy()
    bn["expiry"] = pd.to_datetime(bn["expiry"], errors="coerce")
    bn = bn[bn["expiry"] >= pd.Timestamp(now.date())]
    if bn.empty:
        return None
    bn = bn.sort_values("expiry", ascending=True).iloc[0]
    return int(bn["instrument_token"])

def get_banknifty_weekly_fut_token(df: pd.DataFrame) -> int | None:
    """Get the nearest weekly BANKNIFTY futures contract token"""
    now = datetime.now()
    
    # Filter BANKNIFTY futures
    bn = df[(df["name"] == "BANKNIFTY") & (df["segment"] == "NFO-FUT")].copy()
    if bn.empty:
        return None
    
    # Convert expiry to datetime
    bn["expiry"] = pd.to_datetime(bn["expiry"], errors="coerce")
    
    # Filter for future expiries only
    bn = bn[bn["expiry"] >= pd.Timestamp(now.date())]
    if bn.empty:
        return None
    
    # Weekly contracts typically expire on Thursdays
    # Sort by expiry and get the nearest one (which is usually weekly)
    bn = bn.sort_values("expiry", ascending=True)
    
    # Get the nearest expiry (weekly contracts are closest)
    nearest_contract = bn.iloc[0]
    
    return int(nearest_contract["instrument_token"])

def get_banknifty_token():
    """Convenience function to get weekly BankNifty futures token"""
    df = download_instruments_csv()
    return get_banknifty_weekly_fut_token(df)
