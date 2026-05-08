"""
Data loading and preprocessing module.
"""
import pandas as pd
import numpy as np

def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data and preprocess for visualization.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Preprocessed DataFrame with added color column.
    """
    # Load data
    df = pd.read_csv(filepath)

    # Ensure required columns exist (adjust column names if needed)
    required_columns = ["Latitude", "Longitude", "Band", "RSRP_dBm", "SINR_dB"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in data.")

    # Clean data: drop rows with critical missing values
    df = df.dropna(subset=required_columns)

    # Add color column based on RSRP
    def rsrp_to_color(rsrp):
        if rsrp > -90:
            return [0, 255, 0, 160]  # Green
        elif rsrp >= -110:
            return [255, 255, 0, 160]  # Yellow
        else:
            return [255, 0, 0, 160]  # Red

    df["RSRP_color"] = df["RSRP_dBm"].apply(lambda x: rsrp_to_color(x))

    # Simulate download speed for 3D visualization (if not present)
    if "Download_Speed_Mbps" not in df.columns:
        # Simple simulation: higher RSRP and SINR -> higher speed
        df["Download_Speed_Mbps"] = (
            (df["RSRP_dBm"] + 130) * 0.5 + (df["SINR_dB"] + 5) * 2
        ).clip(10, 300)

    return df
