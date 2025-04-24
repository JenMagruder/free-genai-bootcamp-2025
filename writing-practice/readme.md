# Japanese Writing Practice App

An AI-powered application for practicing Japanese writing through interactive exercises and automated grading.

## 🎯 Features

- **Sentence Generation**
  - AI-generated practice sentences
  - JLPT N5 grammar level
  - Contextual vocabulary usage
  - Progressive difficulty

- **Writing Practice**
  - Image upload for handwritten text
  - Real-time OCR transcription
  - Automated grading system
  - Instant feedback

- **Learning Tools**
  - Translation assistance
  - Grammar explanations
  - Vocabulary suggestions
  - Progress tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Flask backend server (`lang-portal-flask-react`) running on port 5000

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/JenMagruder/free-genai-bootcamp-2025.git
cd writing-practice
```

2. **Set up Python environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Start the backend server**
```bash
# In a separate terminal
cd ../lang-portal-flask-react
# Follow backend setup instructions
```

4. **Run the application**
```bash
# Choose one:
streamlit run app.py        # Streamlit interface
python gradio_app.py       # Gradio interface
```

## 📱 Application Flow

### 1. Setup State
- Initial screen with "Generate Sentence" button
- Click generates a practice sentence
- Transitions to Practice State

### 2. Practice State
- Displays English sentence for translation
- Provides image upload field
- Submit button for grading
- Transitions to Review State on submission

### 3. Review State
- Shows original English sentence
- Displays OCR transcription
- Shows Japanese translation
- Provides grading and feedback
- "Next Question" button for new practice

## 🔧 Technical Architecture

### Components
- **Frontend**: Streamlit/Gradio
- **Backend**: Flask API
- **OCR**: MangaOCR
- **LLM**: GPT for sentence generation and grading
- **Storage**: Local file system

### API Integration
- Fetches word groups from `/api/groups/:id/raw`
- Stores vocabulary in memory
- Communicates with Flask backend for processing

### AI Components
1. **Sentence Generator**
   - Uses LLM for contextual sentences
   - JLPT N5 grammar scope
   - Controlled vocabulary difficulty

2. **Grading System**
   - OCR transcription
   - Translation verification
   - Accuracy scoring (S-Rank system)
   - Feedback generation

## 📁 Project Structure
```
writing-practice/
├── app.py              # Streamlit application
├── gradio_app.py       # Gradio interface
├── gradio_word.py      # Word processing
├── print.py            # Print utilities
├── prompts.yaml        # LLM prompts
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Submit pull request

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](../toki-pona-ocr/CONTRIBUTING.md) for details.

## 📝 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- Andrew Brown and ExamPro for the FREE GenAI Bootcamp
- Japanese language community for resources
- All sponsors who made this possible
