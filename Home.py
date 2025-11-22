# main_app.py

import streamlit as st

st.set_page_config(
    page_title="Forecasters' Tools", 
    layout="centered",
    # Set the navigation pages using the official method
    # All files in the root directory following the pattern 'pages/*.py' 
    # or the new structure (files prefixed with numbers) will appear automatically.
)

st.title("Welcome to the Forecasters' Tools Dashboard")

st.markdown("""
Welcome! Use the **navigation menu on the left** to select the specific forecasting tool you wish to launch.
""")

st.write("### Available Tools:")

# Since Streamlit automatically detects pages1_... and pages2_... 
# you just need to provide links or text for the other tools.

col1, col2 = st.columns(2)

# The Rainfall and Temperature tools are automatically handled by the file structure
with col1:
    st.markdown("* **Rainfall Outlook Map** (Available in the sidebar)")
    st.markdown("* **Temperature Outlook Map** (Available in the sidebar)")

with col2:
    # These tools are not separate .py files, so they are displayed here
    if st.button("Alert Graphic"):
        st.info("Alert Graphic Tool: Coming soon!")
    if st.button("Weekend Forecast"):
        st.info("Weekend Forecast Tool: Coming soon!")

st.markdown("---")
st.caption("Developed by Maldives Meteorological Service")
