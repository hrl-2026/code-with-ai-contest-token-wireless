
# ==========================================
# 你的代码从这里开始... 
# (提示：不要手写，让 AI 帮你写！)
# ==========================================

"""
5G Signal Visualization Dashboard
Main Streamlit application entry point.
"""
import streamlit as st
import pandas as pd
from data_loader import load_and_preprocess_data
from sidebar_filter import create_sidebar_filters
from map_visualizer import render_2d_map, render_3d_map
from chart_generator import plot_band_bar_chart

# Page configuration
st.set_page_config(
    page_title="5G 信号可视化看板",
    page_icon="📡",
    layout="wide"
)

# Title and description
st.title("📡 5G 信号可视化看板")
st.markdown("""
    This interactive dashboard visualizes 5G field test data.
    Use the sidebar filters to explore signal strength (RSRP) and quality (SINR) across different frequency bands.
""")

# Load data with caching
@st.cache_data
def load_data():
    return load_and_preprocess_data("data/signal_samples.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filter Controls")
filtered_df = create_sidebar_filters(df)

# Main content area
tab1, tab2 = st.tabs(["📊 2D Map View", "🌐 3D Map View"])

with tab1:
    st.subheader("2D Signal Strength Map")
    st.pydeck_chart(render_2d_map(filtered_df))

with tab2:
    st.subheader("3D Signal Intensity Map")
    st.pydeck_chart(render_3d_map(filtered_df))

# Charts section
st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Base Station Count by Frequency Band")
    band_chart = plot_band_bar_chart(filtered_df)
    st.plotly_chart(band_chart, use_container_width=True)

with col2:
    st.subheader("Data Summary")
    st.metric("Total Data Points", len(filtered_df))
    st.metric("Average RSRP (dBm)", round(filtered_df["RSRP_dBm"].mean(), 2))
    st.metric("Average SINR (dB)", round(filtered_df["SINR_dB"].mean(), 2))

# Footer
st.caption("Built with AI-assisted development for the 'Code with AI' Contest.")
