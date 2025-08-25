import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from auth.token_manager import load_access_token
from utils.instruments import download_instruments_csv, get_banknifty_weekly_fut_token
from utils.data_fetch import fetch_5min_data
# Import the original strategy functions
from src.strategies.core.original import run_floating_band_strategy, save_strategy_report

load_dotenv()

def print_trade_summary(trades):
    """Print detailed trade summary with enhanced formatting."""
    if not trades:
        print("\n📊 No trades executed.")
        return
    
    print(f"\n📊 Trade Summary ({len(trades)} trades):")
    print("=" * 85)
    print(f"{'#':>2} {'Entry Time':>8} {'Side':>5} {'Entry':>7} {'Exit Time':>8} {'Exit':>7} {'P&L':>8} {'Reason':>15}")
    print("-" * 85)
    
    total_pnl = 0
    winning_trades = 0
    losing_trades = 0
    max_profit = float('-inf')
    max_loss = float('inf')
    
    for i, trade in enumerate(trades, 1):
        pnl = trade['pnl']
        total_pnl += pnl
        
        if pnl > 0:
            winning_trades += 1
            pnl_symbol = "✅"
            max_profit = max(max_profit, pnl)
        else:
            losing_trades += 1
            pnl_symbol = "❌"
            max_loss = min(max_loss, pnl)
        
        # Format times to show only HH:MM
        entry_time = trade['entry_time']
        exit_time = trade['exit_time']
        
        if hasattr(entry_time, 'strftime'):
            entry_str = entry_time.strftime("%H:%M")
        else:
            entry_str = str(entry_time)[:5] if len(str(entry_time)) >= 5 else str(entry_time)
            
        if hasattr(exit_time, 'strftime'):
            exit_str = exit_time.strftime("%H:%M")
        else:
            exit_str = str(exit_time)[:5] if len(str(exit_time)) >= 5 else str(exit_time)
            
        print(f"{i:2d} {entry_str:>8} {trade['side']:>5} {trade['entry_price']:7.2f} "
              f"{exit_str:>8} {trade['exit_price']:7.2f} "
              f"{pnl_symbol}{pnl:+6.2f} {trade['reason']:>15}")
    
    print("-" * 85)
    win_rate = (winning_trades / len(trades)) * 100 if trades else 0
    avg_profit = max_profit if max_profit != float('-inf') else 0
    avg_loss = max_loss if max_loss != float('inf') else 0
    
    print(f"💰 Total P&L: {total_pnl:+8.2f}")
    print(f"📈 Win Rate:  {win_rate:7.1f}% ({winning_trades}W/{losing_trades}L)")
    if max_profit != float('-inf'):
        print(f"🟢 Best Trade: {max_profit:+7.2f}")
    if max_loss != float('inf'):
        print(f"🔴 Worst Trade: {max_loss:+6.2f}")
    print("=" * 85)

def validate_data(df):
    """Validate the fetched data before processing."""
    if df.empty:
        raise ValueError("❌ DataFrame is empty")
    
    required_cols = ["time", "open", "high", "low", "close"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")
    
    # Check for valid OHLC data
    invalid_rows = df[(df['high'] < df['low']) | 
                      (df['high'] < df['open']) | 
                      (df['high'] < df['close']) | 
                      (df['low'] > df['open']) | 
                      (df['low'] > df['close'])].index
    
    if len(invalid_rows) > 0:
        print(f"⚠️  Warning: Found {len(invalid_rows)} invalid OHLC rows, cleaning...")
        df = df.drop(invalid_rows).reset_index(drop=True)
    
    print(f"✅ Data validation passed: {len(df)} valid candles")
    print(f"   Time range: {df['time'].min()} to {df['time'].max()}")
    print(f"   Price range: {df['low'].min():.2f} to {df['high'].max():.2f}")
    
    return df

def prepare_time_column(df):
    """Standardize time column format for better readability."""
    if "time" in df.columns:
        # Convert to datetime if not already
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        
        # Remove timezone info if present
        if df["time"].dt.tz is not None:
            df["time"] = df["time"].dt.tz_localize(None)
    
    return df

def calculate_avg_trade_duration(trades):
    """Calculate average trade duration in minutes."""
    if not trades:
        return "N/A"
    
    total_minutes = 0
    valid_trades = 0
    
    for trade in trades:
        try:
            entry = trade['entry_time']
            exit = trade['exit_time']
            
            if hasattr(entry, 'timestamp') and hasattr(exit, 'timestamp'):
                duration = (exit - entry).total_seconds() / 60
                total_minutes += duration
                valid_trades += 1
        except:
            continue
    
    if valid_trades > 0:
        avg_minutes = total_minutes / valid_trades
        if avg_minutes >= 60:
            return f"{avg_minutes/60:.1f} hours"
        else:
            return f"{avg_minutes:.0f} minutes"
    
    return "N/A"

def display_strategy_preview(df):
    """Show a preview of the data in the exact Excel format."""
    print(f"\n📋 Strategy Data Preview (Excel Column Order):")
    print("   Columns: Time | Volume | Range | High | Low | UB | LB | Signal")
    print("-" * 80)
    
    # Show first few rows with proper formatting
    for i in range(min(5, len(df))):
        time_str = df.loc[i, 'time'].strftime("%H:%M") if hasattr(df.loc[i, 'time'], 'strftime') else str(df.loc[i, 'time'])[:5]
        volume = df.loc[i, 'volume'] if 'volume' in df.columns else 0
        high = df.loc[i, 'high']
        low = df.loc[i, 'low']
        range_val = high - low
        ub = high + range_val
        lb = low - range_val
        
        print(f"   {time_str:>5} | {volume:>6} | {range_val:>5.2f} | {high:>7.2f} | {low:>7.2f} | {ub:>7.2f} | {lb:>7.2f} | {'Initial' if i==0 else '...'}")
    
    print("-" * 80)

def main():
    print("🚀 Starting Original Floating Band UB/LB Strategy")
    print("=" * 60)
    
    # Load environment variables
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise SystemExit("❌ Set API_KEY in .env file")
    
    # Load access token
    access_token = (load_access_token() or "").strip()
    if not access_token:
        raise SystemExit("❌ Run auth/login.py to generate today's access token")

    # Initialize KiteConnect
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)

    try:
        # Download instruments and get BANKNIFTY Weekly token
        print("📥 Downloading instruments dump...")
        df_inst = download_instruments_csv()
        token = get_banknifty_weekly_fut_token(df_inst)
        
        if not token:
            raise SystemExit("❌ Could not resolve BANKNIFTY weekly FUT token")
        print(f"✅ BANKNIFTY Weekly FUT token: {token}")

        # Interactive date input
        print("\n📅 Date Selection:")
        target_date = input("   Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not target_date:
            target_date = datetime.now().strftime("%Y-%m-%d")
            
        print(f"📊 Fetching 5-min candles for {target_date}...")
        df = fetch_5min_data(kite, token, date_str=target_date)
        
        if df.empty:
            raise SystemExit(f"❌ No candles returned for {target_date}. Market holiday or weekend?")
        
        # Validate and prepare data
        df = validate_data(df)
        df = prepare_time_column(df)

        # Display strategy preview
        display_strategy_preview(df)

        # Run the original floating band strategy
        print(f"\n🔄 Executing Original Floating Band Strategy on {len(df)} candles...")
        print("   Following Excel column order: Time | Volume | Range | High | Low | UB | LB | Signal")
        print("-" * 60)
        
        annotated, trades = run_floating_band_strategy(df)
        
        print("-" * 60)
        print("✅ Strategy execution completed")

        # Save report using the target_date with correct column order
        save_strategy_report(annotated, trades, target_date)
        
        # Print comprehensive trade summary
        print_trade_summary(trades)
        
        # Additional statistics
        if trades:
            signals_count = len(annotated[annotated['Signal'] != ''])
            print(f"\n📈 Strategy Performance Summary:")
            print(f"   Analysis Date: {target_date}")
            print(f"   Candles Processed: {len(df)}")
            print(f"   Trading Signals Generated: {signals_count}")
            print(f"   Actual Trades Executed: {len(trades)}")
            print(f"   Average Trade Duration: {calculate_avg_trade_duration(trades)}")
            
            # Signal breakdown
            signal_counts = annotated['Signal'].value_counts()
            if len(signal_counts) > 0:
                print(f"\n🎯 Signal Breakdown:")
                for signal, count in signal_counts.items():
                    if signal and signal.strip():
                        print(f"   {signal}: {count}")
        else:
            print(f"\n📊 Analysis Summary for {target_date}:")
            print(f"   Candles Processed: {len(df)}")
            print(f"   Result: No trades executed (no breakouts occurred)")
            
        print(f"\n📁 Reports saved in 'reports/' directory")
        print(f"📋 Excel columns: Time | Volume | Range | High | Low | UB | LB | Signal")

    except KeyboardInterrupt:
        print("\n⛔ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise SystemExit(1)

if __name__ == "__main__":
    main()