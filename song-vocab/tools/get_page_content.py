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
                
                # Ensure proper encoding of response content
                content = await response.text(encoding='utf-8', errors='replace')
                soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
                
                # Try to find lyrics in common patterns
                japanese_lyrics = None
                romaji_lyrics = None
                for tag in ['div', 'p']:
                    elements = soup.find_all(tag, class_=lambda x: x and ('lyrics' in x.lower() or 'text' in x.lower()))
                    for element in elements:
                        text = clean_text(element.get_text())
                        if text and len(text) > 100:  # Basic validation that we found substantial text
                            if is_primarily_japanese(text):
                                japanese_lyrics = text
                            elif is_primarily_romaji(text):
                                romaji_lyrics = text
                            break
                    if japanese_lyrics and romaji_lyrics:
                        break
                
                if not japanese_lyrics and not romaji_lyrics:
                    # Fallback: look for any large text block that might be lyrics
                    for tag in ['div', 'p']:
                        elements = soup.find_all(tag)
                        for element in elements:
                            text = clean_text(element.get_text())
                            if text and len(text) > 100:
                                if is_primarily_japanese(text):
                                    japanese_lyrics = text
                                elif is_primarily_romaji(text):
                                    romaji_lyrics = text
                                break
                        if japanese_lyrics and romaji_lyrics:
                            break
                
                return {
                    "japanese_lyrics": japanese_lyrics,
                    "romaji_lyrics": romaji_lyrics,
                    "metadata": f"Extracted from {url}"
                }
                
    except Exception as e:
        error_msg = f"Error fetching URL: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "japanese_lyrics": None,
            "romaji_lyrics": None,
            "metadata": error_msg
        }

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