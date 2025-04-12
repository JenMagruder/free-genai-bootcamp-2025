import streamlit as st
import random
from typing import Dict, List, Tuple

class SentenceGenerator:
    def __init__(self):
        self.vocabulary = {
            'subjects': {
                'mi': 'I',
                'sina': 'you',
                'ona': 'he/she/it'
            },
            'verbs': {
                'moku': 'eat',
                'tawa': 'go/move',
                'lukin': 'see/look',
                'pali': 'work/make'
            },
            'objects': {
                'kili': 'fruit',
                'telo': 'water',
                'moku': 'food',
                'tomo': 'house'
            }
        }
        
        self.patterns = [
            "{subject} {verb}",
            "{subject} {verb} {object}",
            "{subject} {verb} lon {location}"
        ]
    
    def generate_sentence(self) -> Tuple[str, str]:
        pattern = random.choice(self.patterns)
        
        # Select random words
        subject = random.choice(list(self.vocabulary['subjects'].items()))
        verb = random.choice(list(self.vocabulary['verbs'].items()))
        obj = random.choice(list(self.vocabulary['objects'].items()))
        
        # Create sentences
        toki_sentence = pattern.format(
            subject=subject[0],
            verb=verb[0],
            object=obj[0]
        )
        
        eng_sentence = pattern.format(
            subject=subject[1],
            verb=verb[1],
            object=obj[1]
        )
        
        return toki_sentence, eng_sentence

def main():
    st.title("Toki Pona Sentence Practice")
    st.markdown("""
    Practice creating and translating simple Toki Pona sentences.
    The generator will create sentences using basic vocabulary and patterns.
    """)

    # Initialize generator
    if 'generator' not in st.session_state:
        st.session_state.generator = SentenceGenerator()
        st.session_state.current_sentences = None
        st.session_state.show_translation = False

    # Generate new sentence button
    if st.button("Generate New Sentence"):
        st.session_state.current_sentences = st.session_state.generator.generate_sentence()
        st.session_state.show_translation = False

    # Display current sentence
    if st.session_state.current_sentences:
        st.markdown("### Toki Pona Sentence:")
        st.write(st.session_state.current_sentences[0])
        
        # Show/Hide translation
        if st.button("Show/Hide Translation"):
            st.session_state.show_translation = not st.session_state.show_translation
        
        if st.session_state.show_translation:
            st.markdown("### English Translation:")
            st.write(st.session_state.current_sentences[1])

    # Vocabulary reference in sidebar
    st.sidebar.markdown("### Vocabulary Reference")
    for category, words in st.session_state.generator.vocabulary.items():
        st.sidebar.markdown(f"#### {category.title()}")
        for toki, eng in words.items():
            st.sidebar.write(f"{toki}: {eng}")

if __name__ == "__main__":
    main()
