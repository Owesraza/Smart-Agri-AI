"""Custom exception classes and global exception handlers."""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


# ── Custom Exceptions ──────────────────────────────────────
class AppException(HTTPException):
    def __init__(self, status_code: int, message: str, detail: str = None):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.extra_detail = detail


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(404, f"{resource} not found")


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(401, message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(403, message)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(409, message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(400, message)


# ── Exception Handlers ─────────────────────────────────────
def error_response(status_code: int, message: str, detail=None) -> dict:
    return {
        "success": False,
        "status_code": status_code,
        "message": message,
        "detail": detail,
    }


async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"AppException [{exc.status_code}]: {exc.message} | {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.status_code, exc.message, exc.extra_detail),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException [{exc.status_code}]: {exc.detail} | {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.status_code, str(exc.detail)),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({"field": field, "message": error["msg"]})
    logger.warning(f"Validation error: {errors} | {request.url}")
    return JSONResponse(
        status_code=422,
        content=error_response(422, "Validation failed", errors),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc} | {request.url}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response(500, "Internal server error. Please try again later."),
    )
