import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from datetime import datetime

# DATE ACQUIRING
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

tab1, tab2 = st.tabs(["Peta", "Detail"])
#st.header("Impact Based Forecast Wilayah Kalimantan Barat")

with tab1:
    st.header("Peta")
    url = "https://nowcasting.bmkg.go.id/infografis/CKB/"+year+"/"+month+"/"+day+"/infografis.jpg"
    st.image(url)

with tab2:
    st.header("Detail")
    url_text = "https://nowcasting.bmkg.go.id/infografis/CKB/"+year+"/"+month+"/"+day+"/infografis_text.jpg"
    st.image(url_text)
