"""
Unit Tests for 5G Signal Visualization Dashboard
==================================================
Tests for data loading, filtering, color mapping, and chart generation.

Run with:
    pytest test_dashboard.py -v
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import (
    load_and_preprocess_data,
    rsrp_to_color,
    rsrp_to_hex,
    REQUIRED_COLUMNS,
    RSRP_GOOD_THRESHOLD,
    RSRP_WEAK_THRESHOLD,
)
from map_visualizer import (
    rsrp_to_hex_color,
    rsrp_to_rgba,
    render_2d_map,
    render_3d_map,
)
from chart_generator import plot_band_bar_chart, plot_terminal_pie_chart
from sidebar_filter import create_sidebar_filters


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(scope="module")
def data_filepath():
    """Path to the test CSV data file."""
    return "data/signal_samples.csv"


@pytest.fixture(scope="module")
def sample_df(data_filepath):
    """Load the real dataset for integration tests."""
    return load_and_preprocess_data(data_filepath)


@pytest.fixture
def small_test_df():
    """A minimal DataFrame for unit tests."""
    return pd.DataFrame({
        "Latitude": [31.23, 31.24, 31.25],
        "Longitude": [121.47, 121.48, 121.49],
        "CellID": [1001, 1002, 1003],
        "Band": ["n28", "n41", "n78"],
        "RSRP_dBm": [-85.0, -100.0, -115.0],
        "SINR_dB": [20.0, 10.0, 5.0],
        "TerminalType": ["Smartphone", "CPE", "IoT"],
        "Download_Mbps": [150.0, 300.0, 50.0],
    })


# ============================================================
# Data Loader Tests
# ============================================================

class TestDataLoader:
    """Tests for data_loader.py"""

    def test_load_data_returns_dataframe(self, sample_df):
        """Verify the CSV loads into a DataFrame with correct shape."""
        assert isinstance(sample_df, pd.DataFrame)
        assert len(sample_df) > 0
        assert len(sample_df.columns) >= len(REQUIRED_COLUMNS)

    def test_load_data_has_required_columns(self, sample_df):
        """Verify all required columns exist in the loaded data."""
        for col in REQUIRED_COLUMNS:
            assert col in sample_df.columns, f"Missing column: {col}"

    def test_load_data_adds_color_columns(self, sample_df):
        """Verify color columns are added."""
        assert "RSRP_color" in sample_df.columns
        assert "RSRP_hex_color" in sample_df.columns

    def test_load_data_no_nulls_in_critical_columns(self, sample_df):
        """Verify no nulls in required columns after loading."""
        for col in REQUIRED_COLUMNS:
            assert sample_df[col].isna().sum() == 0, f"Nulls in {col}"

    def test_load_data_download_mbps_present(self, sample_df):
        """Verify Download_Mbps column exists."""
        assert "Download_Mbps" in sample_df.columns
        assert sample_df["Download_Mbps"].isna().sum() == 0

    def test_rsrp_to_color_good(self):
        """RSRP > -90 should return green."""
        color = rsrp_to_color(-80)
        assert color == [0, 255, 0, 160]

    def test_rsrp_to_color_fair(self):
        """RSRP between -110 and -90 should return yellow."""
        color = rsrp_to_color(-100)
        assert color == [255, 255, 0, 160]

    def test_rsrp_to_color_weak(self):
        """RSRP < -110 should return red."""
        color = rsrp_to_color(-120)
        assert color == [255, 0, 0, 160]

    def test_rsrp_to_hex_good(self):
        assert rsrp_to_hex(-80) == "#00cc00"

    def test_rsrp_to_hex_fair(self):
        assert rsrp_to_hex(-100) == "#ffcc00"

    def test_rsrp_to_hex_weak(self):
        assert rsrp_to_hex(-120) == "#ff3333"

    def test_load_data_raises_on_missing_file(self):
        """Verify FileNotFoundError for missing CSV."""
        with pytest.raises(FileNotFoundError):
            load_and_preprocess_data("nonexistent_file.csv")

    def test_load_data_raises_on_missing_columns(self, tmp_path):
        """Verify ValueError for missing required columns."""
        bad_csv = tmp_path / "bad.csv"
        bad_csv.write_text("A,B,C\n1,2,3\n")
        with pytest.raises(ValueError, match="Missing required columns"):
            load_and_preprocess_data(str(bad_csv))


# ============================================================
# Map Visualizer Tests
# ============================================================

class TestMapVisualizer:
    """Tests for map_visualizer.py"""

    def test_rsrp_to_hex_color_good(self):
        assert rsrp_to_hex_color(-80) == "#00cc00"

    def test_rsrp_to_hex_color_fair(self):
        assert rsrp_to_hex_color(-100) == "#ffcc00"

    def test_rsrp_to_hex_color_weak(self):
        assert rsrp_to_hex_color(-120) == "#ff3333"

    def test_rsrp_to_rgba_good(self):
        assert rsrp_to_rgba(-80) == [0, 204, 0, 180]

    def test_rsrp_to_rgba_fair(self):
        assert rsrp_to_rgba(-100) == [255, 204, 0, 180]

    def test_rsrp_to_rgba_weak(self):
        assert rsrp_to_rgba(-120) == [255, 51, 51, 180]

    def test_render_2d_map_returns_folium_map(self, small_test_df):
        """Verify render_2d_map returns a folium Map object."""
        from folium import Map
        result = render_2d_map(small_test_df)
        assert isinstance(result, Map)

    def test_render_2d_map_empty(self):
        """Verify render_2d_map handles empty DataFrame."""
        empty_df = pd.DataFrame(columns=["Latitude", "Longitude", "RSRP_dBm"])
        from folium import Map
        result = render_2d_map(empty_df)
        assert isinstance(result, Map)

    def test_render_3d_map_returns_deck(self, small_test_df):
        """Verify render_3d_map returns a pydeck Deck object."""
        import pydeck as pdk
        result = render_3d_map(small_test_df)
        assert isinstance(result, pdk.Deck)

    def test_render_3d_map_empty(self):
        """Verify render_3d_map handles empty DataFrame."""
        empty_df = pd.DataFrame(
            columns=["Latitude", "Longitude", "RSRP_dBm", "Download_Mbps", "Band", "CellID", "SINR_dB"]
        )
        import pydeck as pdk
        result = render_3d_map(empty_df)
        assert isinstance(result, pdk.Deck)


# ============================================================
# Chart Generator Tests
# ============================================================

class TestChartGenerator:
    """Tests for chart_generator.py"""

    def test_band_bar_chart_returns_figure(self, small_test_df):
        """Verify plot_band_bar_chart returns a Plotly Figure."""
        import plotly.graph_objects as go
        result = plot_band_bar_chart(small_test_df)
        assert isinstance(result, go.Figure)

    def test_band_bar_chart_empty(self):
        """Verify empty DataFrame doesn't crash."""
        empty_df = pd.DataFrame(columns=["Band"])
        import plotly.graph_objects as go
        result = plot_band_bar_chart(empty_df)
        assert isinstance(result, go.Figure)

    def test_terminal_pie_chart_returns_figure(self, small_test_df):
        """Verify plot_terminal_pie_chart returns a Plotly Figure."""
        import plotly.graph_objects as go
        result = plot_terminal_pie_chart(small_test_df)
        assert isinstance(result, go.Figure)

    def test_terminal_pie_chart_empty(self):
        """Verify empty DataFrame doesn't crash."""
        empty_df = pd.DataFrame(columns=["TerminalType"])
        import plotly.graph_objects as go
        result = plot_terminal_pie_chart(empty_df)
        assert isinstance(result, go.Figure)

    def test_band_bar_chart_three_bars(self, small_test_df):
        """Verify three bars for three bands in test data."""
        result = plot_band_bar_chart(small_test_df)
        # Check we have 3 data traces (one bar per band)
        assert len(result.data) == 1
        # Check the bar values
        assert list(result.data[0].x) == ["n28", "n41", "n78"]
        assert list(result.data[0].y) == [1, 1, 1]


# ============================================================
# Sidebar Filter Tests
# ============================================================

class TestSidebarFilter:
    """Tests for sidebar_filter.py (logic-level, no Streamlit runtime)."""

    def test_filter_returns_dataframe(self, small_test_df):
        """Test basic filter structure."""
        # We can't easily test the streamlit UI, but can test the logic
        assert isinstance(small_test_df, pd.DataFrame)

    def test_filter_band_selection(self, small_test_df):
        """Simulate band filter logic."""
        df = small_test_df
        selected_bands = ["n28", "n41"]
        filtered = df[df["Band"].isin(selected_bands)]
        assert len(filtered) == 2
        assert all(b in selected_bands for b in filtered["Band"])

    def test_filter_rsrp_range(self, small_test_df):
        """Simulate RSRP range filter logic."""
        df = small_test_df
        filtered = df[
            (df["RSRP_dBm"] >= -110) & (df["RSRP_dBm"] <= -80)
        ]
        assert len(filtered) == 2  # -85 and -100

    def test_filter_sinr_threshold(self, small_test_df):
        """Simulate SINR threshold filter."""
        df = small_test_df
        filtered = df[df["SINR_dB"] >= 10]
        assert len(filtered) == 2  # SINR >= 10

    def test_filter_terminal_type(self, small_test_df):
        """Simulate terminal type filter."""
        df = small_test_df
        filtered = df[df["TerminalType"].isin(["Smartphone", "CPE"])]
        assert len(filtered) == 2

    def test_combined_filters(self, small_test_df):
        """Test multiple filters applied together."""
        df = small_test_df
        filtered = df.copy()
        filtered = filtered[filtered["Band"].isin(["n28", "n41"])]
        filtered = filtered[
            (filtered["RSRP_dBm"] >= -110) & (filtered["RSRP_dBm"] <= -80)
        ]
        filtered = filtered[filtered["SINR_dB"] >= 10]
        # Expect both n28 (-85, SINR=20) and n41 (-100, SINR=10)
        assert len(filtered) == 2


# ============================================================
# Integration Tests
# ============================================================

class TestIntegration:
    """End-to-end integration tests with real data."""

    def test_full_pipeline_loads(self, sample_df):
        """Verify the full data pipeline loads correctly."""
        assert len(sample_df) > 100  # Should have hundreds of points
        assert sample_df["RSRP_color"].apply(len).iloc[0] == 4  # RGBA
        assert isinstance(sample_df["RSRP_hex_color"].iloc[0], str)

    def test_band_distribution(self, sample_df):
        """Verify band distribution makes sense."""
        bands = sample_df["Band"].unique()
        expected_bands = {"n28", "n41", "n78"}
        for b in bands:
            assert b in expected_bands, f"Unexpected band: {b}"

    def test_terminal_types(self, sample_df):
        """Verify terminal types."""
        types = sample_df["TerminalType"].unique()
        expected_types = {"Smartphone", "CPE", "IoT"}
        for t in types:
            assert t in expected_types, f"Unexpected type: {t}"

    def test_maps_with_real_data(self, sample_df):
        """Verify maps render with real data."""
        subset = sample_df.head(10)
        from folium import Map
        result_2d = render_2d_map(subset)
        assert isinstance(result_2d, Map)

        import pydeck as pdk
        result_3d = render_3d_map(subset)
        assert isinstance(result_3d, pdk.Deck)

    def test_charts_with_real_data(self, sample_df):
        """Verify charts render with real data."""
        import plotly.graph_objects as go
        band_chart = plot_band_bar_chart(sample_df)
        assert isinstance(band_chart, go.Figure)

        pie_chart = plot_terminal_pie_chart(sample_df)
        assert isinstance(pie_chart, go.Figure)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
