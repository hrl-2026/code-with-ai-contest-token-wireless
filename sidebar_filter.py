"""
Sidebar filter components for interactive data filtering.
"""
import streamlit as st
import pandas as pd

def create_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create sidebar filters and return filtered DataFrame.

    Args:
        df (pd.DataFrame): Original DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame based on user selections.
    """
    # Band multi-select
    available_bands = sorted(df["Band"].unique())
    selected_bands = st.sidebar.multiselect(
        "Frequency Band",
        options=available_bands,
        default=available_bands[:3] if len(available_bands) > 3 else available_bands
    )

    # RSRP range slider
    rsrp_min, rsrp_max = float(df["RSRP_dBm"].min()), float(df["RSRP_dBm"].max())
    rsrp_range = st.sidebar.slider(
        "RSRP Range (dBm)",
        min_value=rsrp_min,
        max_value=rsrp_max,
        value=(rsrp_min, rsrp_max),
        step=1.0
    )

    # SINR threshold slider
    sinr_min, sinr_max = float(df["SINR_dB"].min()), float(df["SINR_dB"].max())
    sinr_threshold = st.sidebar.slider(
        "Minimum SINR (dB)",
        min_value=sinr_min,
        max_value=sinr_max,
        value=sinr_min,
        step=0.5
    )

    # Apply filters
    filtered_df = df.copy()

    if selected_bands:
        filtered_df = filtered_df[filtered_df["Band"].isin(selected_bands)]

    filtered_df = filtered_df[
        (filtered_df["RSRP_dBm"] >= rsrp_range[0]) &
        (filtered_df["RSRP_dBm"] <= rsrp_range[1])
    ]

    filtered_df = filtered_df[filtered_df["SINR_dB"] >= sinr_threshold]

    # Show filter stats
    st.sidebar.info(f"**Filtered Data Points:** {len(filtered_df)} / {len(df)}")

    return filtered_df
