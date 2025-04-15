from langchain.llms.base import LLM
from typing import Optional, List
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

class ReplicateLLM(LLM):
    model: str = "meta/llama-2-70b-chat"
    temperature: float = 0.7
    max_tokens: int = 500
    api_token: Optional[str] = os.getenv("REPLICATE_API_TOKEN")

    @property
    def _llm_type(self) -> str:
        return "replicate"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        output = replicate.run(
            self.model,
            input={
                "prompt": prompt,
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens
            },
            api_token=self.api_token
        )
        return "".join(output)

replicate_llm = ReplicateLLM()
