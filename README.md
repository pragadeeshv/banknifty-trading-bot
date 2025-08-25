# 🚀 BankNifty Floating Band Intraday Trading Bot

A sophisticated **intraday trading bot** for BankNifty futures using the **Floating Band Strategy** with Zerodha Kite Connect API.

## 📊 **Strategy Overview**

The **Floating Band Strategy** is a dynamic breakout-based intraday trading system that:

- **Adapts to Market Conditions**: Bands recalculate based on new highs/lows
- **Directional Trading**: Follows market momentum with trend confirmation
- **Risk Management**: Implements stop-loss and position flipping
- **Real-time Execution**: Live trading with 5-minute data polling

### 🎯 **Strategy Logic**

1. **Initial Setup**: Calculate UB/LB from first 5-min candle (H1/L1)
2. **Dynamic Bands**: Recalculate when price makes new highs/lows
3. **Entry Signals**:
   - **BUY**: Price breaks above Upper Band (UB)
   - **SELL**: Price breaks below Lower Band (LB)
4. **Directional Trading**: Once direction is set, only allow breakouts in opposite direction
5. **Position Flipping**: Close existing position and open opposite when opposite band breaks
6. **EOD Square-off**: Close all positions at 15:10

## ✨ **Features**

- 🔐 **Secure Authentication**: Daily token management with Zerodha Kite Connect
- 📈 **Real-time Data**: Live 5-minute BankNifty futures data
- 🧪 **Backtesting**: Historical strategy testing with detailed reports
- 📊 **Performance Analytics**: Comprehensive P&L and trade analysis
- 🛡️ **Risk Management**: Configurable stop-loss and position limits
- 📱 **Live Trading**: Real-time order execution (with safety controls)
- 📋 **Trade Logging**: Detailed trade history and performance metrics

## 🚀 **Quick Start**

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/banknifty-trading-bot.git
cd banknifty-trading-bot
```

### 2. **Install Dependencies**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. **Configure Environment**

```bash
# Copy example environment file
cp env.example .env

# Edit .env with your Zerodha credentials
nano .env
```

**Required Environment Variables:**

```env
API_KEY=your_kite_api_key_here
API_SECRET=your_kite_api_secret_here
```

### 4. **Generate Access Token**

```bash
python auth/login.py
```

- Open the provided login URL
- Complete Zerodha login
- Copy the `request_token` from redirect URL
- Paste it back to complete authentication

### 5. **Run Backtest**

```bash
python backtest.py
```

### 6. **Live Trading** (Optional)

```bash
# Dry run (no real orders)
python live_trader.py

# Enable live orders (after thorough testing)
ENABLE_LIVE_ORDERS=1 python live_trader.py
```

## 📁 **Project Structure**

```
banknifty-trading-bot/
├── auth/                 # Authentication modules
│   ├── login.py         # Token generation
│   └── token_manager.py # Token management
├── strategy/            # Trading strategies
│   └── core/
│       └── ub_lb.py    # Main Floating Band Strategy
├── utils/              # Utility functions
│   ├── data_fetch.py   # Data fetching utilities
│   └── instruments.py  # Instrument management
├── results/            # Backtest results
├── reports/            # Trading reports
├── backtest.py         # Main backtesting script
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from env.example)
└── README.md          # This file
```

## 📊 **Performance Analysis**

### **Strategy Performance (Jan-Aug 2025)**

- **Total P&L**: -370.20 points (-₹5,553)
- **Win Rate**: 35.9%
- **Total Trades**: 231
- **Best Day**: Thursday (+1027.20 points)
- **Worst Days**: Monday/Tuesday (combined -1428.40 points)

### **Key Insights**

- ✅ **Thursday Performance**: +1027.20 points (66.7% win rate)
- ✅ **August Recovery**: +311.00 points (64.3% win rate)
- ❌ **July Challenges**: -897.00 points (34.8% win rate)
- ❌ **Monday/Tuesday**: Poor performance (-1428.40 points)

## ⚙️ **Configuration**

### **Environment Variables**

```env
# Required
API_KEY=your_kite_api_key
API_SECRET=your_kite_api_secret

# Optional
DEFAULT_QTY=1
DEFAULT_SYMBOL=BANKNIFTY
MARKET_START_TIME=09:15
MARKET_END_TIME=15:30
SQUARE_OFF_TIME=15:10
DAILY_STOP_LOSS=200
MAX_TRADES_PER_DAY=10
ENABLE_LIVE_ORDERS=0
```

### **Strategy Parameters**

Edit `strategy/core/ub_lb.py` to modify:

- Band calculation logic
- Entry/exit conditions
- Stop-loss levels
- Position sizing

## 📈 **Usage Examples**

### **Daily Backtest**

```bash
python backtest.py
# Outputs: reports/BNF_YYYY-MM-DD.xlsx
```

### **Historical Analysis**

```bash
# Analyze specific date range
python analyze_jan_to_august.py
```

### **Live Trading**

```bash
# Test mode (no real orders)
python live_trader.py

# Live trading (real orders)
ENABLE_LIVE_ORDERS=1 python live_trader.py
```

## 🔧 **Customization**

### **Adding New Strategies**

1. Create new strategy file in `strategy/`
2. Implement required interface
3. Update main scripts to use new strategy

### **Modifying Risk Management**

- Edit stop-loss logic in strategy files
- Adjust position sizing in `utils/`
- Modify exit conditions

### **Data Sources**

- Currently uses Zerodha Kite Connect
- Can be extended to other brokers
- Supports multiple timeframes

## ⚠️ **Important Notes**

### **Security**

- ⚠️ **Never commit `.env` file** (contains API secrets)
- ⚠️ **Access tokens expire daily** - run `auth/login.py` each morning
- ⚠️ **Test thoroughly** before live trading

### **Risk Disclaimer**

- 📊 This is for educational purposes
- 💰 Trading involves substantial risk
- 📈 Past performance doesn't guarantee future results
- 🛡️ Always use proper risk management

### **Limitations**

- 🔄 Requires daily token refresh
- 📱 Zerodha API rate limits apply
- ⏰ Market hours only (9:15 AM - 3:30 PM IST)
- 📊 Strategy performance varies with market conditions

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 **Support**

- 📧 **Issues**: [GitHub Issues](https://github.com/yourusername/banknifty-trading-bot/issues)
- 📖 **Documentation**: Check the code comments and strategy files
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/banknifty-trading-bot/discussions)

## 🙏 **Acknowledgments**

- **Zerodha Kite Connect** for the trading API
- **Python Community** for excellent libraries
- **Trading Community** for strategy insights

---

**⭐ Star this repository if you find it helpful!**

**⚠️ Remember: Trading involves risk. Use at your own discretion.**
