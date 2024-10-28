import streamlit as st
import urllib.request, json
import requests
import statistics
from prettytable import PrettyTable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import geopandas as gpd
from shapely.geometry import Polygon, Point, shape, mapping
from shapely.ops import transform
from branca.element import Figure
import folium
import folium.plugins as plugins
from IPython.display import IFrame
import altair as alt


### Main Code Down Here ###
###########################

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
    for i in df_kh_2[(nama_kecamatan)]["cuaca"]:
        nesting.append(i)
    nest1 = nesting[0]
    nest2 = nesting[1]
    nest3 = nesting[2]
    nesting_list = [nest1, nest2, nest3]
    nesting = [element for nestedlist in nesting_list for element in nestedlist]
    return nesting

# Function to Create Data inside Prettytable 
def printcuaca(x):
    n = 0
    t = PrettyTable(['Kecamatan', 'Tanggal', 'Cuaca', 'Angin', 'Suhu', 'Kelembapan'])
    for i in list_kecamatan:
        data = nesting(i)
        for a in range(x):
            angin = str(data[a]["wd"])+" "+str(round(data[a]["ws"]))+"KT"
            t.add_row([list_kecamatan[n],data[a]["utc_datetime"], data[a]["weather_desc"],angin, data[a]["t"], data[a]["hu"]])
        n = n+1
    return t

#psu = ['c1 - cn', 'suhu(min-max)', 'RH (min-max)']
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
    suhu_akhir = str(minsuhu) + "-" + str(maxsuhu)
    rh_akhir = str(minrh) + "-" + str(maxrh)
    angin = max(angin)
    arah = statistics.mode(arah)
    return n, list_tgl, list_cuaca, suhu_akhir, rh_akhir, arah, angin

## Calling Data Kecamatan Daily
def harian_kecamatan(nama):
    (a, b, c, d, e, f, g) = cuaca_gabungan_pagi(nama)
    nama = []
    for x in (a, d, e, f, g):
        if x in (a,d,e,f,g):
            nama.append(x)
    for i in range(len(c)):
        nama.append(c[i])
    order_list = [0,5,6,7,8,9,10,11,12,1,2,3,4]
    nama = [nama[i] for i in order_list]
    if nama[11] == "SE":
        nama[11] = 'Tenggara'
    if nama[11] == "N":
        nama[11] = 'Utara'
    if nama[11] == "E":
        nama[11] = 'Timur'
    if nama[11] == "W":
        nama[11] = 'Barat'
    if nama[11] == "S":
        nama[11] = 'Selatan'
    if nama[11] == "NW":
        nama[11] = 'Barat Laut'
    if nama[11] == "NE":
        nama[11] = 'Timur Laut'
    if nama[11] == "SW":
        nama[11] = 'Barat Daya'
    nama[12] = round(nama[12])
    return nama

## Printing to Web
(a, b, c, d, e, f, g) = cuaca_gabungan_pagi("Bika")
tanggal = b[0][8]+b[0][9]+str("/")+b[0][5]+b[0][6]+str("/")+b[0][0]+b[0][1]+b[0][2]+b[0][3]
jam = []
for i in range(len(b)):
    jam.append(b[i][11]+b[i][12])

jamm = ['Kecamatan', jam, 'Suhu', 'Kelembapan', 'Angin', 'Kecepatan']
jammm = []
for i in jamm:
    if type(i) == list:
        for a in range(len(jam)):
            jammm.append(jam[a])
    else:
        jammm.append(i)

table = PrettyTable(jammm)
#table.title = "CUACA KABUPATEN KAPUAS HULU TANGGAL "+tanggal
for i in list_kecamatan:
    table.add_row(harian_kecamatan(i))
table.align["Kecamatan"]="l"
table.align["Angin"]="l"


#########################
#########################

datacoba = []
for i in list_kecamatan:
    datacoba.append(harian_kecamatan(i))
headers = jammm #['Kecamatan', '12', '15', '18', '21', '00', '03', '06', '09', 'Suhu', 'Kelembapan', 'Angin', 'Kecepatan']
result_dicts = [dict(zip(headers, values)) for values in datacoba]

# Define the local path for the icons
base_path = "../icon/"

# Define the mapping of statuses to icons
status_to_icon = {
    'Cerah': 'cerah-am.ico',
    'Hujan Ringan': 'hujan ringan-am.ico',
    'Hujan Petir': 'hujan ringan-am.ico',
    'Cerah Berawan': 'cerah berawan-am.ico',
    # Add more mappings as necessary
}

# Loop through each dictionary and replace values in columns 2-9
time = []
for i in range(1,9):
    time.append(jammm[i])
for entry in result_dicts:
    for key in time:
        if entry[key] in status_to_icon:
            entry[key] = f'<img src="{base_path}{status_to_icon[entry[key]]}" width="20"/>'

# Convert the updated results to a Pandas DataFrame
df = pd.DataFrame(result_dicts)

# Display the DataFrame as HTML
#HTML(df.to_html(escape=False))

#########################
#########################
# Load SHP data
KH_map = gpd.read_file('https://github.com/sinangga/shp/raw/refs/heads/main/Kapuas_Hulu.shp')
chart = alt.Chart(KH_map).mark_geoshape()


    
### End of Main Code ###
########################


tab1, tab2 = st.tabs(["Kabupaten","Kecamatan"])

with tab1:
    st.header("Kabupaten | Tanggal "+tanggal)
    #st.write(table)
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

with tab2:
    st.header("Kecamatan")
    st.altair_chart(chart)
    # Display Map
    #BorderAZ.plot()

