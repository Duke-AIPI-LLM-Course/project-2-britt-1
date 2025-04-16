from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from agent.llm_chatbot import replicate_llm

@tool
def ai_meng_rag_tool(query: str) -> str:
    """Get information about the Duke AI MEng program using the vector database."""
    db = FAISS.load_local(
        "vectorstore/db",
        HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=replicate_llm, retriever=retriever)
    return qa.run(query)
