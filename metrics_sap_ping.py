import time
import json
import socket
from datetime import datetime, timezone

import requests

from config import NEW_RELIC_LICENSE_KEY, METRIC_URL, HEI_CONTEXT
from logs_json import send_log

INTERVAL_SECONDS = 30
SAP_ENDPOINTS = [
    # personaliza estas URLs
    "https://sap-gateway.example.com/health",
    "https://sap-btp-api.example.com/health",
]

def build_availability_metric(endpoint, success, latency_ms):
    now = int(datetime.now(timezone.utc).timestamp())
    return {
        "name": "hei.service.availability",
        "type": "gauge",
        "value": 1 if success else 0,
        "timestamp": now,
        "attributes": {
            "endpoint": endpoint,
            "latency_ms": latency_ms,
            "host": socket.gethostname(),
            **HEI_CONTEXT,
        },
    }

def send_metrics(metrics):
    payload = [{"metrics": metrics}]
    headers = {
        "Api-Key": NEW_RELIC_LICENSE_KEY,
        "Content-Type": "application/json",
    }
    resp = requests.post(METRIC_URL, headers=headers, data=json.dumps(payload))
    if resp.status_code >= 300:
        print("Error enviando métricas SAP ping:", resp.status_code, resp.text)

def loop():
    while True:
        metrics = []
        for url in SAP_ENDPOINTS:
            start = time.time()
            ok = False
            try:
                r = requests.get(url, timeout=5)
                latency_ms = int((time.time() - start) * 1000)
                ok = r.status_code == 200
            except Exception as e:
                latency_ms = int((time.time() - start) * 1000)
                send_log(
                    f"Error en healthcheck {url}: {e}",
                    level="ERROR",
                    service="heineken.sap.healthcheck",
                    extra={"endpoint": url},
                )

            metrics.append(build_availability_metric(url, ok, latency_ms))

            if not ok:
                send_log(
                    f"Healthcheck FAIL {url}",
                    level="WARN",
                    service="heineken.sap.healthcheck",
                    extra={"endpoint": url, "latency_ms": latency_ms},
                )

        send_metrics(metrics)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    loop()
