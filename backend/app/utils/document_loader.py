from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

import pytesseract
from pdf2image import convert_from_path
from PIL import Image  # noqa: F401  (kept from the original module)
import os


def extract_text_with_ocr(file_path):

    images = convert_from_path(file_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text


def load_and_split(file_path):

    docs = []
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        return _split(docs)

    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

    except Exception:
        docs = []

    # If PDF had no readable text, use OCR
    if not docs or all(not doc.page_content.strip() for doc in docs):

        print("Using OCR to read scanned PDF...")

        text = extract_text_with_ocr(file_path)

        # split_documents() expects Document objects, not plain dicts.
        docs = [Document(page_content=text, metadata={"source": file_path})]

    return _split(docs)


def _split(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(docs)
