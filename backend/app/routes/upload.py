from fastapi import APIRouter, UploadFile, File
import shutil

from app.services.rag_service import ingest_document

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_FOLDER = "uploaded_docs"


@router.post("/")
async def upload_document(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ingest_document(file_path)

    return {"message": result}