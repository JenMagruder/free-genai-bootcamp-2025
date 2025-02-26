from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import logging
from pathlib import Path
from agent import SongLyricsAgent
from dotenv import load_dotenv

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

class LyricsRequest(BaseModel):
    message_request: str

@app.post("/api/agent")
async def get_lyrics(request: LyricsRequest) -> Dict[str, Any]:
    logger.info(f"Received request: {request.message_request}")
    try:
        # Initialize agent
        logger.debug("Initializing SongLyricsAgent")
        agent = SongLyricsAgent(stream_llm=False, available_ram_gb=16)
        
        # Process request
        logger.info("Processing request through agent")
        song_id = await agent.process_request(request.message_request)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
