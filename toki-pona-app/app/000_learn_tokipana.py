import streamlit as st

st.set_page_config(
    page_title="Toki Pona Learning App",
    page_icon="📝",
    layout="centered",
)

st.title("📝 o kama pona tawa lipu sona!")  # Welcome to the Learning App
st.subheader("sina ken kama sona e toki pona lon ni!")  # Use this page to learn Toki Pona
st.divider()

if 'study_mode' not in st.session_state:
    st.session_state.study_mode = None

st.session_state.study_mode = st.radio(
    "sina wile kama sona e seme?",  # What do you want to learn?
    ["nimi lili", "sitelen pona"],  # Basic words, Sitelen Pona (writing system)
    horizontal=True
)

# Display the Toki Pona Chart
image_path = f"img/{st.session_state.study_mode}.jpg"
try:
    st.image(image_path,
             caption=f"{st.session_state.study_mode} lipu. "  # Chart
                     f"tan: https://tokipona.org/")
except FileNotFoundError:
    st.error(
        f"mi ken ala lon e sitelen {st.session_state.study_mode}. "  # Could not load the image
        f"o lukin e nasin ni: {image_path}")  # Please check this path

# Footer
st.divider()
st.markdown(
    """
    🎯 **o kepeken mute!**  # Practice Makes Perfect!
    👉 o tawa **lipu toki mama** en **lipu toki pona** tawa ni: sina ken lukin e sona sina.  # Visit the translation pages to test your knowledge
    🔁 ante e nasin sina lon **nimi lili** en **sitelen pona** tawa ni: sina ken kama sona pona.  # Switch between modes to improve
    🌟 o awen kama sona! o lukin e pona sina!  # Keep practicing and track your progress!
    """,
)