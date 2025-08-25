"""
Strategy-specific configuration settings.
"""

# Strategy V3 Configuration
V3_CONFIG = {
    "name": "Floating Band Strategy V3.0",
    "version": "3.0",
    "description": "Optimized Floating Band Strategy with advanced risk management",
    
    # Position sizing by day
    "position_sizes": {
        "monday": 0.8,      # 80% position size
        "tuesday": 0.4,     # 40% position size (worst day)
        "wednesday": 1.0,   # 100% position size
        "thursday": 1.2,    # 120% position size (best day)
        "friday": 0.9       # 90% position size
    },
    
    # Risk management
    "risk_management": {
        "stop_loss": 45,           # Stop loss in points
        "take_profit": 35,         # Take profit in points
        "daily_loss_limit": 120,   # Daily loss limit in points
        "max_daily_trades": 6,     # Maximum trades per day
        "trailing_stop_trigger": 25,  # Trailing stop after profit
        "time_exit_minutes": 12    # Time-based exit for losing trades
    },
    
    # Time filters
    "time_filters": {
        "trading_start": "10:30",
        "trading_end": "14:00",
        "skip_monday_tuesday_start": True,  # Skip first 30 minutes
        "eod_exit": "15:05"
    },
    
    # Technical filters
    "technical_filters": {
        "atr_thresholds": {
            "monday": 80,      # Lower threshold for volatile days
            "tuesday": 80,     # Lower threshold for volatile days
            "wednesday": 100,  # Standard threshold
            "thursday": 100,   # Standard threshold
            "friday": 120      # Higher threshold for weekend effect
        },
        "volume_multiplier": 1.2,     # Volume filter multiplier
        "trend_strength_min": 0.4,    # Minimum R-squared for trend
        "min_data_points": 50         # Minimum data points required
    },
    
    # Performance targets
    "performance_targets": {
        "monthly_roi": 20.0,      # Target monthly ROI
        "win_rate": 35.0,         # Target win rate
        "profit_factor": 1.5,     # Target profit factor
        "max_drawdown": 5.0       # Maximum acceptable drawdown
    }
}

# Strategy V2 Configuration
V2_CONFIG = {
    "name": "Floating Band Strategy V2.0",
    "version": "2.0",
    "description": "Enhanced Floating Band Strategy with basic risk management",
    
    # Position sizing by day
    "position_sizes": {
        "monday": 0.7,
        "tuesday": 0.5,
        "wednesday": 1.0,
        "thursday": 1.0,
        "friday": 0.8
    },
    
    # Risk management
    "risk_management": {
        "stop_loss": 50,
        "take_profit": 30,
        "daily_loss_limit": 150,
        "max_daily_trades": 8,
        "trailing_stop_trigger": 20,
        "time_exit_minutes": 15
    },
    
    # Time filters
    "time_filters": {
        "trading_start": "10:00",
        "trading_end": "14:30",
        "skip_monday_tuesday_start": False,
        "eod_exit": "15:10"
    },
    
    # Technical filters
    "technical_filters": {
        "atr_threshold": 100,      # Fixed ATR threshold
        "volume_multiplier": 0.8,
        "trend_strength_min": 0.3,
        "min_data_points": 20
    }
}

# Original Strategy Configuration
ORIGINAL_CONFIG = {
    "name": "Floating Band Strategy Original",
    "version": "1.0",
    "description": "Basic Floating Band Strategy without risk management",
    
    # Position sizing
    "position_sizes": {
        "monday": 1.0,
        "tuesday": 1.0,
        "wednesday": 1.0,
        "thursday": 1.0,
        "friday": 1.0
    },
    
    # Risk management (none)
    "risk_management": {
        "stop_loss": None,
        "take_profit": None,
        "daily_loss_limit": None,
        "max_daily_trades": None,
        "trailing_stop_trigger": None,
        "time_exit_minutes": None
    },
    
    # Time filters (none)
    "time_filters": {
        "trading_start": "09:15",
        "trading_end": "15:30",
        "skip_monday_tuesday_start": False,
        "eod_exit": "15:30"
    },
    
    # Technical filters (none)
    "technical_filters": {
        "atr_threshold": None,
        "volume_multiplier": None,
        "trend_strength_min": None,
        "min_data_points": 0
    }
}

# Strategy registry
STRATEGY_REGISTRY = {
    "original": ORIGINAL_CONFIG,
    "v2": V2_CONFIG,
    "v3": V3_CONFIG
}

def get_strategy_config(strategy_name: str):
    """Get configuration for a specific strategy."""
    return STRATEGY_REGISTRY.get(strategy_name.lower(), V3_CONFIG)

def get_available_strategies():
    """Get list of available strategies."""
    return list(STRATEGY_REGISTRY.keys())

def get_strategy_versions():
    """Get version information for all strategies."""
    return {name: config["version"] for name, config in STRATEGY_REGISTRY.items()}
