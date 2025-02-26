1. Python 3.8 or higher installed
2. The Flask backend server (lang-portal-flask-react) running on port 5000
3. All required Python packages installed

## Setup Instructions

1. First, start the Flask backend server:
   ```bash
   # Navigate to the lang-portal-flask-react directory and start the server
   cd ../lang-portal-flask-react
   # Follow the backend setup instructions to run the Flask server
   # The server should be running on http://localhost:5000

### Deploy writing-practice
# Step 1: Create virtual environment
python -m venv venv

# Step 2: Activate virtual environment (choose appropriate command for your shell)
# For Windows Command Prompt:
venv\Scripts\activate
# For Windows PowerShell:
# .\venv\Scripts\activate

# Step 3: Navigate to project directory
cd writing-practice

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Install Streamlit (if not included in requirements.txt)
pip install streamlit

# Step 6: Set OpenAI API Key
# For Windows Command Prompt:
set OPENAI_API_KEY=your-api-key-here
# For Windows PowerShell:
# $env:OPENAI_API_KEY = "your-api-key-here"

# Step 7: Run one of the applications
# For the main Streamlit application:
streamlit run app.py -- --group_id=1
# For word practice:
python gradio_word.py
# For sentence practice:
python gradio_app.py

# Step 8: To stop the application
# Press Ctrl+C in the terminal/command prompt where the app is running
