import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain.agents import initialize_agent, AgentType, Tool, AgentExecutor
from langchain_core.runnables import Runnable
from tools.rag_tool import ai_meng_rag_tool
from tools.events_tool import get_duke_events
from tools.pratt_tool import pratt_rag_tool
from agent.llm_chatbot import replicate_llm

class GeminiLLM(Runnable):
    def invoke(self, input, config=None, **kwargs):
        return replicate_llm(input)

replicate_wrapped_llm = GeminiLLM()

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
