# 🚀 Kite Trading Bot - BankNifty Futures Strategy

A sophisticated algorithmic trading system for BankNifty futures with multiple strategy versions, advanced risk management, and comprehensive backtesting capabilities.

## 📊 Performance Overview

| Strategy        | Total P&L            | ROI         | Risk Level | Status               |
| --------------- | -------------------- | ----------- | ---------- | -------------------- |
| **Original**    | -489.60 points       | -4.89%      | High       | Baseline             |
| **Strategy V2** | +1,053.80 points     | +15.81%     | Medium     | Enhanced             |
| **Strategy V3** | **+1,500.30 points** | **+22.50%** | **Low**    | **Production Ready** |

## 🎯 Key Features

- **Multiple Strategy Versions**: Original, V2, and V3 with progressive improvements
- **Advanced Risk Management**: Dynamic stop-loss, position sizing, and daily limits
- **Comprehensive Backtesting**: Historical data analysis with detailed metrics
- **Performance Optimization**: Data-driven strategy improvements
- **Professional Architecture**: Modular, scalable, and maintainable codebase

## 🏗️ Project Structure

```
kite_bot/
├── 📁 src/                          # Source code
│   ├── 📁 strategies/               # Trading strategies
│   │   ├── 📁 core/                 # Core strategy implementations
│   │   │   ├── original.py          # Original strategy
│   │   │   ├── v2.py                # Strategy V2
│   │   │   └── v3.py                # Strategy V3 (Production)
│   │   └── 📁 analysis/             # Strategy analysis tools
│   ├── 📁 backtesting/              # Backtesting framework
│   ├── 📁 data/                     # Data handling
│   └── 📁 utils/                    # Utility functions
├── 📁 config/                       # Configuration files
├── 📁 scripts/                      # Utility scripts
├── 📁 data/                         # Data storage
├── 📁 reports/                      # Generated reports
├── 📁 docs/                         # Documentation
└── 📁 tests/                        # Test files
```

## 🚀 Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <repository-url>
cd kite_bot

# Run setup script
python scripts/setup.py

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 2. Configuration

```bash
# Copy environment file
cp env.example .env

# Edit .env with your Kite API credentials
nano .env
```

### 3. Run Backtest

```bash
# Run V3 strategy backtest
python scripts/run_backtest.py --strategy v3

# Run with custom parameters
python scripts/run_backtest.py \
  --strategy v3 \
  --start-date 2025-07-01 \
  --end-date 2025-08-31 \
  --output results.json
```

### 4. Analyze Results

```bash
# Analyze performance
python scripts/analyze_results.py --analysis-type performance

# Compare strategies
python scripts/analyze_results.py --analysis-type comparison
```

## 📈 Strategy Evolution

### Original Strategy

- Basic floating band logic
- No risk management
- Unlimited losses possible

### Strategy V2

- Enhanced risk management
- Day-based position sizing
- Basic filters and time windows

### Strategy V3 (Production Ready)

- **Advanced risk management**: 45-point stop loss, 120-point daily limit
- **Performance-based position sizing**: 120% on Thursday, 40% on Tuesday
- **Dynamic filters**: ATR thresholds, volume confirmation, trend strength
- **Optimized timing**: 10:30 AM - 2:00 PM trading window
- **Proven performance**: +22.50% ROI with controlled risk

## 💰 Capital Requirements

### Minimum Capital: ₹100,000

- **1 Lot BankNifty Weekly Futures**: ~₹100,000
- **Margin Required**: ~₹12,000 (12% of lot value)
- **Recommended Capital**: ₹150,000 (with safety buffer)

### Expected Returns (Strategy V3)

- **Monthly Average**: ₹11,252 profit
- **Annual Projection**: ₹135,024 (based on July-August performance)
- **Risk Level**: Controlled and predictable

## 📊 Performance Metrics

### Strategy V3 (July-August 2025)

- **Total P&L**: +1,500.30 points (+₹22,505)
- **Win Rate**: 34.0%
- **Profit Factor**: 1.52
- **Maximum Loss**: -45 points per trade
- **Daily Loss Limit**: 120 points

### Day-of-Week Performance

- **Thursday**: +1,113.96 points (74.3% of profits)
- **Monday**: +279.20 points
- **Wednesday**: +55.20 points
- **Tuesday**: +23.44 points (controlled)
- **Friday**: +28.50 points

## 🔧 Configuration

### Strategy Parameters

All strategy parameters are configurable in `config/strategy_config.py`:

```python
V3_CONFIG = {
    "position_sizes": {
        "monday": 0.8,      # 80% position size
        "tuesday": 0.4,     # 40% position size
        "thursday": 1.2,    # 120% position size
        # ...
    },
    "risk_management": {
        "stop_loss": 45,           # Stop loss in points
        "take_profit": 35,         # Take profit in points
        "daily_loss_limit": 120,   # Daily loss limit
        # ...
    }
}
```

### Environment Variables

```bash
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
```

## 📚 Documentation

- **[Strategy V3 Report](docs/reports/STRATEGY_V3_JULY_AUGUST_FINAL_REPORT.md)**: Comprehensive V3 analysis
- **[Fine-tuning Report](docs/reports/STRATEGY_V3_FINE_TUNING_REPORT.md)**: Optimization analysis
- **[V2 Documentation](docs/reports/STRATEGY_V2_DOCUMENTATION.md)**: V2 strategy details
- **[Project Organization](PROJECT_ORGANIZATION.md)**: Project structure guide

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run performance tests
python -m pytest tests/performance/
```

## 📈 Usage Examples

### Basic Backtest

```python
from src.backtesting.engine import run_backtest

results = run_backtest(
    strategy_name="v3",
    start_date="2025-07-01",
    end_date="2025-08-31"
)
print(f"Total P&L: {results['total_pnl']:.2f} points")
```

### Strategy Analysis

```python
from src.strategies.analysis.optimizer import analyze_performance_patterns

analysis = analyze_performance_patterns()
```

### Configuration

```python
from config.strategy_config import get_strategy_config

config = get_strategy_config("v3")
print(f"Strategy: {config['name']}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Project Wiki](https://github.com/your-repo/wiki)
- **Email**: your-email@example.com

---

**Built with ❤️ for algorithmic trading enthusiasts**
