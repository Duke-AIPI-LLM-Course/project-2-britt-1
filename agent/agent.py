import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables import Runnable
from langchain.tools import Tool

from tools.rag_tool import ai_meng_rag_tool
from tools.events_tool import get_duke_events
from tools.pratt_tool import pratt_rag_tool
from agent.llm_chatbot import replicate_llm

# Wrap your Together.ai call inside a Runnable for LangChain compatibility
class TogetherLLM(Runnable):
    def invoke(self, input, config=None, **kwargs):
        return replicate_llm(input)

# Instantiate the LLM wrapper
wrapped_llm = TogetherLLM()

# Define tools
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

# Initialize agent
agent_executor = initialize_agent(
    tools=tools,
    llm=wrapped_llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate"
)

# Final export function
def run_bot(input_text: str) -> str:
    return agent_executor.run(input_text)
