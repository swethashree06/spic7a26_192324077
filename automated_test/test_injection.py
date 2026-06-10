import requests
import json
import time

with open("input.json", "r") as f:
    config = json.load(f)

BASE_URL = config.get("baseUrl", "http://localhost:8000")

report = []

def log_test(endpoint, method, payload_type, status, finding, severity, note):
    report.append({
        "endpoint": endpoint,
        "method": method,
        "role": "unauthenticated",
        "status": status,
        "expected_status": 400, # We expect errors for bad payloads
        "finding": finding,
        "severity": severity,
        "test_category": "Injection",
        "note": f"Payload type: {payload_type}. {note}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

def test_login_injection():
    url = f"{BASE_URL}/login"
    # Testing for common SQLi strings in login fields
    payloads = [
        {"email": "' OR '1'='1", "password": "password"},
        {"email": "admin@example.com", "password": "' OR '1'='1"}
    ]

    for p in payloads:
        try:
            res = requests.post(url, json=p, timeout=10)
            # If we get a 200 with an injection payload, it's a critical finding
            # If we get a 500, it might be a vulnerable query crashing
            finding = res.status_code == 200 or res.status_code == 500
            log_test("/login", "POST", "SQLi", res.status_code, finding, "Critical" if finding else "Low",
                     "Potentially vulnerable if status is 200/500." if finding else "Input handled or rejected correctly.")
        except Exception as e:
            print(f"Error in test: {e}")

test_login_injection()

with open("automated_test/report_injection.json", "w") as f:
    json.dump(report, f, indent=2)
