"""
5G Signal Visualization - Chart Generation Module
==================================================
Generates interactive Plotly charts for the 5G signal dashboard.

Charts provided:
  1. Band distribution bar chart - counts base stations per frequency band
  2. Terminal type pie chart - shows proportion of terminal types
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# -- Consistent color palette for 5G bands --
BAND_COLORS = {
    "n28": "#636EFA",   # Blue
    "n41": "#EF553B",   # Red
    "n78": "#00CC96",   # Green
}

DEFAULT_COLOR = "#AB63FA"  # Purple fallback


def plot_band_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing the count of data points (base stations)
    per frequency band.

    Args:
        df: DataFrame with a 'Band' column.

    Returns:
        plotly.graph_objects.Figure: Interactive bar chart.
    """
    if df.empty:
        # Return empty figure with a message
        fig = go.Figure()
        fig.add_annotation(
            text="No data available after filtering",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
        )
        fig.update_layout(
            xaxis_title="Frequency Band",
            yaxis_title="Count",
        )
        return fig

    # Count occurrences per band
    band_counts = df["Band"].value_counts().reset_index()
    band_counts.columns = ["Band", "Count"]
    band_counts = band_counts.sort_values("Band")

    # Assign colors
    colors = [BAND_COLORS.get(b, DEFAULT_COLOR) for b in band_counts["Band"]]

    # Create bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=band_counts["Band"],
                y=band_counts["Count"],
                marker_color=colors,
                text=band_counts["Count"],
                textposition="auto",
                hovertemplate=(
                    "<b>Band:</b> %{x}<br>"
                    "<b>Count:</b> %{y}<br>"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Frequency Band",
        yaxis_title="Number of Data Points",
        bargap=0.3,
        height=400,
        hovermode="x unified",
    )

    return fig


def plot_terminal_pie_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing the proportion of different terminal types.

    Args:
        df: DataFrame with a 'TerminalType' column.

    Returns:
        plotly.graph_objects.Figure: Interactive pie chart.
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
        )
        return fig

    terminal_counts = df["TerminalType"].value_counts().reset_index()
    terminal_counts.columns = ["TerminalType", "Count"]

    # Color palette for terminal types
    terminal_colors = {
        "Smartphone": "#636EFA",
        "CPE": "#EF553B",
        "IoT": "#00CC96",
    }

    colors = [
        terminal_colors.get(t, DEFAULT_COLOR)
        for t in terminal_counts["TerminalType"]
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=terminal_counts["TerminalType"],
                values=terminal_counts["Count"],
                marker=dict(colors=colors),
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Count: %{value}<br>"
                    "Percentage: %{percent}<br>"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
    )

    return fig
