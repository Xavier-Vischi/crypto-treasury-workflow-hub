import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Set the style for the plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Create sample data for backtest dashboard
np.random.seed(42)  # For reproducibility

# Date range for the backtest (5 years of monthly data)
dates = pd.date_range(start='2020-01-01', end='2025-01-01', freq='ME')
n_periods = len(dates)

# Portfolio configurations
portfolios = {
    'Traditional': {'BTC_allocation': 0.00},
    'Conservative': {'BTC_allocation': 0.01},
    'Moderate': {'BTC_allocation': 0.05},
    'Aggressive': {'BTC_allocation': 0.10}
}

# Generate returns for Bitcoin and traditional assets
btc_returns = np.random.normal(0.035, 0.20, n_periods)  # Monthly mean 3.5%, vol 20%
trad_returns = np.random.normal(0.005, 0.04, n_periods)  # Monthly mean 0.5%, vol 4%

# Calculate portfolio returns for each configuration
portfolio_returns = {}
for name, config in portfolios.items():
    btc_weight = config['BTC_allocation']
    trad_weight = 1 - btc_weight
    portfolio_returns[name] = btc_weight * btc_returns + trad_weight * trad_returns

# Cumulative returns
cumulative_returns = {name: (1 + returns).cumprod() for name, returns in portfolio_returns.items()}

# Plot cumulative returns
plt.figure(figsize=(14, 8))
for name in portfolios:
    plt.plot(dates, cumulative_returns[name], label=name)

plt.title('Backtest Dashboard: Bitcoin Treasury Allocations (2020-2025)', fontsize=16, fontweight="bold")
plt.xlabel('Date', fontsize=14)
plt.ylabel('Portfolio Value (Normalized)', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
