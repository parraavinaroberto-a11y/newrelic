import time
import json
import socket
import psutil
import requests
from datetime import datetime, timezone

from config import NEW_RELIC_LICENSE_KEY, METRIC_URL, HEI_CONTEXT

INTERVAL_SECONDS = 15

def build_metric(name, value, mtype="gauge", attributes=None):
    now = int(datetime.now(timezone.utc).timestamp())
    attrs = {
        "host": socket.gethostname(),
        **HEI_CONTEXT
    }
    if attributes:
        attrs.update(attributes)

    return {
        "name": name,
        "type": mtype,
        "value": value,
        "timestamp": now,
        "attributes": attrs,
    }

def send_metrics(metrics):
    payload = [{"metrics": metrics}]
    headers = {
        "Api-Key": NEW_RELIC_LICENSE_KEY,
        "Content-Type": "application/json",
    }
    resp = requests.post(METRIC_URL, headers=headers, data=json.dumps(payload))
    if resp.status_code >= 300:
        print("Error enviando métricas:", resp.status_code, resp.text)

def loop():
    print("Iniciando metrics_host loop…")
    while True:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        metrics = [
            build_metric("hei.host.cpu.percent", cpu),
            build_metric("hei.host.mem.percent", mem),
            build_metric("hei.host.disk.percent", disk),
        ]

        send_metrics(metrics)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    loop()
