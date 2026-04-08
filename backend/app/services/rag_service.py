import chromadb
from langchain_community.vectorstores import Chroma
from app.utils.embeddings import get_embeddings
from app.utils.document_loader import load_and_split

persist_directory = "vector_db"

def ingest_document(file_path):

    docs = load_and_split(file_path)

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        persist_directory=persist_directory
    )

    vectordb.persist()

    return "Document processed successfully"


def retrieve_context(query):

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=get_embeddings()
    )

    docs = vectordb.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    return context