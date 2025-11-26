import requests
import json
import time

LOG_API = "https://log-api.newrelic.com/log/v1"
API_KEY = "YOUR_LICENSE_KEY"

payload = [
    {
        "timestamp": int(time.time() * 1000),
        "message": "Error crítico en SAP BTP",
        "service": "sap-basis",
        "level": "ERROR",
        "hostname": "hana-cloud-node01"
    }
]

headers = {
    "Content-Type": "application/json",
    "X-License-Key": API_KEY
}

r = requests.post(LOG_API, headers=headers, data=json.dumps(payload))
print(r.status_code, r.text)
