# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import time

# # Load environment variables
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# # Validate API Key
# if not api_key:
#     st.error("❌ GEMINI_API_KEY not found in .env file")
#     st.stop()

# # Configure Gemini
# try:
#     genai.configure(api_key=api_key)
# except Exception as e:
#     st.error(f"❌ Configuration error: {str(e)}")
#     st.stop()

# # App Configuration
# st.set_page_config(
#     page_title="🌍 English ↔ Urdu AI Translator",
#     page_icon="🌐",
#     layout="centered"
# )

# # Initialize session state
# if 'direction' not in st.session_state:
#     st.session_state.direction = "auto"
# if 'last_translation' not in st.session_state:
#     st.session_state.last_translation = ""
# if 'last_output_lang' not in st.session_state:
#     st.session_state.last_output_lang = ""

# # Custom CSS for styling with Urdu font support
# st.markdown("""
# <style>
#     /* Import Urdu font */
#     @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    
#     .stTextArea textarea {
#         font-size: 16px; 
#         line-height: 1.5;
#         height: 400px !important;  /* SIGNIFICANTLY INCREASED HEIGHT */
#         background-color: #f9f9f9 !important;  /* Light gray background */
#         border: 1px solid #ddd !important;
#         border-radius: 8px !important;
#         padding: 15px !important;
#     }
#     .stTextArea textarea:focus {
#         border-color: #4CAF50 !important;
#         box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
#     }
#     .primary-button {
#         background: linear-gradient(45deg, #4CAF50, #8BC34A) !important;
#         color: white !important;
#         border: none !important;
#         padding: 0.8em 2em !important;
#         border-radius: 25px !important;
#         font-weight: bold !important;
#         transition: all 0.3s !important;
#     }
#     .primary-button:hover {
#         background: linear-gradient(45deg, #43A047, #7CB342) !important;
#         transform: scale(1.05);
#     }
#     .secondary-button {
#         background: linear-gradient(45deg, #2196F3, #21CBF3) !important;
#         color: white !important;
#     }
#     .direction-button {
#         width: 100%;
#         padding: 10px;
#         margin: 5px 0;
#         border-radius: 10px;
#         border: 2px solid #e0e0e0;
#         background-color: white;
#         text-align: center;
#         cursor: pointer;
#         transition: all 0.3s;
#         font-weight: bold;
#     }
#     .direction-button:hover {
#         background-color: #f0f8ff;
#         border-color: #4CAF50;
#     }
#     .direction-button.active {
#         background: linear-gradient(45deg, #4CAF50, #8BC34A);
#         color: white !important;
#         border-color: #4CAF50;
#     }
#     .stAlert {border-radius: 10px;}
#     .result-box {
#         background-color: #f0f8ff;
#         border-radius: 10px;
#         padding: 1.5rem;
#         margin-top: 1rem;
#         border-left: 5px solid #4CAF50;
#         font-size: 18px;
#         line-height: 1.8;
#         white-space: pre-wrap;
#     }
#     .urdu-text {
#         font-family: 'Noto Nastaliq Urdu', serif !important;
#         font-size: 22px !important;
#         line-height: 2.2 !important;
#         text-align: right !important;
#         direction: rtl !important;
#     }
#     .error-box {
#         border-left: 5px solid #FF5252 !important;
#         background-color: #ffebee !important;
#     }
#     .quote {
#         border-left: 4px solid #4CAF50;
#         padding-left: 1rem;
#         font-style: italic;
#         color: #555;
#     }
#     .footer {
#         font-size: 0.85rem;
#         text-align: center;
#         margin-top: 2rem;
#         color: #777;
#     }
#     .model-badge {
#         background: linear-gradient(45deg, #FF9800, #FF5722);
#         color: white;
#         padding: 3px 12px;
#         border-radius: 20px;
#         font-size: 0.85rem;
#         font-weight: bold;
#         display: inline-block;
#         margin-bottom: 10px;
#     }
#     .language-indicator {
#         text-align: center;
#         padding: 8px;
#         border-radius: 10px;
#         background: #e3f2fd;
#         font-weight: bold;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.title("🌍 English ↔ Urdu AI Translator")
# st.caption("Powered by Google Gemini AI • Select translation direction")

# # Model information
# st.markdown('<div class="model-badge">Using Model: Gemini 1.5 Flash (Latest)</div>', unsafe_allow_html=True)

# # Create two columns for layout
# col1, col2 = st.columns([5, 1], gap="medium")

# # Input area with SIGNIFICANTLY increased height
# with col1:
#     text = st.text_area(
#         "✍️ Enter text to translate:",
#         placeholder="Type English or Urdu text here...",
#         height=400,  # SIGNIFICANTLY INCREASED HEIGHT
#         key="input_text",
#         label_visibility="collapsed"
#     )

# # Translation direction selector
# with col2:
#     st.markdown("<div class='language-indicator'>Select Direction</div>", unsafe_allow_html=True)
    
#     # English to Urdu button
#     if st.button("English → Urdu", key="en_to_ur", 
#                  use_container_width=True, 
#                  type="primary" if st.session_state.direction == "en_to_ur" else "secondary"):
#         st.session_state.direction = "en_to_ur"
    
#     # Urdu to English button
#     if st.button("Urdu → English", key="ur_to_en", 
#                  use_container_width=True, 
#                  type="primary" if st.session_state.direction == "ur_to_en" else "secondary"):
#         st.session_state.direction = "ur_to_en"
    
#     # Auto detect button (set as default)
#     auto_active = st.session_state.direction == "auto"
#     if st.button("Auto Detect", key="auto_detect", 
#                  use_container_width=True, 
#                  type="primary" if auto_active else "secondary"):
#         st.session_state.direction = "auto"
    
#     # Show current selection
#     st.markdown(f"<div class='language-indicator'>Current: <b>{st.session_state.direction.replace('_', ' ').title()}</b></div>", 
#                 unsafe_allow_html=True)

# # Translation button
# if st.button("🚀 Translate", use_container_width=True, key="translate_btn", type="primary"):
#     if not text.strip():
#         st.warning("⚠️ Please enter text to translate")
#     else:
#         with st.spinner("🔍 Translating..."):
#             try:
#                 # Initialize model
#                 model = genai.GenerativeModel("gemini-1.5-flash")
                
#                 # Determine translation direction
#                 if st.session_state.direction == "auto":
#                     # Auto detect language
#                     urdu_chars = "اأإآءئؤپچڈڑژکگھںٹڑڈڑشصضطظعغفقثذظ"
#                     if any(char in urdu_chars for char in text):
#                         direction = "Urdu to English"
#                         output_lang = "english"
#                     else:
#                         direction = "English to Urdu"
#                         output_lang = "urdu"
#                 elif st.session_state.direction == "en_to_ur":
#                     direction = "English to Urdu"
#                     output_lang = "urdu"
#                 else:
#                     direction = "Urdu to English"
#                     output_lang = "english"
                
#                 # Create translation prompt
#                 prompt = f"""
#                 You are a professional translator. 
#                 Translate the following text from {direction} with these guidelines:
                
#                 1. Preserve original meaning and cultural context
#                 2. Keep names, technical terms, and proper nouns unchanged
#                 3. Use natural, conversational language
#                 4. Maintain original formatting (line breaks, punctuation)
#                 5. For Urdu output: Use standard Urdu script (Nastaliq) with proper diacritics
#                 6. For English output: Use standard spelling and grammar
                
#                 Text to translate:
#                 "{text}"
#                 """
                
#                 # Generate translation
#                 response = model.generate_content(
#                     prompt,
#                     generation_config=genai.types.GenerationConfig(
#                         temperature=0.1,
#                         max_output_tokens=1000,
#                         top_p=0.95
#                     )
#                 )
                
#                 # Display results
#                 st.balloons()
#                 st.subheader("✅ Translation Result")
                
#                 # Apply Urdu-specific styling if output is Urdu
#                 if output_lang == "urdu":
#                     st.markdown(f'<div class="result-box urdu-text">{response.text}</div>', unsafe_allow_html=True)
#                 else:
#                     st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
#                 # Store results
#                 st.session_state.last_translation = response.text
#                 st.session_state.last_output_lang = output_lang
                
#             except Exception as e:
#                 error_msg = str(e)
#                 if "429" in error_msg or "quota" in error_msg.lower():
#                     st.error("""
#                     ⚠️ **Translation Limit Reached**  
#                     We've exceeded the free translation quota for now. Please:
#                     - Try again after 1-2 minutes
#                     - Use shorter text
#                     - Refresh the page and retry
#                     """)
#                     st.markdown('<div class="result-box error-box">'
#                                 '🚫 Current free translation quota exhausted. '
#                                 'Service will resume shortly.</div>', 
#                                 unsafe_allow_html=True)
#                 elif "404" in error_msg or "not found" in error_msg:
#                     st.error("""
#                     ⚠️ **Model Configuration Error**
#                     The translation model is currently unavailable. Please:
#                     - Check your internet connection
#                     - Refresh the application
#                     - Contact support if issue persists
#                     """)
#                     st.markdown('<div class="result-box error-box">'
#                                 '🔧 Technical issue: Model not available. '
#                                 'We\'re working to restore service.</div>', 
#                                 unsafe_allow_html=True)
#                 else:
#                     st.error(f"⛔ Translation failed: {error_msg}")
#                     st.markdown(f'<div class="result-box error-box">{error_msg}</div>', 
#                                 unsafe_allow_html=True)

# # Copy button for last translation
# if st.session_state.get("last_translation"):
#     if st.button("📋 Copy Translation", use_container_width=True, type="secondary"):
#         st.session_state.copied = True
#         st.toast("✅ Translation copied to clipboard!", icon="📋")

# # Tips Section in English
# st.markdown("---")
# st.subheader("💡 Translation Tips")
# st.markdown("""
# <div class="quote">
# "Translation is the art of bridging cultures through language."
# </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# - **Short Texts**: Works best with sentences under 50 words
# - **Clear Language**: Avoid slang and idioms for best results
# - **Names/Terms**: Proper nouns remain unchanged in translation
# - **Formatting**: Line breaks and punctuation are preserved
# - **Speed**: Gemini Flash provides faster translations
# - **Direction**: Use the direction buttons to force specific translation
# """)

# # Footer
# st.markdown("---")
# st.markdown('<div class="footer">'
#             'Note: Uses Google Gemini 1.5 Flash • Free tier has rate limits • '
#             'For best results, use simple sentences'
#             '</div>', unsafe_allow_html=True)

# # Add a reload button in sidebar
# with st.sidebar:
#     st.header("Troubleshooting")
#     if st.button("🔄 Refresh Connection", use_container_width=True):
#         st.rerun()
#     st.markdown("""
#     **If you encounter issues:**
#     1. Check your internet connection
#     2. Verify API key in .env file
#     3. Wait 1 minute and retry
#     4. Use shorter text inputs
#     5. Select specific translation direction
#     """)
#     st.markdown("---")
#     st.caption("Version 3.2 • Gemini Flash Translator")




















import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Validate API Key
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Configuration error: {str(e)}")
    st.stop()

# App Configuration
st.set_page_config(
    page_title="🌐 AI Multi-Language Translator",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'source_lang' not in st.session_state:
    st.session_state.source_lang = "Auto Detect"
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "Urdu"
if 'last_translation' not in st.session_state:
    st.session_state.last_translation = ""
if 'last_output_lang' not in st.session_state:
    st.session_state.last_output_lang = ""
if 'swap_languages' not in st.session_state:
    st.session_state.swap_languages = False
if 'show_languages' not in st.session_state:
    st.session_state.show_languages = False

# Language options
LANGUAGES = {
    "Auto Detect": {"code": "auto", "emoji": "🔍"},
    "English": {"code": "en", "emoji": "🇬🇧"},
    "Urdu": {"code": "ur", "emoji": "🇵🇰"},
    "Chinese": {"code": "zh", "emoji": "🇨🇳"},
    "Japanese": {"code": "ja", "emoji": "🇯🇵"},
    "French": {"code": "fr", "emoji": "🇫🇷"},
    "Arabic": {"code": "ar", "emoji": "🇸🇦"},
    "Farsi": {"code": "fa", "emoji": "🇮🇷"},
    "Spanish": {"code": "es", "emoji": "🇪🇸"},
    "German": {"code": "de", "emoji": "🇩🇪"},
    "Russian": {"code": "ru", "emoji": "🇷🇺"},
    "Portuguese": {"code": "pt", "emoji": "🇵🇹"}
}

# Custom CSS for styling
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
    
    /* Main container */
    .main-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 0.4rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        font-size: 16px; 
        line-height: 1.6;
        height: 150px !important;
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #9c27b0 !important;
        box-shadow: inset 0 2px 5px rgba(156, 39, 176, 0.1), 0 0 0 2px rgba(156, 39, 176, 0.15) !important;
    }
    
    /* BUTTON STYLES */
    .primary-button {
        background: linear-gradient(45deg, #9C27B0, #2196F3) !important;
        color: white !important;
        border: none !important;
        padding: 15px 20px !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);
        margin: 10px 0;
    }
    .primary-button:hover {
        background: linear-gradient(45deg, #8E24AA, #1E88E5) !important;
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(156, 39, 176, 0.4);
    }
    
    /* REFRESH BUTTON STYLE */
    .refresh-button {
        background: linear-gradient(45deg, #9C27B0, #2196F3) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);
        width: 100% !important;
        margin: 20px 0;
    }
    .refresh-button:hover {
        background: linear-gradient(45deg, #8E24AA, #1E88E5) !important;
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(156, 39, 176, 0.4);
    }
    
    /* BURGER MENU STYLES */
    .burger-menu {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        cursor: pointer;
        font-size: 2rem;
        background: linear-gradient(135deg, #9C27B0, #2196F3);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);
        transition: all 0.3s ease;
    }
    .burger-menu:hover {
        transform: scale(1.1) rotate(90deg);
    }
    
    .languages-panel {
        position: fixed;
        top: 0;
        right: 0;
        width: 300px;
        height: 100%;
        background: white;
        z-index: 999;
        padding: 20px;
        box-shadow: -5px 0 15px rgba(0,0,0,0.1);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        overflow-y: auto;
    }
    .languages-panel.active {
        transform: translateX(0);
    }
    .close-btn {
        position: absolute;
        top: 15px;
        right: 15px;
        font-size: 1.5rem;
        cursor: pointer;
        color: #9C27B0;
    }
    
    /* Result box styling */
    .result-box {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin-top: 1rem;
        border-left: 5px solid #9c27b0;
        font-size: 18px;
        line-height: 1.4;
        white-space: pre-wrap;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    .result-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* HEADER STYLING */
    .header-box {
        background: linear-gradient(135deg, #9C27B0, #2196F3);
        color: white;
        border-radius: 15px;
        padding: 0.rem;
        margin: 0 0 0.25rem 0;
        text-align: center;
        box-shadow: 0 10px 25px rgba(156, 39, 176, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    .header-box h1 {
        font-size: 2.5rem !important;
        margin: 0.5rem 0 !important;
        letter-spacing: 0.5px;
    }
    .header-box p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.8rem 0 !important;
    }
    
    /* Language specific styles */
    .urdu-text, .arabic-text, .farsi-text {
        text-align: right !important;
        direction: rtl !important;
        line-height: 2.2 !important;
    }
    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', serif !important;
        font-size: 24px !important;
    }
    .arabic-text {
        font-family: 'Amiri', serif !important;
        font-size: 22px !important;
    }
    .farsi-text {
        font-family: 'Scheherazade New', serif !important;
        font-size: 22px !important;
    }
    .chinese-text {
        font-family: 'Noto Sans SC', sans-serif !important;
        font-size: 20px !important;
    }
    .japanese-text {
        font-family: 'Noto Sans JP', sans-serif !important;
        font-size: 20px !important;
    }
    
    /* Language selector */
    .language-selector {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    .language-selector:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Footer styling */
    .footer {
        font-size: 0.85rem;
        text-align: center;
        margin-top: 2.5rem;
        color: #777;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    
    /* Animation for translation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .pulse {
        animation: pulse 1.5s infinite;
    }
    
    /* Interactive elements */
    .interactive-element {
        transition: all 0.3s ease;
    }
    .interactive-element:hover {
        transform: scale(1.05);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9C27B0, #2196F3) !important;
        border-radius: 4px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .stTextArea textarea {
            height: 200px !important;
        }
        .language-selector {
            padding: 10px;
        }
        .header-box h1 {
            font-size: 2rem !important;
        }
        .primary-button, .refresh-button {
            font-size: 18px !important;
            padding: 12px 24px !important;
        }
        .burger-menu {
            top: 15px;
            right: 15px;
            width: 40px;
            height: 40px;
            font-size: 1.5rem;
        }
        .languages-panel {
            width: 250px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Function to swap languages
def swap_languages():
    if st.session_state.source_lang != "Auto Detect":
        current_source = st.session_state.source_lang
        current_target = st.session_state.target_lang
        st.session_state.source_lang = current_target
        st.session_state.target_lang = current_source
        st.session_state.swap_languages = True

# Function to toggle languages panel
def toggle_languages():
    st.session_state.show_languages = not st.session_state.show_languages

# Main container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Burger menu icon
    st.markdown("""
    <div class="burger-menu interactive-element" onclick="toggleLanguages()">☰</div>
    <div class="languages-panel" id="languagesPanel">
        <span class="close-btn" onclick="toggleLanguages()">×</span>
        <h2 style="color: #9C27B0; margin-bottom: 20px;">🌍 Supported Languages</h2>
        <div style="display: grid; grid-template-columns: 1fr; gap: 10px;">
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇬🇧 English</h3>
                <p>The global lingua franca</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇵🇰 Urdu</h3>
                <p>Official language of Pakistan</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇨🇳 Chinese</h3>
                <p>Most spoken language worldwide</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇯🇵 Japanese</h3>
                <p>Language of Japan with unique scripts</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇫🇷 French</h3>
                <p>Romance language spoken globally</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇸🇦 Arabic</h3>
                <p>Semitic language with rich history</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇮🇷 Farsi</h3>
                <p>Persian language with poetic tradition</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇪🇸 Spanish</h3>
                <p>Widely spoken in Latin America</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇩🇪 German</h3>
                <p>Language of central Europe</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇷🇺 Russian</h3>
                <p>Largest native language in Europe</p>
            </div>
            <div class="language-card" style="background: #f9f5ff; padding: 15px; border-radius: 10px;">
                <h3>🇵🇹 Portuguese</h3>
                <p>Spoken in Brazil and Portugal</p>
            </div>
        </div>
    </div>
    
    <script>
    function toggleLanguages() {
        const panel = document.getElementById('languagesPanel');
        panel.classList.toggle('active');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Header with magenta-blue gradient
    st.markdown("""
    <div class="header-box">
        <div class="interactive-element" style="font-size: 4rem; margin-bottom: 3px;">🌐</div>
        <h1>AI Multi-Language Translator</h1>
        <p>Translate languages instantly</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selection with swap button
    col1, col2, col3 = st.columns([3, 1, 3])
    with col1:
        st.markdown('<div class="language-selector">', unsafe_allow_html=True)
        st.subheader("Source Language")
        st.session_state.source_lang = st.selectbox(
            "Select source language:",
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(st.session_state.source_lang),
            format_func=lambda x: f"{LANGUAGES[x]['emoji']} {x}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="display: flex; align-items: center; justify-content: center; height: 100%;">', unsafe_allow_html=True)
        if st.button("⇄", key="swap_btn", use_container_width=True, type="secondary", 
                     help="Swap source and target languages", 
                     on_click=swap_languages):
            pass
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="language-selector">', unsafe_allow_html=True)
        st.subheader("Target Language")
        st.session_state.target_lang = st.selectbox(
            "Select target language:",
            [lang for lang in list(LANGUAGES.keys()) if lang != "Auto Detect"],
            index=list(LANGUAGES.keys()).index(st.session_state.target_lang) - 1,
            format_func=lambda x: f"{LANGUAGES[x]['emoji']} {x}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("""
    <div class="interactive-element">
    """, unsafe_allow_html=True)
    text = st.text_area(
        "✍️ Enter text to translate:",
        placeholder="Type or paste your text here...",
        height=250,
        key="input_text",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # TRANSLATE BUTTON
    if st.button("🚀 Translate Text", use_container_width=True, key="translate_btn", type="primary"):
        st.session_state.translate_clicked = True
    
    # Handle translation
    if st.session_state.get('translate_clicked') and text.strip():
        with st.spinner(f"🔍 Translating from {st.session_state.source_lang} to {st.session_state.target_lang}..."):
            progress_bar = st.progress(0)
            
            # Simulate progress steps
            for percent_complete in range(0, 101, 10):
                time.sleep(0.05)
                progress_bar.progress(percent_complete)
                
            try:
                # Initialize model
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Create translation prompt
                prompt = f"""
                You are an expert multilingual translator. 
                Translate the following text according to these guidelines:
                
                - Source language: {st.session_state.source_lang}
                - Target language: {st.session_state.target_lang}
                - Preserve original meaning and cultural context
                - Keep names, technical terms, and proper nouns unchanged
                - Use natural, conversational language
                - Maintain original formatting (line breaks, punctuation)
                - For languages with special scripts (Urdu, Arabic, Farsi, Chinese, Japanese), 
                  use the appropriate script and diacritics
                
                Text to translate:
                "{text}"
                """
                
                # Generate translation
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.1,
                        max_output_tokens=1500,
                        top_p=0.95
                    )
                )
                
                # Display results
                st.balloons()
                st.subheader(f"✅ {st.session_state.source_lang} → {st.session_state.target_lang} Translation")
                
                # Apply language-specific styling
                lang_class = ""
                if st.session_state.target_lang == "Urdu":
                    lang_class = "urdu-text"
                elif st.session_state.target_lang == "Arabic":
                    lang_class = "arabic-text"
                elif st.session_state.target_lang == "Farsi":
                    lang_class = "farsi-text"
                elif st.session_state.target_lang == "Chinese":
                    lang_class = "chinese-text"
                elif st.session_state.target_lang == "Japanese":
                    lang_class = "japanese-text"
                
                st.markdown(f'<div class="result-box pulse {lang_class}">{response.text}</div>', unsafe_allow_html=True)
                
                # Store results
                st.session_state.last_translation = response.text
                st.session_state.last_output_lang = st.session_state.target_lang
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    st.error("""
                    ⚠️ **Translation Limit Reached**  
                    We've exceeded the free translation quota for now. Please:
                    - Try again after 1-2 minutes
                    - Use shorter text
                    - Refresh the page and retry
                    """)
                    st.markdown('<div class="result-box" style="border-left: 5px solid #FF9800; background-color: #fff3e0;">'
                                '🚫 Current free translation quota exhausted. '
                                'Service will resume shortly.</div>', 
                                unsafe_allow_html=True)
                elif "404" in error_msg or "not found" in error_msg:
                    st.error("""
                    ⚠️ **Model Configuration Error**
                    The translation model is currently unavailable. Please:
                    - Check your internet connection
                    - Refresh the application
                    - Contact support if issue persists
                    """)
                    st.markdown('<div class="result-box" style="border-left: 5px solid #2196F3; background-color: #e3f2fd;">'
                                '🔧 Technical issue: Model not available. '
                                'We\'re working to restore service.</div>', 
                                unsafe_allow_html=True)
                else:
                    st.error(f"⛔ Translation failed: {error_msg}")
                    st.markdown(f'<div class="result-box" style="border-left: 5px solid #9C27B0; background-color: #f3e5f5;">{error_msg}</div>', 
                                unsafe_allow_html=True)
            finally:
                progress_bar.empty()
    
    # Copy button for last translation
    if st.session_state.get("last_translation"):
        if st.button("📋 Copy Translation to Clipboard", use_container_width=True, type="primary"):
            st.session_state.copied = True
            st.toast("✅ Translation copied to clipboard!", icon="📋")
    
    # Tips Section
    st.markdown("---")
    st.subheader("💡 Translation Tips")
    
    tips = """
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-top: 20px;">
        <div style="background: #f9f5ff; border-radius: 15px; padding: 20px;">
            <h4>📝 Clear Input</h4>
            <p>Use proper punctuation and avoid slang for best results</p>
        </div>
        <div style="background: #f9f5ff; border-radius: 15px; padding: 20px;">
            <h4>🔤 Special Characters</h4>
            <p>For languages like Arabic and Urdu, ensure correct diacritics</p>
        </div>
        <div style="background: #f9f5ff; border-radius: 15px; padding: 20px;">
            <h4>⏱️ Patience</h4>
            <p>Longer texts may take 10-15 seconds to translate</p>
        </div>
        <div style="background: #f9f5ff; border-radius: 15px; padding: 20px;">
            <h4>🌐 Cultural Context</h4>
            <p>Translations preserve cultural nuances and idioms</p>
        </div>
    </div>
    """
    st.markdown(tips, unsafe_allow_html=True)
    
    # Translation history in sidebar
    with st.sidebar:
        st.header("📚 Translation History")
        if st.session_state.get("last_translation"):
            st.subheader("Last Translation")
            st.write(f"**{st.session_state.source_lang} → {st.session_state.target_lang}**")
            st.markdown(f'<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px;">{st.session_state.last_translation[:200]}...</div>', unsafe_allow_html=True)
        
        st.header("⚙️ Settings")
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 15px; margin-bottom: 20px;">
            <p><strong>Model:</strong> Gemini 1.5 Flash</p>
            <p><strong>Max Length:</strong> 1500 characters</p>
            <p><strong>Quality:</strong> Professional</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("🚨 Troubleshooting")
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 15px; margin-bottom: 20px;">
            <p>If you encounter issues:</p>
            <ol>
                <li>Check your internet connection</li>
                <li>Verify API key in .env file</li>
                <li>Wait 1 minute and retry</li>
                <li>Use shorter text inputs</li>
                <li>Select specific languages</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # REFRESH BUTTON
        if st.button("🔄 Refresh Connection", key="refresh_btn", use_container_width=True, 
                    help="Reset the translator connection", 
                    type="primary"):
            st.rerun()
        
        st.markdown("---")
        st.caption("AI Multi-Language Translator v5.0")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>Powered by Google Gemini 1.5 Flash • Free tier has rate limits</p>
        <p>For best results, use clear and concise sentences • Version 5.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

# JavaScript to handle the burger menu
st.markdown("""
<script>
function toggleLanguages() {
    const panel = document.getElementById('languagesPanel');
    panel.classList.toggle('active');
    
    // Toggle overflow on body to prevent scrolling when panel is open
    if (panel.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

// Close panel when clicking outside
document.addEventListener('click', function(event) {
    const panel = document.getElementById('languagesPanel');
    const burger = document.querySelector('.burger-menu');
    
    if (panel.classList.contains('active') && 
        !panel.contains(event.target) && 
        !burger.contains(event.target)) {
        panel.classList.remove('active');
        document.body.style.overflow = '';
    }
});
</script>
""", unsafe_allow_html=True)