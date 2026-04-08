from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os


def extract_text_with_ocr(file_path):

    images = convert_from_path(file_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text


def load_and_split(file_path):

    docs = []

    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

    except Exception:
        docs = []

    # If PDF had no readable text, use OCR
    if not docs or len(docs[0].page_content.strip()) == 0:

        print("Using OCR to read scanned PDF...")

        text = extract_text_with_ocr(file_path)

        docs = [{"page_content": text}]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(docs)