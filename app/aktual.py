import streamlit as st
tab1, tab2, tab3 = st.tabs(["METAR", "SATELIT", "RADAR"])

with tab1:
   st.header("METAR 24 Jam")
   #st.image("https://static.streamlit.io/examples/cat.jpg", width=None)

with tab2:
   st.header("SATELIT")
   st.image("https://satelit.bmkg.go.id/IMAGE/HIMA/H08_EH_Kalbar.png", width=None)

with tab3:
   st.header("RADAR")
   st.image("https://inderaja.bmkg.go.id/Radar/SINT_SingleLayerCRefQC.png", width=None)
