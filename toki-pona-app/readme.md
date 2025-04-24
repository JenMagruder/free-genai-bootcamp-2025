# Toki Pona Learning App

An interactive web application for learning Toki Pona, a minimalist constructed language designed to simplify thoughts and communication.

## 🎯 Features

- **Interactive Word Learning**
  - English to Toki Pona translations
  - Toki Pona to English translations
  - Visual learning with Sitelen Pona script
  - Progress tracking for vocabulary

- **Learning Tools**
  - Example sentences for context
  - Quiz functionality
  - Instant feedback
  - Visual aids and mnemonics

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/JenMagruder/free-genai-bootcamp-2025.git
cd toki-pona-app
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

3. **Run the application**
```bash
streamlit run app/000_learn_tokipana.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
toki-pona-app/
├── app/
│   ├── 000_learn_tokipana.py    # Main application
│   ├── 00_tokipona_eng          # Toki Pona to English data
│   ├── 01_eng_tokipona          # English to Toki Pona data
│   ├── config.py                # Configuration settings
│   ├── inference.py             # Model inference
│   ├── init_streamlit_app.py    # App initialization
│   ├── ocr_model.py            # OCR model implementation
│   ├── preload_model.py        # Model loading utilities
│   └── train_ocr.py            # Model training script
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation
```

## 🛠️ Development

### Running Tests
```bash
python -m pytest app/tests/
```

### Adding New Features
1. Create a new branch
2. Implement your feature
3. Add tests
4. Submit a pull request

## 🔧 Technical Details

### Application Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **ML Models**: PyTorch
- **Data Storage**: Local files

### Model Architecture
- OCR model based on ResNet34
- Siamese Neural Network for symbol recognition
- Pre-trained on ImageNet

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](../toki-pona-ocr/CONTRIBUTING.md) for details on how to submit pull requests.

## 📝 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- Andrew Brown and ExamPro for the FREE GenAI Bootcamp
- Toki Pona community for resources and feedback
- All sponsors who made this possible
