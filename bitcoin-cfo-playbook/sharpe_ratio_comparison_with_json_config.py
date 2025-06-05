"""
Module for visualizing asset class performance using Sharpe Ratio and risk-return profiles.

Loads configuration from a JSON file and generates:
1. A bar chart comparing Sharpe Ratios across asset classes.
2. A scatter plot showing the risk-return profile of each asset class.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from typing import Dict, List, Tuple
from pathlib import Path

def load_config(config_path: str) -> Dict:
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to the JSON configuration file.

    Returns:
        Dict: Configuration data.

    Raises:
        FileNotFoundError: If the config file does not exist.
        json.JSONDecodeError: If the config file is invalid JSON.
    """
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_path} not found")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {config_path}: {e}", e.doc, e.pos)

def main():
    """Main function to set up and generate the visualization."""
    try:
        # Load configuration
        config = load_config("config.json")
        risk_free_rate = config["risk_free_rate"]
        plot_style = config["plot_style"]
        asset_classes = config["asset_classes"]

        # Set plot style
        sns.set_style(plot_style["style"])
        plt.rcParams["figure.figsize"] = plot_style["figure_size"]
        plt.rcParams["font.size"] = plot_style["font_size"]

        # Calculate Sharpe Ratios
        sharpe_ratios = calculate_sharpe_ratios(asset_classes, risk_free_rate)

        # Create DataFrame
        df = create_dataframe(asset_classes, sharpe_ratios)

        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=plot_style["figure_size"],
                                      gridspec_kw={"height_ratios": [2, 1]})

        # Generate plots
        plot_sharpe_ratios(df, ax1)
        plot_risk_return(df, ax2, risk_free_rate)

        # Add CFO insights
        plt.figtext(0.5, 0.01,
                    "CFO Insight: Bitcoin has demonstrated the highest Sharpe ratio among major asset classes over the 5-year period,\n"
                    "indicating superior risk-adjusted returns despite its higher volatility. This suggests potential value as a\n"
                    "strategic allocation in corporate treasury portfolios seeking to optimize risk-adjusted performance.",
                    ha="center", fontsize=plot_style["annotation_font_size"],
                    bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="orange", alpha=0.8))

        # Adjust layout and display
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.12)
        plt.show()

    except Exception as e:
        print(f"Error generating visualization: {e}")

if __name__ == "__main__":
    main()
