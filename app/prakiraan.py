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
def cuaca_pertama(n):
    suhu = []
    #angin = []
    arah = []
    rh = []
    list_cuaca = []
    list_tgl = []
    for i in range(8):
        suhu.append(nesting(n)[i]["t"])
        #angin.append(nesting(n)[i]["ws"])
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
    #angin = max(angin)
    arah = statistics.mode(arah)
    return n, list_tgl, list_cuaca, suhu_akhir, rh_akhir, arah#, angin

def cuaca_kedua(n):
    suhu = []
    #angin = []
    arah = []
    rh = []
    list_cuaca = []
    list_tgl = []
    for i in range(8,16):
        suhu.append(nesting(n)[i]["t"])
        #angin.append(nesting(n)[i]["ws"])
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
    #angin = max(angin)
    arah = statistics.mode(arah)
    return n, list_tgl, list_cuaca, suhu_akhir, rh_akhir, arah#, angin

## Calling Data Kecamatan Daily
def harian_kecamatan(waktu, nama):
    (a, b, c, d, e, f) = waktu(nama)
    nama = []
    for x in (a, d, e, f):
        if x in (a,d,e,f):
            nama.append(x)
    for i in range(len(c)):
        nama.append(c[i])
    order_list = [0,4,5,6,7,8,9,10,11,1,2,3]
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
    #nama[12] = str(round(nama[12])) + " Knot"
    nama[10] = str(nama[10]) + "%"
    nama[9] = str(nama[9]) + "°C"
    return nama

## Printing to Web
def waktuu(waktu):
    (a, b, c, d, e, f) = waktu("Bika")
    tanggal = b[0][8]+b[0][9]+str("-")+b[0][5]+b[0][6]+str("-")+b[0][0]+b[0][1]+b[0][2]+b[0][3]
    tanalisis = df_kh[0]['cuaca'][0][0]['analysis_date']
    tberlaku = b[0]
    thingga = b[7]
    jam = []
    for i in range(len(b)):
        jam.append(b[i][11]+b[i][12])
    jamm = ['KECAMATAN', jam, 'SUHU', 'KELEMBAPAN', 'ANGIN']
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


tab1, tab2, tab7 = st.tabs(["Infografis","Tabel", 'Post'])
with tab1:
    tab3, tab4 = st.tabs([tanggal, tanggal2])
    
    with tab3:
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
                        padding: 20px; /* Space around the content */
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
                        Berlaku mulai : """+ tberlaku +"""UTC
                        <br>Hingga : """+ thingga +"""UTC
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
                      </colgroup>
                        """ + htmlcode2 + """
                    <div class="footnote">
                        """ + htmlcode3 + """
                    </div>
                </div>
            </body>
            """
        
        st.markdown(htmlcode, unsafe_allow_html=True)
        st.divider()
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
        if st.button("Unduh Infografis "+tanggal+""):
            try:
                output_image_file = "info_prakicu_"+tanggal+".png"  # Define output image file name
                
                # Convert HTML content to an image
                convert_html_to_image(htmlcode, output_image_file)
                
                # Provide download link for the image
                with open(output_image_file, "rb") as file:
                    st.download_button(
                        label="Unduh",
                        data=file,
                        file_name="info_prakicu_"+tanggal+".png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Failed to create image: {e}")
    with tab4:
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
                        padding: 20px; /* Space around the content */
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
                        Berlaku mulai : """+ tberlaku2 +"""UTC
                        <br>Hingga : """+ thingga2 +"""UTC
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
                      </colgroup>
                        """ + htmlcode2 + """
                    <div class="footnote">
                        """ + htmlcode3 + """
                    </div>
                </div>
            </body>
            """
        
        st.markdown(htmlcode, unsafe_allow_html=True)
        st.divider()
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
        if st.button("Unduh Infografis "+tanggal2+""):
            try:
                output_image_file = "info_prakicu_"+tanggal2+".png"  # Define output image file name
                
                # Convert HTML content to an image
                convert_html_to_image(htmlcode, output_image_file)
                
                # Provide download link for the image
                with open(output_image_file, "rb") as file:
                    st.download_button(
                        label="Unduh",
                        data=file,
                        file_name="info_prakicu_"+tanggal2+".png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Failed to create image: {e}")
with tab2:
    tab5, tab6 = st.tabs([tanggal, tanggal2])
    with tab5:
        #st.header("Kabupaten | Tanggal "+tanggal)
        #st.write('Tanggal Analisis :', nesting('Bika')[0]['analysis_date'])
        dfhtml = """
            <p> Tanggal Analisis : """+str(nesting('Bika')[0]['analysis_date'])+"""</p>
            """+dfhtml+"""
        """
        st.markdown(dfhtml, unsafe_allow_html=True)
        st.divider()
        dfhtmlcss = """
            <style>
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
                    color: black;
                    background-color: #95c8e6;
                }
                th {
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
            </style>
           """+ dfhtml+"""
        """
        def convert_html_to_img(html_content, output_file):
            # Specify Chromium executable path
            hti = Html2Image(browser_executable="/usr/bin/chromium")
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html_file:
                temp_html_file.write(html_content.encode("utf-8"))
                temp_html_file.flush()
                
                # Render the HTML as an image
                hti.screenshot(html_file=temp_html_file.name, save_as=output_file, size=(1080, 1650))
        
        # Add a button for image download
        if st.button("Unduh Tabel"+tanggal+""):
            try:
                output_image_filet = "tabel_prakicu_"+tanggal+".png"  # Define output image file name
                
                # Convert HTML content to an image
                convert_html_to_img(dfhtmlcss, output_image_filet)
                
                # Provide download link for the image
                with open(output_image_filet, "rb") as file:
                    st.download_button(
                        label="Unduh",
                        data=file,
                        file_name="tabel_prakicu_"+tanggal+".png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Failed to create image: {e}")

    with tab6:
        #st.header("Kabupaten | Tanggal "+tanggal)
        st.write('Tanggal Analisis :', nesting('Bika')[8]['analysis_date'])
        st.markdown(dfhtml2, unsafe_allow_html=True)
        st.divider()
        dfhtmlcss = """
            <style>
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
                    color: black;
                    background-color: #95c8e6;
                }
                th {
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
            </style>
           """+ dfhtml2+"""
        """
        def convert_html_to_img(html_content, output_file):
            # Specify Chromium executable path
            hti = Html2Image(browser_executable="/usr/bin/chromium")
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html_file:
                temp_html_file.write(html_content.encode("utf-8"))
                temp_html_file.flush()
                
                # Render the HTML as an image
                hti.screenshot(html_file=temp_html_file.name, save_as=output_file, size=(1080, 1650))
        
        # Add a button for image download
        if st.button("Unduh Tabel "+tanggal2+""):
            try:
                output_image_filet = "tabel_prakicu_"+tanggal2+".png"  # Define output image file name
                
                # Convert HTML content to an image
                convert_html_to_img(dfhtmlcss, output_image_filet)
                
                # Provide download link for the image
                with open(output_image_filet, "rb") as file:
                    st.download_button(
                        label="Unduh",
                        data=file,
                        file_name="tabel_prakicu_"+tanggal2+".png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Failed to create image: {e}")
    with tab7:
        st.write("post key : ",st.secrets(client_secret))
