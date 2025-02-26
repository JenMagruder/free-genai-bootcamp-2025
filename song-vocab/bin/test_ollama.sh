#!/bin/bash

echo "Testing Ollama API..."
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "messages": [
      {
        "role": "user",
        "content": "Say hello!"
      }
    ]
  }' | jq .

echo "Done!"
