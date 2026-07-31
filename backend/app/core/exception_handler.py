import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

from app.logging.logging_config import get_logger

logger = get_logger()


async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        "unhandled_exception",
        poc_id="POC-07",
        phase=1,
        associate_id="Panuganti Madhusudan",
        request_id="error",
        operation=request.url.path,
        duration_ms=0,
        status="failure",
        error=str(exc),
        extra={
            "stack_trace": traceback.format_exc()
        }
    )

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error"
        }
    )