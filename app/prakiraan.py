import streamlit as st
import pandas
import urllib.request, json
import requests

###
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

# 
def printcuaca(x):
    n = 0
    for i in list_kecamatan:
        print(list_kecamatan[n])
        data = nesting(i)
        for a in range(x):
            print(data[a]["utc_datetime"], data[a]["weather_desc"])
        n = n+1

###

tab1, tab2 = st.tabs(["Prakicu","Test"])

with tab1:
    st.header("Prakicu")
    st.write(printcuaca(3))
with tab2:
    st.header("Test")
    st.image("https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png", width=None)
   #df = pandas.read_xml("https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanBarat.xml")
   #st.write(df)
   #st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

