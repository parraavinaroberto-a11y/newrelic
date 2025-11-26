from newrelic_telemetry_sdk import GaugeMetric, MetricsClient
import time

API_KEY = "YOUR_INSERT_KEY"

client = MetricsClient(api_key=API_KEY)

cpu_usage = 72.5
memory_usage = 1580

metric = [
    GaugeMetric(name="custom.cpu.usage", value=cpu_usage),
    GaugeMetric(name="custom.memory.used_mb", value=memory_usage)
]

response = client.send(metric)
print("Response:", response)
