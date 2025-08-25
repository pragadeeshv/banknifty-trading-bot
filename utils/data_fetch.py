from datetime import datetime, timedelta
from kiteconnect import KiteConnect
import pandas as pd

def fetch_5min_data(kite: KiteConnect, instrument_token: int, date_str: str = None) -> pd.DataFrame:
    """
    Fetch 5-minute candles for a specific date. Defaults to today if date_str is None.

    Parameters:
    - kite: KiteConnect instance
    - instrument_token: int
    - date_str: 'YYYY-MM-DD' (optional)
    """
    if date_str:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        target_date = datetime.now().date()

    start = datetime(target_date.year, target_date.month, target_date.day, 9, 15)
    end = datetime(target_date.year, target_date.month, target_date.day, 15, 30)

    candles = kite.historical_data(
        instrument_token,
        start,
        end,
        interval="5minute",
        continuous=False,
        oi=False
    )

    if not candles:
        return pd.DataFrame(columns=["time","open","high","low","close","volume"])

    df = pd.DataFrame(candles)
    df.rename(columns={"date": "time"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"])
    return df[["time","open","high","low","close","volume"]]
