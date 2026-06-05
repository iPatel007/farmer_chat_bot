import json
import os

from langchain_core.documents import Document
from langchain_chroma import Chroma

from service.llm_service import embedding_model

DB_PATH = "chroma_db"
DATA_PATH = "data/farmer_qa.json"


def load_documents():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []

    for item in data:
        docs.append(
            Document(
                page_content=f"Q: {item['question']}\nA: {item['answer']}",
                metadata={
                    "language": item["language"]
                }
            )
        )

    return docs


def create_vectorstore():
    if os.path.exists(DB_PATH):
        return

    docs = load_documents()

    Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )


def get_vectorstore():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )