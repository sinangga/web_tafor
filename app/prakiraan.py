import streamlit as st
import requests
import statistics
import pandas as pd
import geopandas as gpd
import altair as alt

# Bypass Forbidden Status Code
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

# Fetch Data from BMKG API
kecamatan_res = requests.get("https://api.bmkg.go.id/publik/prakiraan-cuaca?adm2=61.06", headers=headers)
kecamatan_output = kecamatan_res.json()
df_kh = kecamatan_output['data']

# Process Data
list_kecamatan = [kh['lokasi']['kecamatan'] for kh in df_kh]
df_kh_2 = dict(zip(list_kecamatan, df_kh))

def nesting(nama_kecamatan):
    return [i for i in df_kh_2[nama_kecamatan]["cuaca"]]

def cuaca_gabungan_pagi(n):
    suhu, angin, arah, rh, list_cuaca, list_tgl = [], [], [], [], [], []
    for i in range(8):
        data = nesting(n)[i]
        suhu.append(data["t"])
        angin.append(data["ws"])
        arah.append(data["wd"])
        rh.append(data["hu"])
        list_cuaca.append(data["weather_desc"])
        list_tgl.append(data["utc_datetime"])
    return n, list_tgl, list_cuaca, f"{max(suhu)}-{min(suhu)}", f"{max(rh)}-{min(rh)}", statistics.mode(arah), max(angin)

def harian_kecamatan(nama):
    return cuaca_gabungan_pagi(nama)

datacoba = [harian_kecamatan(i) for i in range(len(list_kecamatan))]
headers = ['Kecamatan', '12', '15', '18', '21', '00', '03', '06', '09', 'Suhu', 'Kelembapan', 'Angin', 'Kecepatan']
result_dicts = [dict(zip(headers, values)) for values in datacoba]

# Map statuses to online icon URLs
status_to_icon = {
    'Cerah': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah-am.png',
    'Hujan Ringan': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20ringan-am.png',
    'Hujan Petir': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah%20berawan-am.png',
    'Cerah Berawan': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah%20berawan-am.png',
}

# Replace weather descriptions with image tags
for entry in result_dicts:
    for key in headers[1:9]:  # Columns for weather statuses
        if entry[key] in status_to_icon:
            entry[key] = f'<img src="{status_to_icon[entry[key]]}" width="20"/>'

df = pd.DataFrame(result_dicts)

# Load SHP data
KH_map = gpd.read_file('https://github.com/sinangga/shp/raw/refs/heads/main/Kapuas_Hulu.shp')
chart = alt.Chart(KH_map).mark_geoshape()

# Streamlit tabs
tab1, tab2 = st.tabs(["Kabupaten", "Kecamatan"])

with tab1:
    st.header("Kabupaten | Tanggal " + b[0])  # Adjust as necessary
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

with tab2:
    st.header("Kecamatan")
    st.altair_chart(chart)
