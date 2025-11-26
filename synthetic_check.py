import os
import time
import json
import socket
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from config import NEW_RELIC_LICENSE_KEY, METRIC_URL, HEI_CONTEXT
from logs_json import send_log

load_dotenv()
INTERVAL_SECONDS = 60
ENDPOINTS = [e.strip() for e in os.getenv("SYNTH_ENDPOINTS", "").split(",") if e.strip()]

def build_synth_metric(endpoint, status, latency_ms):
    now = int(datetime.now(timezone.utc).timestamp())
    return {
        "name": "hei.synthetic.availability",
        "type": "gauge",
        "value": 1 if status == "UP" else 0,
        "timestamp": now,
        "attributes": {
            "endpoint": endpoint,
            "status": status,
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
        print("Error enviando métricas synthetic:", resp.status_code, resp.text)

def loop():
    if not ENDPOINTS:
        raise RuntimeError("No hay endpoints en SYNTH_ENDPOINTS en .env")

    print("Iniciando synthetic_check loop…")
    while True:
        metrics = []
        for url in ENDPOINTS:
            start = time.time()
            status = "DOWN"
            try:
                r = requests.get(url, timeout=10)
                latency_ms = int((time.time() - start) * 1000)
                if 200 <= r.status_code < 300:
                    status = "UP"
            except Exception as e:
                latency_ms = int((time.time() - start) * 1000)
                send_log(
                    f"Error synthetic {url}: {e}",
                    level="ERROR",
                    service="heineken.synthetic",
                    extra={"endpoint": url},
                )

            metrics.append(build_synth_metric(url, status, latency_ms))

            send_log(
                f"Synthetic {url} {status} {latency_ms}ms",
                level="INFO" if status == "UP" else "WARN",
                service="heineken.synthetic",
                extra={"endpoint": url, "latency_ms": latency_ms, "status": status},
            )

        send_metrics(metrics)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    loop()
