import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO


tab1, tab2 = st.tabs(["PETA", "DETAIL"])
#st.header("Impact Based Forecast Wilayah Kalimantan Barat")

with tab1:
    st.header("PETA")
    H00 = "https://web-meteo.bmkg.go.id/media/data/bmkg/ibfnew/20_kalbar_00.png" 
    URL = "https://nowcasting.bmkg.go.id/infografis/CKB/2024/12/16/infografis.jpg"
    st.image(URL)

with tab2:
    st.header("DETAIL")
    H24 = "https://web-meteo.bmkg.go.id/media/data/bmkg/ibfnew/20_kalbar_24.png" 
    URL = "https://nowcasting.bmkg.go.id/infografis/CKB/2024/12/16/infografis.jpg"
    st.image(URL)
