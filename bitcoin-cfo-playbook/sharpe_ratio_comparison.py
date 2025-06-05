"""
Module for visualizing asset class performance using Sharpe Ratio and risk-return profiles.

This script generates two plots:
1. A bar chart comparing Sharpe Ratios across asset classes.
2. A scatter plot showing the risk-return profile of each asset class.

Key features:
- Calculates Sharpe Ratios based on annual returns and volatility.
- Uses customizable asset data and visualization settings.
- Includes CFO-relevant insights for strategic decision-making.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

# Configuration constants
PLOT_STYLE = {
    "style": "whitegrid",
    "figure_size": (12, 12),
    "font_size": 12,
    "title_font_size": 16,
    "label_font_size": 14,
    "annotation_font_size": 12,
    "grid_alpha": 0.3,
    "scatter_size": 100,
    "scatter_alpha": 0.7
}

ASSET_CLASSES = {
    "Bitcoin": {"color": "#F7931A", "return": 0.42, "volatility": 0.65},
    "S&P 500": {"color": "#1E88E5", "return": 0.12, "volatility": 0.18},
    "Gold": {"color": "#FFC107", "return": 0.08, "volatility": 0.15},
    "US Bonds": {"color": "#4CAF50", "return": 0.03, "volatility": 0.05},
    "60/40 Portfolio": {"color": "#9C27B0", "return": 0.09, "volatility": 0.12}
}

RISK_FREE_RATE = 0.025  # 5-year Treasury yield (2.5%)

def calculate_sharpe_ratios(assets: Dict[str, Dict], risk_free_rate: float) -> Dict[str, float]:
    """
    Calculate Sharpe Ratios for each asset class.

    Args:
        assets (Dict[str, Dict]): Dictionary of assets with their returns and volatilities.
        risk_free_rate (float): Risk-free rate for Sharpe Ratio calculation.

    Returns:
        Dict[str, float]: Dictionary of asset names and their Sharpe Ratios.

    Raises:
        ValueError: If return or volatility data is missing or invalid.
    """
    sharpe_ratios = {}
    for asset, data in assets.items():
        if not all(key in data for key in ["return", "volatility"]):
            raise ValueError(f"Missing return or volatility data for {asset}")
        if data["volatility"] <= 0:
            raise ValueError(f"Volatility for {asset} must be positive")
        sharpe_ratios[asset] = (data["return"] - risk_free_rate) / data["volatility"]
    return sharpe_ratios

def create_dataframe(assets: Dict[str, Dict], sharpe_ratios: Dict[str, float]) -> pd.DataFrame:
    """
    Create a DataFrame for visualization from asset data and Sharpe Ratios.

    Args:
        assets (Dict[str, Dict]): Dictionary of assets with their properties.
        sharpe_ratios (Dict[str, float]): Dictionary of asset names and their Sharpe Ratios.

    Returns:
        pd.DataFrame: Sorted DataFrame with asset data for visualization.
    """
    df = pd.DataFrame({
        "Asset": list(assets.keys()),
        "Sharpe Ratio": [sharpe_ratios[asset] for asset in assets],
        "Annual Return": [assets[asset]["return"] for asset in assets],
        "Annual Volatility": [assets[asset]["volatility"] for asset in assets],
        "Color": [assets[asset]["color"] for asset in assets]
    })
    return df.sort_values("Sharpe Ratio", ascending=False).reset_index(drop=True)

def plot_sharpe_ratios(df: pd.DataFrame, ax: plt.Axes) -> None:
    """
    Plot a bar chart of Sharpe Ratios for each asset class.

    Args:
        df (pd.DataFrame): DataFrame containing asset data.
        ax (plt.Axes): Matplotlib axes object for the bar chart.
    """
    bars = ax.bar(df["Asset"], df["Sharpe Ratio"], color=df["Color"])
    ax.set_title("5-Year Sharpe Ratio Comparison (2020-2025)", fontsize=PLOT_STYLE["title_font_size"], fontweight="bold")
    ax.set_ylabel("Sharpe Ratio", fontsize=PLOT_STYLE["label_font_size"])
    ax.grid(True, axis="y", alpha=PLOT_STYLE["grid_alpha"])

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.02,
                f"{height:.2f}", ha="center", fontsize=PLOT_STYLE["annotation_font_size"])

def plot_risk_return(df: pd.DataFrame, ax: plt.Axes, risk_free_rate: float) -> None:
    """
    Plot a scatter chart of risk-return profiles for each asset class.

    Args:
        df (pd.DataFrame): DataFrame containing asset data.
        ax (plt.Axes): Matplotlib axes object for the scatter plot.
        risk_free_rate (float): Risk-free rate for reference line.
    """
    ax.scatter(df["Annual Volatility"], df["Annual Return"],
               s=PLOT_STYLE["scatter_size"], c=df["Color"], alpha=PLOT_STYLE["scatter_alpha"])

    # Add asset labels to scatter points
    for i, asset in enumerate(df["Asset"]):
        ax.annotate(asset,
                    (df["Annual Volatility"][i], df["Annual Return"][i]),
                    xytext=(7, 0),
                    textcoords="offset points",
                    fontsize=PLOT_STYLE["annotation_font_size"])

    # Add risk-free rate horizontal line
    ax.axhline(y=risk_free_rate, color="gray", linestyle="--", alpha=PLOT_STYLE["scatter_alpha"])
    ax.text(0.01, risk_free_rate + 0.005, f"Risk-Free Rate: {risk_free_rate:.1%}",
            fontsize=PLOT_STYLE["annotation_font_size"])

    # Plot settings
    ax.set_title("Risk-Return Profile", fontsize=PLOT_STYLE["title_font_size"], fontweight="bold")
    ax.set_xlabel("Annual Volatility (Risk)", fontsize=PLOT_STYLE["label_font_size"])
    ax.set_ylabel("Annual Return", fontsize=PLOT_STYLE["label_font_size"])
    ax.grid(True, alpha=PLOT_STYLE["grid_alpha"])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))

def main():
    """Main function to set up and generate the visualization."""
    # Set plot style
    sns.set_style(PLOT_STYLE["style"])
    plt.rcParams["figure.figsize"] = PLOT_STYLE["figure_size"]
    plt.rcParams["font.size"] = PLOT_STYLE["font_size"]

    try:
        # Calculate Sharpe Ratios
        sharpe_ratios = calculate_sharpe_ratios(ASSET_CLASSES, RISK_FREE_RATE)

        # Create DataFrame
        df = create_dataframe(ASSET_CLASSES, sharpe_ratios)

        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=PLOT_STYLE["figure_size"],
                                      gridspec_kw={"height_ratios": [2, 1]})

        # Generate plots
        plot_sharpe_ratios(df, ax1)
        plot_risk_return(df, ax2, RISK_FREE_RATE)

        # Add CFO insights
        plt.figtext(0.5, 0.01,
                    "CFO Insight: Bitcoin has demonstrated the highest Sharpe ratio among major asset classes over the 5-year period,\n"
                    "indicating superior risk-adjusted returns despite its higher volatility. This suggests potential value as a\n"
                    "strategic allocation in corporate treasury portfolios seeking to optimize risk-adjusted performance.",
                    ha="center", fontsize=PLOT_STYLE["annotation_font_size"],
                    bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="orange", alpha=0.8))

        # Adjust layout and display
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.12)
        plt.show()

        # Optional: Save the plot
        # plt.savefig("sharpe_ratio_comparison.png", dpi=300, bbox_inches="tight")
        # plt.close()

    except Exception as e:
        print(f"Error generating visualization: {e}")

if __name__ == "__main__":
    main()
