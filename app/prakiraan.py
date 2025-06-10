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
from xhtml2pdf import pisa
from io import BytesIO
from html2image import Html2Image
import tempfile
from zoneinfo import ZoneInfo
from datetime import datetime
import folium
from folium import Popup
from streamlit_folium import st_folium

### Main Code Down Here ###
###########################

# Bypass Forbidden Status Code
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Store Data from BMKG API (Kecamatan / adm2)
#kecamatan_res = requests.get("https://api.bmkg.go.id/publik/prakiraan-cuaca?adm2=61.06", headers=headers)
#kecamatan_output = kecamatan_res.json()
#df_kh = kecamatan_output['data']

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_prakiraan_data():
    print("🔁 Fetching data from API...")
    gabungan_data = []

    # Ambil data untuk awal dan ID khusus
    urls = [
        "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=61.06.01.1001",
        "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=61.06.17.1001",
    ]

    # Tambahkan semua suffix ke URL
    suffixes2_16 = [f"{i:02d}.2001" for i in range(2, 17)]
    suffixes18_23 = [f"{i:02d}.2001" for i in range(18, 24)]
    base_url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=61.06."

    urls += [base_url + suffix for suffix in suffixes2_16]
    urls += [base_url + suffix for suffix in suffixes18_23]

    # Fetch data untuk semua URL
    for url in urls:
        response = requests.get(url)
        response.raise_for_status()
        gabungan_data.append(response.json())

    return gabungan_data

df_kh = fetch_prakiraan_data()

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
    for i in df_kh_2[(nama_kecamatan)]['data'][0]['cuaca']:
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
            t.add_row([list_kecamatan[n],data[a]["local_datetime"], data[a]["weather_desc"],angin, data[a]["t"], data[a]["hu"]])
        n = n+1
    return t

#psu = ['c1 - cn', 'suhu(min-max)', 'RH (min-max)']
def cuaca_pertama(n):
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
        list_tgl.append(nesting(n)[i]["local_datetime"])
    maxsuhu = max(suhu)
    minsuhu = min(suhu)
    maxrh = max(rh)
    minrh = min(rh)
    suhu_akhir = str(minsuhu) + "-" + str(maxsuhu)
    rh_akhir = str(minrh) + "-" + str(maxrh)
    angin = max(angin)
    arah = statistics.mode(arah)
    return n, list_tgl, list_cuaca, suhu_akhir, rh_akhir, arah, angin

def cuaca_kedua(n):
    suhu = []
    angin = []
    arah = []
    rh = []
    list_cuaca = []
    list_tgl = []
    for i in range(8,16):
        suhu.append(nesting(n)[i]["t"])
        angin.append(nesting(n)[i]["ws"])
        arah.append(nesting(n)[i]["wd"])
        rh.append(nesting(n)[i]["hu"])
        list_cuaca.append(nesting(n)[i]["weather_desc"])
        list_tgl.append(nesting(n)[i]["local_datetime"])
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
def harian_kecamatan(waktu, nama):
    (a, b, c, d, e, f, g) = waktu(nama)
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
    nama[12] = str(round(nama[12])) + " Knot"
    nama[10] = str(nama[10]) + "%"
    nama[9] = str(nama[9]) + "°C"
    return nama

## Printing to Web
def waktuu(waktu):
    (a, b, c, d, e, f, g) = waktu("Bika")
    tanggal = b[0][8]+b[0][9]+str("-")+b[0][5]+b[0][6]+str("-")+b[0][0]+b[0][1]+b[0][2]+b[0][3]
    tanalisis = df_kh[0]['data'][0]['cuaca'][0][0]['analysis_date']
    tberlaku = b[0]
    # Parse and attach UTC timezone
    tberlaku = datetime.strptime(tberlaku, "%Y-%m-%d %H:%M:%S")
    tberlaku = tberlaku.strftime("%d-%m-%Y %H:%M:%S")
    tberlaku = str(tberlaku)
    tberlaku = tberlaku[0:16]
    thingga = b[7]
    # Parse and attach UTC timezone
    thingga = datetime.strptime(thingga, "%Y-%m-%d %H:%M:%S")
    thingga = thingga.strftime("%d-%m-%Y %H:%M:%S")
    thingga = str(thingga)
    thingga = thingga[0:16]
    jam = []
    for i in range(len(b)):
        textjam = b[i][11:13]
        textjamdirection ={
            "05": "12",
            "08": "15",
            "11": "18",
            "14": "21",
            "17": "24",
            "20": "03",
            "23": "06",
            "02": "09"
        }
        #textjam = textjamdirection.get(b[i][11:13], b[i][11:13])
        textjam = textjam
        jam.append(textjam)       
    jamm = ['KECAMATAN', jam, 'SUHU', 'KELEMBAPAN', 'ANGIN', 'KECEPATAN']
    jammm = []
    for i in jamm:
        if type(i) == list:
            for a in range(len(jam)):
                jammm.append(jam[a])
        else:
            jammm.append(i)
    return tanggal, tanalisis, tberlaku, thingga, jam, jamm, jammm
(tanggal, tanalisis, tberlaku, thingga, jam, jamm, jammm) = waktuu(cuaca_pertama)
table_pertama = PrettyTable(jammm)
#table.title = "CUACA KABUPATEN KAPUAS HULU TANGGAL "+tanggal
for i in list_kecamatan:
    table_pertama.add_row(harian_kecamatan(cuaca_pertama, i))
table_pertama.align["Kecamatan"]="l"
table_pertama.align["Angin"]="l"

(tanggal2, tanalisis2, tberlaku2, thingga2, jam2, jamm2, jammm2) = waktuu(cuaca_kedua)
table_kedua = PrettyTable(jammm2)
#table.title = "CUACA KABUPATEN KAPUAS HULU TANGGAL "+tanggal
for i in list_kecamatan:
    table_kedua.add_row(harian_kecamatan(cuaca_kedua, i))
table_kedua.align["Kecamatan"]="l"
table_kedua.align["Angin"]="l"

#########################
#########################

def resultdict(waktu, jjaamm):
    datacoba = []
    for i in list_kecamatan:
        datacoba.append(harian_kecamatan(waktu, i))
    headers = jjaamm #['Kecamatan', '12', '15', '18', '21', '00', '03', '06', '09', 'Suhu', 'Kelembapan', 'Angin', 'Kecepatan']
    result_dicts = [dict(zip(headers, values)) for values in datacoba]
    return datacoba, headers, result_dicts

# Define the local path for the icons
#base_path = "/mount/src/web_tafor/icon/"

# Define the mapping of statuses to icons
status_to_icon = {
    'Cerah': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah-am.png',
    'Hujan Ringan': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20ringan-am.png',
    'Hujan Petir': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png',
    'Petir': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png',
    'Cerah Berawan': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah%20berawan-am.png',
    'Hujan Lebat': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20lebat-am.png',
    'Hujan Sedang': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20sedang-am.png',
    'Kabut/Asap': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/kabut-am.png',
    'Udara Kabur': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/udara%20kabur.png',
    'Berawan': 'https://api-apps.bmkg.go.id/storage/icon/cuaca/berawan-am.svg'
}

# DATA TABEL PERTAMA
(datacoba, headers, result_dicts) = resultdict(cuaca_pertama, jammm)
# Loop through each dictionary and replace values in columns 2-9
time = []
for i in range(1,9):
    time.append(jammm[i])
for entry in result_dicts:
    for key in time:
        if entry[key] in status_to_icon:
            entry[key] = f'<img src="{status_to_icon[entry[key]]}" width="50">'

# Convert the updated results to a Pandas DataFrame
df = pd.DataFrame(result_dicts)
dfhtml = df.to_html(index = False, escape=False)


# DATA TABEL KEDUA
(datacoba2, headers2, result_dicts2) = resultdict(cuaca_kedua, jammm2)
# Loop through each dictionary and replace values in columns 2-9
time2 = []
for i in range(1,9):
    time2.append(jammm2[i])
for entry in result_dicts2:
    for key in time2:
        if entry[key] in status_to_icon:
            entry[key] = f'<img src="{status_to_icon[entry[key]]}" width="50">'

# Convert the updated results to a Pandas DataFrame
df2 = pd.DataFrame(result_dicts2)
dfhtml2 = df2.to_html(index = False, escape=False)

### End of Main Code ###
########################
### End of Main Code ###
########################


tab1, tab7 = st.tabs(["Infografis", "Peta Interaktif"])
with tab1:
    tab3, tab4 = st.tabs([tanggal, tanggal2])
    
    with tab3:
        st.write('Tanggal Analisis :', nesting('Bika')[8]['analysis_date'])
        #st.divider()
        # convert your links to html tags 
        def path_to_image_html(path):
            return '<img src="'+ path + ' "width="30px"; >'
        
        
        # Loop through each dictionary and replace values in columns 2-9
        time = []
        for i in range(1,9):
            time.append(jammm[i])
        result_info = [dict(zip(headers, values)) for values in datacoba]
        for entryinfo in result_info:
            for key in time:
                if entryinfo[key] in status_to_icon:
                    entryinfo[key] = status_to_icon[entryinfo[key]]
        
        
        image_cols = jam  #<- define which columns will be used to convert to html
        
        # Create the dictionariy to be passed as formatters
        format_dictinfo = {}
        for image_col in image_cols:
            format_dictinfo[image_col] = path_to_image_html
        
        # Convert the updated results to a Pandas DataFrame
        df2_info = pd.DataFrame(result_info)
        htmlcode2 = df2_info.to_html(index = False, escape=False ,formatters=format_dictinfo)
        htmlcode3 = 'Tanggal Analisis : '+str(nesting('Bika')[0]['analysis_date'])
        htmlcode = """
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>BMKG Pangsuma</title>
                <style>
                    body {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background-color: #c1efff;
                        margin: 0;
                    }
                    * {
                      font-family: Arial, sans-serif;
                      font-weight: bold;
                    }
                    table {
                        width: 100%;
                        border-collapse: separate;
                        border-spacing: 0;
                        border: 1px solid #ddd;
                        border-radius: 15px;
                        overflow: hidden;
                        align-items: center;
                        justify-content: center;
                        background-color: white;
                        color: black;
                    }
                    tr{
                      text-align: center;
                      background-color: #d0edf7;
                      color: black;
                      height: 30px;
                      overflow: hidden;
                    }
                    th{
                      text-align: center;
                      background-color: #0a2f69;
                      color: white;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        text-align: center;
                        padding: 8px;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    tr:nth-child(odd) {
                        background-color: #ffffff;
                    }
                    td:nth-child(2) img {
                      width: 30px; /*Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(3) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(4) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(5) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }td:nth-child(6) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(7) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(8) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(9) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(10) img {
                      width: 50px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    .footnote {
                        color: grey;
                        text-align: left;
                        font-size: 15px;
                    }
                    .logo-container {
                        display: flex;
                        flex-direction: column; /* Stack items vertically */
                        align-items: center;
                        /* background-color: #c1efff; White background */
                        background-color: white;
                        padding: 10px; /* Space around the content */
                        border-radius: 8px; /* Rounded corners */
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                        color: black
                    }
                    .logo {
                        width: 40px; /* Adjust size as needed */
                        height: auto;
                    }
                    .main-text {
                        font-size: 20px;
                        color: black;
                        margin: 10px 0; /* Space around the text */
                        text-align: center;
                    }
                    .sub-text {
                        font-size: 16px; /* Slightly smaller font size */
                        color: black; /* Darker gray for the subtitle */
                        text-align: center;
                    }
                    hr.gradient {
                        height: 3px;
                        border: none;
                        border-radius: 6px;
                        background: linear-gradient(
                            90deg,
                            rgba(13, 8, 96, 1) 0%,
                            rgba(9, 9, 121, 1) 11%,
                            rgba(6, 84, 170, 1) 31%,
                            rgba(0, 255, 113, 1) 100%
                        );
                    }
                </style>
            </head>
            <body>
                <div class="logo-container">
                    <img src="https://cdn.bmkg.go.id/Web/Logo-BMKG-new.png" alt="BMKG Logo" class="logo" />
                    <div class="main-text">
                        Stasiun Meteorologi Pangsuma Kapuas Hulu
                        <br> Prakiraan Cuaca Kabupaten
                    </div>
                    <div class="sub-text">
                        Berlaku : """+ tberlaku +""" WIB | Hingga : """+ thingga +""" WIB
                        <hr class="gradient">
                    </div>
                      <colgroup>
                        <col style="width: 20%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 10%;">
                        <col style="width: 10%;">
                        <col style="width: 10%;">
                        <col style="width: 10%;">
                      </colgroup>
                        """ + htmlcode2 + """
                        <!-- This is the second table (your weather icons table) -->
                        <div style="text-align: right; font-size: small;"><sup><i>Developed by Sinangga</i></sup></div>
                        <table>
                            <thead>
                                <tr>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah-am.png" alt="Cerah Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Cerah</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah%20berawan-am.png" alt="Cerah Berawan Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Cerah Berawan</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://api-apps.bmkg.go.id/storage/icon/cuaca/berawan-am.svg" alt="Berawan Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Berawan</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/kabut-am.png" alt="Kabut/Asap Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Kabut/Asap</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/udara%20kabur.png" alt="Udara Kabur Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Udara Kabur</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20ringan-am.png" alt="Hujan Ringan Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Ringan</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20sedang-am.png" alt="Hujan Sedang Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Sedang</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20lebat-am.png" alt="Hujan Lebat Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Lebat</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png" alt="Hujan Petir Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Petir</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png" alt="Petir Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Petir</small>
                                    </th>
                                </tr>
                            </thead>
                        </table> 
                </div>
            </body>
            """
        
        #st.markdown(htmlcode, unsafe_allow_html=True)
        #st.divider()
        def convert_html_to_image(html_content, output_file):
            # Specify Chromium executable path
            hti = Html2Image(browser_executable="/usr/bin/chromium")
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html_file:
                temp_html_file.write(html_content.encode("utf-8"))
                temp_html_file.flush()
                
                # Render the HTML as an image
                hti.screenshot(html_file=temp_html_file.name, save_as=output_file, size=(1080, 1400))
        
        # Add a button for image download
        output_image_file = "info_prakicu_"+tanggal+".png"
        convert_html_to_image(htmlcode, output_image_file)
        st.image(output_image_file)
    with tab4:
        st.write('Tanggal Analisis :', nesting('Bika')[8]['analysis_date'])
        #st.divider()
        # convert your links to html tags 
        def path_to_image_html(path):
            return '<img src="'+ path + ' "width="30px"; >'
        
        
        # Loop through each dictionary and replace values in columns 2-9
        time = []
        for i in range(1,9):
            time.append(jammm[i])
        result_info2 = [dict(zip(headers, values)) for values in datacoba2]
        for entryinfo2 in result_info2:
            for key in time:
                if entryinfo2[key] in status_to_icon:
                    entryinfo2[key] = status_to_icon[entryinfo2[key]]
        
        
        image_cols2 = jam2  #<- define which columns will be used to convert to html
        
        # Create the dictionariy to be passed as formatters
        format_dictinfo2 = {}
        for image_col in image_cols2:
            format_dictinfo2[image_col] = path_to_image_html
        
        # Convert the updated results to a Pandas DataFrame
        df2_info2 = pd.DataFrame(result_info2)
        htmlcode2 = df2_info2.to_html(index = False, escape=False ,formatters=format_dictinfo2)
        htmlcode3 = 'Tanggal Analisis : '+ str(nesting('Bika')[8]['analysis_date'])
        htmlcode = """
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>BMKG Pangsuma</title>
                <style>
                    body {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background-color: #c1efff;
                        margin: 0;
                    }
                    * {
                      font-family: Arial, sans-serif;
                      font-weight: bold;
                    }
                    table {
                        width: 100%;
                        border-collapse: separate;
                        border-spacing: 0;
                        border: 1px solid #ddd;
                        border-radius: 15px;
                        overflow: hidden;
                        align-items: center;
                        justify-content: center;
                        background-color: white;
                        color: black;
                    }
                    tr{
                      text-align: center;
                      background-color: #d0edf7;
                      color: black;
                      height: 30px;
                      overflow: hidden;
                    }
                    th{
                      text-align: center;
                      background-color: #0a2f69;
                      color: white;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        text-align: center;
                        padding: 8px;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    tr:nth-child(odd) {
                        background-color: #ffffff;
                    }
                    td:nth-child(2) img {
                      width: 30px; /*Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(3) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(4) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(5) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }td:nth-child(6) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(7) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(8) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(9) img {
                      width: 30px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    td:nth-child(10) img {
                      width: 50px; /* Set desired image width */
                      height: auto; /* Keep aspect ratio */
                    }
                    .footnote {
                        color: grey;
                        text-align: left;
                        font-size: 15px;
                    }
                    .logo-container {
                        display: flex;
                        flex-direction: column; /* Stack items vertically */
                        align-items: center;
                        /* background-color: #c1efff; White background */
                        background-color: white;
                        padding: 10px; /* Space around the content */
                        border-radius: 8px; /* Rounded corners */
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                        color: black
                    }
                    .logo {
                        width: 40px; /* Adjust size as needed */
                        height: auto;
                    }
                    .main-text {
                        font-size: 20px;
                        color: black;
                        margin: 10px 0; /* Space around the text */
                        text-align: center;
                    }
                    .sub-text {
                        font-size: 16px; /* Slightly smaller font size */
                        color: black; /* Darker gray for the subtitle */
                        text-align: center;
                    }
                    hr.gradient {
                        height: 3px;
                        border: none;
                        border-radius: 6px;
                        background: linear-gradient(
                            90deg,
                            rgba(13, 8, 96, 1) 0%,
                            rgba(9, 9, 121, 1) 11%,
                            rgba(6, 84, 170, 1) 31%,
                            rgba(0, 255, 113, 1) 100%
                        );
                    }
                </style>
            </head>
            <body>
                <div class="logo-container">
                    <img src="https://cdn.bmkg.go.id/Web/Logo-BMKG-new.png" alt="BMKG Logo" class="logo" />
                    <div class="main-text">
                        Stasiun Meteorologi Pangsuma Kapuas Hulu
                        <br> Prakiraan Cuaca Kabupaten
                    </div>
                    <div class="sub-text">
                        Berlaku : """+ tberlaku2 +""" WIB | Hingga : """+ thingga2 +""" WIB
                        <hr class="gradient">
                    </div>
                      <colgroup>
                        <col style="width: 20%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 5%;">
                        <col style="width: 10%;">
                        <col style="width: 10%;">
                        <col style="width: 10%;">
                        <col style="width: 10%;">
                      </colgroup>
                        """ + htmlcode2 + """
                        <div class="coder-left"><sup><i>Developed by Sinangga</i></sup></div>
                        <!-- This is the second table (your weather icons table) -->
                        <table>
                            <thead>
                                <tr>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah-am.png" alt="Cerah Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Cerah</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah%20berawan-am.png" alt="Cerah Berawan Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Cerah Berawan</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://api-apps.bmkg.go.id/storage/icon/cuaca/berawan-am.svg" alt="Berawan Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Berawan</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/kabut-am.png" alt="Kabut/Asap Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Kabut/Asap</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/udara%20kabur.png" alt="Udara Kabur Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Udara Kabur</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20ringan-am.png" alt="Hujan Ringan Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Ringan</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20sedang-am.png" alt="Hujan Sedang Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Sedang</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20lebat-am.png" alt="Hujan Lebat Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Lebat</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png" alt="Hujan Petir Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Hujan Petir</small>
                                    </th>
                                    <th style="text-align: center; padding: 10px;">
                                        <img src="https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png" alt="Petir Icon" style="width: 30px; height: auto; display: block; margin: 0 auto 5px;">
                                        <small>Petir</small>
                                    </th>
                                </tr>
                            </thead>
                        </table> 
                </div>
            </body>
            """
        
        #st.markdown(htmlcode, unsafe_allow_html=True)
        #st.divider()
        def convert_html_to_image(html_content, output_file):
            # Specify Chromium executable path
            hti = Html2Image(browser_executable="/usr/bin/chromium")
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html_file:
                temp_html_file.write(html_content.encode("utf-8"))
                temp_html_file.flush()
                
                # Render the HTML as an image
                hti.screenshot(html_file=temp_html_file.name, save_as=output_file, size=(1080, 1400))
        
        # Add a button for image download
        output_image_file = "info_prakicu_"+tanggal2+".png"
        convert_html_to_image(htmlcode, output_image_file)
        st.image(output_image_file)

    with tab7:
        from folium.features import GeoJsonTooltip, GeoJsonPopup
        import matplotlib.cm as cm
        import matplotlib.colors as colors
        
        #from get_data_BMKG import fetch_bmkg_data, process_bmkg_data
        
        # Title
        st.title("Peta Prakiraan Cuaca Harian - Kapuas Hulu")
        
        # Load GeoJSON
        gdf = gpd.read_file("KH_kecamatan_fix.json")
        gdf = gdf[gdf.is_valid & ~gdf.is_empty]
        gdf['kecamatan'] = gdf['kecamatan'].astype(str).str.strip().str.lower()
        
        # Get weather data
        #with st.spinner("Mengambil data dari BMKG..."):
            #bmkg_data = fetch_bmkg_data()
            #result_dicts, jammm, status_to_icon = process_bmkg_data(bmkg_data)
        
        # Convert to DataFrame
        weather = pd.DataFrame(result_dicts)
        weather["kecamatan"] = weather["KECAMATAN"].str.strip().str.lower()
        
        # Estimate rainfall
        def estimate_rain(entry):
            descriptions = "".join(str(entry[col]) for col in jammm[1:9])
            if "hujan" in descriptions.lower():
                return 30
            elif "berawan" in descriptions.lower():
                return 5
            else:
                return 0
        
        weather["total_rainfall"] = weather.apply(estimate_rain, axis=1)
        
        # Merge to GeoDataFrame
        gdf = gdf.merge(weather[["kecamatan", "total_rainfall"]], on="kecamatan")
        
        # Color map (white to blue)
        norm = colors.Normalize(vmin=0, vmax=50)
        cmap = cm.get_cmap('Blues')
        
        def get_color_by_rain(total):
            rgba = cmap(norm(min(total, 50)))
            return colors.to_hex(rgba)
        
        # HTML table popups
        popup_tables = {}
        for entry in result_dicts:
            kec = entry['KECAMATAN'].strip().lower()
            rows = "".join(f"<tr><td>{t}:00</td><td>{entry[t]}</td></tr>" for t in jammm[1:9])
            table = f"""
                <b>Kecamatan: {kec.title()}</b><br>
                <table style='font-size:10px'>
                    <tr><th>Time</th><th>Condition</th></tr>
                    {rows}
                </table>
            """
            popup_tables[kec] = table
        
        gdf["popup"] = gdf["kecamatan"].map(popup_tables)
        
        rain_dict = dict(zip(gdf["kecamatan"], gdf["total_rainfall"]))
        
        def style_function(feature):
            kecamatan = feature["properties"].get("kecamatan", "").strip().lower()
            total_rain = rain_dict.get(kecamatan, 0.0)
            return {
                "fillColor": get_color_by_rain(total_rain),
                "color": "black",
                "weight": 0.8,
                "fillOpacity": 0.6,
            }
            
        @st.experimental_fragment
        def show_map(gdf, style_function):
            m = folium.Map(location=[0.9, 112.9], zoom_start=8, tiles="cartodbpositron")
        
            folium.GeoJson(
                gdf,
                name="Cuaca",
                style_function=style_function,
                tooltip=GeoJsonTooltip(fields=["kecamatan"], aliases=["Kecamatan"]),
                popup=folium.GeoJsonPopup(fields=["popup"], labels=False, max_width=400)
            ).add_to(m)
        
            st_folium(m, width=700, height=500, key="static_map")
        
        
        # Usage
        show_map(gdf, style_function)



        


    
