import requests
import json
import asyncio
from app.models.chat_models import ChatRequest, Message


def get_prompt(mode: str) -> Message:
    PROMPT_TEMPLATES = {
        "math_tutor": (
            "You are a kind and patient math teacher who ONLY helps students understand math problems step-by-step. "
            "Explain concepts clearly and gently, focusing only on the math problem the user just asked. "
            "For multiplication, explain it as repeated addition. For example, 4 * 4 means adding 4 four times. "
            "If the user says 'I don't know' or is unsure, provide gentle hints to help them continue. "
            "Do NOT provide the final answer or result by yourself. Instead, stop right before the final sum and ask the student to try finishing it themselves, e.g., 'Can you try adding these numbers to find the total?' "
            "If the user provides a numeric answer, check if it correctly answers the last math problem you asked: "
            "- If the answer is correct, reply briefly with 'Correct!' or 'Exactly!'. "
            "- If the answer is incorrect, reply gently with a hint or encouragement to try again, and remind them of the problem to stay on track. "
            "If the user asks questions unrelated to math, politely respond: "
            "'I'm here to help only with math questions. Please ask me a math problem!' "
            "Always stay focused on the specific problem at hand and avoid changing topics or giving unrelated explanations."
        ),
        "storyteller": (
            "You are a creative storyteller who writes engaging stories for all ages. "
            "You ONLY create stories or talk about storytelling. "
            "If the user asks anything else, reply with: "
            "'I'm here to tell stories. Please ask me to tell you a story!'"
        ),
        "friendly_ai": (
            "You are a friendly and helpful AI assistant who answers questions clearly and politely."
        )
    }

    prompt = PROMPT_TEMPLATES.get(mode, PROMPT_TEMPLATES["friendly_ai"])
    return Message(role="system", content=prompt)


def get_generation_settings(chat_request: ChatRequest) -> dict:
    defaults = {
        "math_tutor": {"temperature": 0.2, "top_p": 1.0, "max_tokens": 256},
        "storyteller": {"temperature": 0.9, "top_p": 0.95, "max_tokens": 800},
        "friendly_ai": {"temperature": 0.7, "top_p": 1.0, "max_tokens": 512}
    }

    mode_defaults = defaults.get(chat_request.mode, defaults["friendly_ai"])

    return {
        "temperature": getattr(chat_request, "temperature", mode_defaults["temperature"]),
        "top_p": getattr(chat_request, "top_p", mode_defaults["top_p"]),
        "max_tokens": getattr(chat_request, "max_tokens", mode_defaults["max_tokens"]),
    }


async def get_mistral_response(chat_request: ChatRequest):
    url = "http://localhost:11434/api/chat"
    system_message = get_prompt(chat_request.mode)
    all_messages = [system_message] + chat_request.messages
    generation_settings = get_generation_settings(chat_request)

    payload = {
        "model": "mistral",
        "messages": [msg.dict() for msg in all_messages],
        "stream": True,
        **generation_settings
    }

    # Dette er nu en async generator
    async def stream_response():
        with requests.post(url, json=payload, stream=True) as resp:
            for line in resp.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
                    except json.JSONDecodeError:
                        continue

    return stream_response()  