import time
import uuid
from datetime import datetime, timezone

from newrelic_telemetry_sdk import Span, SpanClient
from config import NEW_RELIC_LICENSE_KEY, HEI_CONTEXT

_span_client = SpanClient(license_key=NEW_RELIC_LICENSE_KEY)

def create_span(name, parent_id=None, attributes=None, duration_ms=None):
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    start_ts = int(datetime.now(timezone.utc).timestamp() * 1000)

    attrs = {**HEI_CONTEXT}
    if attributes:
        attrs.update(attributes)

    span = Span(
        id=span_id,
        trace_id=trace_id,
        timestamp=start_ts,
        name=name,
        duration_ms=duration_ms or 0,
        parent_id=parent_id,
        attributes=attrs,
    )
    return span

class span_timer:
    """Context manager para medir duración de un bloque y enviar span."""

    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes or {}
        self._start = None

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = int((time.time() - self._start) * 1000)
        span = create_span(
            self.name,
            attributes={**self.attributes, "error": bool(exc_type)},
            duration_ms=duration_ms,
        )
        response = _span_client.send(span)
        print("Span enviado, status:", getattr(response, "status", None))

if __name__ == "__main__":
    with span_timer("hei.batch.sap_order_sync", {"system": "SAP"}):
        time.sleep(0.5)
