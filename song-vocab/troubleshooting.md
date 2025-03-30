# Troubleshooting Guide - Song Lyrics API Project

## Known Issues and Solutions

### 1. SERP API Integration Issues
- **Problem**: Empty results from search_web_serp
- **Cause**: API key configuration or rate limiting
- **Solution**: 
  - Verify SERP_API_KEY in .env file
  - Check API quota and usage
  - Add debug logging to search_web_serp.py

### 2. LLM Model Issues
- **Problem**: Model trying to use non-existent tools
- **Cause**: Unclear tool specifications in system prompt
- **Solution**:
  - Updated system prompt with explicit tool formats
  - Added stricter tool parsing in agent.py
  - Improved error handling for unknown tools

### 3. Japanese Text Handling
- **Problem**: Character encoding issues with Japanese lyrics
- **Cause**: UTF-8 encoding not properly maintained
- **Solution**:
  - Added ensure_ascii=False to JSON operations
  - Set proper content-type headers
  - Used proper encoding in file operations

### 4. Async/Await Implementation
- **Problem**: Inconsistent async handling
- **Cause**: Mixed sync/async code
- **Solution**:
  - Properly chained async operations
  - Added proper error handling for async functions
  - Fixed conversation flow in agent.py

### 5. Environment Setup
- **Problem**: Virtual environment activation issues
- **Solution**:
  ```powershell
  # Create new environment
  python -m venv venv311
  
  # Activate environment
  .\venv311\Scripts\activate
  
  # Install dependencies
  pip install -r requirements.txt


