import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Forecasters' Tools", layout="centered")

st.title("Forecasters' Tools")

st.write("Select a tool to launch:")

# Define the path to the map script
rainfall_script_path = "map_app_rainfall.py"

col1, col2 = st.columns(2)

with col1:
    if st.button("Rainfall Outlook Map"):
        # Check if the map script exists before trying to run it
        if os.path.exists(rainfall_script_path):
            st.info(f"Launching **Rainfall Outlook Map**... (A new window/tab should open shortly)")
            # Launches the map script as a new Streamlit app
            subprocess.Popen(["streamlit", "run", rainfall_script_path])
        else:
            st.error(f"Error: The required file '{rainfall_script_path}' was not found.")

    if st.button("Temperature Outlook Map"):
        # You will need to create 'map_app_temperature.py' similarly
        # subprocess.Popen(["streamlit", "run", "map_app_temperature.py"])
        st.info("Temperature Outlook Map application not yet implemented.")

with col2:
    if st.button("Alert Graphic"):
        st.info("Coming soon!")
    if st.button("Weekend Forecast"):
        st.info("Coming soon!")

st.markdown("---")
st.caption("Developed by Maldives Meteorological Service")
