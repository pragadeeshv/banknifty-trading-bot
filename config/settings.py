"""
Main settings configuration for the Kite Trading Bot.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"

# Reports directory
REPORTS_DIR = PROJECT_ROOT / "reports"

# Authentication
AUTH_DIR = PROJECT_ROOT / "auth"
ACCESS_TOKEN_FILE = AUTH_DIR / "access_token.json"

# Kite Connect settings
KITE_API_KEY = os.getenv("KITE_API_KEY", "")
KITE_API_SECRET = os.getenv("KITE_API_SECRET", "")

# Trading settings
INSTRUMENT = "BANKNIFTY"  # Trading instrument
LOT_SIZE = 15  # BankNifty lot size
POINT_VALUE = 15  # Rupees per point

# Strategy settings
DEFAULT_STRATEGY = "v3"  # Default strategy to use
AVAILABLE_STRATEGIES = ["original", "v2", "v3"]

# Backtesting settings
DEFAULT_START_DATE = "2025-01-01"
DEFAULT_END_DATE = "2025-08-31"
DEFAULT_TIMEFRAME = "5minute"

# Risk management settings
MAX_DAILY_LOSS = 120  # Maximum daily loss in points
MAX_SINGLE_TRADE_LOSS = 45  # Maximum single trade loss in points
DAILY_LOSS_LIMIT = 120  # Daily loss limit in points

# Position sizing settings
POSITION_SIZES = {
    "monday": 0.8,
    "tuesday": 0.4,
    "wednesday": 1.0,
    "thursday": 1.2,
    "friday": 0.9
}

# Time settings
TRADING_START_TIME = "10:30"
TRADING_END_TIME = "14:00"
MARKET_OPEN_TIME = "09:15"
MARKET_CLOSE_TIME = "15:30"

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = PROJECT_ROOT / "logs" / "trading_bot.log"

# Performance settings
PERFORMANCE_METRICS = [
    "total_pnl",
    "win_rate",
    "profit_factor",
    "max_drawdown",
    "sharpe_ratio",
    "roi"
]

# File paths
ENV_EXAMPLE_FILE = PROJECT_ROOT / "env.example"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
README_FILE = PROJECT_ROOT / "README.md"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, RESULTS_DIR, 
                  REPORTS_DIR, AUTH_DIR, PROJECT_ROOT / "logs"]:
    directory.mkdir(parents=True, exist_ok=True)
