import re
from typing import Dict

def generate_song_id(artist: str, title: str) -> Dict[str, str]:
    """
    Generate a URL-safe song ID from artist and title.
    
    Args:
        artist (str): The artist name
        title (str): The song title
        
    Returns:
        Dict[str, str]: Dictionary containing the generated song_id
    """
    def clean_string(s: str) -> str:
        # Remove special characters and convert to lowercase
        s = re.sub(r'[^\w\s-]', '', s.lower())
        # Replace spaces with hyphens
        return re.sub(r'[-\s]+', '-', s).strip('-')
    
    song_id = f"{clean_string(artist)}-{clean_string(title)}"
    return {"song_id": song_id}
