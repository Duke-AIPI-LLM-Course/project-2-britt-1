import os
import requests
from dotenv import load_dotenv
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

load_dotenv()

api_key = os.getenv("TOGETHER_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def _call_llm(prompt) -> str:
    if isinstance(prompt, list) and all(isinstance(m, BaseMessage) for m in prompt):
        messages = []
        for msg in prompt:
            role = "user"
            if isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, SystemMessage):
                role = "system"
            else:
                role = "assistant"
            messages.append({"role": role, "content": msg.content})
    else:
        messages = [{"role": "user", "content": str(prompt)}]

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Together AI error {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()

# Make it runnable by LangChain
class TogetherLLM(Runnable):
    def invoke(self, input, config=None, **kwargs):
        return _call_llm(input)

replicate_llm = TogetherLLM()
