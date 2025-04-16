import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env!")

GEN_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"

def replicate_llm(prompt) -> str:
    if isinstance(prompt, dict) and "input" in prompt:
        prompt = prompt["input"]
    elif isinstance(prompt, tuple):
        prompt = prompt[-1]

    if isinstance(prompt, list):
        prompt = next((m.content for m in prompt if hasattr(m, "content")), str(prompt))

    if not isinstance(prompt, str):
        prompt = str(prompt)

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEN_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Gemini error: {response.status_code} - {response.text}")

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
