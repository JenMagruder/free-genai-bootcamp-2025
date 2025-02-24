### Deploy

## Create virtual environment
python -m venv venv

## Activate it (Windows)
venv\Scripts\activate

## Install the dependencies:
$ cd writing-practice
$ pip install -r requirements.txt

## Set your OpenAI API Key as an environment variable:
# https://platform.openai.com/signup
# Windows Command Prompt
set OPENAI_API_KEY=your-api-key-here

## Windows PowerShell
$ env:OPENAI_API_KEY = "your-api-key-here"

### Run the Streamlit app:
streamlit run app.py
### For word practice:
python gradio_word.py
### For sentence practice:
python gradio_app.py


# bTo stop the Streamlit app, you can:

Press Ctrl+C in the terminal/command prompt where the app is running