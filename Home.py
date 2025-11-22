# Home.py

import streamlit as st

st.set_page_config(
    page_title="Forecasters' Tools", 
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("☀️ Forecasters' Tools Dashboard")

st.markdown("""
Welcome! Use the **navigation menu on the left** to select a specific forecasting tool.
""")

st.markdown("---")

st.write("### Quick Access Tools:")

col1, col2 = st.columns(2)

with col1:
    # These tools are not separate .py files, so they are displayed here
    if st.button("Alert Graphic"):
        st.info("Alert Graphic Tool: Coming soon!")
    
with col2:
    if st.button("Weekend Forecast"):
        st.info("Weekend Forecast Tool: Coming soon!")

st.markdown("---")
st.caption("Developed by Maldives Meteorological Service")
