# 📚 Document Q&A Bot using RAG

## Overview

This project is a Retrieval-Augmented Generation (RAG) based Document Q&A Bot built using Python, ChromaDB, and Google Gemini.

The system allows users to ask natural language questions about uploaded documents and receive accurate, context-grounded answers along with source citations.

The application ingests PDF and DOCX documents, creates embeddings, stores them in a vector database, retrieves relevant content using semantic search, and generates answers using Gemini.

---

## Features

* PDF and DOCX document ingestion
* Text chunking with overlap
* Gemini embeddings
* ChromaDB vector storage
* Semantic similarity search
* Grounded answer generation
* Source citations
* Streamlit web interface
* Hallucination prevention

---

## Tech Stack

### Language

* Python 3.11

### Libraries

* chromadb
* google-generativeai
* pypdf
* python-docx
* python-dotenv
* streamlit
* tqdm

### Models

* Embedding Model: `gemini-embedding-001`
* LLM: `gemini-2.5-flash`

### Vector Database

* ChromaDB

---

## Project Structure

```text
document-qa-bot/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── AI_Fundamentals.pdf
│   ├── Machine_Learning.pdf
│   ├── Cloud_Computing.pdf
│   ├── Cybersecurity.docx
│   └── Business_Analytics.docx
│
├── db/
│
└── src/
    ├── ingest.py
    ├── query.py
    └── main.py
```

## Architecture

```text
Documents
    │
    ▼
Document Loader
    │
    ▼
Text Chunking
    │
    ▼
Gemini Embeddings
    │
    ▼
ChromaDB
    │
    ▼
Similarity Search
    │
    ▼
Retrieved Context
    │
    ▼
Gemini LLM
    │
    ▼
Grounded Answer + Citations
```

## Chunking Strategy

The application uses fixed-size chunking.

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

The overlap helps preserve context across chunk boundaries and improves retrieval accuracy.

---

## Embedding Model

The project uses Google's Gemini embedding model:

```text
gemini-embedding-001
```

Reason:

* High-quality semantic embeddings
* Efficient retrieval performance
* Native Gemini ecosystem integration

---

## Vector Database

ChromaDB was selected because:

* Lightweight and easy to use
* Persistent local storage
* Fast similarity search
* No separate server required

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd document-qa-bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Index Documents

```bash
python src/ingest.py
```

---

## Run Application

```bash
streamlit run src/main.py
```

---

## Example Queries

1. What is Artificial Intelligence?
2. What is Machine Learning?
3. Explain cloud deployment models.
4. What are common cybersecurity threats?
5. What is predictive analytics?

---

## Hallucination Prevention

The system is instructed to answer only using retrieved document context.

If the requested information is not available in the indexed documents, the bot informs the user that the answer could not be found in the knowledge base.

---

## Known Limitations

* Supports PDF and DOCX files only
* No multi-turn conversational memory
* Retrieval quality depends on chunk size and document quality
* Large document collections may increase indexing time

---

## Future Improvements

* Hybrid search (semantic + keyword)
* Conversation memory
* Additional document formats
* Cloud deployment
* Advanced chunking strategies

---

## Author

**Rachana Hegde[Rachana-Hegde]**
