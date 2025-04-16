import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

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
