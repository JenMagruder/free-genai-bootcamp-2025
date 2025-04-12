import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TOKI_PONA_DIR = DATA_DIR / "toki_pona"
USER_PROGRESS_DIR = DATA_DIR / "user_progress"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
TOKI_PONA_DIR.mkdir(exist_ok=True)
USER_PROGRESS_DIR.mkdir(exist_ok=True)

# File paths
VOCABULARY_FILE = TOKI_PONA_DIR / "vocabulary.json"
EXAMPLES_FILE = TOKI_PONA_DIR / "examples.json"
PROGRESS_FILE = USER_PROGRESS_DIR / "progress.json"