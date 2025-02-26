# Writing Practice Setup Guide

## Prerequisites

Before setting up the project, ensure you have the following installed:

1. **Python 3.8 or higher**
2. **Flask backend server** (`lang-portal-flask-react`) running on port `5000`
3. **All required Python packages** installed

---

## Setup Instructions

### Step 1: Start the Flask Backend Server

1. Navigate to the `lang-portal-flask-react` directory:
   ```bash
   cd ../lang-portal-flask-react
   ```
2. Follow the backend setup instructions to run the Flask server.
3. Ensure the server is running at: [http://localhost:5000](http://localhost:5000)

---

### Step 2: Deploy `writing-practice`

#### 1. Create a Virtual Environment
```bash
python -m venv venv
```

#### 2. Activate the Virtual Environment

- **For Windows (Command Prompt):**
  ```bash
  venv\Scripts\activate
  ```
- **For Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\activate
  ```

#### 3. Navigate to the Project Directory
```bash
cd writing-practice
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Install Streamlit (if not included in `requirements.txt`)
```bash
pip install streamlit
```

#### 6. Set OpenAI API Key

- **For Windows (Command Prompt):**
  ```bash
  set OPENAI_API_KEY=your-api-key-here
  ```
- **For Windows (PowerShell):**
  ```powershell
  $env:OPENAI_API_KEY = "your-api-key-here"
  ```
