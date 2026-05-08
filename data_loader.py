"""
5G Signal Visualization - Data Loading and Preprocessing Module
================================================================
Loads the 5G signal CSV data, validates required columns,
and preprocesses for visualization.

Adds:
  - RSRP_color (RGBA) for PyDeck 3D rendering
  - RSRP_hex_color for Folium 2D rendering
  - Download_Speed_Mbps (simulated if missing)
"""

import pandas as pd
import numpy as np


# RSRP thresholds (dBm)
RSRP_GOOD_THRESHOLD = -90    # Above this → green
RSRP_WEAK_THRESHOLD = -110   # Below this → red

# Required columns that must exist in the CSV
REQUIRED_COLUMNS = [
    "Latitude", "Longitude", "CellID", "Band",
    "RSRP_dBm", "SINR_dB", "TerminalType",
]


def rsrp_to_color(rsrp: float) -> list:
    """
    Convert RSRP value to RGBA color array for PyDeck.

    Args:
        rsrp: Signal strength in dBm.

    Returns:
        RGBA list: [R, G, B, A] with values 0-255.
    """
    if rsrp > RSRP_GOOD_THRESHOLD:
        return [0, 255, 0, 160]       # Green - strong signal
    elif rsrp >= RSRP_WEAK_THRESHOLD:
        return [255, 255, 0, 160]     # Yellow - fair signal
    else:
        return [255, 0, 0, 160]       # Red - weak signal


def rsrp_to_hex(rsrp: float) -> str:
    """
    Convert RSRP value to hex color string for Folium.

    Args:
        rsrp: Signal strength in dBm.

    Returns:
        Hex color string like '#00cc00'.
    """
    if rsrp > RSRP_GOOD_THRESHOLD:
        return "#00cc00"
    elif rsrp >= RSRP_WEAK_THRESHOLD:
        return "#ffcc00"
    else:
        return "#ff3333"


def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data and preprocess for visualization.

    Args:
        filepath (str): Path to the CSV data file.

    Returns:
        pd.DataFrame: Preprocessed DataFrame with added color columns.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing from the data.
    """
    # Load raw data
    df = pd.read_csv(filepath)

    # Validate required columns exist
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}. "
            f"Expected columns: {REQUIRED_COLUMNS}"
        )

    # Drop rows with critical missing values
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # --- Add color columns for visualization ---

    # RGBA color for PyDeck (3D map)
    df["RSRP_color"] = df["RSRP_dBm"].apply(rsrp_to_color)

    # Hex color for Folium (2D map)
    df["RSRP_hex_color"] = df["RSRP_dBm"].apply(rsrp_to_hex)

    # --- Simulate download speed if not present in data ---
    if "Download_Mbps" not in df.columns:
        # Real CSV has Download_Mbps, but keep fallback for safety
        df["Download_Mbps"] = (
            (df["RSRP_dBm"] + 130) * 0.5 + (df["SINR_dB"] + 5) * 2
        ).clip(10, 300)
    else:
        # Ensure no nulls in existing Download_Mbps column
        df["Download_Mbps"] = df["Download_Mbps"].fillna(
            ((df["RSRP_dBm"] + 130) * 0.5 + (df["SINR_dB"] + 5) * 2).clip(10, 1000)
        )

    return df
