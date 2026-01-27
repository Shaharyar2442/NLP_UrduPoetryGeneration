import streamlit as st
import os
import numpy as np
from utils import load_tokenizer, load_poetry_model, generate_poetry, roman_to_urdu_map
from card_generator import create_poetry_card
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="Urdu Poetry Generator",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Dark Rustic/Vintage Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&family=Cinzel:wght@400;700&family=Playfair+Display:wght@400;700&display=swap');
    
    /* Global Background */
    .stApp {
        background-color: #121212;
        background-image: linear-gradient(rgba(18, 18, 18, 0.85), rgba(18, 18, 18, 0.95)), 
                          url("https://www.transparenttextures.com/patterns/black-linen.png");
        background-size: cover;
        background-attachment: fixed;
        color: #E0D6C2; /* Cream */
    }

    /* Hide Streamlit Elements */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none;}
    
    /* Headlines */
    h1, h2, h3, h4, .big-font {
        font-family: 'Cinzel', serif;
        color: #C5A059; /* Antique Gold */
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    p, label {
        font-family: 'Playfair Display', serif;
        color: #E0D6C2;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #2E2E2E !important;
        color: #E0D6C2 !important; /* Cream Text */
        border: 2px solid #C5A059 !important;
        border-radius: 5px;
        font-family: 'Noto Nastaliq Urdu', serif;
        text-align: right;
        font-size: 20px;
        padding: 10px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d0d0d;
        border-right: 1px solid #333;
    }
    
    .sidebar-text {
        color: #E0D6C2;
        font-family: 'Playfair Display', serif;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(#121212, #1E1E1E);
        color: #C5A059;
        border: 1px solid #C5A059;
        border-radius: 2px;
        padding: 10px 30px;
        font-family: 'Cinzel', serif;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: #C5A059;
        color: #121212;
        box-shadow: 0 0 15px rgba(197, 160, 89, 0.3);
    }

    /* Vintage Card Container */
    .poetry-container {
        position: relative;
        background: rgba(30, 30, 30, 0.6);
        border: 1px solid rgba(197, 160, 89, 0.3);
        padding: 40px;
        margin-top: 30px;
        border-radius: 4px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        text-align: center;
    }

    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', serif;
        font-size: 36px;
        color: #fff;
        line-height: 2.2;
        direction: rtl;
        text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.2);
    }
    
    /* Transliteration Text */
    .transliteration-box {
        text_align: center;
        color: #C5A059; 
        font-family: 'Noto Nastaliq Urdu', serif; 
        font-size: 1.2rem;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    
    model_choice = st.selectbox(
        "Choose AI Model",
        ("RNN", "LSTM", "Transformer"),
        index=2,
        help="Select the deep learning architecture."
    )
    
    model_map = {
        "RNN": "RNN",
        "LSTM": "LSTM",
        "Transformer": "Transformer"
    }
    selected_model_key = model_map[model_choice]

    temperature = st.slider("Creativity (Temperature)", 0.5, 1.5, 1.0, 0.1, help="Higher values make the poetry more abstract.")
    length = st.slider("Verse Length", 5, 30, 15)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("Tip: Start with standard Roman Urdu (e.g., 'Dil'). The ink will transform it.")

# --- Main Content ---
st.markdown("<h1 style='font-size: 3.5rem;'>The Gilded Diwan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; opacity: 0.8;'>Soulless AI Generated Poetry</p>", unsafe_allow_html=True)
st.markdown("---")

# 1. Load Resources
MAX_SEQUENCE_LEN = 14 # Default fallback
with st.spinner("Summoning the Muse..."):
    tokenizer = load_tokenizer()
    model = load_poetry_model(selected_model_key)

if model:
    try:
        if hasattr(model, 'input_shape'):
             MAX_SEQUENCE_LEN = model.input_shape[1] + 1
    except:
        pass

# 2. Input
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Text Input (Default: English/Roman)
    raw_input = st.text_input("First Word:", "Muhabbat", help="Enter a word to begin the Ghazal (Roman or Urdu)")
    
    # Transliteration Logic
    urdu_input = roman_to_urdu_map(raw_input)
    
    # Display Transliteration Feedback
    if raw_input.strip():
        st.markdown(f"<div style='text-align: center; color: #C5A059; font-family: Noto Nastaliq Urdu; margin-top: 5px;'>Transliterated to: {urdu_input}</div>", unsafe_allow_html=True)

# 3. Generate
if st.button("Ink the Page"):
    if not model or not tokenizer:
        st.error("The quill is broken (Model failed to load).")
    elif not urdu_input.strip():
        st.warning("Even a blank page needs a thought to begin.")
    else:
        with st.spinner("Composing..."):
            try:
                # Use the Transliterated Urdu Input
                generated_verse = generate_poetry(
                    model, 
                    tokenizer, 
                    urdu_input, 
                    length, 
                    temperature, 
                    MAX_SEQUENCE_LEN
                )
                
                # Display Result in Vintage Container
                st.markdown(f"""
                <div class="poetry-container">
                    <div class="urdu-text">{generated_verse}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate Image Card
                card_img = create_poetry_card(generated_verse, attribution="AI Poet")
                
                # Save to buffer
                buf = BytesIO()
                card_img.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1,1,1])
                with c2:
                    st.download_button(
                        label="Download Keepsake 📥",
                        data=byte_im,
                        file_name="urdu_verse_card.png",
                        mime="image/png",
                    )
                    
            except Exception as e:
                st.error(f"Ink spilled: {e}")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-family: Cinzel; color: #555; font-size: 0.8rem;'>Neural Networks • Urdu Literature • Generative Art</div>", unsafe_allow_html=True)
