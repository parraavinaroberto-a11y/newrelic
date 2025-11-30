import os
import time
import json
import socket
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEW_RELIC_INSERT_KEY = os.getenv("NEW_RELIC_INSERT_KEY")
NEW_RELIC_REGION = os.getenv("NEW_RELIC_REGION", "US").upper()

if NEW_RELIC_REGION == "EU":
    LOGS_URL = "https://log-api.eu.newrelic.com/log/v1"
else:
    LOGS_URL = "https://log-api.newrelic.com/log/v1"


def send_log(message: str, level: str = "INFO", extra: dict | None = None):
    if extra is None:
        extra = {}

    if not NEW_RELIC_INSERT_KEY:
        raise RuntimeError("Falta NEW_RELIC_INSERT_KEY")

    headers = {
        "Content-Type": "application/json",
        "Api-Key": NEW_RELIC_INSERT_KEY,
    }

    log_entry = {
        "timestamp": int(time.time() * 1000),
        "message": message,
        "loglevel": level,
        "service": "python-observability-demo",
        "hostname": socket.gethostname(),
        **extra,
    }

    payload = [
        {
            "common": {
                "attributes": {
                    "env": "dev",
                    "language": "python",
                }
            },
            "logs": [log_entry],
        }
    ]

    resp = requests.post(LOGS_URL, headers=headers, data=json.dumps(payload))
    resp.raise_for_status()
    return resp.status_code


if __name__ == "__main__":
    print("Enviando logs de ejemplo a New Relic...")
    send_log("Aplicación iniciada", "INFO")
    try:
        x = 1 / 0
    except ZeroDivisionError as e:
        send_log(
            "Error en procesamiento",
            "ERROR",
            {"error.type": type(e).__name__, "error.message": str(e)},
        )
    print("Listo.")
