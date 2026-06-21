import os
import chromadb
import google.generativeai as genai

from dotenv import load_dotenv
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

client = chromadb.PersistentClient(path="db")

embedding_function = GoogleGenerativeAiEmbeddingFunction(
    api_key=API_KEY,
    model_name="models/gemini-embedding-001"
)

collection = client.get_collection(
    name="document_knowledge_base",
    embedding_function=embedding_function
)


def ask_question(question):

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = ""

    citations = []

    for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]):

        citation = f"{meta['source']} Page {meta['page']}"

        citations.append(citation)

        context += f"\n[{citation}]\n{doc}\n"

    prompt = f"""
You are a document Q&A assistant.

Use ONLY the provided context.

If the answer is not present in the context, say:

"I am sorry, but the provided documents do not contain the answer."

Context:
{context}

Question:
{question}

Answer:
"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text, citations, context