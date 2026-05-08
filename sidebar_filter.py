"""
5G Signal Visualization - Sidebar Filter Module
================================================
Provides interactive sidebar filters for the 5G dashboard.

Filters:
  - Frequency Band: Multi-select dropdown
  - RSRP Range: Slider (dBm)
  - SINR Minimum: Slider (dB)
  - Terminal Type: Multi-select dropdown
  - Cell ID search: Text input

All filters update the displayed data in real time.
"""

import streamlit as st
import pandas as pd


def create_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create sidebar filter widgets and return the filtered DataFrame.

    Args:
        df (pd.DataFrame): Original unfiltered DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame based on user selections.
    """
    st.sidebar.header("🔧 Filter Controls")

    # -- Frequency Band multi-select --
    available_bands = sorted(df["Band"].unique())
    selected_bands = st.sidebar.multiselect(
        "📡 Frequency Band",
        options=available_bands,
        default=available_bands[:3] if len(available_bands) > 3 else available_bands,
        help="Select one or more 5G frequency bands to display.",
    )

    # -- RSRP range slider --
    rsrp_min = float(df["RSRP_dBm"].min())
    rsrp_max = float(df["RSRP_dBm"].max())
    rsrp_range = st.sidebar.slider(
        "📶 RSRP Range (dBm)",
        min_value=rsrp_min,
        max_value=rsrp_max,
        value=(rsrp_min, rsrp_max),
        step=1.0,
        help="Filter by Reference Signal Received Power range. "
             "Higher values (closer to 0) = stronger signal.",
    )

    # -- SINR minimum threshold --
    sinr_min = float(df["SINR_dB"].min())
    sinr_max = float(df["SINR_dB"].max())
    sinr_threshold = st.sidebar.slider(
        "📊 Min SINR (dB)",
        min_value=sinr_min,
        max_value=sinr_max,
        value=sinr_min,
        step=0.5,
        help="Filter by minimum Signal-to-Interference-plus-Noise Ratio. "
             "Higher = cleaner signal.",
    )

    # -- Terminal Type multi-select --
    available_types = sorted(df["TerminalType"].unique())
    selected_types = st.sidebar.multiselect(
        "📱 Terminal Type",
        options=available_types,
        default=available_types,
        help="Filter by terminal device type.",
    )

    # -- Cell ID search (optional) --
    cell_id_search = st.sidebar.text_input(
        "🔍 Cell ID Search",
        value="",
        placeholder="e.g. 1926",
        help="Filter by Cell ID number.",
    )

    st.sidebar.divider()
    st.sidebar.caption("🔄 All filters update the map and charts in real time.")

    # -- Apply filters --
    filtered_df = df.copy()

    if selected_bands:
        filtered_df = filtered_df[filtered_df["Band"].isin(selected_bands)]

    filtered_df = filtered_df[
        (filtered_df["RSRP_dBm"] >= rsrp_range[0]) &
        (filtered_df["RSRP_dBm"] <= rsrp_range[1])
    ]

    filtered_df = filtered_df[filtered_df["SINR_dB"] >= sinr_threshold]

    if selected_types:
        filtered_df = filtered_df[filtered_df["TerminalType"].isin(selected_types)]

    if cell_id_search.strip():
        try:
            cell_id = int(cell_id_search.strip())
            filtered_df = filtered_df[filtered_df["CellID"] == cell_id]
        except ValueError:
            pass  # Ignore non-numeric input

    # -- Show filter stats --
    total = len(df)
    remaining = len(filtered_df)
    st.sidebar.info(
        f"**Filtered:** {remaining} / {total} points "
        f"({remaining / total * 100:.1f}%)"
    )

    return filtered_df
