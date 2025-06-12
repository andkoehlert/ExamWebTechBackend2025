from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_mistral(chat_request: ChatRequest):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": chat_request.message,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return {"response": response.json().get("response", "")}
    else:
        return {"error": response.text}
