import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO


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
   # Step 1: Load the image
   image_url = "https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png"  # Replace with your actual image path
   response = requests.get(image_url)
   image = Image.open(BytesIO(response.content))
   # Step 2: Draw a rectangle
   draw = ImageDraw.Draw(image)
   rect_x1, rect_y1 = 925, 375  # Starting coordinates (top-left corner)
   rect_x2, rect_y2 = 1125, 575  # Ending coordinates (bottom-right corner)
   draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline="red", width=3)
   
   # Step 3: Display the image in Streamlit
   st.image(image)
   #st.image("https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png", width=None)

with tab3:
   st.header("RADAR")
    # Step 1: Load the image
   image_url_rad = "https://inderaja.bmkg.go.id/Radar/SINT_SingleLayerCRefQC.png"  # Replace with your actual image path
   response_rad = requests.get(image_url_rad)
   image_rad = Image.open(BytesIO(response_rad.content))
   # Step 2: Draw a rectangle
   draw_rad = ImageDraw.Draw(image_rad)
   rect_x1r, rect_y1r = 910, 290 # Starting coordinates (top-left corner)
   rect_x2r, rect_y2r = 1110, 490  # Ending coordinates (bottom-right corner)
   draw_rad.rectangle([rect_x1r, rect_y1r, rect_x2r, rect_y2r], outline="red", width=3)
   
   # Step 3: Display the image in Streamlit
   st.image(image_rad)
   #st.image("https://inderaja.bmkg.go.id/Radar/SINT_SingleLayerCRefQC.png", width=None)
