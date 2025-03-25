import gradio as gr
from lib.adventure_text import AdventureText

class Game:
    def __init__(self):
        self.adventure = AdventureText()
        self.current_room = "entrance"

    def process_command(self, message: str) -> str:
        # Generate adventure text based on the command
        prompt = f"Current room: {self.current_room}\nCommand: {message}"
        return self.adventure.generate_text(prompt)

# Initialize game state
game = Game()

def respond(message, history):
    # Process the command through our game engine
    response = game.process_command(message)
    # Return empty message (to clear input) and update history
    return "", history + [(message, response)]

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_classes=["dark"],
        height=400
    )
    msg = gr.Textbox(
        show_label=False,
        placeholder="Type your message here...",
        container=False,
        elem_classes=["input-area"]
    )
    submit = gr.Button(
        "Send",
        variant="primary",
        elem_classes=["submit-btn"]
    )

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])

# Launch the app
if __name__ == "__main__":
    demo.launch()