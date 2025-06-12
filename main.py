from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_mistral(chat_request: ChatRequest):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "mistral",
        "messages": [{"role": "user", "content": chat_request.message}]
    }

    response = requests.post(url, json=payload, stream=True)
    result = ""

    if response.status_code == 200:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        result += json_data["message"]["content"]
                except json.JSONDecodeError:
                    continue
        return {"response": result}
    else:
        return {"error": response.text}
