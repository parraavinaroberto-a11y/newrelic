from newrelic_telemetry_sdk import Span, SpansClient
import time, uuid

client = SpansClient(api_key="YOUR_INSERT_KEY")

trace_id = str(uuid.uuid4())

span = Span(
    id=str(uuid.uuid4()),
    trace_id=trace_id,
    timestamp=int(time.time() * 1000),
    name="sap_api_call",
    duration_ms=150,
    attributes={"system": "SAP", "endpoint": "/orders"}
)

response = client.send([span])
print("Trace result:", response)
