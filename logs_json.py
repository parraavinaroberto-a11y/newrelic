import json
import socket
import time
from datetime import datetime, timezone

import requests
from config import NEW_RELIC_LICENSE_KEY, LOG_URL, HEI_CONTEXT

def send_log(message, level="INFO", service="unknown", extra=None):
    ts_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    base = {
        "timestamp": ts_ms,
        "message": message,
        "level": level,
        "service": service,
        "host": socket.gethostname(),
        **HEI_CONTEXT,
    }
    if extra:
        base.update(extra)

    payload = [base]
    headers = {
        "Content-Type": "application/json",
        "X-License-Key": NEW_RELIC_LICENSE_KEY,
    }

    resp = requests.post(LOG_URL, headers=headers, data=json.dumps(payload))
    if resp.status_code >= 300:
        print("Error enviando log:", resp.status_code, resp.text)

if __name__ == "__main__":
    send_log("Prueba de log JSON desde Heineken kit", "INFO", "heineken.observability")
