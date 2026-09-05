from fastapi import HTTPException


class ChequeAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "error": {
                    "code": code,
                    "message": message
                }
            }
        )