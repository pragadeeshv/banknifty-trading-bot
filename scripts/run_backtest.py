#!/usr/bin/env python3
"""
Script to run backtests for the Kite Trading Bot.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from backtesting.engine import run_backtest
from strategies.core import original, v2, v3
from config.settings import DEFAULT_START_DATE, DEFAULT_END_DATE, DEFAULT_STRATEGY
from config.strategy_config import get_strategy_config, get_available_strategies

def main():
    parser = argparse.ArgumentParser(description="Run backtest for trading strategies")
    parser.add_argument("--strategy", "-s", 
                       choices=get_available_strategies(),
                       default=DEFAULT_STRATEGY,
                       help="Strategy to test (default: v3)")
    parser.add_argument("--start-date", 
                       default=DEFAULT_START_DATE,
                       help="Start date for backtest (YYYY-MM-DD)")
    parser.add_argument("--end-date", 
                       default=DEFAULT_END_DATE,
                       help="End date for backtest (YYYY-MM-DD)")
    parser.add_argument("--timeframe", 
                       default="5minute",
                       choices=["1minute", "5minute", "15minute", "30minute"],
                       help="Timeframe for data")
    parser.add_argument("--instrument", 
                       default="BANKNIFTY",
                       help="Trading instrument")
    parser.add_argument("--output", "-o",
                       help="Output file for results")
    parser.add_argument("--verbose", "-v",
                       action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    print(f"🚀 Running backtest for {args.strategy.upper()} strategy")
    print(f"📅 Period: {args.start_date} to {args.end_date}")
    print(f"⏰ Timeframe: {args.timeframe}")
    print(f"📊 Instrument: {args.instrument}")
    print("-" * 50)
    
    # Get strategy configuration
    config = get_strategy_config(args.strategy)
    print(f"📋 Strategy: {config['name']} v{config['version']}")
    print(f"📝 Description: {config['description']}")
    
    # Run backtest
    try:
        results = run_backtest(
            strategy_name=args.strategy,
            start_date=args.start_date,
            end_date=args.end_date,
            timeframe=args.timeframe,
            instrument=args.instrument,
            verbose=args.verbose
        )
        
        # Display results
        print("\n📊 BACKTEST RESULTS:")
        print("=" * 50)
        print(f"Total P&L: {results['total_pnl']:.2f} points")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Win Rate: {results['win_rate']:.1f}%")
        print(f"ROI: {(results['total_pnl'] * 15 / 100000 * 100):.2f}%")
        
        # Save results if output file specified
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Results saved to: {args.output}")
            
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
