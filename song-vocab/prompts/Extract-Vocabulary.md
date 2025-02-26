Extract ALL Japanese vocabulary from the provided text. For each word:

1. Include EVERY word from the text:
   - Nouns (名詞)
   - Verbs (動詞)
   - Adjectives (形容詞)
   - Adverbs (副詞)

2. Ignore grammer or fixed expressions:
   - Particles (助詞)
   - Expressions (表現)

3. Break down each word into its parts:
   - Individual kanji/kana components
   - Romaji reading for each part
   - English meaning

Format each word exactly like this example:
{
    "kanji": "新しい",
    "romaji": "atarashii",
    "english": "new",
    "parts": [
        { "kanji": "新", "romaji": ["a","ta","ra"] },
        { "kanji": "し", "romaji": ["shi"] },
        { "kanji": "い", "romaji": ["i"] }
    ]
}

Important:
- Do not skip any words, even common ones
- Convert words to their dictionary form
- Break down compound words into their parts
- Make sure romaji is accurate for each part
