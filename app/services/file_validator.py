from io import BytesIO

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader

from app.config import MAX_FILE_SIZE


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
}

ALLOWED_PDF_TYPE = "application/pdf"


def invalid_image(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "success": False,
            "error": {
                "code": "INVALID_IMAGE",
                "message": message,
            },
        },
    )


async def validate_file(file: UploadFile) -> bytes:
    if file.content_type not in ALLOWED_IMAGE_TYPES | {ALLOWED_PDF_TYPE}:
        raise invalid_image("Unsupported file format")

    file_content = await file.read()

    if len(file_content) == 0:
        raise invalid_image("Empty file")

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "success": False,
                "error": {
                    "code": "FILE_TOO_LARGE",
                    "message": "File size exceeds 5 MB limit",
                },
            },
        )

    if file.content_type in ALLOWED_IMAGE_TYPES:
        _validate_image(file_content)

    elif file.content_type == ALLOWED_PDF_TYPE:
        _validate_pdf(file_content)

    return file_content


def _validate_image(file_content: bytes) -> None:
    try:
        with Image.open(BytesIO(file_content)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError):
        raise invalid_image("Invalid or corrupted image file")


def _validate_pdf(file_content: bytes) -> None:
    try:
        reader = PdfReader(BytesIO(file_content))

        if len(reader.pages) != 1:
            raise invalid_image("PDF must contain exactly one page")

    except HTTPException:
        raise

    except Exception:
        raise invalid_image("Invalid or corrupted PDF file")