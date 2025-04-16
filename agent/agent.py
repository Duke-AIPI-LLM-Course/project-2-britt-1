import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from tools.rag_tool import ai_meng_rag_tool
from tools.events_tool import get_duke_events
from tools.pratt_tool import pratt_rag_tool
from langchain.agents import AgentExecutor
from agent.llm_chatbot import replicate_llm  


tools = [
    Tool(
        name="AI MEng Info",
        func=ai_meng_rag_tool,
        description="Use this tool to get details about the Duke AI MEng program"
    ),
    Tool(
        name="Events",
        func=get_duke_events,
        description="Use this tool to find upcoming Duke campus events"
    ),
    Tool(
        name="Pratt Facts",
        func=pratt_rag_tool,
        description="Use this tool to find quick facts about the Pratt School of Engineering"
    )
]


agent = initialize_agent(
    tools=tools,
    llm=replicate_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Wrap it to handle weird output parsing
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