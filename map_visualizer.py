"""
5G Signal Visualization - Map Rendering Module
===============================================
Provides 2D (Folium) and 3D (PyDeck) map rendering functions
for 5G signal data visualization.

Key Features:
  - 2D map uses real MapQuest/OpenStreetMap tile background
  - Data points colored by RSRP signal strength (green/yellow/red)
  - Small, semi-transparent points for a scattered, professional look
  - 3D column map with height proportional to download speed
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import pydeck as pdk


# -- Color mapping constants --
# RSRP thresholds (dBm)
RSRP_GOOD_THRESHOLD = -90    # Above this → green
RSRP_WEAK_THRESHOLD = -110   # Below this → red

# Colors as hex strings for Folium
COLOR_GOOD = "#00cc00"   # Bright green - strong signal
COLOR_FAIR = "#ffcc00"   # Yellow/amber - moderate signal
COLOR_WEAK = "#ff3333"   # Red - weak signal

# RGBA colors for PyDeck (0-255)
COLOR_GOOD_RGBA = [0, 204, 0, 180]
COLOR_FAIR_RGBA = [255, 204, 0, 180]
COLOR_WEAK_RGBA = [255, 51, 51, 180]


def rsrp_to_hex_color(rsrp: float) -> str:
    """
    Map RSRP value (dBm) to a hex color string.

    Args:
        rsrp: Signal strength in dBm.

    Returns:
        Hex color string (e.g. '#00cc00').
    """
    if rsrp > RSRP_GOOD_THRESHOLD:
        return COLOR_GOOD
    elif rsrp >= RSRP_WEAK_THRESHOLD:
        return COLOR_FAIR
    else:
        return COLOR_WEAK


def rsrp_to_rgba(rsrp: float) -> list:
    """
    Map RSRP value (dBm) to an RGBA color list for PyDeck.

    Args:
        rsrp: Signal strength in dBm.

    Returns:
        RGBA list [r, g, b, a].
    """
    if rsrp > RSRP_GOOD_THRESHOLD:
        return COLOR_GOOD_RGBA
    elif rsrp >= RSRP_WEAK_THRESHOLD:
        return COLOR_FAIR_RGBA
    else:
        return COLOR_WEAK_RGBA


def render_2d_map(df: pd.DataFrame) -> folium.Map:
    """
    Render a 2D interactive map using Folium with real map tiles.

    Each data point is rendered as a small circle marker colored by
    RSRP signal strength. A heatmap overlay is also added for density
    visualization.

    Args:
        df: DataFrame with columns 'Latitude', 'Longitude', 'RSRP_dBm',
            'CellID', 'Band', 'SINR_dB'.

    Returns:
        folium.Map object ready for display with st_folium().
    """
    if df.empty:
        # Return a default map centered on Shanghai with no data
        return folium.Map(location=[31.23, 121.47], zoom_start=11,
                          tiles="OpenStreetMap")

    # Calculate map center from data
    center_lat = df["Latitude"].mean()
    center_lon = df["Longitude"].mean()

    # Create base map with OpenStreetMap tiles (real map background)
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    # Add tile layer options in the layer control
    folium.TileLayer("CartoDB positron", name="Light Map").add_to(m)
    folium.TileLayer("OpenStreetMap", name="Street Map").add_to(m)

    # Draw each data point as a small circle marker
    for _, row in df.iterrows():
        color = rsrp_to_hex_color(row["RSRP_dBm"])

        # Popup with detailed signal info
        popup_text = (
            f"<b>Cell ID:</b> {row.get('CellID', 'N/A')}<br>"
            f"<b>Band:</b> {row.get('Band', 'N/A')}<br>"
            f"<b>RSRP:</b> {row['RSRP_dBm']:.2f} dBm<br>"
            f"<b>SINR:</b> {row.get('SINR_dB', 'N/A'):.2f} dB<br>"
            f"<b>Speed:</b> {row.get('Download_Mbps', 'N/A'):.1f} Mbps"
        )

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=3,               # Small points for clean look
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,       # Semi-transparent for scattered feel
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"RSRP: {row['RSRP_dBm']:.1f} dBm",
        ).add_to(m)

    # Add a legend (as an HTML overlay)
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 10px;
        z-index: 1000;
        background: white;
        padding: 8px 12px;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.3);
        font-size: 13px;
        font-family: Arial, sans-serif;
    ">
        <b>RSRP Signal Strength</b><br>
        <span style="color:#00cc00;">●</span> &gt; -90 dBm (Good)<br>
        <span style="color:#ffcc00;">●</span> -110 ~ -90 dBm (Fair)<br>
        <span style="color:#ff3333;">●</span> &lt; -110 dBm (Weak)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add layer control
    folium.LayerControl().add_to(m)

    return m


def render_3d_map(df: pd.DataFrame) -> pdk.Deck:
    """
    Render a 3D map using PyDeck (deck.gl) with columns whose height
    represents download speed and color represents RSRP signal strength.

    Args:
        df: DataFrame with Latitude, Longitude, RSRP_dBm, Download_Mbps,
            Band, CellID columns.

    Returns:
        pydeck.Deck object ready for st.pydeck_chart().
    """
    if df.empty:
        return pdk.Deck()

    # Prepare data for PyDeck: add a color column as RGB arrays
    plot_df = df.copy()
    plot_df["color_rgba"] = plot_df["RSRP_dBm"].apply(rsrp_to_rgba)

    # Normalize elevation: scale Download_Mbps to meters
    max_speed = plot_df["Download_Mbps"].max()
    min_speed = plot_df["Download_Mbps"].min()
    speed_range = max_speed - min_speed if max_speed > min_speed else 1
    plot_df["elevation"] = (
        (plot_df["Download_Mbps"] - min_speed) / speed_range * 500 + 50
    )

    # Define the column layer for 3D visualization
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=plot_df,
        get_position=["Longitude", "Latitude"],
        get_elevation="elevation",
        elevation_scale=1,
        radius=15,
        get_fill_color="color_rgba",
        pickable=True,
        auto_highlight=True,
    )

    # Calculate view state centered on data
    view_state = pdk.ViewState(
        latitude=plot_df["Latitude"].mean(),
        longitude=plot_df["Longitude"].mean(),
        zoom=12,
        pitch=45,        # Tilt for 3D effect
        bearing=0,
    )

    # Tooltip on hover
    tooltip = {
        "html": (
            "<b>Cell ID:</b> {CellID}<br>"
            "<b>Band:</b> {Band}<br>"
            "<b>RSRP:</b> {RSRP_dBm} dBm<br>"
            "<b>SINR:</b> {SINR_dB} dB<br>"
            "<b>Speed:</b> {Download_Mbps} Mbps<br>"
            "<b>Elevation:</b> {elevation:.0f}m"
        ),
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
        },
    }

    return pdk.Deck(
        layers=[column_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_provider="carto",
        map_style="light",
    )
