# Home.py
# HIDES THE STREAMLIT HEADER/MENU ICONS
hide_streamlit_header_css = """
<style>
.stApp header {
    display: none;
}
</style>
"""
st.markdown(hide_streamlit_header_css, unsafe_allow_html=True)


import streamlit as st

st.set_page_config(
    page_title="Monthly Outlook Generator", 
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Monthly Outlook Generator")

st.markdown("""
Please use the navigation menu on the left to select an Outlook Map.
""")

