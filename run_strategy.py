#!/usr/bin/env python3
"""
Strategy selector for the Kite Trading Bot.
This script allows you to choose which strategy to run.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def show_strategy_menu():
    """Show available strategies menu."""
    print("🚀 Kite Trading Bot - Strategy Selector")
    print("=" * 50)
    print("📈 Available Strategies:")
    print("1. Original (Floating Band UB/LB) - Default ✅")
    print("2. Exit")
    print("-" * 50)

def run_original_strategy():
    """Run the original strategy."""
    print("📊 Running Original Strategy...")
    print("📈 Strategy: Floating Band UB/LB")
    print("⏰ Timeframe: 5minute")
    print("📊 Instrument: BankNifty Weekly Futures")
    print("-" * 40)
    
    from backtesting.engine import main
    main()

def run_original_strategy():
    """Run the original strategy."""
    print("📊 Running Original Strategy...")
    print("📈 Strategy: Floating Band UB/LB")
    print("⏰ Timeframe: 5minute")
    print("📊 Instrument: BankNifty Weekly Futures")
    print("-" * 40)
    
    from backtesting.engine import main
    main()



def main():
    """Main function to select and run strategy."""
    while True:
        show_strategy_menu()
        
        try:
            choice = input("🎯 Select strategy (1-2): ").strip()
            
            if choice == "1":
                run_original_strategy()
                break
            elif choice == "2":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-2.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main()
