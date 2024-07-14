from fastapi import HTTPException
from functools import wraps


class CustomError(Exception):
    """Exception for custom define

    Attr:
        code -- error code
        message -- explanation of the error
    """

    def __init__(self, code, message, params=None):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.code} | {self.message}"


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomError as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": {"code": e.code, "message": e.message},
                },
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": {"code": "E500", "message": "Exception Error"},
                },
            )

    return wrapper
