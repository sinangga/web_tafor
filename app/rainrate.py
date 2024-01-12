import streamlit as st
from datetime import datetime
import datetime as dttime

tab1, tab2 = st.tabs(["IFS", "WRF"])

now = datetime.utcnow()
t1 = datetime.utcnow() - dttime.timedelta(hours = int(now.strftime('%H'))%3)
t2 = t1 + dttime.timedelta(hours=3)
t3 = t1 + dttime.timedelta(hours=6)
t4 = t1 + dttime.timedelta(hours=9)
t5 = t1 + dttime.timedelta(hours=12)
t6 = t1 + dttime.timedelta(hours=15)
t7 = t1 + dttime.timedelta(hours=18)
t8 = t1 + dttime.timedelta(hours=21)

now = datetime.utcnow()
t1 = datetime.utcnow() - dttime.timedelta(hours = int(now.strftime('%H'))%3)
t2 = t1 + dttime.timedelta(hours=3)
t3 = t1 + dttime.timedelta(hours=6)
t4 = t1 + dttime.timedelta(hours=9)
t5 = t1 + dttime.timedelta(hours=12)
t6 = t1 + dttime.timedelta(hours=15)
t7 = t1 + dttime.timedelta(hours=18)
t8 = t1 + dttime.timedelta(hours=21)
tl1 = t1 + dttime.timedelta(hours=7)
tl2 = tl1 + dttime.timedelta(hours=3)
tl3 = tl2 + dttime.timedelta(hours=3)
tl4 = tl3 + dttime.timedelta(hours=3)
tl5 = tl4 + dttime.timedelta(hours=3)
tl6 = tl5 + dttime.timedelta(hours=3)
tl7 = tl6 + dttime.timedelta(hours=3)
tl8 = tl7 + dttime.timedelta(hours=3)

listtime = [t1.strftime('%H'),t2.strftime('%H'),t3.strftime('%H'),t4.strftime('%H'),t5.strftime('%H'),t6.strftime('%H'),t7.strftime('%H'),t8.strftime('%H')]
listtimel = [tl1.strftime('%H'),tl2.strftime('%H'),tl3.strftime('%H'),tl4.strftime('%H'),tl5.strftime('%H'),tl6.strftime('%H'),tl7.strftime('%H'),tl8.strftime('%H')]

with tab1:
    st.header("IFS")
    tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(listtimel)
    with tab3:        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+str(tl1.strftime('%H'))+"0000.png", width=None)
    with tab4:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl2.strftime('%Y'))+str(tl2.strftime('%m'))+str(tl2.strftime('%d'))+str(tl2.strftime('%H'))+"0000.png", width=None)
    with tab5:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl3.strftime('%Y'))+str(tl3.strftime('%m'))+str(tl3.strftime('%d'))+str(tl3.strftime('%H'))+"0000.png", width=None)
    with tab6:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl4.strftime('%Y'))+str(tl4.strftime('%m'))+str(tl4.strftime('%d'))+str(tl4.strftime('%H'))+"0000.png", width=None)
    with tab7:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl5.strftime('%Y'))+str(tl5.strftime('%m'))+str(tl5.strftime('%d'))+str(tl5.strftime('%H'))+"0000.png", width=None)
    with tab8:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl6.strftime('%Y'))+str(tl6.strftime('%m'))+str(tl6.strftime('%d'))+str(tl6.strftime('%H'))+"0000.png", width=None)
    with tab9:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl7.strftime('%Y'))+str(tl7.strftime('%m'))+str(tl7.strftime('%d'))+str(tl7.strftime('%H'))+"0000.png", width=None)
    with tab10:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl8.strftime('%Y'))+str(tl8.strftime('%m'))+str(tl8.strftime('%d'))+str(tl8.strftime('%H'))+"0000.png", width=None)

with tab2:
    st.header("WRF")
    tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18 = st.tabs(listtime)
    with tab11:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t1.strftime('%Y'))+str(t1.strftime('%m'))+str(t1.strftime('%d'))+str(t1.strftime('%H'))+"0000.png", width=None)
    with tab12:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t2.strftime('%Y'))+str(t2.strftime('%m'))+str(t2.strftime('%d'))+str(t2.strftime('%H'))+"0000.png", width=None)
    with tab13:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t3.strftime('%Y'))+str(t3.strftime('%m'))+str(t3.strftime('%d'))+str(t3.strftime('%H'))+"0000.png", width=None)
    with tab14:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t4.strftime('%Y'))+str(t4.strftime('%m'))+str(t4.strftime('%d'))+str(t4.strftime('%H'))+"0000.png", width=None)
    with tab15:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t5.strftime('%Y'))+str(t5.strftime('%m'))+str(t5.strftime('%d'))+str(t5.strftime('%H'))+"0000.png", width=None)
    with tab16:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t6.strftime('%Y'))+str(t6.strftime('%m'))+str(t6.strftime('%d'))+str(t6.strftime('%H'))+"0000.png", width=None)
    with tab17:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t7.strftime('%Y'))+str(t7.strftime('%m'))+str(t7.strftime('%d'))+str(t7.strftime('%H'))+"0000.png", width=None)
    with tab18:
        st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t8.strftime('%Y'))+str(t8.strftime('%m'))+str(t8.strftime('%d'))+str(t8.strftime('%H'))+"0000.png", width=None)
