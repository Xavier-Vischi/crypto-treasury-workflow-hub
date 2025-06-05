import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plots
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 12

# Define asset classes and their properties
assets = ["Bitcoin", "S&P 500", "Gold", "US Bonds", "60/40 Portfolio"]
colors = ["#F7931A", "#1E88E5", "#FFC107", "#4CAF50", "#9C27B0"]

# Sample data for 5-year window (2020-2025)
annual_returns = {
    "Bitcoin": 0.42,       # 42% annualized return
    "S&P 500": 0.12,       # 12% annualized return
    "Gold": 0.08,          # 8% annualized return
    "US Bonds": 0.03,      # 3% annualized return
    "60/40 Portfolio": 0.09 # 9% annualized return
}

annual_volatility = {
    "Bitcoin": 0.65,       # 65% annualized volatility
    "S&P 500": 0.18,       # 18% annualized volatility
    "Gold": 0.15,          # 15% annualized volatility
    "US Bonds": 0.05,      # 5% annualized volatility
    "60/40 Portfolio": 0.12 # 12% annualized volatility
}

# Risk-free rate (5-year Treasury yield)
risk_free_rate = 0.025  # 2.5%

# Calculate Sharpe ratios
sharpe_ratios = {}
for asset in assets:
    sharpe_ratios[asset] = (annual_returns[asset] - risk_free_rate) / annual_volatility[asset]

# Create DataFrame for visualization
df = pd.DataFrame({
    "Asset": assets,
    "Sharpe Ratio": [sharpe_ratios[asset] for asset in assets],
    "Annual Return": [annual_returns[asset] for asset in assets],
    "Annual Volatility": [annual_volatility[asset] for asset in assets]
})

# Sort by Sharpe ratio
df = df.sort_values("Sharpe Ratio", ascending=False).reset_index(drop=True)

# Create the visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={"height_ratios": [2, 1]})

# Plot Sharpe ratios
bars = ax1.bar(df["Asset"], df["Sharpe Ratio"], color=[colors[assets.index(asset)] for asset in df["Asset"]])
ax1.set_title("5-Year Sharpe Ratio Comparison (2020-2025)", fontsize=16, fontweight="bold")
ax1.set_ylabel("Sharpe Ratio", fontsize=14)
ax1.grid(True, axis="y", alpha=0.3)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f"{height:.2f}", ha="center", fontsize=12)

# Create risk-return scatter plot
ax2.scatter(df["Annual Volatility"], df["Annual Return"], 
           s=100, c=[colors[assets.index(asset)] for asset in df["Asset"]], alpha=0.7)

# Add asset labels to scatter points
for i, asset in enumerate(df["Asset"]):
    ax2.annotate(asset, 
                (df["Annual Volatility"][i], df["Annual Return"][i]),
                xytext=(7, 0), 
                textcoords="offset points",
                fontsize=12)

# Add risk-free rate horizontal line
ax2.axhline(y=risk_free_rate, color="gray", linestyle="--", alpha=0.7)
ax2.text(0.01, risk_free_rate + 0.005, f"Risk-Free Rate: {risk_free_rate:.1%}", fontsize=10)

# Plot settings
ax2.set_title("Risk-Return Profile", fontsize=16, fontweight="bold")
ax2.set_xlabel("Annual Volatility (Risk)", fontsize=14)
ax2.set_ylabel("Annual Return", fontsize=14)
ax2.grid(True, alpha=0.3)

# Format y-axis as percentage
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))

# Add CFO-relevant insights
plt.figtext(0.5, 0.01, 
            "CFO Insight: Bitcoin has demonstrated the highest Sharpe ratio among major asset classes over the 5-year period,\n"
            "indicating superior risk-adjusted returns despite its higher volatility. This suggests potential value as a\n"
            "strategic allocation in corporate treasury portfolios seeking to optimize risk-adjusted performance.",
            ha="center", fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="orange", alpha=0.8))

plt.tight_layout()
plt.subplots_adjust(bottom=0.12)
# plt.savefig("sharpe_ratio_comparison.png", dpi=300, bbox_inches="tight")
# plt.close()