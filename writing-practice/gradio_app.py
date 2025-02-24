import gradio as gr
import requests
import json
import random
import logging
from openai import OpenAI
import os
import dotenv
import yaml

dotenv.load_dotenv()

def load_prompts():
    """Load prompts from YAML file"""
    with open('prompts.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Setup logging
logger = logging.getLogger('japanese_app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('gradio_app.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class JapaneseWritingApp:
    def __init__(self):
        self.client = OpenAI()
        self.vocabulary = None
        self.current_word = None
        self.current_sentence = None
        self.mocr = None
        self.load_vocabulary()

    def load_vocabulary(self):
        """Fetch vocabulary from API using group_id"""
        try:
            # Get group_id from environment variable or use default
            group_id = os.getenv('GROUP_ID', '1')
            url = f"http://localhost:5000/api/groups/{group_id}/words/raw"
            logger.debug(f"Fetching vocabulary from: {url}")
            
            response = requests.get(url)
            if response.status_code == 200:
                self.vocabulary = response.json()
                logger.info(f"Loaded {len(self.vocabulary.get('words', []))} words")
            else:
                logger.error(f"Failed to load vocabulary. Status code: {response.status_code}")
                self.vocabulary = {"words": []}
        except Exception as e:
            logger.error(f"Error loading vocabulary: {str(e)}")
            self.vocabulary = {"words": []}

    def generate_sentence(self, word):
        """Generate a sentence using OpenAI API"""
        logger.debug(f"Generating sentence for word: {word.get('kanji', '')}")
        
        try:
            prompts = load_prompts()
            messages = [
                {"role": "system", "content": prompts['sentence_generation']['system']},
                {"role": "user", "content": prompts['sentence_generation']['user'].format(word=word.get('kanji', ''))}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            sentence = response.choices[0].message.content.strip()
            logger.info(f"Generated sentence: {sentence}")
            return sentence
        except Exception as e:
            logger.error(f"Error generating sentence: {str(e)}")
            return "Error generating sentence. Please try again."

    def get_random_word_and_sentence(self):
        """Get a random word and generate a sentence"""
        logger.debug("Getting random word and generating sentence")
        
        if not self.vocabulary or not self.vocabulary.get('words'):
            return "No vocabulary loaded", "", "", "Please make sure vocabulary is loaded properly."
            
        self.current_word = random.choice(self.vocabulary['words'])
        self.current_sentence = self.generate_sentence(self.current_word)
        
        return (
            self.current_sentence,
            f"English: {self.current_word.get('english', '')}",
            f"Kanji: {self.current_word.get('kanji', '')}",
            f"Reading: {self.current_word.get('reading', '')}"
        )

    def grade_submission(self, image):
        """Process image submission and grade it using MangaOCR and LLM"""
        try:
            # Initialize MangaOCR for transcription if not already initialized
            if self.mocr is None:
                logger.info("Initializing MangaOCR")
                from manga_ocr import MangaOcr
                self.mocr = MangaOcr()
            
            # Transcribe the image
            logger.info("Transcribing image with MangaOCR")
            transcription = self.mocr(image)
            logger.debug(f"Transcription result: {transcription}")
            
            # Load prompts
            prompts = load_prompts()
            
            # Get literal translation
            logger.info("Getting literal translation")
            translation_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompts['translation']['system']},
                    {"role": "user", "content": prompts['translation']['user'].format(text=transcription)}
                ],
                temperature=0.3
            )
            translation = translation_response.choices[0].message.content.strip()
            logger.debug(f"Translation: {translation}")
            
            # Get grading and feedback
            logger.info("Getting grade and feedback")
            grading_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompts['grading']['system']},
                    {"role": "user", "content": prompts['grading']['user'].format(
                        target_sentence=self.current_sentence,
                        submission=transcription,
                        translation=translation
                    )}
                ],
                temperature=0.3
            )
            
            feedback = grading_response.choices[0].message.content.strip()
            # Parse grade and feedback from response
            grade = 'C'  # Default grade
            if 'Grade: S' in feedback:
                grade = 'S'
            elif 'Grade: A' in feedback:
                grade = 'A'
            elif 'Grade: B' in feedback:
                grade = 'B'
            
            # Extract just the feedback part
            feedback = feedback.split('Feedback:')[-1].strip()
            
            logger.info(f"Grading complete: {grade}")
            logger.debug(f"Feedback: {feedback}")
            
            return transcription, translation, grade, feedback
            
        except Exception as e:
            logger.error(f"Error in grade_submission: {str(e)}")
            return "Error processing submission", "Error processing submission", "C", f"An error occurred: {str(e)}"

def create_ui():
    app = JapaneseWritingApp()
    
    # Custom CSS for larger text
    custom_css = """
    .large-text-output textarea {
        font-size: 40px !important;
        line-height: 1.5 !important;
        font-family: 'Noto Sans JP', sans-serif !important;
    }
    """
    
    with gr.Blocks(
        title="Japanese Writing Practice",
        css=custom_css
    ) as interface:
        gr.Markdown("# Japanese Writing Practice")
        
        with gr.Row():
            with gr.Column():
                generate_btn = gr.Button("Generate New Sentence", variant="primary")
                # Make sentence output more prominent with larger text and more lines
                sentence_output = gr.Textbox(
                    label="Generated Sentence",
                    lines=3,
                    scale=2,  # Make the component larger
                    show_label=True,
                    container=True,
                    # Add custom CSS for larger text
                    elem_classes=["large-text-output"]
                )
                word_info = gr.Markdown("### Word Information")
                english_output = gr.Textbox(label="English", interactive=False)
                kanji_output = gr.Textbox(label="Kanji", interactive=False)
                reading_output = gr.Textbox(label="Reading", interactive=False)
            
            with gr.Column():
                image_input = gr.Image(label="Upload your handwritten sentence", type="filepath")
                submit_btn = gr.Button("Submit", variant="secondary")
                
                with gr.Group():
                    gr.Markdown("### Feedback")
                    transcription_output = gr.Textbox(
                        label="Transcription",
                        lines=3,
                        scale=2,
                        show_label=True,
                        container=True,
                        elem_classes=["large-text-output"]
                    )
                    translation_output = gr.Textbox(label="Translation", lines=2)
                    grade_output = gr.Textbox(label="Grade")
                    feedback_output = gr.Textbox(label="Feedback", lines=3)

        # Event handlers
        generate_btn.click(
            fn=app.get_random_word_and_sentence,
            outputs=[sentence_output, english_output, kanji_output, reading_output]
        )
        
        def handle_submission(image):
            return app.grade_submission(image)
            
        submit_btn.click(
            fn=handle_submission,
            inputs=[image_input],
            outputs=[transcription_output, translation_output, grade_output, feedback_output]
        )

    return interface

if __name__ == "__main__":
    interface = create_ui()
    interface.launch(server_name="0.0.0.0", server_port=8081)