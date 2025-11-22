import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# --- 0. FILE PATHS AND BASE64 CONVERSION ---
# ⚠️ IMPORTANT: Ensure these files exist in the same directory as this script,
# or adjust the paths accordingly.
MAP_FILE_PATH = "maldives_map.jpg"
# CORRECTED PATH: Using the uploaded emblem file name
EMBLEM_FILE_PATH = "image_7b055b.png" 

# Font paths (assuming they exist in the specified subfolder 'static/fonts/')
# Ensure these files are present to avoid errors.
FARUMA_FONT = "static/fonts/Faruma.ttf"
MVLHOHI_FONT = "static/fonts/Mvlhohi bold.ttf"


def get_asset_base64_uri(path):
    """Converts a local file (image or font) to a Base64 Data URI."""
    if not os.path.exists(path):
        # Using a default error image for demonstration, but you must supply the files.
        st.error(f"❌ Error: Required file not found at path: **{path}**")
        return None
    try:
        with open(path, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
            if path.lower().endswith(('.png', '.gif', '.webp')):
                mime_type = 'image/png' 
            elif path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = 'image/jpeg'
            elif path.lower().endswith(('.ttf', '.otf', '.woff', '.woff2')):
                mime_type = 'font/ttf' 
            else:
                mime_type = 'application/octet-stream'
            return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        st.error(f"❌ Error reading or encoding file **{path}**: {e}")
        return None

# Convert all image assets to Base64
MAP_IMAGE_DATA_URI = get_asset_base64_uri(MAP_FILE_PATH)
EMBLEM_IMAGE_DATA_URI = get_asset_base64_uri(EMBLEM_FILE_PATH)


# --- 1. PAGE CONFIG and STYLING ---
st.set_page_config(
    page_title="Viber Forecast Tool",
    page_icon="📱",
    layout="wide"
)

# 🚀 AGGRESSIVE TOP-SPACE REMOVAL: Uses negative margin to pull content up.
st.markdown("""
    <style>
    /* Targets the main content block container */
    .block-container {
        padding-top: 0rem; /* Remove default top padding */
        margin-top: -50px; /* Pull the content aggressively up into the default header area */
        max-width: 100%; /* Ensure wide layout is respected */
    }
    /* Targets the inner block that contains the components to pull it up */
    .css-1r6bpt { 
        padding-top: 0; 
    }
    </style>
""", unsafe_allow_html=True)


# --- 2. EMBEDDED HTML/CSS/JS GENERATOR ---

if any(uri is None for uri in [MAP_IMAGE_DATA_URI, EMBLEM_IMAGE_DATA_URI]):
    st.warning("Please resolve the file path errors for the images listed above before running the tool.")
    st.stop()


# Define the massive HTML/CSS/JS block using f-string and triple quotes
HTML_GENERATOR = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Maldives Weather Forecast Board (Full Editor & Post)</title>

<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<style>
    /* Add CSS variables for flexible control */
    :root {{
    }}

    /* --- Base layout and fonts --- */
    body {{
        font-family: Arial, sans-serif;
        background-color: #eef3f7;
        margin: 0;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    
    /* ========================================
    *** FONT DEFINITIONS ***
    ======================================== */
    @font-face {{
        font-family: 'Faruma';
        src: url('{FARUMA_FONT}') format('truetype');
        font-weight: normal;
    }}
    @font-face {{
        font-family: 'Mvlhohi-Bold';
        src: url('{MVLHOHI_FONT}') format('truetype');
        font-weight: bold;
    }}

    /* --- EDITOR STYLES --- */
    .editor-container {{
        width: 100%;
        max-width: 650px; 
        background: #ffffff;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-top: 5px solid #004d99;
    }}
    .editor-container h2 {{ margin-top: 0; color: #004d99; }}
    .datetime-group {{ display: flex; gap: 20px; margin-bottom: 10px; }}
    .datetime-group .input-item {{ flex: 1; }}
    
    label {{ display: block; font-weight: bold; color: #004d99; margin-bottom: 4px; }}
    
    /* Global Textarea/Input Styling */
    textarea, input[type="date"], select {{ width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; box-sizing: border-box; }}
    
    /* Default forecast textareas (Fixed height, standard) */
    .forecast-textarea {{ height: 50px; resize: vertical; }}
    
    /* Advisory Textareas (Auto-resizing) */
    .advisory-textarea {{ 
        min-height: 25px; /* Ensures minimum one-line height */
        height: auto; 
        overflow-y: hidden; /* Hides scrollbar */
        resize: none; 
    }}

    button {{ background-color: #004d99; color: white; border: none; border-radius: 6px; padding: 10px 16px; font-size: 15px; cursor: pointer; margin-top: 8px; width: 49%; box-sizing: border-box; }}
    button:nth-child(even) {{ margin-left: 1%; }}
    button:hover {{ background-color: #0066cc; }}

    /* --- POST PREVIEW STYLES --- */
    .weather-post-container {{
        width: 100%;
        max-width: 650px; 
        background-color: #ffffff; 
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        border-radius: 12px;
        padding: 20px 0; 
        display: flex;
        flex-direction: row; 
        gap: 15px; 
        align-items: stretch; 
        overflow: hidden;
    }}

    /* --- Map area (FIXED WIDTH, DYNAMIC HEIGHT) --- */
    .map-area {{
        flex: 0 0 120px; 
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0; 
        background-color: #ffffff; 
        position: relative; 
    }}
    .map-area img {{
        width: 100%;
        max-width: 100%; 
        height: auto; 
        object-fit: contain; 
        border-radius: 0;
        box-shadow: none;
        padding-left: 10px; 
    }}

    /* --- Content area (Right side) --- */
    .post-content-area {{
        flex: 1; 
        background-color: #ffffff;
        border-radius: 10px;
        padding: 0; 
        display: flex;
        flex-direction: column; 
    }}

    /* --- Advisory section (Base style) --- */
    .advisory-section {{
        background-color: #fffde7; 
        border-radius: 8px; /* Added: Slightly more rounded */
        margin: 5px 0 5px 0; 
        padding: 5px 15px; /* Adjusted padding: 5px top/bottom, 15px left/right */
        display: none; 
        overflow: hidden; 
    }}
    
    /* --- Advisory Red Styling (From user request) --- */
    .red-advisory-style {{
        background-color: #b30000; /* Darker, solid red background */
        border: none; /* Removed the border to make it a solid block */
    }}
    
    .red-advisory-style .advisory-dv p, 
    .red-advisory-style .advisory-dv span,
    .red-advisory-style .advisory-en p, 
    .red-advisory-style .advisory-en span {{
        color: white !important; 
        font-weight: bold; /* Added: Makes the text bold */
    }}
    
    .advisory-en p, .advisory-dv p {{
        font-size: 0.95em;
        margin: 0; /* Ensures no extra vertical space around text */
        line-height: 1.4em;
        display: block; 
        width: 100%;
    }}
    
    .advisory-en p {{ text-align: left; }}

    .advisory-dv p {{
        direction: rtl;
        text-align: right;
        font-family: 'Faruma', Arial, sans-serif;
    }}

    /* ========================================
    *** FORECAST SECTIONS ***
    ======================================== */
    .bilingual-vertical-sections {{
        flex: 1; 
        display: flex;
        flex-direction: column; 
        padding: 0 15px 0 25px; 
        padding-top: 20px; 
    }}
    
    .section-top-header {{
        text-align: center;
        padding: 5px 0; 
        margin-bottom: 0px; 
        border-radius: 8px 0 0 0;
    }}

    .dhivehi-block-header {{ border-bottom: 4px solid #004d99; background-color: #e0f2f7; margin-top: 0; }}
    .english-block-header {{ border-bottom: 4px solid #004d99; background-color: #e0f2f7; margin-top: 5px; }}

    .dhivehi-header-title {{
        font-size: 1.7em; color: #004d99; margin: 0; direction: rtl;
        font-family: 'Faruma', Arial, sans-serif; 
    }}

    .english-header-title {{
        font-size: 1.5em; color: #004d99; font-weight: bold; margin: 0; letter-spacing: 1px;
    }}
    
    .dhivehi-header-date {{
        font-size: 1.05em; font-weight: bold; color: #333; margin-top: 0; direction: rtl;
        font-family: 'Faruma', Arial, sans-serif; 
    }}
    
    .english-header-date {{ font-size: 1.05em; font-weight: bold; color: #333; margin-top: 0; }}
    
    .forecast-item {{ margin-bottom: 6px; }}
    .forecast-line {{ font-size: 0.95em; line-height: 1.4; margin: 0; }}
    
    .english-section .forecast-line {{ text-align: left; }}

    .dhivehi-section .forecast-line {{
        text-align: right; direction: rtl; font-family: 'Faruma', Arial, sans-serif; 
    }}

    .english-section {{ padding-top: 5px; }}
    
    /* ========================================
    *** FOOTER STYLES ***
    ======================================== */
    .footer {{
        display: flex; align-items: center; justify-content: space-between; 
        padding: 10px 15px 10px 25px; background-color: #e0f2f7;
        border-top: 1px solid #004d99; font-size: 13px; margin-top: auto; 
        border-radius: 0 0 0 8px;
    }}

    .footer-left {{ 
        display: flex; 
        align-items: center; 
        gap: 10px; 
        flex-grow: 1; 
    }}
    .footer-left span {{
        font-weight: bold; color: #004d99; font-size: 12px; white-space: nowrap; 
    }}

    .footer-center {{
        flex-grow: 1; 
        text-align: center;
    }}
    .footer-center img {{ height: 28px; width: auto; }}
    
    .footer-right {{
        display: flex; align-items: center; gap: 10px;
        font-family: 'Faruma', Arial, sans-serif; color: #004d99; 
        white-space: nowrap; font-size: 13px; padding-right: 0; 
        justify-content: flex-end;
    }}

    .social-icons {{ display: flex; gap: 4px; }}
    .social-icons svg {{ width: 18px; height: 18px; transition: transform 0.2s ease, opacity 0.2s ease; cursor: pointer; }}
    .icon-link:hover svg {{ transform: scale(1.2); opacity: 0.8; }}
</style>
</head>
<body>

<div class="editor-container">
    <h2>📝 Daily Forecast Editor</h2>
    
    <div class="datetime-group">
        <div class="input-item">
            <label for="date-input">Date</label>
            <input type="date" id="date-input" value="2025-11-10" onchange="updatePost()">
        </div>
        <div class="input-item">
            <label for="time-select">Valid Until Time (hrs)</label>
            <select id="time-select" onchange="updatePost()">
            </select>
        </div>
        <div class="input-item">
            <label for="forecast-period">Forecast Period</label>
            <select id="forecast-period" onchange="updatePost()">
                <option value="today">Today's Weather</option>
                <option value="tonight">Tonight's Weather</option>
            </select>
        </div>
    </div>
    
    <div class="input-group">
        <label for="adv-en">⚠️ Advisory (English)</label>
        <textarea id="adv-en" class="advisory-textarea" oninput="autoSizeTextarea(this); updatePost()">All are advised to be cautious.</textarea>
    </div>
    <div class="input-group">
        <label for="adv-dv">⚠️ Advisory (Dhivehi)</label>
        <textarea id="adv-dv" class="advisory-textarea" oninput="autoSizeTextarea(this); updatePost()">ހުރިހާ ފަރާތްތަކުންވެސް ސަމާލުވުން އެދެމެވެ.</textarea>
    </div>

    <div class="input-group">
        <label for="wx-en">Weather (English)</label>
        <textarea id="wx-en" class="forecast-textarea" oninput="updatePost()">Scattered showers with a few thunderstorms are expected over the country.</textarea>
    </div>
    <div class="input-group">
        <label for="wx-dv">Weather: (Dhivehi)</label>
        <textarea id="wx-dv" class="forecast-textarea" oninput="updatePost()"> މުޅި ރާއްޖެއަށް ވިއްސާރަކުރުން އެކަށީގެންވޭ</textarea>
    </div>
    <div class="input-group">
        <label for="wind-en">Wind (English)</label>
        <textarea id="wind-en" class="forecast-textarea" oninput="updatePost()"> W to NW at 10 - 20 knots, gusting 45 knots during showers.</textarea>
    </div>
    <div class="input-group">
        <label for="wind-dv">Wind (Dhivehi)</label>
        <textarea id="wind-dv" class="forecast-textarea" oninput="updatePost()"> ހުޅަނގު-އުތުރުން 10-20 ނޮޓަށް، ވިއްސާރާގައި 45 ނޮޓަށް ބާރުވާނެ.</textarea>
    </div>
    <div class="input-group">
        <label for="sea-en">Sea (English)</label>
        <textarea id="sea-en" class="forecast-textarea" oninput="updatePost()">Generally rough in southern atolls and moderate becoming rough during showers elsewhere.</textarea>
    </div>
    <div class="input-group">
        <label for="sea-dv">Sea (Dhivehi)</label>
        <textarea id="sea-dv" class="forecast-textarea" oninput="updatePost()"> ދެކުނުގެ އަތޮޅުތަކަށް އާދައިގެ ވަރަކަށް، އެހެން ހިސާބުތަކަށް ގަދަވާނެ.</textarea>
    </div>
    <div class="input-group">
        <label for="wave-en">Wave Height (English)</label>
        <textarea id="wave-en" class="forecast-textarea" oninput="updatePost()">: 4–7 feet.</textarea>
    </div>
    <div class="input-group">
        <label for="wave-dv">Wave Height (Dhivehi)</label>
        <textarea id="wave-dv" class="forecast-textarea" oninput="updatePost()"> 4-7 ފޫޓު.</textarea>
    </div>

    <button onclick="updatePost()">🔄 Update Preview</button>
    <button onclick="downloadPost()">⬇️ Download Image</button>
</div>

<div class="weather-post-container" id="weather-post">
    
    <div class="map-area" id="map-area">
        <img src="{MAP_IMAGE_DATA_URI}" alt="Maldives Map" crossorigin="anonymous">
    </div>

    <div class="post-content-area" id="post-content-area">

        <div class="bilingual-vertical-sections" id="bilingual-sections">
            
            <div class="section-top-header dhivehi-block-header">
                <h2 class="dhivehi-header-title" id="dv-header-title"></h2>
                <p class="dhivehi-header-date" id="dv-header-date"></p>
            </div>
            
            <div class="advisory-section red-advisory-style" id="adv-dv-section">
                <div class="advisory-dv" id="adv-dv-container"></div>
            </div>

            <div class="dhivehi-section">
                <div class="forecast-item" id="wx-dv-container"></div>
                <div class="forecast-item" id="wind-dv-container"></div>
                <div class="forecast-item" id="sea-dv-container"></div>
                <div class="forecast-item" id="wave-dv-container"></div>
            </div>
            
            <div class="section-top-header english-block-header">
                <h2 class="english-header-title" id="en-header-title"></h2>
                <p class="english-header-date" id="en-header-date"></p>
            </div>

            <div class="advisory-section red-advisory-style" id="adv-en-section">
                <div class="advisory-en" id="adv-en-container"></div>
            </div>

            <div class="english-section">
                <div class="forecast-item" id="wx-en-container"></div>
                <div class="forecast-item" id="wind-en-container"></div>
                <div class="forecast-item" id="sea-en-container"></div>
                <div class="forecast-item" id="wave-en-container"></div>
            </div>

        </div>

        <footer class="footer">
            <div class="footer-left">
                <span>Maldives Meteorological Service</span>
            </div>

            <div class="footer-center">
                <img src="{EMBLEM_IMAGE_DATA_URI}" alt="Maldives Emblem" crossorigin="anonymous">
            </div>

            <div class="footer-right">
                މޯލްޑިވްސް މީޓިއޮރޮލޮޖިކަލް ސަރވިސް
                <div class="social-icons">
                    <a href="https://www.viber.com" target="_blank" class="icon-link" title="Viber">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">
                            <rect width="240" height="240" rx="48" ry="48" fill="#7360f2"/>
                            <path fill="#fff" d="M168 155c-7-7-43-31-50-35s-11-5-18 2-21 26-27 31-10 7-18 3-36-14-68-43S-47 71-53 63-55 49-49 44s14-13 20-19 2-12-2-18S-61-5-67-12s-9-7-15-7-14 0-22 11S-133 5-133 40s33 75 38 80 64 95 153 134c55 25 78 27 95 24s47-21 53-33 6-20 6-23-2-3-8-10z" transform="translate(132 60) scale(0.55)"/>
                            <path fill="#fff" d="M141.7 86.2c-2.5 0-4.5 2-4.5 4.5s2 4.5 4.5 4.5c12.9 0 23.4 10.5 23.4 23.4 0 2.5 2 4.5 4.5 4.5s4.5-2 4.5-4.5c.1-17.8-14.5-32.4-32.4-32.4zm.6-22.7c-2.5 0-4.5 2-4.5 4.5s2 4.5 4.5 4.5c25.5 0 46.3 20.8 46.3 46.3 0 2.5 2 4.5 4.5 4.5s4.5-2 4.5-4.5c0-30.5-24.8-55.3-55.3-55.3zm-3.3-22.5c-2.5 0-4.5 2-4.5 4.5s2 4.5 4.5 4.5c37.8 0 68.6 30.8 68.6 68.6 0 2.5 2 4.5 4.5 4.5s4.5-2 4.5-4.5c.1-42.7-34.8-77.6-77.6-77.6z"/>
                        </svg>
                    </a>
                    <a href="https://x.com/" target="_blank" class="icon-link" title="X (Twitter)">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <path fill="#000000" d="M18.244 2.25h3.308l-7.227 8.26L22 21.75h-5.956l-4.67-6.104L6.06 21.75H2.75l7.73-8.839L2 2.25h6.056l4.215 5.624L18.244 2.25zM17.208 19.59h1.833L7.08 4.33H5.12l12.088 15.26z"/>
                        </svg>
                    </a>
                    <a href="https://facebook.com/" target="_blank" class="icon-link" title="Facebook">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                            <path fill="#1877F2" d="M512 256C512 114.6 397.4 0 256 0S0 114.6 0 256c0 128.5 94.1 235.1 216 253.4V330h-65v-74h65v-56.4c0-64.4 38.3-100 96.8-100 28.1 0 57.6 5 57.6 5v63h-32.4c-31.9 0-41.9 19.8-41.9 40v48.4h71l-11.3 74h-59.7v179.4C417.9 491.1 512 384.5 512 256z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </footer>
    </div>
</div>

<script>
    // Dhivehi Month Names (Standard)
    const dhivehiMonths = [
        "ޖެނުއަރީ", "ފެބުރުއަރީ", "މާރިޗު", "އެޕްރީލް", "މޭ", "ޖޫން",
        "ޖުލައި", "އޮގަސްޓު", "ސެޕްޓެމްބަރު", "އޮކްޓޯބަރު", "ނޮވެމްބަރު", "ޑިސެމްބަރު"
    ];

    // Helper functions 
    function getMonthName(monthIndex) {{
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        return months[monthIndex];
    }}
    
    function getDhivehiMonthName(monthIndex) {{ return dhivehiMonths[monthIndex]; }}

    function getDaySuffix(day) {{
        if (day > 3 && day < 21) return 'th'; 
        switch (day % 10) {{
            case 1:  return "st";
            case 2:  return "nd";
            case 3:  return "rd";
            default: return "th";
        }}
    }}
    
    function updateForecastItem(lang, id, heading, content) {{
        const container = document.getElementById(`${{id}}-${{lang}}-container`);
        const contentText = content || document.getElementById(`${{id}}-${{lang}}`).value;
        const section = document.getElementById(`${{id}}-${{lang}}-section`); 
        
        const isContentEmpty = contentText.trim() === '';
        
        if (section) {{ section.style.display = isContentEmpty ? 'none' : 'block'; }}

        let line = '';
        if (!isContentEmpty || id !== 'adv') {{ 
            line = `<p class="forecast-line">`;
            
            if (lang === 'en') {{
                let color = id === 'adv' ? 'white' : '#004d99'; 
                let headingText = id === 'adv' ? 'Advisory' : heading.toUpperCase();
                
                line += `<span style="font-weight: bold; color: ${{color}}; margin-right: 5px;">${{headingText}}:</span>${{contentText}}`;
            }} else if (lang === 'dv') {{
                let color = id === 'adv' ? 'white' : '#004d99'; 
                let dvHeadingText;
                if (id === 'adv') dvHeadingText = ' އިރުޝާދު:'
                else if (id === 'wx') dvHeadingText = 'މޫސުން:'
                else if (id === 'wind') dvHeadingText = 'ވައި: '
                else if (id === 'sea') dvHeadingText = 'ކަނޑު:'
                else if (id === 'wave') dvHeadingText = 'ރާޅުގެ އުސްމިން:'
                else return;

                line += `<span style="font-family: 'Faruma'; font-weight: bold; color: ${{color}}; margin-left: 5px;">${{dvHeadingText}}</span> ${{contentText}}`;
            }}
            
            line += `</p>`;
        }}
        
        container.innerHTML = line;
    }}

    /* === Auto-size Textarea === */
    function autoSizeTextarea(element) {{
        element.style.height = 'auto'; // Reset height to recalculate
        // Set height to scrollHeight (content height)
        element.style.height = element.scrollHeight + 'px'; 
    }}
    /* ==================================== */

    /* === Dynamic Height Adjustment (for Map) === */
    function adjustMapHeight() {{
        const contentArea = document.getElementById('post-content-area');
        const mapArea = document.getElementById('map-area');

        if (!contentArea || !mapArea) return;

        // Get the actual computed height of the content area 
        const contentHeight = contentArea.offsetHeight;

        // Apply that height to the map container. 
        mapArea.style.height = `${{contentHeight}}px`;
    }}
    /* ==================================== */

    function updatePost() {{
        const dateInputEl = document.getElementById('date-input');
        const timeInputEl = document.getElementById('time-select');
        const periodEl = document.getElementById('forecast-period');
        
        if (!dateInputEl || !timeInputEl || !periodEl) return; 

        const dateInput = dateInputEl.value;
        const timeInput = timeInputEl.value;
        const period = periodEl.value;

        // 1. Dynamic Titles
        let enHeader, dvHeader;
        if (period === 'today') {{
            enHeader = "Today's Weather";
            dvHeader = "މިއަދުގެ މޫސުން";
        }} else {{
            enHeader = "TONIGHT'S WEATHER";
            dvHeader = "މިރޭގެ މޫސުން";
        }}

        // 2. Dynamic Time/Date Formatting
        const dateParts = dateInput.split('-');
        const date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
        const day = date.getDate();
        const monthIndex = date.getMonth();
        const monthEn = getMonthName(monthIndex);
        const monthDv = getDhivehiMonthName(monthIndex);
        const year = date.getFullYear();
        const time = timeInput ? timeInput.replace(':', '') : '0000';
        const suffix = getDaySuffix(day);

        const forecastDateEn = `Valid until ${{time}} hrs, ${{day}}${{suffix}} ${{monthEn}} ${{year}}`;
        const forecastDateDv = `${{year}} ${{monthDv}} ${{day}} ވަނަ ދުވަހުގެ ${{time}} އާ ހަމައަށް`;
        
        // 3. Update the new header fields
        document.getElementById('dv-header-title').textContent = dvHeader;
        document.getElementById('dv-header-date').textContent = forecastDateDv;
        document.getElementById('en-header-title').textContent = enHeader;
        document.getElementById('en-header-date').textContent = forecastDateEn;

        // 4. Update Input Fields 
        updateForecastItem('en', 'adv', 'Advisory', document.getElementById('adv-en').value);
        updateForecastItem('dv', 'adv', 'އިރުޝާދު', document.getElementById('adv-dv').value);

        updateForecastItem('en', 'wx', 'Weather', document.getElementById('wx-en').value);
        updateForecastItem('en', 'wind', 'Wind', document.getElementById('wind-en').value);
        updateForecastItem('en', 'sea', 'Sea', document.getElementById('sea-en').value);
        updateForecastItem('en', 'wave', 'Wave height', document.getElementById('wave-en').value);

        updateForecastItem('dv', 'wx', 'މޫސުން', document.getElementById('wx-dv').value);
        updateForecastItem('dv', 'wind', 'ވައި', document.getElementById('wind-dv').value);
        updateForecastItem('dv', 'sea', 'ކަނޑު ', document.getElementById('sea-dv').value);
        updateForecastItem('dv', 'wave', 'ރާޅުގެ އުސްމިން', document.getElementById('wave-dv').value);

        // 5. Adjust map height to match the (now correctly-sized) content area
        adjustMapHeight(); 
    }}

    function populateTimeSelect() {{
        const select = document.getElementById('time-select');
        if (!select) return; 
        select.innerHTML = ''; 
        for (let h = 0; h < 24; h++) {{
            const hour = String(h).padStart(2, '0');
            const time = `${{hour}}:00`;
            const option = document.createElement('option');
            option.value = time;
            option.textContent = time;
            select.appendChild(option);
        }}
        select.value = "18:00"; 
    }}

    function downloadPost() {{
        const element = document.getElementById('weather-post');
        if (!element) {{
             // Use console.error instead of alert
             console.error("❌ Preview element not found. Please try refreshing the page.");
             return;
        }}

        // Ensure the height is correct before capturing
        adjustMapHeight();

        html2canvas(element, {{ 
            scale: 2, 
            useCORS: true,
            allowTaint: false, 
            logging: false, 
            imageTimeout: 15000 
        }}).then(canvas => {{
            const link = document.createElement('a');
            const dateVal = document.getElementById('date-input').value.replace(/-/g, '_');
            const timeVal = document.getElementById('time-select').value.replace(':', '');
            
            link.download = `Maldives_Forecast_${{dateVal}}_${{timeVal}}.png`;
            link.href = canvas.toDataURL('image/png');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}).catch(err => {{
            console.error("Image generation failed:", err);
            // WARNING for the user
            // Use a custom message display instead of alert
            const errorBox = document.createElement('div');
            errorBox.style.cssText = "position: fixed; top: 10px; right: 10px; background: #f8d7da; color: #721c24; padding: 10px; border: 1px solid #f5c6cb; border-radius: 5px; z-index: 1000;";
            errorBox.textContent = "❌ Download Failed! If the preview looks fine, try updating the preview first, then downloading. If assets are missing, check the browser console for errors.";
            document.body.appendChild(errorBox);
            setTimeout(() => document.body.removeChild(errorBox), 5000);
        }});
    }}

    function initializeEditor() {{
        populateTimeSelect();
        
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const today = `${{year}}-${{month}}-${{day}}`;

        const dateInput = document.getElementById('date-input');
        if (dateInput) {{ dateInput.value = today; }}
        
        // Auto-size the advisory textareas on initial load
        document.querySelectorAll('.advisory-textarea').forEach(autoSizeTextarea);
        
        updatePost();
    }}
    
    // Initialize the script after a brief timeout to ensure DOM is fully loaded
    (function() {{
        setTimeout(initializeEditor, 100); 
    }})();

</script>
</body>
</html>
"""

# --- 3. STREAMLIT RENDERING ---

st.markdown("<h2 style='text-align:center; color: #004d99;'>📱 Viber / Social Media Post Generator</h2>", unsafe_allow_html=True)

# Render the entire HTML/CSS/JS generator
components.html(
    HTML_GENERATOR,
    height=1600,
    scrolling=True

)
