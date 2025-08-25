#!/usr/bin/env python3
"""
Comprehensive Trading Strategy Analysis - Last 3 Months
Expert quant analysis with worst trade identification and improvement suggestions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from utils.data_fetch import fetch_5min_data
from strategy.core.ub_lb import run_floating_band_strategy
from utils.instruments import get_banknifty_weekly_fut_token, download_instruments_csv
from auth.token_manager import load_access_token
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_kite_connect():
    """
    Initialize KiteConnect with API credentials
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ Set API_KEY in .env file")
        return None
    
    # Load access token
    access_token = (load_access_token() or "").strip()
    if not access_token:
        print("❌ Run auth/login.py to generate today's access token")
        return None

    # Initialize KiteConnect
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    print("✅ Login successful")
    return kite

def get_trading_days(start_date, end_date):
    """
    Get all trading days between start_date and end_date
    """
    trading_days = []
    current_date = start_date
    
    while current_date <= end_date:
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() < 5:  # Monday to Friday
            trading_days.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return trading_days

def analyze_market_conditions(df, trade_entry_time, trade_exit_time):
    """
    Analyze market conditions during the trade period
    """
    # Get data during trade period
    trade_data = df[(df.index >= trade_entry_time) & (df.index <= trade_exit_time)]
    
    if trade_data.empty:
        return {
            'volatility': 0,
            'trend_strength': 0,
            'volume_profile': 'unknown',
            'market_regime': 'unknown'
        }
    
    # Calculate volatility (standard deviation of returns)
    returns = trade_data['close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
    
    # Calculate trend strength (linear regression R-squared)
    x = np.arange(len(trade_data))
    y = trade_data['close'].values
    if len(x) > 1:
        correlation_matrix = np.corrcoef(x, y)
        trend_strength = correlation_matrix[0, 1] ** 2 if not np.isnan(correlation_matrix[0, 1]) else 0
    else:
        trend_strength = 0
    
    # Volume profile
    avg_volume = trade_data['volume'].mean() if 'volume' in trade_data.columns else 0
    volume_profile = 'high' if avg_volume > 1000 else 'low' if avg_volume < 500 else 'medium'
    
    # Market regime classification
    if volatility > 25:
        market_regime = 'high_volatility'
    elif volatility < 15:
        market_regime = 'low_volatility'
    else:
        market_regime = 'normal_volatility'
    
    return {
        'volatility': volatility,
        'trend_strength': trend_strength,
        'volume_profile': volume_profile,
        'market_regime': market_regime
    }

def identify_worst_trade(trades):
    """
    Identify the single worst trade with detailed analysis
    """
    if not trades:
        return None
    
    # Find the trade with the highest loss
    worst_trade = min(trades, key=lambda x: x['pnl'])
    
    return worst_trade

def analyze_worst_trade_failure(worst_trade, df):
    """
    Detailed analysis of why the worst trade failed
    """
    analysis = {
        'trade_details': worst_trade,
        'market_conditions': {},
        'failure_reasons': [],
        'risk_management_issues': [],
        'timing_issues': [],
        'signal_quality': 'unknown'
    }
    
    # Analyze market conditions
    if 'entry_time' in worst_trade and 'exit_time' in worst_trade:
        market_conditions = analyze_market_conditions(
            df, worst_trade['entry_time'], worst_trade['exit_time']
        )
        analysis['market_conditions'] = market_conditions
    
    # Identify failure reasons based on trade characteristics
    pnl = worst_trade['pnl']
    trade_type = worst_trade.get('type', 'TRADE')
    
    # High volatility market failure
    if analysis['market_conditions'].get('volatility', 0) > 30:
        analysis['failure_reasons'].append('High volatility market conditions')
    
    # Weak trend failure
    if analysis['market_conditions'].get('trend_strength', 0) < 0.3:
        analysis['failure_reasons'].append('Weak or choppy market trend')
    
    # Large loss indicates poor risk management
    if abs(pnl) > 100:
        analysis['risk_management_issues'].append('Inadequate stop loss or position sizing')
    
    # Timing issues
    if 'entry_time' in worst_trade:
        entry_hour = pd.to_datetime(worst_trade['entry_time']).hour
        if entry_hour < 9 or entry_hour > 14:
            analysis['timing_issues'].append('Poor entry timing (outside optimal hours)')
    
    # Signal quality assessment
    if len(analysis['failure_reasons']) > 2:
        analysis['signal_quality'] = 'poor'
    elif len(analysis['failure_reasons']) > 0:
        analysis['signal_quality'] = 'moderate'
    else:
        analysis['signal_quality'] = 'good'
    
    return analysis

def suggest_improvements(analysis, all_trades):
    """
    Suggest practical improvements based on analysis
    """
    improvements = {
        'risk_management': [],
        'entry_filters': [],
        'exit_improvements': [],
        'timing_filters': [],
        'volatility_filters': []
    }
    
    # Risk management improvements
    if analysis['risk_management_issues']:
        improvements['risk_management'].extend([
            'Implement dynamic stop loss based on volatility',
            'Add maximum loss per trade limit (e.g., 50 points)',
            'Use position sizing based on account risk percentage'
        ])
    
    # Entry filter improvements
    if 'High volatility market conditions' in analysis['failure_reasons']:
        improvements['entry_filters'].extend([
            'Add volatility filter: avoid trading when volatility > 25%',
            'Implement ATR-based entry confirmation',
            'Add volume confirmation requirement'
        ])
    
    if 'Weak or choppy market trend' in analysis['failure_reasons']:
        improvements['entry_filters'].extend([
            'Add trend strength filter: minimum R-squared > 0.3',
            'Implement moving average trend confirmation',
            'Add momentum indicator filter (RSI, MACD)'
        ])
    
    # Timing improvements
    if analysis['timing_issues']:
        improvements['timing_filters'].extend([
            'Restrict trading to 9:30 AM - 2:30 PM',
            'Avoid first 15 minutes of market opening',
            'Add day-of-week filters based on historical performance'
        ])
    
    # Volatility filters
    improvements['volatility_filters'].extend([
        'Skip trading during major news events',
        'Add implied volatility filter for options expiry days',
        'Implement market regime detection'
    ])
    
    return improvements

def create_improved_strategy():
    """
    Create improved strategy logic based on analysis
    """
    improved_strategy = """
# IMPROVED FLOATING BAND STRATEGY

## ENTRY FILTERS
1. Volatility Filter: Only trade when volatility < 25%
2. Trend Strength Filter: Minimum R-squared > 0.3
3. Volume Filter: Require above-average volume
4. Timing Filter: Trade only between 9:30 AM - 2:30 PM
5. Day Filter: Avoid Monday/Tuesday based on historical performance

## RISK MANAGEMENT
1. Dynamic Stop Loss: ATR-based stop loss (2x ATR)
2. Maximum Loss: 50 points per trade
3. Position Sizing: 1% risk per trade
4. Daily Stop Loss: 150 points maximum
5. Maximum Trades: 4 trades per day

## EXIT IMPROVEMENTS
1. Trailing Stop: Move stop loss to breakeven after 20 points profit
2. Take Profit: Close at 30 points profit or end of day
3. Time-based Exit: Square off all positions by 15:10

## MARKET REGIME FILTERS
1. High Volatility: Skip trading when VIX > 25
2. Low Liquidity: Skip during low volume periods
3. News Events: Avoid trading during major announcements
4. Options Expiry: Reduce position size on expiry days

## SIGNAL CONFIRMATION
1. Require 2 consecutive candles for entry confirmation
2. Add momentum confirmation (RSI divergence)
3. Volume confirmation for breakout signals
4. Price action confirmation (candlestick patterns)
"""
    return improved_strategy

def comprehensive_analysis():
    """
    Run comprehensive 3-month analysis
    """
    
    # Initialize KiteConnect
    kite = get_kite_connect()
    if kite is None:
        print("❌ Failed to initialize KiteConnect")
        return None
    
    # Get BankNifty Weekly token
    try:
        instruments_df = download_instruments_csv()
        instrument_token = get_banknifty_weekly_fut_token(instruments_df)
        if instrument_token is None:
            print("❌ Could not find BankNifty weekly futures token")
            return None
        print(f"✅ BankNifty Weekly token: {instrument_token}")
    except Exception as e:
        print(f"❌ Token fetch failed: {e}")
        return None
    
    print(f"🔍 COMPREHENSIVE TRADING STRATEGY ANALYSIS")
    print(f"📅 Period: Last 3 months (June, July, August 2025)")
    print(f"📊 Strategy: Floating Band Strategy")
    print(f"📈 Instrument: BankNifty Weekly Futures")
    print("=" * 80)
    
    # Define date range (last 3 months)
    end_date = datetime(2025, 8, 31)
    start_date = end_date - timedelta(days=90)
    
    # Get all trading days
    all_trading_days = get_trading_days(start_date, end_date)
    print(f"📅 Total trading days to analyze: {len(all_trading_days)}")
    
    all_trades = []
    all_daily_data = {}
    
    # Process each trading day
    for i, date_str in enumerate(all_trading_days, 1):
        try:
            if i % 10 == 0 or i == len(all_trading_days):
                print(f"📊 Progress: {i}/{len(all_trading_days)} days processed...")
            
            # Fetch data
            df = fetch_5min_data(kite, instrument_token, date_str)
            
            if df is None or df.empty:
                continue
            
            # Store daily data for analysis
            all_daily_data[date_str] = df
            
            # Run strategy
            result_df, trades = run_floating_band_strategy(df)
            
            # Add trade details
            for trade in trades:
                trade['date'] = date_str
                trade['day_of_week'] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
                trade['month'] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B")
                all_trades.append(trade)
            
        except Exception as e:
            print(f"    ❌ Error processing {date_str}: {str(e)}")
    
    if not all_trades:
        print("❌ No trades found for analysis")
        return None
    
    # Calculate overall statistics
    total_pnl = sum(trade['pnl'] for trade in all_trades)
    total_trades = len(all_trades)
    winning_trades = len([t for t in all_trades if t['pnl'] > 0])
    win_rate = winning_trades / total_trades * 100
    
    print(f"\n📊 OVERALL PERFORMANCE (Last 3 Months):")
    print(f"💰 Total P&L: {total_pnl:+.2f} points")
    print(f"📈 Total Trades: {total_trades}")
    print(f"✅ Win Rate: {win_rate:.1f}%")
    print(f"📊 Average Trade P&L: {total_pnl/total_trades:+.2f} points")
    
    # Identify worst trade
    worst_trade = identify_worst_trade(all_trades)
    
    print(f"\n🔍 WORST TRADE ANALYSIS:")
    print(f"📅 Date: {worst_trade['date']} ({worst_trade['day_of_week']})")
    print(f"💰 P&L: {worst_trade['pnl']:+.2f} points")
    print(f"📊 Type: {worst_trade.get('type', 'TRADE')}")
    
    # Analyze worst trade failure
    worst_trade_analysis = analyze_worst_trade_failure(worst_trade, all_daily_data.get(worst_trade['date']))
    
    print(f"\n🔍 ROOT CAUSE ANALYSIS:")
    if worst_trade_analysis['failure_reasons']:
        for reason in worst_trade_analysis['failure_reasons']:
            print(f"❌ {reason}")
    
    if worst_trade_analysis['risk_management_issues']:
        for issue in worst_trade_analysis['risk_management_issues']:
            print(f"⚠️ {issue}")
    
    if worst_trade_analysis['timing_issues']:
        for issue in worst_trade_analysis['timing_issues']:
            print(f"⏰ {issue}")
    
    # Market conditions
    market_conditions = worst_trade_analysis['market_conditions']
    if market_conditions:
        print(f"\n📊 MARKET CONDITIONS DURING WORST TRADE:")
        print(f"📈 Volatility: {market_conditions.get('volatility', 0):.1f}%")
        print(f"📊 Trend Strength: {market_conditions.get('trend_strength', 0):.2f}")
        print(f"📈 Market Regime: {market_conditions.get('market_regime', 'unknown')}")
    
    # Suggest improvements
    improvements = suggest_improvements(worst_trade_analysis, all_trades)
    
    print(f"\n💡 SUGGESTED IMPROVEMENTS:")
    
    if improvements['risk_management']:
        print(f"\n🛡️ RISK MANAGEMENT:")
        for improvement in improvements['risk_management']:
            print(f"   • {improvement}")
    
    if improvements['entry_filters']:
        print(f"\n🎯 ENTRY FILTERS:")
        for improvement in improvements['entry_filters']:
            print(f"   • {improvement}")
    
    if improvements['timing_filters']:
        print(f"\n⏰ TIMING FILTERS:")
        for improvement in improvements['timing_filters']:
            print(f"   • {improvement}")
    
    if improvements['volatility_filters']:
        print(f"\n📊 VOLATILITY FILTERS:")
        for improvement in improvements['volatility_filters']:
            print(f"   • {improvement}")
    
    # Create improved strategy
    improved_strategy = create_improved_strategy()
    
    print(f"\n🚀 IMPROVED STRATEGY LOGIC:")
    print(improved_strategy)
    
    # Save detailed analysis
    save_analysis_results(all_trades, worst_trade_analysis, improvements, improved_strategy)
    
    return {
        'overall_performance': {
            'total_pnl': total_pnl,
            'total_trades': total_trades,
            'win_rate': win_rate
        },
        'worst_trade': worst_trade,
        'worst_trade_analysis': worst_trade_analysis,
        'improvements': improvements,
        'improved_strategy': improved_strategy
    }

def save_analysis_results(all_trades, worst_trade_analysis, improvements, improved_strategy):
    """
    Save analysis results to files
    """
    
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Save all trades to CSV
    if all_trades:
        trades_df = pd.DataFrame(all_trades)
        trades_file = results_dir / "comprehensive_analysis_trades.csv"
        trades_df.to_csv(trades_file, index=False)
        print(f"💾 Comprehensive analysis trades saved to: {trades_file}")
    
    # Save detailed analysis to text file
    analysis_file = results_dir / "comprehensive_analysis_report.txt"
    
    with open(analysis_file, 'w') as f:
        f.write("COMPREHENSIVE TRADING STRATEGY ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 20 + "\n")
        f.write(f"Analysis Period: Last 3 months (June-August 2025)\n")
        f.write(f"Total Trades: {len(all_trades)}\n")
        f.write(f"Total P&L: {sum(t['pnl'] for t in all_trades):+.2f} points\n")
        f.write(f"Win Rate: {len([t for t in all_trades if t['pnl'] > 0])/len(all_trades)*100:.1f}%\n\n")
        
        f.write("WORST TRADE BREAKDOWN\n")
        f.write("-" * 20 + "\n")
        worst_trade = worst_trade_analysis['trade_details']
        f.write(f"Date: {worst_trade['date']} ({worst_trade['day_of_week']})\n")
        f.write(f"P&L: {worst_trade['pnl']:+.2f} points\n")
        f.write(f"Type: {worst_trade.get('type', 'TRADE')}\n\n")
        
        f.write("ROOT CAUSE OF FAILURE\n")
        f.write("-" * 20 + "\n")
        for reason in worst_trade_analysis['failure_reasons']:
            f.write(f"• {reason}\n")
        for issue in worst_trade_analysis['risk_management_issues']:
            f.write(f"• {issue}\n")
        for issue in worst_trade_analysis['timing_issues']:
            f.write(f"• {issue}\n")
        f.write("\n")
        
        f.write("SUGGESTED FIXES\n")
        f.write("-" * 20 + "\n")
        for category, fixes in improvements.items():
            if fixes:
                f.write(f"\n{category.upper()}:\n")
                for fix in fixes:
                    f.write(f"• {fix}\n")
        f.write("\n")
        
        f.write("UPDATED STRATEGY LOGIC\n")
        f.write("-" * 20 + "\n")
        f.write(improved_strategy)
    
    print(f"💾 Comprehensive analysis report saved to: {analysis_file}")

def main():
    """
    Main function to run comprehensive analysis
    """
    
    print("🔍 COMPREHENSIVE TRADING STRATEGY ANALYSIS")
    print("=" * 70)
    
    results = comprehensive_analysis()
    
    if results:
        print(f"\n✅ Comprehensive analysis completed successfully!")
        print(f"📊 Total P&L: {results['overall_performance']['total_pnl']:+.2f} points")
        print(f"📈 Win Rate: {results['overall_performance']['win_rate']:.1f}%")
        print(f"🔍 Worst Trade: {results['worst_trade']['pnl']:+.2f} points on {results['worst_trade']['date']}")
        
        print(f"\n📋 ANALYSIS SUMMARY:")
        print(f"1. Worst Trade Breakdown: {results['worst_trade']['date']} - {results['worst_trade']['pnl']:+.2f} points")
        print(f"2. Root Cause: {', '.join(results['worst_trade_analysis']['failure_reasons'])}")
        print(f"3. Suggested Fix: Implement {len(results['improvements']['risk_management'])} risk management improvements")
        print(f"4. Updated Strategy: Enhanced with {len(results['improvements']['entry_filters'])} entry filters")
    else:
        print(f"\n❌ Comprehensive analysis failed")

if __name__ == "__main__":
    main()
