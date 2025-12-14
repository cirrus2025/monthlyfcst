# pages/Temperature_Outlook.py

import streamlit as st # <--- Streamlit imported first
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import io
import warnings
import os

# --- HIDES THE STREAMLIT HEADER/MENU ICONS (Applied here) ---
hide_streamlit_header_css = """
<style>
.stApp header {
    display: none;
}
</style>
"""
st.markdown(hide_streamlit_header_css, unsafe_allow_html=True)
# ------------------------------------------------------------


st.title("🌡️ Temperature Outlook Map Generator")
st.markdown("Use the sidebar to adjust the probabilities for each Atoll.")


# --- Ignore harmless warnings ---
warnings.filterwarnings("ignore", message="missing ScriptRunContext")
warnings.filterwarnings("ignore", message="not compatible with tight_layout")

# --- Corrected Shapefile Path for Streamlit Cloud ---
shp = 'data/Atoll_boundary2016.shp'
shp_filename = os.path.basename(shp)
# --- End Path Correction ---

# --- Load shapefile ---
try:
    if not os.path.exists(shp):
        st.error(f"Error: Shapefile not found at the expected path: `{shp}`. Please ensure `{shp_filename}` is in the `data` folder.")
        st.stop()

    gdf = gpd.read_file(shp).to_crs(epsg=4326)
except Exception as e:
    st.error(f"Error loading shapefile: {e}. Please check the path and ensure required libraries (like `fiona`) are in `requirements.txt`.")
    st.stop()

bbox = box(71, -1, 75, 7.5)
gdf = gdf[gdf.intersects(bbox)]

# --- Default probabilities (Keep as provided) ---
default_probs = {
    'Haa Alifu Atoll': 65, 'Haa Dhaalu Atoll': 70, 'Noonu Atoll': 68, 'Baa Atoll': 72,
    'Lhaviyani Atoll': 65, 'Raa Atoll': 68, 'Shaviyani Atoll': 70, 'Kaafu Atoll': 75,
    'Alifu Alifu Atoll': 65, 'Alifu Dhaalu Atoll': 70, 'Vaavu Atoll': 68, 'Meemu Atoll': 62,
    "Male' City": 75, 'Faafu Atoll': 50, 'Dhaalu Atoll': 52, 'Thaa Atoll': 45,
    'Laamu Atoll': 55, 'Gaafu Alifu Atoll': 64, 'Gaafu Dhaalu Atoll': 62, 
    'Gnaviyani Atoll': 65, 'Seenu Atoll': 75
}

# --- Colormaps for categories ---
category_colors = {
    "Above Normal": ['#ffffff', '#ffed5c', '#ffb833', '#ff8f00', '#f15c00', '#e20000'],
    "Normal": ['#ffffff', '#b2df8a', '#6dc068', '#2d933e', '#006a2e', '#014723'],
    "Below Normal": ['#ffffff', '#c8c8ff', '#a6b6ff', '#8798f0', '#6c7be0', '#3c4fc2']
}

# --- Sidebar UI ---
st.sidebar.header("🎛️ Adjust Atoll Probabilities & Categories")
custom_title = st.sidebar.text_input(
    "📝 Map Title:",
    value="Maximum Temperature Outlook for OND 2025"
)

# User inputs per atoll
user_probs = {}
user_categories = {}
for atoll, default in default_probs.items():
    st.sidebar.markdown(f"**{atoll}**")
    user_probs[atoll] = st.sidebar.slider(f"{atoll} Probability", 0, 100, default, step=1, key=f"prob_{atoll}")
    user_categories[atoll] = st.sidebar.selectbox(
        f"{atoll} Category",
        ["Above Normal", "Normal", "Below Normal"],
        index=1,
        key=f"cat_{atoll}"
    )

# Map user inputs to GeoDataFrame
gdf_display = gdf.copy()
gdf_display['prob'] = gdf_display['Name'].map(user_probs)
gdf_display['category'] = gdf_display['Name'].map(user_categories)

# --- Colormap setup ---
bins = [0, 35, 45, 55, 65, 75, 100]
norm = BoundaryNorm(bins, ncolors=len(bins)-1, clip=True)
tick_positions = [35, 45, 55, 65, 75]
tick_labels = ['35', '45', '55', '65', '75']

# --- Plot map ---
with st.spinner('Generating map...'):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot each atoll individually according to its category
    for cat, cmap_list in category_colors.items():
        subset = gdf_display[gdf_display['category'] == cat]
        if not subset.empty:
            cmap = ListedColormap(cmap_list)
            subset.plot(
                column='prob', cmap=cmap, norm=norm,
                edgecolor='black', linewidth=0.5, ax=ax
            )

    # Map settings
    ax.set_xlim(71, 75)
    ax.set_ylim(-1, 7.5)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title(custom_title, fontsize=16)
    ax.set_xticks([71, 72, 73, 74, 75])
    ax.set_xticklabels(["71°E", "72°E", "73°E", "74°E", "75°E"])

    # --- Colorbars ---
    width = "40%"
    height = "2.5%"
    start_x = 0.05
    start_y = 0.1
    spacing = 0.09

    def make_cb(ax, cmap, title, offset):
        cax = inset_axes(ax, width=width, height=height, loc='lower left',
                          bbox_to_anchor=(start_x, start_y + offset, 1, 1),
                          bbox_transform=ax.transAxes, borderpad=0)
        cb = colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=bins,
                                    ticks=tick_positions, spacing='uniform', orientation='horizontal')
        cb.set_ticklabels(tick_labels)
        cax.set_title(title, fontsize=10, pad=6)
        cb.ax.tick_params(labelsize=9, pad=2)

    # Add all three category colorbars
    make_cb(ax, ListedColormap(category_colors["Above Normal"]), "Above Normal", 2 * spacing)
    make_cb(ax, ListedColormap(category_colors["Normal"]), "Normal", spacing)
    make_cb(ax, ListedColormap(category_colors["Below Normal"]), "Below Normal", 0)

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    # --- Display map ---
    st.pyplot(fig)

    # --- Download button ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    st.download_button(
        label="💾 Download Map Image (PNG)",
        data=buf,
        file_name="Temperature_Outlook_Map.png",
        mime="image/png"
    )

st.success("✅ Map displayed. **Changes in the sidebar update the map automatically.**")
