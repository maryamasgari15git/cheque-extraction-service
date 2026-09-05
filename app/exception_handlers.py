from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import ChequeAPIException


async def cheque_exception_handler(
    request: Request,
    exc: ChequeAPIException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    print("UNHANDLED ERROR")
    print(type(exc).__name__)
    print(str(exc))

    return JSONResponse(
        status_code=502,
        content={
            "success": False,
            "error": {
                "code": "MODEL_ERROR",
                "message": "Internal server error"
            }
        }
    )