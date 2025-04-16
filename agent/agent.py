import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain.agents import initialize_agent, AgentType, Tool
from tools.rag_tool import ai_meng_rag_tool
from tools.events_tool import get_duke_events
from tools.pratt_tool import pratt_rag_tool
from agent.llm_chatbot import replicate_llm

tools = [
    Tool(
        name="AI MEng Info",
        func=ai_meng_rag_tool,
        description="Get info about the Duke AI MEng program"
    ),
    Tool(
        name="Events",
        func=get_duke_events,
        description="Find upcoming campus events at Duke"
    ),
    Tool(
        name="Pratt Info",
        func=pratt_rag_tool,
        description="Get details about the Pratt School of Engineering"
    )
]

from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import FakeListLLM  # Gemini not natively supported

# Wrap Gemini as a callable LLM for LangChain
class GeminiLLM:
    def __init__(self, call_func):
        self.call_func = call_func

    def __call__(self, prompt, **kwargs):
        return {"output": self.call_func(prompt)}

    def invoke(self, input, **kwargs):
        return self.call_func(input)

replicate_wrapped_llm = GeminiLLM(replicate_llm)

agent = initialize_agent(
    tools=tools,
    llm=replicate_wrapped_llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent.agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate",
)

def run_bot(input_text):
    return agent_executor.run(input_text)
