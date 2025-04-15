from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from tools.ai_meng_rag_tool import ai_meng_rag_tool
from tools.events_tool import get_duke_events
from tools.pratt_tool import get_pratt_facts
from llm import replicate_llm  


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
        func=get_pratt_facts,
        description="Use this tool to find quick facts about the Pratt School of Engineering"
    )
]


agent = initialize_agent(
    tools,
    replicate_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_bot(input_text):
    return agent.run(input_text)
