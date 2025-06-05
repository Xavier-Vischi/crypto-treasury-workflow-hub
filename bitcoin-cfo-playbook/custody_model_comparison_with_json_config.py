"""
Module for visualizing Bitcoin custody model comparisons using a heatmap.

This script loads custody model data from a JSON configuration file and generates
a heatmap to compare different custody models across various attributes.

Key features:
- Compares custody models based on attributes like security, cost, and compliance.
- Uses a customizable heatmap for visualization.
- Includes error handling and configuration file support for flexibility.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from typing import Dict, List
from pathlib import Path

# Configuration constants
PLOT_STYLE = {
    "style": "whitegrid",
    "figure_size": (10, 6),
    "font_size": 12,
    "title_font_size": 14
}

def load_config(config_path: str) -> Dict:
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to the JSON configuration file.

    Returns:
        Dict: Configuration data containing custody models, attributes, and scores.

    Raises:
        FileNotFoundError: If the config file does not exist.
        json.JSONDecodeError: If the config file is invalid JSON.
        ValueError: If required configuration keys are missing or invalid.
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        # Validate required keys
        required_keys = ["custody_models", "attributes", "scores"]
        if not all(key in config for key in required_keys):
            raise ValueError(f"Config file missing required keys: {required_keys}")
        
        # Validate scores structure
        if not all(model in config["scores"] for model in config["custody_models"]):
            raise ValueError("Scores dictionary missing data for some custody models")
        for model, scores in config["scores"].items():
            if len(scores) != len(config["attributes"]):
                raise ValueError(f"Scores for {model} do not match number of attributes")
            if not all(isinstance(score, (int, float)) and 1 <= score <= 5 for score in scores):
                raise ValueError(f"Scores for {model} must be numbers between 1 and 5")
        
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_path} not found")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {config_path}: {e}", e.doc, e.pos)

def create_dataframe(custody_models: List[str], attributes: List[str], scores: Dict[str, List[float]]) -> pd.DataFrame:
    """
    Create a DataFrame for custody model comparison.

    Args:
        custody_models (List[str]): List of custody model names.
        attributes (List[str]): List of attributes for comparison.
        scores (Dict[str, List[float]]): Dictionary of scores for each custody model.

    Returns:
        pd.DataFrame: DataFrame with custody models as columns and attributes as rows.
    """
    return pd.DataFrame(scores, index=attributes)

def plot_heatmap(df: pd.DataFrame, title: str) -> None:
    """
    Plot a heatmap for custody model comparison.

    Args:
        df (pd.DataFrame): DataFrame containing comparison data.
        title (str): Title for the heatmap.
    """
    plt.figure(figsize=PLOT_STYLE["figure_size"])
    sns.heatmap(df, annot=True, cmap="YlGnBu", cbar=False, fmt=".1f")
    plt.title(title, fontsize=PLOT_STYLE["title_font_size"])
    plt.tight_layout()

def main():
    """Main function to set up and generate the custody model comparison heatmap."""
    try:
        # Load configuration
        config = load_config("custody_config.json")
        custody_models = config["custody_models"]
        attributes = config["attributes"]
        scores = config["scores"]

        # Set plot style
        sns.set_style(PLOT_STYLE["style"])
        plt.rcParams["font.size"] = PLOT_STYLE["font_size"]

        # Create DataFrame
        df = create_dataframe(custody_models, attributes, scores)

        # Plot heatmap
        plot_heatmap(df, "Bitcoin Custody Model Comparison")

        # Display plot
        plt.show()

    except Exception as e:
        print(f"Error generating visualization: {e}")

if __name__ == "__main__":
    main()
