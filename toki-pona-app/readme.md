# Toki Pona Learning App

An interactive web application for learning Toki Pona, a minimalist constructed language designed to simplify thoughts and communication.

## Overview

Toki Pona is a philosophical constructed language known for its simplicity, with only 120-125 root words. This app helps users learn the language through interactive exercises and visual aids.

## Features

- Interactive word learning with English translations
- Sitelen Pona writing system visualization
- Example sentences for context
- Progress tracking for learned words
- Quiz functionality to test knowledge

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/free-genai-bootcamp-2025.git
cd toki-pona-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install streamlit pillow python-dotenv
```

4. Run the application:
```bash
streamlit run app/000_learn_tokipana.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
toki-pona-app/
├── app/
│   ├── 000_learn_tokipana.py    # Main application file
│   └── requirement.txt           # Python dependencies
└── README.md                    # Documentation
```

## Usage

1. **Word Learning**: Browse through Toki Pona words and their English translations
2. **Writing System**: Explore the sitelen pona writing system
3. **Practice**: Use example sentences and quizzes to test your knowledge
4. **Track Progress**: Monitor your learning progress through the built-in tracking system

## Usage Guide

### 1. Word Learning
- Browse through the vocabulary list
- Click on words to see detailed translations
- Practice with example sentences
- Take quizzes to test your knowledge

### 2. Writing System
- Study the sitelen pona characters
- Practice writing system recognition
- Learn symbol combinations
- View example usage

### 3. Progress Tracking
- Monitor your learning progress
- Review mastered words
- Identify areas needing practice
- Track quiz scores

## Troubleshooting

### Common Issues

1. **Streamlit Port Already in Use**
   - Kill the existing process
   - Use a different port: `streamlit run app/000_learn_tokipana.py --server.port=8502`

2. **Package Installation Issues**
   - Ensure virtual environment is activated
   - Update pip: `python -m pip install --upgrade pip`
   - Install packages individually if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Acknowledgments

- Toki Pona created by Sonja Lang
- Built with Streamlit framework
- Submitted for GenAI Bootcamp 2025 by ExamPro
