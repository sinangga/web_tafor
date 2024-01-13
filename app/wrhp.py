import streamlit as st
from datetime import datetime
import datetime as dttime

tl1 = datetime.utcnow()

tab1, tab2, tab3 = st.tabs(["Analisis Streamline", "SIGWX MED", "SIGWX HIGH"])

with tab1:
   st.header("Analisis Streamline")
   st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/streamline//T_PGXA15_C_WIIX_20240111120000.STREAMLINES925.png", width=None)

with tab2:
   st.header("SIGWX MED")
   sig1, sig2 = st.tabs(["A", "B"])
   with sig1:
      st.image("https://aviation.bmkg.go.id/shared/sigwx/"+str(tl1.strftime('%Y'))+"/"+str(tl1.strftime('%m'))+"/sigwx_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+"0000.jpeg", width=None)
   with sig2:
      st.image("https://aviation.bmkg.go.id/shared/sigwx/"+str(tl1.strftime('%Y'))+"/"+str(tl1.strftime('%m'))+"/sigwx_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+"0600.jpeg", width=None)

with tab3:
   st.header("Isobar")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=None)
