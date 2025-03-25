from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class AdventureText:
    def __init__(self):
        self.client = OpenAI()
        self.context = """
        You are a Japanese language learning text adventure game.
        Generate engaging responses that teach Japanese vocabulary naturally.
        Keep responses concise and focused on the current action.
        Always include relevant Japanese vocabulary with format: 日本語 (romaji / english)
        """
    
    def generate_text(self, prompt: str) -> str:
        """Generate text based on a prompt using OpenAI LLMs"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.context},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"