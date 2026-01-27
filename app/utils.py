import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Sequential, Model
from tensorflow.keras.layers import Layer, Dense, LayerNormalization, MultiHeadAttention, Dropout, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
import streamlit as st

# --- Custom Layers (Must match training code exactly) ---

@tf.keras.utils.register_keras_serializable()
class TransformerBlock(Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1, **kwargs):
        super(TransformerBlock, self).__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.rate = rate
        self.att = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = Sequential([Dense(ff_dim, activation="relu"), Dense(embed_dim),])
        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(rate)
        self.dropout2 = Dropout(rate)

    def call(self, inputs, training=None):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "ff_dim": self.ff_dim,
            "rate": self.rate,
        })
        return config

@tf.keras.utils.register_keras_serializable()
class TokenAndPositionEmbedding(Layer):
    def __init__(self, maxlen, vocab_size, embed_dim, **kwargs):
        super(TokenAndPositionEmbedding, self).__init__(**kwargs)
        self.maxlen = maxlen
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.token_emb = Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "maxlen": self.maxlen,
            "vocab_size": self.vocab_size,
            "embed_dim": self.embed_dim,
        })
        return config

# --- Loading Functions ---

@st.cache_resource(show_spinner=False)
def load_tokenizer(path='../models/tokenizer.pickle'):
    """Loads the tokenizer. Cached to run once."""
    if not os.path.exists(path):
         if os.path.exists("models/tokenizer.pickle"):
             path = "models/tokenizer.pickle"
         else:
             st.error(f"Tokenizer not found at {path}")
             return None

    with open(path, 'rb') as handle:
        tokenizer = pickle.load(handle)
        return tokenizer

@st.cache_resource(show_spinner=False)
def load_poetry_model(model_name, base_path='../models'):
    """
    Loads a model by name. 
    Mapping:
    - 'RMSprop' variants are selected as the 'Best' options.
    """
    if not os.path.exists(base_path):
        if os.path.exists("models"):
            base_path = "models"
    
    file_map = {
        "RNN": "RNN_RMSprop.keras",
        "LSTM": "LSTM_RMSprop.keras",
        "Transformer": "Transformer_RMSprop.keras"
    }
    
    filename = file_map.get(model_name)
    if not filename:
        return None
        
    filepath = os.path.join(base_path, filename)
    
    if not os.path.exists(filepath):
        st.error(f"Model file not found: {filepath}")
        return None

    custom_objects = {
        'TokenAndPositionEmbedding': TokenAndPositionEmbedding,
        'TransformerBlock': TransformerBlock
    }
    
    try:
        model = load_model(filepath, custom_objects=custom_objects)
        return model
    except Exception as e:
        st.error(f"Failed to load model {model_name}: {e}")
        return None

# --- Helpers ---

def roman_to_urdu_map(text):
    """
    Simple mapping for common poetic words.
    Expand this dictionary as needed.
    """
    mapping = {
        "muhabbat": "محبت",
        "mohabbat": "محبت",
        "dil": "دل",
        "shaam": "شام",
        "sham": "شام",
        "yaad": "یاد",
        "yad": "یاد",
        "khushi": "خوشی",
        "zindagi": "زندگی",
        "duniya": "دنیا",
        "ishq": "عشق",
        "raat": "رات",
        "subah": "صبح",
        "dard": "درد",
        "bewafa": "بے وفا",
        "sanam": "صنم",
        "khuda": "خدا",
        "jaan": "جان",
        "jahaan": "جہاں"
    }
    
    lower_text = text.lower().strip()
    return mapping.get(lower_text, text) # Return original if not found

# --- Generation Logic ---

def generate_poetry(model, tokenizer, seed_text, next_words, temperature, max_sequence_len):
    """Generates poetry text given a model and seed."""
    output_text = seed_text
    
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([output_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        
        try:
            predictions = model.predict(token_list, verbose=0)[0]
        except:
             break 
             
        predictions = np.log(predictions + 1e-7) / temperature
        exp_preds = np.exp(predictions)
        predictions = exp_preds / np.sum(exp_preds)
        
        predicted_id = np.random.choice(len(predictions), p=predictions)
        
        predicted_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_id:
                predicted_word = word
                break
        
        if predicted_word == "": 
            break
            
        output_text += " " + predicted_word
        
    return output_text
