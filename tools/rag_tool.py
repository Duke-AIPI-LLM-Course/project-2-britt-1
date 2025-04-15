from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool

@tool
def ai_meng_rag_tool(query: str) -> str:
    """
    Uses a vector database to answer questions about Duke's AI MEng program.
    """
    db = FAISS.load_local("vectorstore/db", OpenAIEmbeddings())
    retriever = db.as_retriever()
    llm = ChatOpenAI()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(query)
