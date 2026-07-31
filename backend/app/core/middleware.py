import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()


class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):
        request_id = str(uuid.uuid4())

        start = time.time()

        try:

            response = await call_next(
                request
            )

            logger.info(
                "request_complete",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti_Madhusudan",
                request_id=request_id,
                operation=f"{request.method} {request.url.path}",
                duration_ms=int(
                    (time.time() - start) * 1000
                ),
                status="success",
                error=None,
                extra={}
            )

            return response

        except Exception as ex:

            logger.error(
                "request_failed",
                poc_id="POC-07",
                phase=1,
                associate_id="Panuganti_Madhusudan",
                request_id=request_id,
                operation=f"{request.method} {request.url.path}",
                duration_ms=int(
                    (time.time() - start) * 1000
                ),
                status="failure",
                error=str(ex),
                extra={}
            )

            raise