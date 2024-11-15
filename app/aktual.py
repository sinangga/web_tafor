import streamlit as st
from PIL import Image, ImageDraw
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
   # Step 1: Load the image
   image_path = "https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png"  # Replace with your actual image path
   image = Image.open(image_path)
   
   # Step 2: Draw a rectangle
   draw = ImageDraw.Draw(image)
   rect_x1, rect_y1 = 50, 50  # Starting coordinates (top-left corner)
   rect_x2, rect_y2 = 200, 200  # Ending coordinates (bottom-right corner)
   draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline="red", width=3)
   
   # Optionally, draw a line
   line_start = (50, 250)  # Starting point of the line (x, y)
   line_end = (250, 250)   # Ending point of the line (x, y)
   draw.line([line_start, line_end], fill="blue", width=2)
   
   # Step 3: Display the image in Streamlit
   st.image(image, caption="Image with overlay")#, use_column_width=True)
   #st.image("https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png", width=None)

with tab3:
   st.header("RADAR")
   st.image("https://inderaja.bmkg.go.id/Radar/SINT_SingleLayerCRefQC.png", width=None)
