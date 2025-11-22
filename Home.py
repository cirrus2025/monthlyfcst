# Home.py

import streamlit as st

# 1. Set the page configuration
st.set_page_config(
    page_title="Forecasters' Tools",
    page_icon="🗺️",
    layout="wide"
)

# 2. Inject Custom CSS for the Blue Header and Centered Buttons
# This CSS attempts to mimic the exact look of your image.
st.markdown(
    """
    <style>
    /* ------------------------------------------- */
    /* 1. CUSTOM BLUE HEADER BAR */
    /* Fix the header to the top of the screen */
    .main-header {
        background-color: #1E90FF; /* Bright Blue */
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
    
    /* Optional: Small 'Log Out' text on the right */
    .logout-link {
        position: absolute;
        right: 20px;
        top: 15px;
        font-size: 14px;
        color: white;
        text-decoration: none;
    }
    /* ------------------------------------------- */


    /* 2. CUSTOM BUTTON STYLING (Centered and Stacked) */
    /* Center the button containers */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-bottom: 5px; 
    }
    
    /* Style the actual button elements */
    .stButton > button {
        width: 250px;
        height: 40px;
        margin: 5px 0;
        font-size: 16px;
        border: 1px solid #1E90FF; 
        color: #1E90FF;
        background-color: white;
    }
    .stButton > button:hover {
        background-color: #1E90FF;
        color: white;
    }

    /* Hide the default Streamlit footer/menu icon */
    .st-emotion-cache-1g8i5u7, .st-emotion-cache-6qob1r, .st-emotion-cache-1y4pm5r {
        padding-top: 80px; /* Adjust top padding for fixed header */
    }
    .st-emotion-cache-1629p8f { /* Target the hamburger menu button */
        display: none !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 3. Custom Header HTML to be displayed
st.markdown('<div class="main-header">Forecasters\' Tools <a href="#" class="logout-link">Log Out</a></div>', unsafe_allow_html=True)


# 4. Main Page Content (Below the Header)
# Use a centered column for the menu instructions and buttons
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Instruction text
    st.markdown("<h3 style='text-align: center; margin-top: 20px;'>Select a Tool from the Sidebar Menu on the Left</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # The list of buttons from your image (Note: These are placeholders)
    st.button("Tide Chart")
    st.button("Alert Graphic")
    st.button("Forecast Graphic")
    st.button("Weekend Forecast")
    st.button("Satellite Image")
    st.button("Forecast App (Testing)")
    st.button("Weather News")
    
    st.markdown("---")
    st.info("Your custom map tools are now fully functional and accessible as **'Rainfall Outlook'** and **'Temperature Outlook'** in the Streamlit sidebar menu.")
