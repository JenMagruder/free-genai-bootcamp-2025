from typing import List, Dict, Any
import json
import logging
from pathlib import Path

logger = logging.getLogger('song_vocab')

def save_results(song_id: str, lyrics: str, vocabulary: List[Dict[str, Any]], lyrics_path: Path, vocabulary_path: Path) -> str:
    """
    Save lyrics and vocabulary to their respective files.
    
    Args:
        song_id (str): ID of the song
        lyrics (str): Japanese lyrics text
        vocabulary (List[Dict[str, Any]]): List of vocabulary items
        lyrics_path (Path): Directory to save lyrics files
        vocabulary_path (Path): Directory to save vocabulary files
    
    Returns:
        str: The song_id that was used to save the files
    """
    try:
        # Ensure the lyrics are properly encoded
        if isinstance(lyrics, bytes):
            lyrics = lyrics.decode('utf-8', errors='replace')
        elif isinstance(lyrics, str):
            lyrics = lyrics.encode('utf-8', errors='replace').decode('utf-8')
        
        # Save lyrics with UTF-8 encoding
        lyrics_file = lyrics_path / f"{song_id}.txt"
        lyrics_file.write_text(lyrics, encoding='utf-8')
        logger.info(f"Saved lyrics to {lyrics_file}")
        
        # Save vocabulary with UTF-8 encoding
        vocab_file = vocabulary_path / f"{song_id}.json"
        vocab_file.write_text(
            json.dumps(vocabulary, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        logger.info(f"Saved vocabulary to {vocab_file}")
        
        return song_id
        
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        raise
