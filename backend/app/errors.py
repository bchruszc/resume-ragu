"""Custom exception classes and error response models."""

from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse


# ---------------------------------------------------------------------------
# Exception classes
# ---------------------------------------------------------------------------

class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, status_code: int = 500, code: str = "APP_ERROR"):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class NotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=404, code="NOT_FOUND")


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=422, code="VALIDATION_ERROR")


class AIServiceError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=502, code="AI_SERVICE_ERROR")


class StorageError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500, code="STORAGE_ERROR")


# ---------------------------------------------------------------------------
# Error response models
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle AppError exceptions and return a consistent error envelope."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(code=exc.code, message=exc.message)
        ).model_dump(),
    )
