from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers import ContextualCompressionRetriever
from agent.llm_chatbot import replicate_llm

@tool
def pratt_rag_tool(query: str) -> str:
    """Get details about the Pratt School of Engineering using the local vector database."""
    db = FAISS.load_local(
        "vectorstore/pratt_db",
        HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    
    # Optional: compress to remove irrelevant chunks even after similarity
    filter = EmbeddingsFilter(
        embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        similarity_threshold=0.75  # adjust for strictness
    )
    compressed = ContextualCompressionRetriever(base_compressor=filter, base_retriever=retriever)

    qa = RetrievalQA.from_chain_type(llm=replicate_llm, retriever=compressed, return_source_documents=True)
    result = qa.invoke({"query": query})
    
    return result["result"]
