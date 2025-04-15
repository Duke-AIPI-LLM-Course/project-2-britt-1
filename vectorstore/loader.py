from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import os

def build_vectorstore():
    # Load raw text from your file
    loader = TextLoader("vectorstore/data/ai_meng.txt")
    documents = loader.load()

    # Split text into smaller overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Create embeddings using HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Build vector DB
    vectordb = FAISS.from_documents(chunks, embeddings)

    # Save vectorstore
    vectordb.save_local("vectorstore/db")
    print("Vectorstore built and saved at vectorstore/db")

if __name__ == "__main__":
    build_vectorstore()
