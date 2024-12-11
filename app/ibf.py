import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO


tab1, tab2, tab3 = st.tabs(["H0", "H24", "H48"])
#st.header("Impact Based Forecast Wilayah Kalimantan Barat")

with tab1:
    st.header("H-0")
    H00 = "https://web-meteo.bmkg.go.id/media/data/bmkg/ibfnew/20_kalbar_00.png"  
    st.image(H00)

with tab2:
    st.header("H-24")
    H24 = "https://web-meteo.bmkg.go.id/media/data/bmkg/ibfnew/20_kalbar_24.png"  
    st.image(H24)

with tab3:
    st.header("H-48")
    H48 = "https://web-meteo.bmkg.go.id/media/data/bmkg/ibfnew/20_kalbar_48.png"  
    st.image(H48)
