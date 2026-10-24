from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
import shutil

from app.services.rag_service import ingest_document

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_FOLDER = Path("uploaded_docs")
ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """Save an uploaded document and ingest it into the vector store.

    Only PDF and plain-text files are accepted. The upload folder is
    created on demand so a first upload on a fresh checkout cannot crash
    with ``FileNotFoundError``.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was provided.")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{suffix or '(none)'}'. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
            ),
        )

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    # Keep only the basename so a crafted filename cannot escape the folder.
    file_path = UPLOAD_FOLDER / Path(file.filename).name

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except OSError as exc:
        raise HTTPException(
            status_code=500, detail=f"Could not save the uploaded file: {exc}"
        ) from exc
    finally:
        await file.close()

    try:
        result = ingest_document(str(file_path))
    except Exception as exc:  # parsing / embedding failures surface as 422
        raise HTTPException(
            status_code=422,
            detail=f"File was uploaded but could not be processed: {exc}",
        ) from exc

    return {"message": result, "filename": file_path.name}
