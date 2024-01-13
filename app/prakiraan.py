import streamlit as st
import pandas
tab1 = st.tabs(["XML"])

with tab1:
   st.header("XML")
   df = pandas.read_xml("https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanBarat.xml")
   st.write(df)
   #st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

