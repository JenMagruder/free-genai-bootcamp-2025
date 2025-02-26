import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

async def get_page_content(url: str) -> Dict[str, Optional[str]]:
    """
    Extract lyrics content from a webpage.
    
    Args:
        url (str): URL of the webpage to extract content from
        
    Returns:
        Dict[str, Optional[str]]: Dictionary containing japanese_lyrics, romaji_lyrics, and metadata
    """
    logger.info(f"Fetching content from URL: {url}")
    try:
        async with aiohttp.ClientSession() as session:
            logger.debug("Making HTTP request...")
            async with session.get(url) as response:
                if response.status != 200:
                    error_msg = f"Error: HTTP {response.status}"
                    logger.error(error_msg)
                    return {
                        "japanese_lyrics": None,
                        "romaji_lyrics": None,
                        "metadata": error_msg
                    }
                
                logger.debug("Reading response content...")
                html = await response.text()
                logger.info(f"Successfully fetched page content ({len(html)} bytes)")
                return extract_lyrics_from_html(html, url)
    except Exception as e:
        error_msg = f"Error fetching page: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "japanese_lyrics": None,
            "romaji_lyrics": None,
            "metadata": error_msg
        }

def extract_lyrics_from_html(html: str, url: str) -> Dict[str, Optional[str]]:
    """
    Extract lyrics from HTML content based on common patterns in lyrics websites.
    """
    logger.info("Starting lyrics extraction from HTML")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    logger.debug("Cleaning HTML content...")
    for element in soup(['script', 'style', 'header', 'footer', 'nav']):
        element.decompose()
    
    # Common patterns for lyrics containers
    lyrics_patterns = [
        # Class patterns
        {"class_": re.compile(r"lyrics?|kashi|romaji|original", re.I)},
        {"class_": re.compile(r"song-content|song-text|track-text", re.I)},
        # ID patterns
        {"id": re.compile(r"lyrics?|kashi|romaji|original", re.I)},
        # Common Japanese lyrics sites patterns
        {"class_": "lyrics_box"},  # Uta-Net
        {"class_": "hiragana"},    # J-Lyrics
        {"class_": "romaji"}       # J-Lyrics
    ]
    
    japanese_lyrics = None
    romaji_lyrics = None
    metadata = ""
    
    # Try to find lyrics containers
    logger.debug("Searching for lyrics containers...")
    for pattern in lyrics_patterns:
        logger.debug(f"Trying pattern: {pattern}")
        elements = soup.find_all(**pattern)
        logger.debug(f"Found {len(elements)} matching elements")
        
        for element in elements:
            text = clean_text(element.get_text())
            logger.debug(f"Extracted text length: {len(text)} chars")
            
            # Detect if text is primarily Japanese or romaji
            if is_primarily_japanese(text) and not japanese_lyrics:
                logger.info("Found Japanese lyrics")
                japanese_lyrics = text
            elif is_primarily_romaji(text) and not romaji_lyrics:
                logger.info("Found romaji lyrics")
                romaji_lyrics = text
    
    # If no structured containers found, try to find the largest text block
    if not japanese_lyrics and not romaji_lyrics:
        logger.info("No lyrics found in structured containers, trying fallback method")
        text_blocks = [clean_text(p.get_text()) for p in soup.find_all('p')]
        if text_blocks:
            largest_block = max(text_blocks, key=len)
            logger.debug(f"Found largest text block: {len(largest_block)} chars")
            
            if is_primarily_japanese(largest_block):
                logger.info("Largest block contains Japanese text")
                japanese_lyrics = largest_block
            elif is_primarily_romaji(largest_block):
                logger.info("Largest block contains romaji text")
                romaji_lyrics = largest_block
    
    result = {
        "japanese_lyrics": japanese_lyrics,
        "romaji_lyrics": romaji_lyrics,
        "metadata": metadata or "Lyrics extracted successfully"
    }
    
    # Log the results
    if japanese_lyrics:
        logger.info(f"Found Japanese lyrics ({len(japanese_lyrics)} chars)")
    if romaji_lyrics:
        logger.info(f"Found romaji lyrics ({len(romaji_lyrics)} chars)")
    
    return result

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace and unnecessary characters.
    """
    logger.debug(f"Cleaning text of length {len(text)}")
    # Remove HTML entities
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    # Remove leading/trailing whitespace
    result = text.strip()
    logger.debug(f"Text cleaned, new length: {len(result)}")
    return result

def is_primarily_japanese(text: str) -> bool:
    """
    Check if text contains primarily Japanese characters.
    """
    # Count Japanese characters (hiragana, katakana, kanji)
    japanese_chars = len(re.findall(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    ratio = japanese_chars / total_chars if total_chars > 0 else 0
    logger.debug(f"Japanese character ratio: {ratio:.2f} ({japanese_chars}/{total_chars})")
    return japanese_chars > 0 and ratio > 0.3

def is_primarily_romaji(text: str) -> bool:
    """
    Check if text contains primarily romaji characters.
    """
    # Count romaji characters (basic Latin alphabet)
    romaji_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(text.strip())
    ratio = romaji_chars / total_chars if total_chars > 0 else 0
    logger.debug(f"Romaji character ratio: {ratio:.2f} ({romaji_chars}/{total_chars})")
    return romaji_chars > 0 and ratio > 0.3