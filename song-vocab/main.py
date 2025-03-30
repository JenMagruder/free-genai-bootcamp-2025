from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import json
import logging
from pathlib import Path
from agent import SongLyricsAgent
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set default level to INFO
    format='%(message)s'  # Simplified format for better readability
)

# Configure specific loggers
logger = logging.getLogger('song_vocab')  # Root logger for our app
logger.setLevel(logging.DEBUG)

# Silence noisy third-party loggers
for noisy_logger in ['httpcore', 'httpx', 'urllib3']:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Song Vocab API",
        "endpoints": {
            "/api/agent": "POST - Find lyrics and generate vocabulary"
        }
    }

class LyricsRequest(BaseModel):
    message_request: str

@app.post("/api/agent")
async def get_lyrics(request: LyricsRequest) -> JSONResponse:
    """Process a lyrics request through the agent."""
    try:
        logger.info(f"Received request: {request.message_request}")
        # Initialize agent
        logger.debug("Initializing SongLyricsAgent")
        agent = SongLyricsAgent(stream_llm=False, available_ram_gb=16)
        
        # Process request
        logger.info("Processing request through agent")
        system_prompt = """You are a helpful AI assistant that helps find Japanese song lyrics and extract Japanese vocabulary from them.

IMPORTANT: You can ONLY use these exact tools:
1. search_web_serp(query: str) - Search for Japanese song lyrics
2. get_page_content(url: str) - Extract content from a webpage
3. extract_vocabulary(text: str) - Extract Japanese vocabulary
4. generate_song_id(title: str) - Generate URL-safe song ID
5. save_results(song_id: str, lyrics: str, vocabulary: List[Dict]) - Save results

DO NOT try to use any other tools. Follow these steps:
1. Use search_web_serp to find the lyrics
2. Use get_page_content to extract the lyrics
3. Use extract_vocabulary to analyze the lyrics
4. Use generate_song_id to create an ID
5. Use save_results to store everything

End your response with FINISHED when done."""

        conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message_request}
        ]
        
        song_id = await agent.process_request(conversation)
        logger.info(f"Got song_id: {song_id}")
        
        # Read the stored files
        lyrics_file = Path(agent.lyrics_path) / f"{song_id}.txt"
        vocab_file = Path(agent.vocabulary_path) / f"{song_id}.json"
        
        logger.debug(f"Checking files: {lyrics_file}, {vocab_file}")
        if not lyrics_file.exists() or not vocab_file.exists():
            logger.error(f"Files not found: lyrics={lyrics_file.exists()}, vocab={vocab_file.exists()}")
            raise HTTPException(status_code=404, detail="Lyrics or vocabulary not found")
        
        # Read file contents
        logger.debug("Reading files")
        lyrics = lyrics_file.read_text()
        vocabulary = json.loads(vocab_file.read_text())
        logger.info(f"Successfully read lyrics ({len(lyrics)} chars) and vocabulary ({len(vocabulary)} items)")
        
        response = {
            "song_id": song_id,
            "lyrics": lyrics,
            "vocabulary": vocabulary
        }
        
        # Ensure all strings are properly encoded
        return JSONResponse(
            content=json.loads(json.dumps(response, ensure_ascii=False)),
            media_type="application/json; charset=utf-8"
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Run test query on startup"""
    logger.info("Testing lyrics search on startup...")
    test_request = LyricsRequest(message_request="Find lyrics for Gurenge by LiSA from Demon Slayer")
    try:
        # Initialize agent with system prompt
        agent = SongLyricsAgent(stream_llm=True, available_ram_gb=16)
        
        # Test request
        logger.info(f"Received request: {test_request.message_request}")
        
        # Process request with explicit tool instructions
        system_prompt = """You are a helpful AI assistant that helps find Japanese song lyrics and extract Japanese vocabulary from them.

IMPORTANT: You can ONLY use these exact tools:
1. search_web_serp(query: str) - Search for Japanese song lyrics
2. get_page_content(url: str) - Extract content from a webpage
3. extract_vocabulary(text: str) - Extract Japanese vocabulary
4. generate_song_id(title: str) - Generate URL-safe song ID
5. save_results(song_id: str, lyrics: str, vocabulary: List[Dict]) - Save results

To use a tool, respond with:
Tool: tool_name
Arguments: {"arg1": "value1", "arg2": "value2"}

Follow these steps:
1. Use search_web_serp to find the lyrics
2. Use get_page_content to extract the lyrics
3. Use extract_vocabulary to analyze the lyrics
4. Use generate_song_id to create an ID
5. Use save_results to store everything

End your response with FINISHED when done."""

        # Create test conversation
        test_conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": test_request.message_request}
        ]
        
        # Process the request
        try:
            result = await agent.process_request(test_conversation)
            logger.info(f"Test search completed successfully: {result}")
        except Exception as e:
            logger.error(f"Test search failed: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error in startup: {str(e)}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
