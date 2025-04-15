from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os

@tool
def pratt_rag_tool(query: str) -> str:
    """
    Search the entire Pratt website using a local vector database.
    """
    # Load prebuilt vector database
    db = FAISS.load_local("vectorstore/pratt_db", OpenAIEmbeddings())
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)
    return qa.run(query)
