from typing import Any
from fastapi.responses import JSONResponse

def success(data: Any = None, message: str = "Success"):
    return JSONResponse(status_code=200, content={
        "code": 0,
        "message": message,
        "data": data
    })

def error(message: str = "Error", code: int = 1):
    return JSONResponse(status_code=200, content={
        "code": code,
        "message": message,
        "data": None
    })
