"""
Project      : Inventory Management & Procurement System (POC-07)
Author       : Panuganti Madhusudan
Description  : Lightweight tracing utility for Phase-1 observability
"""

from contextlib import contextmanager
from datetime import datetime
import time
import uuid


@contextmanager
def span(span_name: str):
    trace_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    print(
        f"[TRACE START] "
        f"span={span_name} "
        f"trace_id={trace_id} "
        f"time={datetime.now()}"
    )

    try:
        yield
    except Exception as ex:
        print(
            f"[TRACE ERROR] "
            f"span={span_name} "
            f"trace_id={trace_id} "
            f"error={str(ex)}"
        )
        raise
    finally:
        elapsed = round((time.time() - start_time) * 1000, 2)

        print(
            f"[TRACE END] "
            f"span={span_name} "
            f"trace_id={trace_id} "
            f"duration_ms={elapsed}"
        )
