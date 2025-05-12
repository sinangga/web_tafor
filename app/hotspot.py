import pandas as pd
import requests
from io import StringIO
import folium
import streamlit as st
from folium.plugins import MarkerCluster

# === 1. Config ===
API_KEY = "c3d37be8d94206e3181b95791f4b6aad"
DAYS = 3
COUNTRY = "IDN"
PRODUCT = "MODIS_NRT"
LAT_GRID = 0.09
LON_GRID = 0.09

# === 2. Load FIRMS Data ===
FIRMS_URL = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/{PRODUCT}/{COUNTRY}/{DAYS}"
response = requests.get(FIRMS_URL)
df = pd.read_csv(StringIO(response.text))

# === 3. Preprocess ===
df['acq_date'] = pd.to_datetime(df['acq_date'])
df['lat_bin'] = (df['latitude'] // LAT_GRID) * LAT_GRID
df['lon_bin'] = (df['longitude'] // LON_GRID) * LON_GRID

# === 4. Detect persistent hotspots (≥ 3 days in same grid) ===
grid_days = df.groupby(['lat_bin', 'lon_bin'])['acq_date'].nunique().reset_index()
grid_days.columns = ['lat_bin', 'lon_bin', 'days_detected']
persistent_bins = grid_days[grid_days['days_detected'] >= 3]

# Merge to tag persistent status
df = df.merge(persistent_bins, on=['lat_bin', 'lon_bin'], how='left')
df['persistent'] = df['days_detected'].fillna(0) >= 3

# === 5. Create Folium Map ===
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():
    popup_html = f"""
    <b>Date:</b> {row['acq_date'].date()}<br>
    <b>Latitude:</b> {row['latitude']}<br>
    <b>Longitude:</b> {row['longitude']}<br>
    <b>Brightness:</b> {row['brightness']}<br>
    <b>Persistent:</b> {"✅ Yes" if row['persistent'] else "❌ No"}
    """
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='red' if row['persistent'] else 'blue',
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(marker_cluster)

# === 6. Render Map in Streamlit ===
# Convert the Folium map to HTML and render in Streamlit
from streamlit_folium import st_folium
st.title("FIRMS Hotspot Monitoring System")
st.markdown("**Hotspots detected over the last 3 days**")
st_folium(m, width=700, height=500)

# Display additional info as table
st.subheader("Recent Hotspot Details")
st.write(df[['acq_date', 'latitude', 'longitude', 'brightness', 'persistent']].head(10))

