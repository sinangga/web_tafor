import streamlit as st
import requests
tab1, tab2, tab3 = st.tabs(["METAR", "SATELIT", "RADAR"])

with tab1:
   st.header("METAR & TAFOR")
   URL = "https://api.bmkg.go.id/cuaca-bandara?icao=WIOP"

   r=requests.get(URL, headers={"X-API-KEY": "}Af*4TG=ZGp99sT",
                               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
   data = r.json()
   st.write("Bandar Udara Pangsuma Kapuas Hulu")
   st.write("Latest METAR : ", data["last_observation"])
   st.write("Latest TAFOR : ", data["last_forecast"])
   st.divider()
   st.write("Produced by: BMKG Pangsuma Kapuas Hulu")

with tab2:
   st.header("SATELIT")
   st.image("https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png", width=None)

with tab3:
   st.header("RADAR")
   st.image("https://inderaja.bmkg.go.id/Radar/SINT_SingleLayerCRefQC.png", width=None)
