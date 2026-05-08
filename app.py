"""
📡 5G Signal Visualization Dashboard
=====================================
Main entry point for the 5G signal data visualization web application.

Built with Streamlit + Folium + PyDeck + Plotly for the
"Code with AI" 5G Signal Visualization Challenge.

Usage:
    streamlit run app.py

Author: AI-assisted development via Hermes Agent
"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from data_loader import load_and_preprocess_data
from sidebar_filter import create_sidebar_filters
from map_visualizer import render_2d_map, render_3d_map
from chart_generator import plot_band_bar_chart, plot_terminal_pie_chart

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="5G 信号可视化看板",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Title and Description
# ============================================================
st.title("📡 5G 信号可视化看板")
st.markdown(
    """
    Interactive dashboard for 5G field test data visualization.
    Explore signal strength (RSRP) and quality (SINR) across
    different frequency bands in the Shanghai area.
    """
)

# ============================================================
# Data Loading (with caching)
# ============================================================
@st.cache_data
def load_data():
    """Load and preprocess the 5G signal CSV data."""
    return load_and_preprocess_data("data/signal_samples.csv")


df = load_data()

# ============================================================
# Sidebar Filters
# ============================================================
st.sidebar.title("📡 5G Dashboard")
filtered_df = create_sidebar_filters(df)

# ============================================================
# Main Content - Tabbed Layout
# ============================================================
tab1, tab2 = st.tabs(
    ["🗺️ 2D Signal Map", "🌐 3D Signal Map"]
)

# --- Tab 1: 2D Folium Map ---
with tab1:
    st.subheader("2D Signal Strength Map (Folium)")
    st.caption(
        "Points colored by RSRP: 🟢 **Good** (> -90 dBm)  |  "
        "🟡 **Fair** (-110 ~ -90 dBm)  |  "
        "🔴 **Weak** (< -110 dBm). "
        "Hover for details, use layer control to switch map style."
    )

    if filtered_df.empty:
        st.warning("No data points match the current filter criteria.")
    else:
        folium_map = render_2d_map(filtered_df)
        # Use the streamlit-folium component to render the map
        # This uses st_folium underneath with proper height and width
        map_data = st_folium(
            folium_map,
            width="100%",
            height=600,
            returned_objects=[],
            key="folium_map_2d",
        )

    # Quick stats below map
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Total Points", len(filtered_df))
    with col_s2:
        st.metric(
            "Avg RSRP",
            f"{filtered_df['RSRP_dBm'].mean():.1f} dBm"
            if not filtered_df.empty else "N/A",
        )
    with col_s3:
        st.metric(
            "Avg SINR",
            f"{filtered_df['SINR_dB'].mean():.1f} dB"
            if not filtered_df.empty else "N/A",
        )
    with col_s4:
        st.metric(
            "Avg Speed",
            f"{filtered_df['Download_Mbps'].mean():.1f} Mbps"
            if not filtered_df.empty else "N/A",
        )

    # --- Data overview chart below 2D map ---
    st.divider()
    st.markdown("#### 📊 各频段基站数量")
    band_chart = plot_band_bar_chart(filtered_df)
    st.plotly_chart(band_chart, use_container_width=True)

    # Raw data table (expandable)
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            filtered_df[
                [
                    "Latitude", "Longitude", "CellID", "Band",
                    "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps",
                ]
            ],
            use_container_width=True,
            height=300,
        )

# --- Tab 2: 3D PyDeck Map ---
with tab2:
    st.subheader("3D Signal Intensity Map (PyDeck)")
    st.caption(
        "3D columns where **height** represents download speed (Mbps) "
        "and **color** represents RSRP signal strength. "
        "Drag to rotate, scroll to zoom."
    )

    if filtered_df.empty:
        st.warning("No data points match the current filter criteria.")
    else:
        deck = render_3d_map(filtered_df)
        with st.container(height=650):
            st.pydeck_chart(deck, use_container_width=True)

    # --- Data overview chart below 3D map ---
    st.divider()
    st.markdown("#### 📊 不同类型终端占比")
    pie_chart = plot_terminal_pie_chart(filtered_df)
    st.plotly_chart(pie_chart, use_container_width=True)

# ============================================================
# Footer
# ============================================================
st.divider()
st.caption(
    "Built with ❤️ using Streamlit, Folium, PyDeck & Plotly "
    "— AI-assisted development for the 'Code with AI' Contest. "
    f"Data source: {len(df)} 5G signal samples in Shanghai area."
)
