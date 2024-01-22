import streamlit as st
from datetime import datetime
import datetime as dttime
import numpy as np
import requests
from io import BytesIO
from PIL import Image
#import matplotlib.pyplot as plt
#%matplotlib inline
from imagedominantcolor import DominantColor

# INDEX RGB HUJAN
hujan_50 = (230,  24, 180)
hujan_20 = (237,  36,  29)
hujan_17 = (233, 101,  30)
hujan_14 = (236, 141,  28)
hujan_10 = (234, 168,  27)
hujan_7 = (238, 209,  21)
hujan_5 = (241, 241,  31)
hujan_3 = (163, 237,  26)
hujan_1 = (103, 243,  33)
hujan_03 = (135, 243, 134)
hujan_01 = (171, 177, 186)
hujan_001 = (231, 231, 230)
tidak_hujan = (255, 255, 255)

# BOX Putussibau
putussibau = (580,235,600,255)

# FUNGSI DOMINAN
def kategori_hujan(url):
    global hujan_psu
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    if img.mode == 'RGBA':
        rgb_image = img.convert('RGB')
    if img.mode == 'CMYK':
        rgb_image = img.convert('RGB')
    if img.mode == 'RGB':
        rgb_image = img
    if img.mode == 'HSV':
        rgb_image = img.convert('RGB')
    psu = rgb_image.crop(putussibau)#img_arr = np.asarray(psu)
    psu_image = psu.copy()
    psu = sorted(psu.getcolors(2 ** 24), reverse=True)[0][1]
    if psu == hujan_50:
        hujan_psu = "50 mm/jam"
    if psu == hujan_20:
        hujan_psu = "20 mm/jam"
    if psu == hujan_17:
        hujan_psu = "17 mm/jam"
    if psu == hujan_14:
        hujan_psu = "14 mm/jam"
    if psu == hujan_10:
        hujan_psu = "10 mm/jam"
    if psu == hujan_7:
        hujan_psu = "7 mm/jam"
    if psu == hujan_5:
        hujan_psu = "5 mm/jam"
    if psu == hujan_3:
        hujan_psu = "3 mm/jam"
    if psu == hujan_1:
        hujan_psu = "1 mm/jam"
    if psu == hujan_03:
        hujan_psu = "0.3 mm/jam"
    if psu == hujan_01:
        hujan_psu = "0.1 mm/jam"
    if psu == hujan_001:
        hujan_psu = "0.01 mm/jam"
    if psu == tidak_hujan:
        hujan_psu = "Tidak Hujan"

        
    # Rata-rata hujan
    rr50, rr20, rr17, rr14, rr10, rr7, rr5, rr3, rr1, rr03, rr01, rr001, norain = 0,0,0,0,0,0,0,0,0,0,0,0,0
    data = psu_image.getdata()
    for pixel in data:
        if pixel == (230,  24, 180):
            rr50 += 1
        else:
            if pixel == (237,  36,  29):
                rr20 += 1
            else:
                if pixel == (233, 101,  30):
                    rr17 += 1
                else:
                    if pixel == (236, 141,  28):
                        rr14 += 1
                    else:
                        if pixel == (234, 168,  27):
                            rr10 += 1
                        else:
                            if pixel == (238, 209,  21):
                                rr7 += 1
                            else:
                                if pixel == (241, 241,  31):
                                    rr5 += 1
                                else:
                                    if pixel == (163, 237,  26):
                                        rr3 += 1
                                    else:
                                        if pixel == (103, 243,  33):
                                            rr1 += 1
                                        else:
                                            if pixel == (135, 243, 134):
                                                rr03 += 1
                                            else:
                                                if pixel == (171, 177, 186):
                                                    rr01 += 1
                                                else:
                                                    if pixel == (231, 231, 230):
                                                        rr001 += 1
                                                    else:
                                                        if pixel == (255, 255, 255):
                                                            norain += 1
    
    #print("pixel hujan 50 =",rr50,"pixel hujan 20 =",rr20,"pixel hujan 17 = ",rr17,"pixel hujan 14 = ",rr14, "pixel hujan 10 =",rr10,"pixel hujan 7 = ",rr7,"pixel hujan 5 =",rr5,"pixel hujan 3 = ",rr3,"pixel hujan 1 =",rr1,"pixel hujan 0.3 = ",rr03,"pixel hujan 0.1 =",rr01,"pixel hujan 0.01 = ",rr001,"pixel tidak hujan = ",norain)
    ratarata = (rr50 * 50) + (rr20 * 20) + (rr17 * 17) + (rr14 * 14) + (rr10 * 10) + (rr7 * 7) + (rr5 *5) + (rr3 *3)+ (rr1 * 1) + (rr03 * 0.3) + (rr01 * 0.1) + (rr001 * 0.01)
    ratarata = round(ratarata / (400-norain),2)        
    return hujan_psu, ratarata


# MAIN PAGE
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
    with tab3:
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+str(tl1.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab4:
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl2.strftime('%Y'))+str(tl2.strftime('%m'))+str(tl2.strftime('%d'))+str(tl2.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab5:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl3.strftime('%Y'))+str(tl3.strftime('%m'))+str(tl3.strftime('%d'))+str(tl3.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl3.strftime('%Y'))+str(tl3.strftime('%m'))+str(tl3.strftime('%d'))+str(tl3.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab6:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl4.strftime('%Y'))+str(tl4.strftime('%m'))+str(tl4.strftime('%d'))+str(tl4.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl4.strftime('%Y'))+str(tl4.strftime('%m'))+str(tl4.strftime('%d'))+str(tl4.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab7:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl5.strftime('%Y'))+str(tl5.strftime('%m'))+str(tl5.strftime('%d'))+str(tl5.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl5.strftime('%Y'))+str(tl5.strftime('%m'))+str(tl5.strftime('%d'))+str(tl5.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab8:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl6.strftime('%Y'))+str(tl6.strftime('%m'))+str(tl6.strftime('%d'))+str(tl6.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl6.strftime('%Y'))+str(tl6.strftime('%m'))+str(tl6.strftime('%d'))+str(tl6.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab9:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl7.strftime('%Y'))+str(tl7.strftime('%m'))+str(tl7.strftime('%d'))+str(tl7.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl7.strftime('%Y'))+str(tl7.strftime('%m'))+str(tl7.strftime('%d'))+str(tl7.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab10:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl8.strftime('%Y'))+str(tl8.strftime('%m'))+str(tl8.strftime('%d'))+str(tl8.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/ecmwf/prakiraan/Backup/RAIN/rainrate_ifs0p125_sfc_"+str(tl8.strftime('%Y'))+str(tl8.strftime('%m'))+str(tl8.strftime('%d'))+str(tl8.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
with tab2:
    st.header("WRF")
    tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18 = st.tabs(listtime)
    with tab11:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t1.strftime('%Y'))+str(t1.strftime('%m'))+str(t1.strftime('%d'))+str(t1.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t1.strftime('%Y'))+str(t1.strftime('%m'))+str(t1.strftime('%d'))+str(t1.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab12:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t2.strftime('%Y'))+str(t2.strftime('%m'))+str(t2.strftime('%d'))+str(t2.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t2.strftime('%Y'))+str(t2.strftime('%m'))+str(t2.strftime('%d'))+str(t2.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab13:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t3.strftime('%Y'))+str(t3.strftime('%m'))+str(t3.strftime('%d'))+str(t3.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t3.strftime('%Y'))+str(t3.strftime('%m'))+str(t3.strftime('%d'))+str(t3.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab14:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t4.strftime('%Y'))+str(t4.strftime('%m'))+str(t4.strftime('%d'))+str(t4.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t4.strftime('%Y'))+str(t4.strftime('%m'))+str(t4.strftime('%d'))+str(t4.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab15:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t5.strftime('%Y'))+str(t5.strftime('%m'))+str(t5.strftime('%d'))+str(t5.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t5.strftime('%Y'))+str(t5.strftime('%m'))+str(t5.strftime('%d'))+str(t5.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab16:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t6.strftime('%Y'))+str(t6.strftime('%m'))+str(t6.strftime('%d'))+str(t6.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t6.strftime('%Y'))+str(t6.strftime('%m'))+str(t6.strftime('%d'))+str(t6.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab17:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t7.strftime('%Y'))+str(t7.strftime('%m'))+str(t7.strftime('%d'))+str(t7.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t7.strftime('%Y'))+str(t7.strftime('%m'))+str(t7.strftime('%d'))+str(t7.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
    with tab18:
        #st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t8.strftime('%Y'))+str(t8.strftime('%m'))+str(t8.strftime('%d'))+str(t8.strftime('%H'))+"0000.png", width=None)
        url = "https://web.meteo.bmkg.go.id//media/data/bmkg/mfy/wrf/prakiraan/RAIN/rainrate_wrf10km_sfc_"+str(t8.strftime('%Y'))+str(t8.strftime('%m'))+str(t8.strftime('%d'))+str(t8.strftime('%H'))+"0000.png"
        st.image(url, width=None)
        hujan_psu, ratarata = kategori_hujan(url)
        st.write("Kondisi cuaca dominan", hujan_psu,"dengan rata-rata curah hujan untuk wilayah Kapuas Hulu sebesar ",ratarata,"mm/jam")
