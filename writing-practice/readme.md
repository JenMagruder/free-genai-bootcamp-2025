# Japanese Writing Practice App

AI-powered application for practicing Japanese writing through interactive exercises and automated grading.

## Features

**Sentence Generation:** AI-generated practice sentences at JLPT N5 grammar level with contextual vocabulary usage and progressive difficulty.

**Writing Practice:** Image upload for handwritten text with real-time OCR transcription, automated grading system, and instant feedback.

**Learning Tools:** Translation assistance, grammar explanations, vocabulary suggestions, and progress tracking.

## Quick Start

**Prerequisites:** Python 3.8+, pip, Git, Flask backend server (lang-portal-flask-react) running on port 5000

**Installation:**

```bash
# Clone repository
git clone https://github.com/JenMagruder/free-genai-bootcamp-2025.git
cd writing-practice

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

**Start backend server:**
```bash
# In separate terminal
cd ../lang-portal-flask-react
# Follow backend setup instructions
```

**Run application:**
```bash
streamlit run app.py      # Streamlit interface
# or
python gradio_app.py     # Gradio interface
```

## Application Flow

**Setup State:** Initial screen with "Generate Sentence" button. Click generates practice sentence and transitions to Practice State.

**Practice State:** Displays English sentence for translation, provides image upload field, submit button for grading. Transitions to Review State on submission.

**Review State:** Shows original English sentence, OCR transcription, Japanese translation, grading and feedback. "Next Question" button for new practice.

## Technical Architecture

**Components:** Streamlit/Gradio frontend, Flask API backend, MangaOCR for handwriting recognition, GPT for sentence generation and grading, local file system storage.

**API Integration:** Fetches word groups from `/api/groups/:id/raw`, stores vocabulary in memory, communicates with Flask backend for processing.

**AI Components:** Sentence Generator uses LLM for contextual sentences at JLPT N5 grammar scope with controlled vocabulary difficulty. Grading System performs OCR transcription, translation verification, accuracy scoring (S-Rank system), and feedback generation.

## Project Structure

```
writing-practice/
├── app.py
├── gradio_app.py
├── gradio_word.py
├── print.py
├── prompts.yaml
├── requirements.txt
└── README.md
```

## Development

**Tests:** `python -m pytest tests/`

**Adding Features:** Create feature branch, implement changes, add tests, submit pull request.

## Contributing

Contributions welcome. Read Contributing Guidelines for details.

## License

MIT License - See LICENSE file for details.

## Acknowledgments

Andrew Brown and ExamPro for the FREE GenAI Bootcamp, Japanese language community for resources, all sponsors who made this possible.
