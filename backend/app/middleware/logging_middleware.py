"""Request/Response logging middleware with execution time tracking."""
import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("smartagri.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        # Log incoming request
        logger.info(
            f"[{request_id}] ➜  {request.method} {request.url.path}"
            + (f"?{request.url.query}" if request.url.query else "")
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"[{request_id}] ✗  {request.method} {request.url.path} "
                f"| ERROR: {exc} | {elapsed:.1f}ms"
            )
            raise

        elapsed = (time.perf_counter() - start_time) * 1000
        status = response.status_code
        emoji = "✅" if status < 400 else ("⚠️" if status < 500 else "❌")

        logger.info(
            f"[{request_id}] {emoji} {request.method} {request.url.path} "
            f"| {status} | {elapsed:.1f}ms"
        )

        # Attach request ID and timing to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{elapsed:.1f}ms"
        return response
