import streamlit as st
import requests
from enum import Enum
import json
from typing import Optional, List, Dict
import openai
import logging
import random
import os

# Setup Custom Logging -----------------------
# Create a custom logger for your app only
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# Remove any existing handlers to prevent duplicate logging
if logger.hasHandlers():
    logger.handlers.clear()

# Create file handler
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - MY_APP - %(message)s')
fh.setFormatter(formatter)

# Add handler to logger
logger.addHandler(fh)

# Prevent propagation to root logger
logger.propagate = False

# State Management
class AppState(Enum):
    SETUP = "setup"
    PRACTICE = "practice"
    REVIEW = "review"

class JapaneseLearningApp:
    def __init__(self):
        logger.debug("Initializing Japanese Learning App...")
        self.initialize_session_state()
        self.load_vocabulary()

    def initialize_session_state(self):
        """Initialize or get session state variables"""
        if 'app_state' not in st.session_state:
            st.session_state.app_state = AppState.SETUP
        if 'current_sentence' not in st.session_state:
            st.session_state.current_sentence = ""
        if 'review_data' not in st.session_state:
            st.session_state.review_data = None

    def load_vocabulary(self):
        """Fetch vocabulary from API using group_id from query parameters"""
        # Define default vocabulary
        default_vocab = {
            "group_name": "Default Japanese Vocabulary",
            "words": [
                {"id": 1, "kanji": "本", "hiragana": "ほん", "reading": "hon", "english": "book"},
                {"id": 2, "kanji": "水", "hiragana": "みず", "reading": "mizu", "english": "water"},
                {"id": 3, "kanji": "食べる", "hiragana": "たべる", "reading": "taberu", "english": "to eat"},
                {"id": 4, "kanji": "猫", "hiragana": "ねこ", "reading": "neko", "english": "cat"},
                {"id": 5, "kanji": "犬", "hiragana": "いぬ", "reading": "inu", "english": "dog"},
                {"id": 6, "kanji": "行く", "hiragana": "いく", "reading": "iku", "english": "to go"}
            ]
        }

        try:
            # Get group_id from query parameters
            group_id = st.query_params.get('group_id', '')

            if not group_id:
                logger.info("No group_id provided, using default vocabulary")
                self.vocabulary = default_vocab
                return

            # Make API request with the actual group_id
            url = f'http://localhost:5000/api/groups/{group_id}/words/raw'
            logger.debug(url)
            response = requests.get(url)
            logger.debug(f"Response status: {response.status_code}")

            # Check if response is successful and contains data
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data and data.get('words'):
                        logger.debug(f"Received data for group: {data.get('group_name', 'unknown')}") 
                        self.vocabulary = data
                    else:
                        logger.warning("Received empty data from API, using default vocabulary")
                        self.vocabulary = default_vocab
                except Exception as e:
                    logger.error(f"Error parsing API response: {str(e)}")
                    self.vocabulary = default_vocab
            else:
                logger.warning(f"API request failed, using default vocabulary")
                self.vocabulary = default_vocab
        except Exception as e:
            logger.error(f"Error in load_vocabulary: {str(e)}")
            self.vocabulary = default_vocab

    def generate_sentence(self, word: dict) -> str:
        """Generate a sentence using OpenAI API"""
        try:
            kanji = word.get('kanji', '')
            logger.debug(f"Generating sentence for word: {kanji}")

            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                error_msg = "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
                logger.error(error_msg)
                return error_msg

            # Create client with explicit api_key
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            prompt = f"""Generate a simple Japanese sentence using the word '{kanji}'.
            The grammar should be scoped to JLPTN5 grammar.
            You can use the following vocabulary to construct a simple sentence:
            - simple objects eg. book, car, ramen, sushi
            - simple verbs, to drink, to eat, to meet
            - simple times eg. tomorrow, today, yesterday

            Please provide the response in this format:
            Japanese: [sentence in kanji/hiragana]
            English: [English translation]
            """

            logger.debug("Sending request to OpenAI API")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.debug("Received response from OpenAI API")
            result = response.choices[0].message.content.strip()
            logger.debug(f"Generated sentence: {result}")
            return result
        except Exception as e:
            error_msg = f"Error generating sentence: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def grade_submission(self, image) -> Dict:
        """Process image submission and grade it"""
        # TODO: Implement MangaOCR integration
        # For now, return mock data
        return {
            "transcription": "今日はラーメンを食べます",
            "translation": "I will eat ramen today",
            "grade": "S",
            "feedback": "Excellent work! The sentence accurately conveys the meaning."
        }

    def render_setup_state(self):
        """Render the setup state UI"""
        logger.debug("Entering render_setup_state")
        st.title("Japanese Writing Practice")

        if not self.vocabulary:
            logger.debug("No vocabulary loaded")
            st.warning("No vocabulary loaded. Please make sure a valid group_id is provided.")
            return

        # Add key to button to ensure proper state management
        generate_button = st.button("Generate Sentence", key="generate_sentence_btn")
        logger.debug(f"Generate button state: {generate_button}")

        if generate_button:
            logger.info("Generate button clicked")
            # Pick a random word from vocabulary
            if not self.vocabulary.get('words'):
                st.error("No words found in the vocabulary group")
                return

            word = random.choice(self.vocabulary['words'])
            logger.debug(f"Selected word: {word.get('english')} - {word.get('kanji')}")

            # Generate and display the sentence
            sentence = self.generate_sentence(word)
            st.markdown("### Generated Sentence")
            if sentence.startswith("Error"):
                st.error(sentence)
            else:
                st.write(sentence)

            # Store the current sentence
            st.session_state.current_sentence = sentence

            # Add a continue button
            if st.button("Continue to Practice", key="continue_btn"):
                st.session_state.app_state = AppState.PRACTICE
                st.experimental_rerun()

    def render_practice_state(self):
        """Render the practice state UI"""
        st.title("Practice Japanese")
        st.write(f"English Sentence: {st.session_state.current_sentence}")

        uploaded_file = st.file_uploader("Upload your written Japanese", type=['png', 'jpg', 'jpeg'])

        if st.button("Submit for Review") and uploaded_file:
            st.session_state.review_data = self.grade_submission(uploaded_file)
            st.session_state.app_state = AppState.REVIEW
            st.experimental_rerun()

    def render_review_state(self):
        """Render the review state UI"""
        st.title("Review")
        st.write(f"English Sentence: {st.session_state.current_sentence}")

        review_data = st.session_state.review_data
        st.subheader("Your Submission")
        st.write(f"Transcription: {review_data['transcription']}")
        st.write(f"Translation: {review_data['translation']}")
        st.write(f"Grade: {review_data['grade']}")
        st.write(f"Feedback: {review_data['feedback']}")

        if st.button("Next Question"):
            st.session_state.app_state = AppState.SETUP
            st.session_state.current_sentence = ""
            st.session_state.review_data = None
            st.experimental_rerun()

    def run(self):
        """Main app loop"""
        print("Running main app loop")
        if st.session_state.app_state == AppState.SETUP:
            self.render_setup_state()
        elif st.session_state.app_state == AppState.PRACTICE:
            self.render_practice_state()
        elif st.session_state.app_state == AppState.REVIEW:
            self.render_review_state()

# Run the app
if __name__ == "__main__":
    # Add custom CSS with purple background
    st.markdown("""
        <style>
        .stApp {
            background-color: #9C27B0;
            background: linear-gradient(135deg, #9C27B0 0%, #673AB7 100%);
        }
        .stMarkdown, .stButton, div[data-testid="stFileUploader"] {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
        }
        .stMarkdown {
            color: white !important;
        }
        h1, h2, h3 {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    app = JapaneseLearningApp()
    app.run()
