import time

from fastapi import Depends, FastAPI, File, UploadFile
from app.auth import verify_api_key
from app.services.extraction_service import extract_cheque
from app.services.file_validator import validate_file
from app.exception_handlers import (
    cheque_exception_handler,
    general_exception_handler
)
from fastapi.responses import FileResponse
from pathlib import Path

from app.exceptions import ChequeAPIException


app = FastAPI(
    title="Cheque Extraction Service",
    version="0.1.0"
)
app.add_exception_handler(
    ChequeAPIException,
    cheque_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)
@app.get("/")
def serve_homepage():
    return FileResponse(
        Path(__file__).parent / "static" / "index.html"
    )
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/api/v1/cheque/extract")
async def extract_cheque_endpoint(
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key),
):
    start_time = time.perf_counter()

    file_content = await validate_file(file)

    data = await extract_cheque(
        file_content=file_content,
        mime_type=file.content_type,
    )

    processing_time_ms = int(
        (time.perf_counter() - start_time) * 1000
    )

    return {
        "success": True,
        "data": data.model_dump(),
        "processing_time_ms": processing_time_ms,
    }