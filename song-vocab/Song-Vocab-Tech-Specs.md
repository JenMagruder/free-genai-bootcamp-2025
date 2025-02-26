# Tech Specs

## Business Goal
We want to create a program that will find lyrics off the internet for a target song in a specific langauge and produce vocabulary to be imported into our database.

## Technical Requirements

- FastAPI
- Ollama via the Ollama Python SDK
    - Mistral 7B
- Instructor (for structured json output)
- SQLite3 (for database)
- duckduckgo-search (to search for lyrics)

## API Endpoints

### GetLyrics POST /api/agent 

### Behaviour

This endpoint goes to our agent which is uses the reAct framework
so that it can go to the internet, find multiple possible version of lyrics
and then extract out the correct lyrics and format the lyrics into vocaulary.

Tools avaliable:
- tools/extract_vocabulary.py
- tools/get_page_content.py
- tools/search_web.py

### JSON Request Parameters
- `message_request` (str): A string that describes the song and/or artist to get lyrics for a song from the ineternet

### JSON Response
- `lyrics` (str): The lyrics of the song
- `vocabulary` (list): A list of vocabulary words found in the lyrics