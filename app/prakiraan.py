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
from IPython.core.display import display, HTML
import altair as alt
from html2image import Html2Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


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
    #nest3 = nesting[2]
    nesting_list = [nest1, nest2]
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
    nama[12] = str(round(nama[12])) + " Knot"
    nama[10] = str(nama[10]) + "%"
    nama[9] = str(nama[9]) + "°C"
    return nama

## Printing to Web
(a, b, c, d, e, f, g) = cuaca_gabungan_pagi("Bika")
tanggal = b[0][8]+b[0][9]+str("/")+b[0][5]+b[0][6]+str("/")+b[0][0]+b[0][1]+b[0][2]+b[0][3]
tanalisis = df_kh[0]['cuaca'][0][0]['analysis_date']
jam = []
for i in range(len(b)):
    jam.append(b[i][11]+b[i][12])

jamm = ['KECAMATAN', jam, 'SUHU', 'KELEMBAPAN', 'ANGIN', 'KECEPATAN']
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

# Loop through each dictionary and replace values in columns 2-9
time = []
for i in range(1,9):
    time.append(jammm[i])
for entry in result_dicts:
    for key in time:
        if entry[key] in status_to_icon:
            entry[key] = f'<img src="{status_to_icon[entry[key]]}" width="70">'

# Convert the updated results to a Pandas DataFrame
df = pd.DataFrame(result_dicts)

# Display the DataFrame as HTML
#display = HTML(df.to_html(escape=False))

#########################
#########################
# Load SHP data
KH_map = gpd.read_file('https://github.com/sinangga/shp/raw/refs/heads/main/Kapuas_Hulu.shp')
chart = alt.Chart(KH_map).mark_geoshape()


    
### End of Main Code ###
########################


tab1, tab2 = st.tabs(["Kabupaten","Kecamatan"])

with tab1:
    tab3, tab4, tab5 = st.tabs([tanggal,'Hari Kedua', 'Unduh Tabel'])
    with tab3:
        #st.header("Kabupaten | Tanggal "+tanggal)
        st.write('Tanggal Analisis :',df_kh[0]['cuaca'][0][0]['analysis_date'])
        st.markdown(df.to_html(index = False, escape=False), unsafe_allow_html=True)
    with tab5:
        # convert your links to html tags 
        def path_to_image_html(path):
            return '<img src="'+ path + '" width="40" >'
        
        
        # Loop through each dictionary and replace values in columns 2-9
        time = []
        for i in range(1,9):
            time.append(jammm[i])
        result_dicts2 = [dict(zip(headers, values)) for values in datacoba]
        for entry2 in result_dicts2:
            for key in time:
                if entry2[key] in status_to_icon:
                    entry2[key] = status_to_icon[entry2[key]]
        
        
        image_cols = jam  #<- define which columns will be used to convert to html
        
        # Create the dictionariy to be passed as formatters
        format_dict2 = {}
        for image_col in image_cols:
            format_dict2[image_col] = path_to_image_html
        
        # Convert the updated results to a Pandas DataFrame
        df2 = pd.DataFrame(result_dicts2)
        htmlcode2 = df2.to_html(index = False, escape=False ,formatters=format_dict2)
        htmlcode3 = 'Tanggal Analisis : '+str(df_kh[0]['cuaca'][0][0]['analysis_date'])
        htmlcode = """
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>BMKG Logo</title>
                <style>
                    body {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        background-color: ##c1efff;
                        margin: 0;
                    }
                    table {
                        align-items: center
                        justify-content: center;
                        background-color: #c1efff;
                        color: black;
                    }
                    th {
                        background-color: blue;
                        color: white;
                        pading: 10px;
                    }
                    td {
                        text-align: center;
                    }
                    .footnote {
                        color: grey;
                        text-align: left;
                    }
                    .logo-container {
                        display: flex;
                        flex-direction: column; /* Stack items vertically */
                        align-items: center;
                        background-color: #c1efff; /* White background */
                        padding: 20px; /* Space around the content */
                        border-radius: 8px; /* Rounded corners */
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                        color: black
                    }
                    .logo {
                        width: 100px; /* Adjust size as needed */
                        height: auto;
                    }
                    .main-text {
                        font-size: 20px;
                        color: black;
                        margin: 10px 0; /* Space around the text */
                    }
                    .sub-text {
                        font-size: 16px; /* Slightly smaller font size */
                        color: black; /* Darker gray for the subtitle */
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
                    </div>
                    <div class="sub-text">
                        Prakiraan Cuaca Kabupaten Kapuas Hulu
                        <hr class="gradient">
                    </div>
                        """ + htmlcode2 + """
                    <div class="footnote">
                        """ + htmlcode3 + """
                    </div>
                </div>
            </body>
            """
        
        st.markdown(htmlcode, unsafe_allow_html=True)

        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Function to initialize WebDriver
        @st.cache_resource  # Cache the WebDriver to avoid reinitialization
        def init_webdriver():
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Specify path to your ChromeDriver if necessary, e.g., executable_path="/path/to/chromedriver"
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        
        # Function to capture HTML as an image and save as a file
        def capture_html_as_image(html_content, file_name="page_image.png"):
            # Save HTML content to a temporary file
            with open("temp.html", "w") as f:
                f.write(html_content)
            
            # Open the temporary HTML file in the browser
            driver.get("file://" + "temp.html")
            
            # Allow time for the page to render fully
            time.sleep(2)
            
            # Capture a screenshot and save it as an image file
            driver.save_screenshot(file_name)
            return file_name
        
        # Capture the HTML content as an image and save it to a file
        image_file = capture_html_as_image(htmlcode)
        
        # Display the image in Streamlit
        #st.image(image_file, caption="Captured HTML Page as Image", use_column_width=True)
        
        # Create a download button for the image file in Streamlit
        with open(image_file, "rb") as img_file:
            st.download_button(
                label="Download",
                data=img_file,
                file_name="page_image.png",
                mime="image/png"
            )
        
        # Close the browser
        driver.quit()
        #st.image("page_image.png", caption="Captured HTML Page as Image", use_column_width=True)
        #st.markdown(dff, unsafe_allow_html=True)
        #st.markdown('Tanggal Analisis'+tanalisis)
        #df.to_html(escape=False ,formatters=format_dict)
        # Display the DataFrame as HTML

with tab2:
    st.header("Kecamatan")
    st.altair_chart(chart)
    # Display Map
    #BorderAZ.plot()
