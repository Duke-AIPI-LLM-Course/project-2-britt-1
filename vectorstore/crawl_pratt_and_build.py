import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

BASE_URL = "https://pratt.duke.edu"
MAX_PAGES = 30 

def is_internal_link(link):
    return link.startswith("/") or BASE_URL in link

def crawl_site(start_url, max_pages=15):
    visited = set()
    to_visit = [start_url]
    pages = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            print(f"Scraping: {url}")
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")

            text = soup.get_text(separator=" ", strip=True)
            pages.append(Document(page_content=text, metadata={"source": url}))

            for a in soup.find_all("a", href=True):
                link = urljoin(BASE_URL, a["href"])
                if is_internal_link(link) and BASE_URL in link and link not in visited:
                    to_visit.append(link)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return pages

def build_pratt_vector_db():
    docs = crawl_site(BASE_URL, MAX_PAGES)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    vectordb = FAISS.from_documents(chunks, OpenAIEmbeddings())
    vectordb.save_local("vectorstore/pratt_db")
    print("Vector database saved!")

if __name__ == "__main__":
    build_pratt_vector_db()
