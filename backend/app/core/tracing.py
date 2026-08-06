"""
Project      : Inventory Management & Procurement System (POC-07)
Author       : Panuganti Madhusudan
Description  : OpenTelemetry tracing utility for Phase-1 observability
"""

from contextlib import contextmanager
import time

from opentelemetry import trace


tracer = trace.get_tracer(__name__)


@contextmanager
def span(span_name: str):
    start_time = time.time()

    with tracer.start_as_current_span(span_name):
        try:
            yield
        except Exception as ex:
            current_span = trace.get_current_span()
            current_span.record_exception(ex)
            raise
        finally:
            elapsed = round((time.time() - start_time) * 1000, 2)

            print(
                f"[TRACE END] "
                f"span={span_name} "
                f"duration_ms={elapsed}"
            )