import streamlit as st
tab1, tab2, tab3, tab4 = st.tabs(["MJO", "SURGE", "SST NINO", "IOD"])

with tab1:
   st.header("MJO")
   st.image("https://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/combphase_noCFSfull.gif", width=None)

with tab2:
   st.header("SURGE")
   st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/sur_idx.png", width=None)
    
with tab3:
   st.header("SST NINO 3.4")
   st.image("http://www.bom.gov.au/climate/enso/wrap-up/archive/20240109.sstOutlooks_nino34.png", width=None)

with tab4:
   st.header("IOD")
   st.image("http://www.bom.gov.au/clim_data/IDCK000072/iod1.png", width=None)