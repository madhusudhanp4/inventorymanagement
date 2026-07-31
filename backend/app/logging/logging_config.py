import logging
import structlog
import sys
import uuid


def get_logger():

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    return structlog.get_logger().bind(
        request_id=str(uuid.uuid4())[:8]
    )