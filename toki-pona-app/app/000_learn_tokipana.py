import streamlit as st
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Must be the first Streamlit command
st.set_page_config(
    page_title="Toki Pona Learning App",
    page_icon="📝",
    layout="centered",
)

# Add just the background color
st.markdown("""
<style>
    .stApp {
        background-color: #1a237e;
    }
</style>
""", unsafe_allow_html=True)

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

# Example sentences for each word
EXAMPLE_SENTENCES = {
    "mi": {
        "toki_pona": "mi pona.",
        "english": "I am good.",
        "explanation": "'mi' is used as the subject 'I'"
    },
    "sina": {
        "toki_pona": "sina suli.",
        "english": "You are important.",
        "explanation": "'sina' is the subject 'you'"
    },
    "ona": {
        "toki_pona": "ona li pona.",
        "english": "They are good.",
        "explanation": "'ona' with 'li' for third person"
    },
    "ni": {
        "toki_pona": "ni li suli.",
        "english": "This is important.",
        "explanation": "'ni' as demonstrative 'this'"
    },
    "pona": {
        "toki_pona": "tomo ni li pona.",
        "english": "This house is good.",
        "explanation": "'pona' as predicate adjective"
    },
    "ike": {
        "toki_pona": "jan ike li kama.",
        "english": "A bad person comes.",
        "explanation": "'ike' as attributive adjective"
    },
    "suli": {
        "toki_pona": "tomo suli li pona.",
        "english": "The big house is good.",
        "explanation": "'suli' describing size"
    },
    "lili": {
        "toki_pona": "jan lili li moku.",
        "english": "The child eats.",
        "explanation": "'lili' can mean small/young"
    },
    "kama": {
        "toki_pona": "mi kama sona.",
        "english": "I am learning.",
        "explanation": "'kama' with 'sona' means 'learn'"
    },
    "tawa": {
        "toki_pona": "mi tawa tomo.",
        "english": "I go to the house.",
        "explanation": "'tawa' as verb of motion"
    },
    "moku": {
        "toki_pona": "mi moku e kili.",
        "english": "I eat fruit.",
        "explanation": "'moku' as verb with object"
    },
    "tomo": {
        "toki_pona": "mi lon tomo.",
        "english": "I am in the house.",
        "explanation": "'tomo' as location"
    },
    "jan": {
        "toki_pona": "jan pona li kama.",
        "english": "A friend comes.",
        "explanation": "'jan pona' means friend"
    },
    "wile": {
        "toki_pona": "mi wile moku.",
        "english": "I want to eat.",
        "explanation": "'wile' as auxiliary verb"
    },
    "sona": {
        "toki_pona": "mi sona toki.",
        "english": "I know how to talk.",
        "explanation": "'sona' with verb"
    },
    "lukin": {
        "toki_pona": "mi lukin e sina.",
        "english": "I see you.",
        "explanation": "'lukin' with direct object"
    },
    "kepeken": {
        "toki_pona": "mi kepeken ilo.",
        "english": "I use a tool.",
        "explanation": "'kepeken' with object"
    },
    "lon": {
        "toki_pona": "mi lon tomo.",
        "english": "I am at home.",
        "explanation": "'lon' for location"
    },
    "tan": {
        "toki_pona": "mi kama tan tomo.",
        "english": "I come from home.",
        "explanation": "'tan' for origin"
    },
    "sama": {
        "toki_pona": "ona li sama mi.",
        "english": "They are like me.",
        "explanation": "'sama' for comparison"
    }
}

# Sitelen Pona characters (basic set)
SITELEN_PONA = {
    "mi": "𝌆",  # Example Unicode character (not actual sitelen pona)
    "sina": "𝌇",
    "ona": "𝌈",
    "ni": "𝌉",
    "pona": "𝌊",
    "ike": "𝌋",
    "suli": "𝌌",
    "lili": "𝌍",
    "kama": "𝌎",
    "tawa": "𝌏",
    "moku": "𝌐",
    "tomo": "𝌑",
    "jan": "𝌒",
    "wile": "𝌓",
    "sona": "𝌔",
    "lukin": "𝌕",
    "kepeken": "𝌖",
    "lon": "𝌗",
    "tan": "𝌘",
    "sama": "𝌙"
}

def get_random_options(correct_answer, num_options=4):
    """Get random options for multiple choice, including the correct answer."""
    options = [correct_answer]
    possible_answers = list(TOKI_PONA_WORDS.values())
    possible_answers.remove(correct_answer)
    options.extend(random.sample(possible_answers, num_options - 1))
    random.shuffle(options)
    return options

def get_new_word(previous_word=None, progress_data=None):
    """Get a new word, prioritizing those that need more practice."""
    available_words = list(TOKI_PONA_WORDS.keys())
    if previous_word in available_words:
        available_words.remove(previous_word)
    
    if progress_data:
        # Sort words by mastery level (lower = needs more practice)
        sorted_words = sorted(available_words, key=lambda w: progress_data.get(w, {}).get('mastery', 0))
        # 70% chance to pick from the bottom half (words that need practice)
        if random.random() < 0.7 and sorted_words:
            return sorted_words[0]
    
    return random.choice(available_words)

def update_progress(word, correct):
    """Update progress for a word based on quiz performance."""
    if 'progress' not in st.session_state:
        st.session_state.progress = {}
    
    if word not in st.session_state.progress:
        st.session_state.progress[word] = {
            'attempts': 0,
            'correct': 0,
            'mastery': 0,
            'last_seen': None
        }
    
    data = st.session_state.progress[word]
    data['attempts'] += 1
    if correct:
        data['correct'] += 1
    data['mastery'] = (data['correct'] / data['attempts']) * 100
    data['last_seen'] = datetime.now().strftime("%Y-%m-%d %H:%M")

def show_progress():
    """Display progress statistics."""
    if 'progress' not in st.session_state:
        st.info("Start practicing to see your progress!")
        return
    
    progress = st.session_state.progress
    
    # Overall statistics
    total_words = len(TOKI_PONA_WORDS)
    words_started = len(progress)
    if words_started > 0:
        avg_mastery = sum(data['mastery'] for data in progress.values()) / words_started
    else:
        avg_mastery = 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Words Started", f"{words_started}/{total_words}")
    with col2:
        st.metric("Average Mastery", f"{avg_mastery:.1f}%")
    with col3:
        mastered = sum(1 for data in progress.values() if data['mastery'] >= 80)
        st.metric("Words Mastered", f"{mastered}/{total_words}")
    
    # Detailed progress
    st.divider()
    st.subheader("Word Progress")
    
    # Create three columns for different mastery levels
    need_practice = []
    learning = []
    mastered_words = []
    
    for word, data in progress.items():
        mastery = data['mastery']
        if mastery < 50:
            need_practice.append((word, data))
        elif mastery < 80:
            learning.append((word, data))
        else:
            mastered_words.append((word, data))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📚 Need Practice")
        for word, data in need_practice:
            st.markdown(f"""
            **{word}** - {TOKI_PONA_WORDS[word]}  
            Mastery: {data['mastery']:.1f}%
            """)
    
    with col2:
        st.markdown("#### 🌱 Learning")
        for word, data in learning:
            st.markdown(f"""
            **{word}** - {TOKI_PONA_WORDS[word]}  
            Mastery: {data['mastery']:.1f}%
            """)
    
    with col3:
        st.markdown("#### ⭐ Mastered")
        for word, data in mastered_words:
            st.markdown(f"""
            **{word}** - {TOKI_PONA_WORDS[word]}  
            Mastery: {data['mastery']:.1f}%
            """)

def create_writing_example(word, size=(300, 100)):
    """Create a simple image showing the word in Latin and sitelen pona."""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw the word in Latin
    draw.text((10, 10), word, fill='black', font=None, size=24)
    
    # Draw the sitelen pona character
    if word in SITELEN_PONA:
        draw.text((10, 50), SITELEN_PONA[word], fill='black', font=None, size=36)
    
    # Convert to base64 for displaying in Streamlit
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def show_writing_system():
    """Display the writing system learning interface."""
    st.header("sitelen pona")
    st.markdown("""
    sitelen pona is the official writing system of Toki Pona. Each word has its own unique symbol!
    
    Here are some key features:
    - Simple, pictographic symbols
    - One symbol per word
    - Can be combined to form compound words
    - Written left to right, top to bottom
    """)
    
    # Word selection
    selected_word = st.selectbox(
        "Choose a word to see its sitelen pona:",
        list(SITELEN_PONA.keys())
    )
    
    if selected_word:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Word")
            st.markdown(f"""
            **{selected_word}**  
            Meaning: {TOKI_PONA_WORDS[selected_word]}
            """)
            
            # Show example sentence
            example = EXAMPLE_SENTENCES[selected_word]
            st.markdown(f"""
            **Example:**  
            {example['toki_pona']}  
            *{example['english']}*
            """)
        
        with col2:
            st.subheader("sitelen pona")
            img_data = create_writing_example(selected_word)
            st.markdown(f'<img src="data:image/png;base64,{img_data}" alt="sitelen pona">', unsafe_allow_html=True)
            
            st.markdown("""
            **Writing Tips:**
            1. Start from the top-left
            2. Keep symbols the same size
            3. Leave space between symbols
            """)
    
    # Practice section
    st.divider()
    st.subheader("Practice")
    st.markdown("""
    Coming soon:
    - Drawing practice with canvas
    - Symbol recognition
    - Compound word creation
    """)

# Initialize session state
if 'current_word' not in st.session_state:
    st.session_state.current_word = get_new_word()
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'current_options' not in st.session_state:
    st.session_state.current_options = None

# Learning mode selection
study_mode = st.radio(
    "sina wile kama sona e seme?",  # What do you want to learn?
    ["nimi lili (Basic Words)", "sitelen pona (Writing System)", "o lukin sona! (Quiz)", "Progress"],
    horizontal=True
)

if study_mode == "Progress":
    show_progress()
elif study_mode == "nimi lili (Basic Words)":
    # Word learning section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Word:")
        st.header(st.session_state.current_word)
        st.write(f"Meaning: {TOKI_PONA_WORDS[st.session_state.current_word]}")
        
        # Add example sentence
        st.divider()
        st.subheader("Example:")
        example = EXAMPLE_SENTENCES[st.session_state.current_word]
        st.markdown(f"""
        🗣️ **{example['toki_pona']}**  
        🌍 *{example['english']}*  
        💡 {example['explanation']}
        """)
        
    with col2:
        if st.button("Next Word"):
            st.session_state.current_word = get_new_word(st.session_state.current_word, st.session_state.get('progress', {}))
            st.rerun()

elif study_mode == "o lukin sona! (Quiz)":
    st.subheader("Test your knowledge!")
    
    # Display score
    st.write(f"Score: {st.session_state.score}/{st.session_state.questions_answered}")
    
    # Display current word
    word = st.session_state.current_word
    correct_meaning = TOKI_PONA_WORDS[word]
    
    # Show the word
    st.write(f"What does '**{word}**' mean?")
    
    if not st.session_state.answered:
        # Generate options only if not already generated
        if st.session_state.current_options is None:
            st.session_state.current_options = get_random_options(correct_meaning)
        
        # Show answer options
        cols = st.columns(2)
        for idx, option in enumerate(st.session_state.current_options):
            col = cols[idx % 2]
            with col:
                if st.button(option, key=f"option_{idx}"):
                    st.session_state.questions_answered += 1
                    correct = option == correct_meaning
                    if correct:
                        st.session_state.score += 1
                        st.session_state.feedback = "✨ Correct! pona!"
                    else:
                        st.session_state.feedback = f"❌ Wrong. The correct meaning is: {correct_meaning}"
                    st.session_state.answered = True
                    update_progress(word, correct)
                    st.rerun()
    else:
        # Show feedback and example sentence
        if st.session_state.feedback:
            if "Correct" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
        
        # Show example after answering
        example = EXAMPLE_SENTENCES[word]
        st.divider()
        st.markdown(f"""
        **Example:**
        🗣️ **{example['toki_pona']}**  
        🌍 *{example['english']}*  
        💡 {example['explanation']}
        """)
        
        if st.button("Next Word →"):
            st.session_state.current_word = get_new_word(st.session_state.current_word, st.session_state.get('progress', {}))
            st.session_state.answered = False
            st.session_state.feedback = None
            st.session_state.current_options = None
            st.rerun()

elif study_mode == "sitelen pona (Writing System)":
    show_writing_system()

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