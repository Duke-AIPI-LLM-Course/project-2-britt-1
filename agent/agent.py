import os
import sys

# Add project root to the system path so modules are found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain.agents import initialize_agent, AgentType, Tool, AgentExecutor
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

agent_executor = initialize_agent(
    tools=tools,
    llm=replicate_llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate"
)

def run_bot(input_text: str) -> str:
    return agent_executor.run(input_text)
