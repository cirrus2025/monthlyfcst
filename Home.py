# Home.py

import streamlit as st

st.set_page_config(
    page_title="Forecasters' Tools",
    page_icon="🗺️",
    layout="wide"
)

# Inject Custom CSS for the Blue Header Bar and Button Styling
st.markdown(
    """
    <style>
    /* CUSTOM BLUE HEADER BAR */
    .main-header {
        background-color: #1E90FF;
        color: white;
        padding: 10px 0;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Push main content down to account for the fixed header */
    .st-emotion-cache-1g8i5u7, .st-emotion-cache-6qob1r, .st-emotion-cache-1y4pm5r {
        padding-top: 80px; 
    }
    .logout-link {
        position: absolute;
        right: 20px;
        top: 15px;
        font-size: 14px;
        color: white;
        text-decoration: none;
    }
    /* CUSTOM BUTTON STYLING */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-bottom: 5px; 
    }
    .stButton > button {
        width: 250px;
        height: 40px;
        margin: 5px 0;
        font-size: 16px;
        border: 1px solid #1E90FF; 
        color: #1E90FF;
        background-color: white;
    }
    .st-emotion-cache-1629p8f { /* Hide hamburger menu icon */
        display: none !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">Forecasters\' Tools <a href="#" class="logout-link">Log Out</a></div>', unsafe_allow_html=True)

# Main Page Content (Below the Header)
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown("<h3 style='text-align: center; margin-top: 20px;'>Select a Tool from the Sidebar Menu on the Left</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Placeholder buttons
    st.button("Tide Chart")
    st.button("Alert Graphic")
    st.button("Forecast Graphic")
    st.button("Weekend Forecast")
    st.button("Satellite Image")
    st.button("Forecast App (Testing)")
    st.button("Weather News")

    st.markdown("---")
    st.info("Your custom map tools are now available as **'Rainfall Outlook'** and **'Temperature Outlook'** in the Streamlit sidebar menu.")