import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TOGETHER_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def replicate_llm(prompt) -> str:
    if isinstance(prompt, dict) and "input" in prompt:
        prompt = prompt["input"]
    elif isinstance(prompt, list):
        prompt = next((m.content for m in prompt if hasattr(m, "content")), str(prompt))
    elif isinstance(prompt, tuple):
        prompt = prompt[-1]

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Together AI error {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
