import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env!")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="models/gemini-pro")

def replicate_llm(prompt) -> str:
    if isinstance(prompt, dict) and "input" in prompt:
        prompt = prompt["input"]
    elif isinstance(prompt, tuple):
        prompt = prompt[-1]

    if isinstance(prompt, list):
        prompt = next((m.content for m in prompt if hasattr(m, "content")), str(prompt))

    if not isinstance(prompt, str):
        prompt = str(prompt)

    response = model.generate_content(prompt)
    return response.text
