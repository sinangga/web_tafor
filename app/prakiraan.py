import streamlit as st
import urllib.request, json
import requests
import pandas as pd
import statistics
from prettytable import PrettyTable
from IPython.core.display import display, HTML

# Bypass Forbidden Status Code
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Store Data from BMKG API (Kecamatan / adm2)
kecamatan_res = requests.get("https://api.bmkg.go.id/publik/prakiraan-cuaca?adm2=61.06", headers=headers)
kecamatan_output = kecamatan_res.json()
df_kh = kecamatan_output['data']

# Clustering Data into Single Dataset
list_kecamatan = []
for kh in df_kh:
    list_kecamatan.append(kh['lokasi']['kecamatan'])

#### Main Dataset ####
df_kh_2 = dict(zip(list_kecamatan, df_kh)) 
######################

# Function to Call Specific Weather Data Kecamatan
def nesting(nama_kecamatan):
    nesting = []
    for i in df_kh_2[nama_kecamatan]["cuaca"]:
        nesting.append(i)
    return [element for nestedlist in nesting for element in nestedlist]

# Function to Create Data inside Prettytable 
def printcuaca(x):
    n = 0
    t = PrettyTable(['Kecamatan', 'Tanggal', 'Cuaca', 'Angin', 'Suhu', 'Kelembapan'])
    for i in list_kecamatan:
        data = nesting(i)
        for a in range(x):
            angin = str(data[a]["wd"]) + " " + str(round(data[a]["ws"])) + "KT"
            t.add_row([list_kecamatan[n], data[a]["utc_datetime"], data[a]["weather_desc"], angin, data[a]["t"], data[a]["hu"]])
        n += 1
    return t

# Function to collect weather data
def cuaca_gabungan_pagi(n):
    suhu = []
    angin = []
    arah = []
    rh = []
    list_cuaca = []
    list_tgl = []
    for i in range(8):
        suhu.append(nesting(n)[i]["t"])
        angin.append(nesting(n)[i]["ws"])
        arah.append(nesting(n)[i]["wd"])
        rh.append(nesting(n)[i]["hu"])
        list_cuaca.append(nesting(n)[i]["weather_desc"])
        list_tgl.append(nesting(n)[i]["utc_datetime"])
    
    maxsuhu = max(suhu)
    minsuhu = min(suhu)
    maxrh = max(rh)
    minrh = min(rh)
    suhu_akhir = f"{maxsuhu}-{minsuhu}"
    rh_akhir = f"{maxrh}-{minrh}"
    angin = max(angin)
    arah = statistics.mode(arah)
    return n, list_tgl, list_cuaca, suhu_akhir, rh_akhir, arah, angin

# Create combined data for all kecamatan
datacoba = []
for i in list_kecamatan:
    datacoba.append(cuaca_gabungan_pagi(i))
headers = ['Kecamatan', '12', '15', '18', '21', '00', '03', '06', '09', 'Suhu', 'Kelembapan', 'Angin', 'Kecepatan']
result_dicts = [dict(zip(headers, values)) for values in datacoba]

# Define the local path for the icons
base_path = "DATA/icon/"

# Define the mapping of statuses to icons
status_to_icon = {
    'Cerah': 'cerah-am.ico',
    'Hujan Ringan': 'hujan ringan-am.ico',
    'Hujan Petir': 'hujan ringan-am.ico',
    'Cerah Berawan': 'cerah berawan-am.ico',
}

# Loop through each dictionary and replace values in columns 2-9
for entry in result_dicts:
    for key in ['12', '15', '18', '21', '00', '03', '06', '09']:
        if entry[key] in status_to_icon:
            entry[key] = f'<img src="{base_path}{status_to_icon[entry[key]]}" width="20"/>'

# Convert the updated results to a Pandas DataFrame
df = pd.DataFrame(result_dicts)

# Display the DataFrame as HTML in Streamlit
st.title("Weather Data")
st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
