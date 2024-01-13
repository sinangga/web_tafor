import streamlit as st
from datetime import datetime
import datetime as dttime
import streamlit.components.v1 as components


tl1 = datetime.utcnow()

tab1, tab2, tab3 = st.tabs(["Analisis Streamline", "SIGWX MED", "RASON"])

with tab1:
   st.header("Analisis Streamline")
   stm, st1, st2, st3= st.tabs(["H1", "H2", "H3", "H4"])
   with st1:
      st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/streamline//T_PGXA15_C_WIIX_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(int(tl1.strftime('%d'))-1)+"000000.STREAMLINES925.png", width=None)      
   with st2:
      st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/streamline//T_PGXA15_C_WIIX_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(int(tl1.strftime('%d'))-1)+"120000.STREAMLINES925.png", width=None)
   with st3:
      st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/streamline//T_PGXA15_C_WIIX_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+"000000.STREAMLINES925.png", width=None)
   with stm:
      st.image("https://web.meteo.bmkg.go.id//media/data/bmkg/streamline//T_PGXA15_C_WIIX_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+"000000.STREAMLINES925.png", width=None)

with tab2:
   st.header("SIGWX MED")
   sig1, sig2 = st.tabs(["A", "B"])
   with sig1:
      st.image("https://aviation.bmkg.go.id/shared/sigwx/"+str(tl1.strftime('%Y'))+"/"+str(tl1.strftime('%m'))+"/sigwx_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+"0000.jpeg", width=None)
   with sig2:
      st.image("https://aviation.bmkg.go.id/shared/sigwx/"+str(tl1.strftime('%Y'))+"/"+str(tl1.strftime('%m'))+"/sigwx_"+str(tl1.strftime('%Y'))+str(tl1.strftime('%m'))+str(tl1.strftime('%d'))+"0600.jpeg", width=None)

with tab3:
   st.header("RASON")
   def run():
      iframe_src = "https://aviation.bmkg.go.id/monitoring_rason/index"
      components.iframe(iframe_src, height=750)
   # You can add height and width to the component of course.

   if __name__ == "__main__":
      run()
