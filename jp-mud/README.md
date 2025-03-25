# Japanese Language Learning MUD

A text-based adventure game for learning Japanese vocabulary, implemented with Gradio for a simple web interface.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python game/mud.py
```

3. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:7860)

## How to Play

The game is set in a Japanese cafe where you can:
- Move between rooms using `move [direction]`
- Look at objects using `look [object]` or `見ます [object]`
- Talk to NPCs using `talk [npc]` or `話します [npc]`

Your goal is to learn all 30 vocabulary words by interacting with objects and talking to NPCs throughout the cafe.

### Example Commands:
- `move north` - Move to the next room
- `look ドア` - Look at the door
- `talk 田中さん` - Talk to Tanaka-san

The game tracks your progress in learning vocabulary words. Try to master all 30 words!
