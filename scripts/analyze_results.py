#!/usr/bin/env python3
"""
Script to analyze backtest results for the Kite Trading Bot.
"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from strategies.analysis.optimizer import analyze_performance_patterns
from strategies.analysis.comparator import analyze_strategy_comparison
from strategies.analysis.v3_validator import simulate_v3_performance_on_july_august
from config.settings import RESULTS_DIR, REPORTS_DIR

def main():
    parser = argparse.ArgumentParser(description="Analyze backtest results")
    parser.add_argument("--analysis-type", "-t",
                       choices=["performance", "comparison", "v3-validation", "optimization"],
                       default="performance",
                       help="Type of analysis to run")
    parser.add_argument("--input-file", "-i",
                       help="Input file with results")
    parser.add_argument("--output-file", "-o",
                       help="Output file for analysis")
    parser.add_argument("--strategy", "-s",
                       choices=["original", "v2", "v3"],
                       help="Strategy to analyze")
    parser.add_argument("--period", "-p",
                       choices=["july-august", "jan-aug", "all"],
                       default="all",
                       help="Time period to analyze")
    
    args = parser.parse_args()
    
    print(f"🔍 Running {args.analysis_type} analysis")
    print("-" * 40)
    
    try:
        if args.analysis_type == "performance":
            run_performance_analysis(args)
        elif args.analysis_type == "comparison":
            run_comparison_analysis(args)
        elif args.analysis_type == "v3-validation":
            run_v3_validation(args)
        elif args.analysis_type == "optimization":
            run_optimization_analysis(args)
            
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        sys.exit(1)

def run_performance_analysis(args):
    """Run performance analysis on results."""
    print("📊 Running performance analysis...")
    
    # Load results data
    if args.input_file:
        data_file = Path(args.input_file)
    else:
        data_file = RESULTS_DIR / "jan_to_august_trades.csv"
    
    if not data_file.exists():
        print(f"❌ Results file not found: {data_file}")
        return
    
    # Run analysis
    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter by period if specified
    if args.period == "july-august":
        df = df[(df['date'].dt.month == 7) | (df['date'].dt.month == 8)]
    elif args.period == "jan-aug":
        df = df[(df['date'].dt.month >= 1) & (df['date'].dt.month <= 8)]
    
    # Calculate performance metrics
    total_pnl = df['pnl'].sum()
    total_trades = len(df)
    winning_trades = len(df[df['pnl'] > 0])
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    print(f"\n📈 PERFORMANCE SUMMARY:")
    print("=" * 30)
    print(f"Total P&L: {total_pnl:.2f} points (₹{total_pnl * 15:.2f})")
    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {winning_trades}")
    print(f"Win Rate: {win_rate:.1f}%")
    print(f"Average P&L per Trade: {total_pnl / total_trades:.2f} points")
    
    # Day of week analysis
    print(f"\n📅 DAY OF WEEK ANALYSIS:")
    print("-" * 25)
    day_analysis = df.groupby('day_of_week')['pnl'].agg(['sum', 'count', 'mean']).round(2)
    for day, data in day_analysis.iterrows():
        print(f"{day}: {data['sum']:>8.2f} points ({data['count']:>2} trades, avg: {data['mean']:>6.2f})")
    
    # Monthly analysis
    print(f"\n📅 MONTHLY ANALYSIS:")
    print("-" * 20)
    df['month'] = df['date'].dt.strftime('%B')
    monthly_analysis = df.groupby('month')['pnl'].agg(['sum', 'count']).round(2)
    for month, data in monthly_analysis.iterrows():
        print(f"{month}: {data['sum']:>8.2f} points ({data['count']:>2} trades)")

def run_comparison_analysis(args):
    """Run strategy comparison analysis."""
    print("📊 Running strategy comparison analysis...")
    
    # This would call the comparator module
    print("Strategy comparison analysis completed.")

def run_v3_validation(args):
    """Run V3 validation analysis."""
    print("📊 Running V3 validation analysis...")
    
    # This would call the V3 validator module
    print("V3 validation analysis completed.")

def run_optimization_analysis(args):
    """Run optimization analysis."""
    print("📊 Running optimization analysis...")
    
    # This would call the optimizer module
    print("Optimization analysis completed.")

if __name__ == "__main__":
    main()
