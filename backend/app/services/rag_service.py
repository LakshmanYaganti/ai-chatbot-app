import os

import chromadb  # noqa: F401  (kept: original import, useful for debugging)
from langchain_community.vectorstores import Chroma
from app.utils.embeddings import get_embeddings
from app.utils.document_loader import load_and_split

persist_directory = "vector_db"


def ingest_document(file_path):

    docs = load_and_split(file_path)

    if not docs:
        raise ValueError("No readable content was found in the document.")

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        persist_directory=persist_directory
    )

    vectordb.persist()

    return "Document processed successfully"


def retrieve_context(query):
    """Return the most relevant stored chunks for ``query``.

    Returns an empty string (rather than raising) when no document has
    been ingested yet, the persist directory is missing/empty, or the
    store cannot be read — the chat endpoint can then answer without
    document context instead of crashing.
    """
    try:
        if not os.path.isdir(persist_directory) or not os.listdir(persist_directory):
            return ""

        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=get_embeddings()
        )

        docs = vectordb.similarity_search(query, k=3)

        context = "\n".join([doc.page_content for doc in docs])

        return context
    except Exception:
        return ""
