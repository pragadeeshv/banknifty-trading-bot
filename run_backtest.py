#!/usr/bin/env python3
"""
Simple backtest runner for the Kite Trading Bot.
This script provides easy access to run backtests from the root directory.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    """Main function to run backtest."""
    print("🚀 Kite Trading Bot - Backtest Runner")
    print("=" * 40)
    
    try:
        # Import and run the backtest engine
        from backtesting.engine import main
        
        # Show available strategies
        print("📈 Available Strategies:")
        print("   • Original (Floating Band UB/LB) - Default ✅")
        print()
        
        # Run backtest with default parameters
        print("📊 Running backtest with default parameters...")
        print("📅 Date: Today (interactive)")
        print("📈 Strategy: Original (Floating Band UB/LB)")
        print("⏰ Timeframe: 5minute")
        print("📊 Instrument: BankNifty Weekly Futures")
        print("-" * 40)
        
        # Run the backtest
        main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have:")
        print("   1. Installed dependencies: pip install -r requirements.txt")
        print("   2. Set up environment variables in .env file")
        print("   3. Generated access token using auth/login.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
