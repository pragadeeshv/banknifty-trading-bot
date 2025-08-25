# Contributing to BankNifty Trading Bot

Thank you for your interest in contributing to the BankNifty Trading Bot! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. **Fork the Repository**

- Click the "Fork" button on the GitHub repository page
- Clone your forked repository to your local machine

### 2. **Create a Feature Branch**

```bash
git checkout -b feature/your-feature-name
```

### 3. **Make Your Changes**

- Write clean, well-documented code
- Follow the existing code style and conventions
- Add tests for new functionality
- Update documentation as needed

### 4. **Test Your Changes**

```bash
# Run the backtest to ensure everything works
python backtest.py

# Test with your own Zerodha account (if applicable)
```

### 5. **Commit Your Changes**

```bash
git add .
git commit -m "Add: brief description of your changes"
```

### 6. **Push and Create Pull Request**

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Contribution Guidelines

### **Code Style**

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### **Documentation**

- Update README.md for new features
- Add docstrings to new functions
- Include usage examples
- Update any relevant configuration files

### **Testing**

- Test your changes thoroughly
- Ensure no breaking changes to existing functionality
- Test with different market conditions
- Verify risk management features work correctly

## 🎯 Areas for Contribution

### **Strategy Improvements**

- New trading strategies
- Enhanced risk management
- Better entry/exit conditions
- Performance optimizations

### **Features**

- Additional data sources
- More comprehensive analytics
- UI/UX improvements
- Mobile app integration

### **Documentation**

- Strategy explanations
- Tutorial videos
- Performance analysis
- Best practices guide

### **Bug Fixes**

- API integration issues
- Data handling problems
- Performance bottlenecks
- Security vulnerabilities

## 🚨 Important Notes

### **Security**

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Follow security best practices

### **Testing**

- Always test in a safe environment first
- Use paper trading when possible
- Test with historical data before live trading

### **Risk Management**

- Ensure all changes maintain proper risk controls
- Test stop-loss and position management
- Verify no unintended side effects

## 📞 Getting Help

- **Issues**: Create a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Code Review**: Request review from maintainers

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the BankNifty Trading Bot community! 🚀
