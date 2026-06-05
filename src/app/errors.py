from typing import Any, Dict, List, Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        title: str,
        detail: str,
        type_uri: str = "about:blank",
        invalid_params: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.type_uri = type_uri
        self.invalid_params = invalid_params

async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppException)
    content: Dict[str, Any] = {
        "type": exc.type_uri,
        "title": exc.title,
        "status": exc.status_code,
        "detail": exc.detail,
        "instance": str(request.url),
    }
    if exc.invalid_params is not None:
        content["invalid_params"] = exc.invalid_params
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        media_type="application/problem+json"
    )

async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    invalid_params: List[Dict[str, Any]] = []
    for error in exc.errors():
        loc = " -> ".join(str(x) for x in error["loc"])
        invalid_params.append({
            "name": loc,
            "reason": error["msg"]
        })
    content: Dict[str, Any] = {
        "type": "about:blank",
        "title": "Validation Failed",
        "status": 422,
        "detail": "The request entity has validation errors.",
        "instance": str(request.url),
        "invalid_params": invalid_params
    }
    return JSONResponse(
        status_code=422,
        content=content,
        media_type="application/problem+json"
    )

async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    content: Dict[str, Any] = {
        "type": "about:blank",
        "title": "HTTP Error",
        "status": exc.status_code,
        "detail": str(exc.detail),
        "instance": str(request.url)
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        media_type="application/problem+json"
    )

