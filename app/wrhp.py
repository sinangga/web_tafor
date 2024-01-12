import streamlit as st
tab1, tab2, tab3 = st.tabs(["Analisis Streamline", "", ""])

with tab1:
   st.header("Analisis Streamline")
   st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/streamline//T_PGXA15_C_WIIX_20240111120000.STREAMLINES925.png", width=None)

with tab2:
   st.header("RH")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("Isobar")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)