import json
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load intents from JSON
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

# Initialize FastAPI app
app = FastAPI()

# Allow frontend (React) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class ChatRequest(BaseModel):
    message: str

# Function to find matching response
def get_response(user_message):
    user_message = user_message.lower()

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message:
                return random.choice(intent["responses"])

    return "I'm sorry, I don't understand. Can you rephrase?"

# Chatbot API endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    response_text = get_response(request.message)
    return {"response": response_text}

