# Basic Toki Pona words (core vocabulary)
ALL_WORDS = [
    # pronouns and basic concepts
    "mi", "sina", "ona", "ni", "ale", "ala",
    # common actions
    "kama", "pali", "tawa", "moku", "pona", "ike",
    # descriptors
    "suli", "lili", "wawa", "suwi", "mute", "wan",
    # objects and places
    "tomo", "ma", "suno", "mun", "soweli", "kili",
    # abstracts
    "pilin", "sona", "wile", "lukin", "tenpo", "ijo"
]

# Sitelen Pona symbols (using emoji as placeholders - replace with actual sitelen pona)
ALL_SITELEN_PONA = [
    "🗣️", "👉", "👤", "📍", "⭕", "❌",
    "➡️", "🛠️", "🚶", "🍽️", "✨", "💔",
    "⬆️", "⬇️", "💪", "🍯", "📚", "1️⃣",
    "🏠", "🌍", "☀️", "🌙", "🐾", "🍎",
    "❤️", "📚", "💭", "👀", "⏳", "📦"
]

# Dictionary for basic/advanced mode selection
SELECT_MODE_DICT = {
    "nimi lili": ALL_WORDS[:15],    # Basic words
    "nimi suli": ALL_WORDS[15:]     # Advanced words
}

# Mapping from words to sitelen pona
WORD_TO_SITELEN = {
    # pronouns and basic concepts
    "mi": "🗣️",
    "sina": "👉",
    "ona": "👤",
    "ni": "📍",
    "ale": "⭕",
    "ala": "❌",
    # common actions
    "kama": "➡️",
    "pali": "🛠️",
    "tawa": "🚶",
    "moku": "🍽️",
    "pona": "✨",
    "ike": "💔",
    # descriptors
    "suli": "⬆️",
    "lili": "⬇️",
    "wawa": "💪",
    "suwi": "🍯",
    "mute": "📚",
    "wan": "1️⃣",
    # objects and places
    "tomo": "🏠",
    "ma": "🌍",
    "suno": "☀️",
    "mun": "🌙",
    "soweli": "🐾",
    "kili": "🍎",
    # abstracts
    "pilin": "❤️",
    "sona": "📚",
    "wile": "💭",
    "lukin": "👀",
    "tenpo": "⏳",
    "ijo": "📦"
}

# Mapping from sitelen pona to words
SITELEN_TO_WORD = {v: k for k, v in WORD_TO_SITELEN.items()}

# Check dictionary for validation
CHECK_DICT = {
    "nimi lili": SITELEN_TO_WORD,
    "nimi suli": SITELEN_TO_WORD
}

# Categories for organizing words
WORD_CATEGORIES = {
    "nimi jan": ["mi", "sina", "ona"],           # people words
    "nimi pali": ["kama", "pali", "tawa"],       # action words
    "nimi suli": ["suli", "lili", "mute"],       # descriptive words
    "nimi ijo": ["tomo", "ma", "kili"],          # object words
    "nimi pilin": ["pona", "ike", "wile"],       # feeling words
    "nimi sona": ["sona", "lukin", "tenpo"]      # concept words
}