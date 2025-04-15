from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.tools import tool
from llm import replicate_llm  
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os

@tool
def pratt_rag_tool(query: str) -> str:
    """
    Search the entire Pratt website using a local vector database.
    """
    
    db = FAISS.load_local("vectorstore/pratt_db", HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=replicate_llm, retriever=retriever)
    return qa.run(query)
