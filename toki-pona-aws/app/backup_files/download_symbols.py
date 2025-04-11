#!/usr/bin/env python3
import requests
import os

def download_symbols():
    # List of core Toki Pona words to download
    core_words = [
        "mi", "sina", "ona",  # pronouns
        "pona", "ike",        # good/bad
        "tawa", "moku",       # common verbs
        "suli", "lili",       # size
        "tomo", "ma"          # places
    ]

    # Base URL for the SVG files
    base_url = "https://raw.githubusercontent.com/lipu-linku/ijo/main/sitelenpona/sitelen-seli-kiwen/{}.svg"

    # Directory to save SVGs
    svg_dir = "img/sitelen_pona/svg"
    os.makedirs(svg_dir, exist_ok=True)
    
    # Download each symbol
    for word in core_words:
        url = base_url.format(word)
        svg_path = os.path.join(svg_dir, f"{word}.svg")
        print(f"Downloading {word}.svg...")
        
        try:
            # Download SVG
            response = requests.get(url)
            response.raise_for_status()
            
            # Save SVG
            with open(svg_path, "wb") as f:
                f.write(response.content)
            print(f"✓ Saved {word}.svg")
            
        except Exception as e:
            print(f"✗ Error downloading {word}: {e}")

if __name__ == "__main__":
    download_symbols()
