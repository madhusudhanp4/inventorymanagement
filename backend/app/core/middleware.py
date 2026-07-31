import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next
    ):
        request_id = str(uuid.uuid4())

        start = time.time()

        # ENTRY LOG
        logger.info(
            "request_start",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            request_id=request_id,
            operation=f"{request.method} {request.url.path}",
            duration_ms=0,
            status="started",
            error=None,
            extra={
                "query_params": str(request.query_params)
            }
        )

        try:

            response = await call_next(
                request
            )

            duration_ms = int(
                (time.time() - start) * 1000
            )

            # EXIT LOG
            logger.info(
                "request_end",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti Madhusudan",
                request_id=request_id,
                operation=f"{request.method} {request.url.path}",
                duration_ms=duration_ms,
                status="success",
                error=None,
                extra={
                    "status_code": response.status_code
                }
            )

            return response

        except Exception as ex:

            duration_ms = int(
                (time.time() - start) * 1000
            )

            logger.error(
                "request_failed",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti Madhusudan",
                request_id=request_id,
                operation=f"{request.method} {request.url.path}",
                duration_ms=duration_ms,
                status="failure",
                error=str(ex),
                extra={}
            )

            raise