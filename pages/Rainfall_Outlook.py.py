# --- NEW: Inject CSS to hide the top-right menu/editing tools ---
st.markdown("""
<style>
/* Targets the main container of the toolbar */
.stApp header {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------
