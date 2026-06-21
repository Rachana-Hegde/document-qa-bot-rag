import os
import streamlit as st
import chromadb
from tqdm import tqdm
from pypdf import PdfReader
from docx import Document

from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    API_KEY = st.secrets["GEMINI_API_KEY"]

DATA_FOLDER = "data"

DB_PATH = "db"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_pdf(path):

    docs = []

    try:
        if os.path.getsize(path) == 0:
            print(f"Skipping empty file: {path}")
            return docs

        reader = PdfReader(path)

        for page_num, page in enumerate(reader.pages):

            text = page.extract_text()

            if text:
                docs.append({
                    "text": text,
                    "metadata": {
                        "source": os.path.basename(path),
                        "page": page_num + 1
                    }
                })

    except Exception as e:
        print(f"Error reading {path}: {e}")

    return docs

def load_docx(path):

    docs = []

    try:
        doc = Document(path)

        text = "\n".join([p.text for p in doc.paragraphs])

        if text.strip():

            docs.append({
                "text": text,
                "metadata": {
                    "source": os.path.basename(path),
                    "page": 1
                }
            })

    except Exception as e:
        print(f"Error reading DOCX {path}: {e}")

    return docs

def chunk_documents(documents):

    chunks = []

    for doc in documents:

        text = doc["text"]

        start = 0

        while start < len(text):

            end = min(start + CHUNK_SIZE, len(text))

            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "metadata": doc["metadata"]
            })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

def create_collection():

    client = chromadb.PersistentClient(path=DB_PATH)

    embedding_function = GoogleGenerativeAiEmbeddingFunction(
        api_key=API_KEY,
        model_name="models/gemini-embedding-001"
    )

    collection = client.get_or_create_collection(
        name="document_knowledge_base",
        embedding_function=embedding_function
    )

    return collection

def index_documents():

    documents = []

    for file in os.listdir(DATA_FOLDER):

        path = os.path.join(DATA_FOLDER, file)

        print(f"Processing: {path}")

        if file.endswith(".pdf"):
            documents.extend(load_pdf(path))

        elif file.endswith(".docx"):
            documents.extend(load_docx(path))

    print(f"Loaded {len(documents)} document pages")

    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks")

    collection = create_collection()

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    texts = [c["text"] for c in chunks]
    metadata = [c["metadata"] for c in chunks]

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadata
    )

    print(f"{len(chunks)} chunks indexed.")

if __name__ == "__main__":
    index_documents()