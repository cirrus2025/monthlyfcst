import streamlit as st
import subprocess

st.set_page_config(page_title="Forecasters' Tools", layout="centered")

st.title("Forecasters' Tools")

st.write("Select a tool to launch:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Rainfall Outlook Map"):
        subprocess.Popen(["streamlit", "run", "map_app_rainfall.py"])
    if st.button("Temperature Outlook Map"):
        subprocess.Popen(["streamlit", "run", "map_app_temperature.py"])

with col2:
    if st.button("Alert Graphic"):
        st.info("Coming soon!")
    if st.button("Weekend Forecast"):
        st.info("Coming soon!")

st.markdown("---")
st.caption("Developed by Maldives Meteorological Service")
