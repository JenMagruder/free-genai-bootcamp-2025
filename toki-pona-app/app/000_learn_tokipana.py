import streamlit as st
import random

# Constants for Toki Pona
TOKI_PONA_WORDS = {
    "mi": "I, me, we",
    "sina": "you",
    "ona": "he, she, it, they",
    "ni": "this, that",
    "pona": "good, simple",
    "ike": "bad, complex",
    "suli": "big, important",
    "lili": "small, little",
    "kama": "come, become",
    "tawa": "to, for, moving",
    "moku": "food, eat",
    "tomo": "house, building",
    "jan": "person, human",
    "wile": "want, need",
    "sona": "knowledge, know",
    "lukin": "see, look",
    "kepeken": "use, with",
    "lon": "at, exist",
    "tan": "from, because",
    "sama": "same, similar"
}

st.set_page_config(
    page_title="Toki Pona Learning App",
    page_icon="📝",
    layout="centered",
)

st.title("📝 o kama pona tawa lipu sona!")  # Welcome to the Learning App
st.subheader("sina ken kama sona e toki pona lon ni!")  # Use this page to learn Toki Pona
st.divider()

# Initialize session state
if 'current_word' not in st.session_state:
    st.session_state.current_word = random.choice(list(TOKI_PONA_WORDS.keys()))

# Learning mode selection
study_mode = st.radio(
    "sina wile kama sona e seme?",  # What do you want to learn?
    ["nimi lili (Basic Words)", "sitelen pona (Writing System)"],
    horizontal=True
)

if study_mode == "nimi lili (Basic Words)":
    # Word learning section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Word:")
        st.header(st.session_state.current_word)
        st.write(f"Meaning: {TOKI_PONA_WORDS[st.session_state.current_word]}")
        
    with col2:
        if st.button("Next Word"):
            st.session_state.current_word = random.choice(list(TOKI_PONA_WORDS.keys()))
            st.rerun()

else:
    st.info("The writing system practice will be available in the next update! For now, try learning the basic words.")

# Footer
st.divider()
st.markdown(
    """
    🎯 **o kepeken mute!** (Practice Makes Perfect!)
    👉 Learn one word at a time and try to use it in sentences.
    🌟 o awen kama sona! (Keep learning!)
    """
)