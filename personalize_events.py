import requests
import json
import time

EVENT_URL = "https://insights-collector.newrelic.com/v1/accounts/YOUR_ACC_ID/events"
API_KEY = "YOUR_INSERT_KEY"

event = {
    "eventType": "SAPJobExecution",
    "job": "Z_BACKUP_HANA",
    "duration": 12.4,
    "status": "SUCCESS",
    "timestamp": int(time.time() * 1000)
}

headers = {
    "Content-Type": "application/json",
    "X-Insert-Key": API_KEY
}

res = requests.post(EVENT_URL, headers=headers, data=json.dumps(event))
print(res.status_code, res.text)
