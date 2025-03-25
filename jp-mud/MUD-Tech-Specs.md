# Technical Specficiations

## Business Scenario

Build a game like Advetnure using MUD (Minimal Unrealistic Dungeon).

## Technical Requirements
- Python
- Gradio
- OpenAI

## Backend

### Backend Components

#### World Generator LLM

This LLM is responsible for generating a world document similar to the format of the example-world.txt.

It also needs to reading the Adventure Text Prompt so it has context to generate the world.

#### Text Adventure LLM

This LLM is responsible for generating text-based adventures text based on the:
- World Document

The text adventure LLM needs

#### Japanese Langauge Validator LLM

This LLM is responsible for validating the Japanese language of the text inputted before its passed to the text adventure LLM.

#### Loading Chat History and Gamestate

This is the state of the game when the user first enters the game.

#### Saving Chat History and Gamestate

After each turn the state of the game is updated.






## Frontend

### UI Inteface Requirements
- Text chat
- Text input

