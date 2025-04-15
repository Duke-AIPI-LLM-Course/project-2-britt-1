from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.tools import tool
from agent.llm_chatbot import replicate_llm 

@tool
def ai_meng_rag_tool(query: str) -> str:
    """Searches the Duke AI MEng vector database and returns relevant info."""
    db = FAISS.load_local("vectorstore/db", HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=replicate_llm, retriever=retriever)
    return qa.run(query)
