from fastapi import Header, HTTPException, status

from app.config import SERVICE_API_KEY


def verify_api_key(
    x_api_key: str | None = Header(default=None)
):
    if not SERVICE_API_KEY:
        raise RuntimeError("SERVICE_API_KEY is not configured")

    if x_api_key != SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Invalid or missing API key"
                }
            }
        )

    return x_api_key