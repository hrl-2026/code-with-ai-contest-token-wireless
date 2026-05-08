# Screenshots

Due to the headless environment (no browser), the following HTML files
were generated as screenshot equivalents:

## Screenshot 1: 2D Signal Map
File: `map_2d.html`
Description: Folium map with OpenStreetMap tiles showing signal points
colored by RSRP strength (Green > -90dBm, Yellow -110~-90dBm, Red < -110dBm).
Points are small (radius=3) and scattered with hover tooltips.

## Screenshot 2: 3D Signal Map
File: `map_3d.html`
Description: PyDeck 3D column map where column height represents
Download_Mbps and color represents RSRP signal strength.

## Screenshot 3: Data Charts
File: `charts.png` (if available) or `band_chart.html` + `pie_chart.html`
Description: 
- Band Bar Chart: Number of data points per frequency band (n28, n41, n78)
- Terminal Pie Chart: Proportion of Smartphone, CPE, and IoT terminal types

---

### How to view screenshots:
1. Open the .html files in any browser for interactive maps/charts
2. Or run `streamlit run app.py` and take actual screenshots
