import streamlit as st
import os
import numpy as np
import time
from utils import load_tokenizer, load_poetry_model, generate_poetry
from card_generator import create_poetry_card
from io import BytesIO
from googletrans import Translator
from streamlit_lottie import st_lottie
import requests

# --- Helpers ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def transliterate_to_urdu(text):
    """
    Attempts to transliterate/translate Roman Urdu or English to Urdu Script.
    """
    if not text:
        return ""
    
    # Check if text contains mostly ASCII (English/Roman)
    is_ascii = all(ord(char) < 128 for char in text.replace(" ", ""))
    
    if is_ascii:
        try:
            translator = Translator()
            # "ur" destination usually handles Roman -> Urdu transliteration well for common words
            result = translator.translate(text, dest='ur')
            return result.text
        except Exception as e:
            # Fallback if offline or error
            return text
    return text

# --- Page Config ---
st.set_page_config(
    page_title="Urdu Poetry Generator",
    page_icon="✒️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Enhanced Midnight Premium Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&family=Cinzel:wght@400;700&display=swap');
    
    /* Main Background with Animated Gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #141E30);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #e0e0e0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        color: #FFD700; /* Gold */
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
        font-weight: 700;
    }
    
    /* Input Area - Fix Visibility */
    .stTextInput label {
        color: #d4af37 !important;
        font-size: 1.2rem;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 2px solid #d4af37 !important;
        font-family: 'Noto Nastaliq Urdu', serif;
        text-align: right;
        font-size: 24px !important;
        padding: 10px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        background-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.6);
        outline: none;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #d4af37, #f7ef8a, #d4af37);
        background-size: 200% auto;
        color: #000;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        font-weight: bold;
        font-family: 'Cinzel', serif;
        letter-spacing: 1px;
        transition: 0.5s;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stButton > button:hover {
        background-position: right center;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
    }
    
    /* Output Card with Fade In */
    .poetry-card-container {
        animation: fadeIn 2s ease-in-out;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .poetry-card {
        background: rgba(16, 16, 16, 0.7);
        border: 2px solid #d4af37;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-top: 30px;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    /* Decorative Corner Elements (CSS Pseudo-elements) */
    .poetry-card::before {
        content: "Draft";
        position: absolute;
        top: -10px;
        left: -10px;
        width: 50px;
        height: 50px;
        border-top: 3px solid #d4af37;
        border-left: 3px solid #d4af37;
        opacity: 0; /* Hidden for now, just an example idea */
    }
    
    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', serif;
        font-size: 38px;
        color: #fff;
        line-height: 2.2;
        direction: rtl;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    
    .translation-text {
         font-family: 'Cinzel', serif;
         font-size: 14px;
         color: #aaa;
         margin-top: 10px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0c0e14;
        border-right: 1px solid #333;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    # Lottie Animation for sidebar
    lottie_poetry = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json") # Feather Pen
    if lottie_poetry:
        st_lottie(lottie_poetry, height=150, key="sidebar_anim")
    else:
        st.image("https://img.icons8.com/clouds/200/poetry.png", width=100)
        
    st.markdown("### ⚙️ Settings")
    
    model_choice = st.selectbox(
        "Choose AI Model",
        ("RNN (Creative)", "LSTM (Balanced)", "Transformer (Advanced)"),
        index=2
    )
    
    # Map friendly names to internal keys
    model_map = {
        "RNN (Creative)": "RNN",
        "LSTM (Balanced)": "LSTM",
        "Transformer (Advanced)": "Transformer"
    }
    selected_model_key = model_map[model_choice]

    temperature = st.slider("Creativity (Temperature)", 0.5, 1.5, 1.0, 0.1)
    length = st.slider("Verse Length (Words)", 5, 30, 15)
    
    st.markdown("---")
    st.info("💡 **Tip:** Higher temperature makes the poetry more unique but unpredictable.")

# --- Main Content ---
col1, col2 = st.columns([1, 6])
with col1:
    lottie_book = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_4kji20y9.json") # Magic Book
    if lottie_book:
        st_lottie(lottie_book, height=80, key="header_anim")
with col2:
    st.title("✨ Shair-o-Shayari AI ✨")
st.markdown("<h3 style='text-align: center; color: #aaa; margin-top: -20px;'><i>Artificial Intelligence for Urdu Poetry</i></h3>", unsafe_allow_html=True)

# 1. Load Resources
with st.spinner("Summoning the Muse..."):
    tokenizer = load_tokenizer()
    # Attempt to detect input shape from model
    MAX_SEQUENCE_LEN = 14 # Default fallback
    model = load_poetry_model(selected_model_key)
    
    if model:
        try:
             if hasattr(model, 'input_shape'):
                 # Check if input_shape is available and valid
                 shape = model.input_shape
                 if shape and len(shape) > 1:
                    MAX_SEQUENCE_LEN = shape[1] + 1
        except:
            pass

# 2. Input
st.markdown("<br>", unsafe_allow_html=True)
concept_col1, concept_col2 = st.columns([4, 1])

with concept_col1:
    user_input = st.text_input("Enter the first word (English/Urdu):", "Mohabbat")
    
    # Transliteration Logic
    seed_text = user_input
    if user_input:
        converted_text = transliterate_to_urdu(user_input)
        if converted_text != user_input:
           st.caption(f"✨ Transliterated to: **{converted_text}**")
           seed_text = converted_text

# 3. Generate
if st.button("✨ Compose Verse ✨"):
    if not model or not tokenizer:
        st.error("Model or Tokenizer failed to load. Please check file paths.")
    elif not seed_text.strip():
        st.warning("Please enter a starting word.")
    else:
        with st.spinner("Weaving words of wisdom..."):
            try:
                generated_verse = generate_poetry(
                    model, 
                    tokenizer, 
                    seed_text, 
                    length, 
                    temperature, 
                    MAX_SEQUENCE_LEN
                )
                
                # Display Result with Animation Container
                st.markdown(f"""
                <div class="poetry-card-container">
                    <div class="poetry-card">
                        <div class="urdu-text">{generated_verse}</div>
                        <div class="translation-text">generated by {selected_model_key} model</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate Image Card
                card_img = create_poetry_card(generated_verse, attribution="AI Poet")
                
                # Save to buffer for download
                buf = BytesIO()
                card_img.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.markdown("<br>", unsafe_allow_html=True)
                d_col1, d_col2, d_col3 = st.columns([1,2,1])
                with d_col2:
                    st.download_button(
                        label="📷 Download Poetry Card",
                        data=byte_im,
                        file_name="urdu_poetry_card.png",
                        mime="image/png",
                    )
                    
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
                st.info("Tip: Try a different model or shorter length.")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #555; font-size: 0.8em;'>Crafted with ❤️ & Deep Learning</div>", unsafe_allow_html=True)
