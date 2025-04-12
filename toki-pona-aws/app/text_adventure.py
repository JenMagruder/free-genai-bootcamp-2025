import streamlit as st
import random

# Dictionary of Toki Pona words with translations and categories
TOKI_PONA_DICT = {
    'mi': {'translation': 'I/me', 'category': 'pronoun'},
    'sina': {'translation': 'you', 'category': 'pronoun'},
    'ona': {'translation': 'he/she/it', 'category': 'pronoun'},
    'pona': {'translation': 'good/simple', 'category': 'adjective'},
    'ike': {'translation': 'bad/complex', 'category': 'adjective'},
    'suli': {'translation': 'big/important', 'category': 'adjective'},
    'lili': {'translation': 'small/little', 'category': 'adjective'},
    'tomo': {'translation': 'house/building', 'category': 'noun'},
    'ma': {'translation': 'land/country', 'category': 'noun'},
    'moku': {'translation': 'food/eat', 'category': 'noun/verb'},
    'tawa': {'translation': 'to/towards/walk', 'category': 'preposition/verb'}
}

# Game states and their descriptions
GAME_STATES = {
    'start': {
        'description': 'You find yourself in a small village (ma lili). The sun is setting, and you need to find shelter.',
        'options': {
            'tomo': 'Go to the nearby house',
            'ma': 'Explore the village',
            'moku': 'Look for food'
        }
    },
    'tomo': {
        'description': 'You approach a cozy house (tomo pona). The owner greets you.',
        'options': {
            'pona': 'Be friendly and greet back',
            'tawa': 'Walk away',
            'moku': 'Ask for food'
        }
    },
    'ma': {
        'description': 'The village (ma) is peaceful. You see people going about their day.',
        'options': {
            'tomo': 'Return to the house',
            'moku': 'Visit the food market',
            'tawa': 'Keep walking'
        }
    },
    'moku': {
        'description': 'You find a small market with fresh food (moku pona).',
        'options': {
            'pona': 'Thank the vendor',
            'tomo': 'Take food home',
            'tawa': 'Look elsewhere'
        }
    }
}

def initialize_game():
    """Initialize game state if not already done"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'start'
        st.session_state.learned_words = set()
        st.session_state.score = 0

def update_score(word):
    """Update score when player learns new words"""
    if word not in st.session_state.learned_words:
        st.session_state.score += 10
        st.session_state.learned_words.add(word)

def display_translation(text):
    """Display Toki Pona text with translations"""
    words = text.split()
    translated = []
    for word in words:
        word = word.lower()
        if word in TOKI_PONA_DICT:
            update_score(word)
            translated.append(f"{word} ({TOKI_PONA_DICT[word]['translation']})")
        else:
            translated.append(word)
    return ' '.join(translated)

def display_state(state):
    """Display current game state with translations"""
    st.markdown("---")
    st.markdown("### Current Location")
    st.write(display_translation(GAME_STATES[state]['description']))
    
    st.markdown("### Available Actions")
    options = GAME_STATES[state]['options']
    choice = st.radio(
        "What would you like to do?",
        list(options.keys()),
        format_func=lambda x: f"{x} - {TOKI_PONA_DICT[x]['translation']}: {options[x]}"
    )
    
    if st.button("Take Action"):
        st.session_state.game_state = choice
        st.experimental_rerun()

def display_vocabulary():
    """Display learned vocabulary"""
    st.sidebar.markdown("### Learned Words")
    st.sidebar.markdown(f"Score: {st.session_state.score}")
    
    if st.session_state.learned_words:
        for word in sorted(st.session_state.learned_words):
            st.sidebar.markdown(
                f"- **{word}** ({TOKI_PONA_DICT[word]['translation']}) - "
                f"_{TOKI_PONA_DICT[word]['category']}_"
            )

def main():
    st.title("Toki Pona Text Adventure")
    st.markdown("""
    Welcome to the Toki Pona learning adventure! Explore the village, interact with people,
    and learn Toki Pona words along the way. Each new word you encounter will be added to
    your vocabulary list.
    
    *Tip: Pay attention to the translations in parentheses to learn new words!*
    """)
    
    initialize_game()
    display_state(st.session_state.game_state)
    display_vocabulary()

if __name__ == "__main__":
    main()
