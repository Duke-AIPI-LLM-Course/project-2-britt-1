import os
import sys

# Add root project directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain.agents import Tool, AgentExecutor, StructuredChatAgent
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder

from tools.rag_tool import ai_meng_rag_tool
from tools.events_tool import get_duke_events
from tools.pratt_tool import pratt_rag_tool
from agent.llm_chatbot import replicate_llm

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

# Custom prompt to handle any type of input, not just questions
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful Duke University assistant. Respond to anything the user types — even if it's not a question. Use tools when helpful."),
    MessagesPlaceholder(variable_name="chat_history")
])

# Agent setup
agent = StructuredChatAgent.from_llm_and_tools(
    llm=replicate_llm,
    tools=tools,
    prompt=prompt,
    verbose=True
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate"
)

# Entry function
def run_bot(input_text: str) -> str:
    return agent_executor.run(input_text)
