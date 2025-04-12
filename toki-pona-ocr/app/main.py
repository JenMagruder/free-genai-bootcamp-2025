import streamlit as st
from ocr_practice import main as ocr_page
from text_adventure import main as adventure_page
from sentence_practice import main as sentence_page

st.set_page_config(
    page_title="Toki Pona Learning Suite",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("Toki Pona Learning Suite")
st.markdown("""
This app helps you learn Toki Pona through multiple interactive methods:
- 📷 OCR Practice: Upload and recognize Toki Pona symbols
- 📚 Text Adventure: Explore a text-based adventure game
- ✍️ Sentence Practice: Generate and practice simple sentences
""")

def main():
    st.sidebar.title("Navigation")
    
    # Navigation
    page = st.sidebar.radio(
        "Go to",
        ["OCR Practice", "Text Adventure", "Sentence Practice"]
    )
    
    if page == "OCR Practice":
        ocr_page()
    elif page == "Text Adventure":
        adventure_page()
    elif page == "Sentence Practice":
        sentence_page()

if __name__ == "__main__":
    main()
