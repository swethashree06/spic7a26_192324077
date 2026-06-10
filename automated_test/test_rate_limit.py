import requests
import json
import time

with open("input.json", "r") as f:
    config = json.load(f)

BASE_URL = config.get("baseUrl", "http://localhost:8000")

def test_rate_limiting():
    url = f"{BASE_URL}/"
    codes = []
    print("Firing 30 requests to check for rate limiting...")
    for i in range(30):
        try:
            res = requests.get(url, timeout=5)
            codes.append(res.status_code)
        except:
            codes.append(0)

    ratelimited = 429 in codes
    print(f"Results: {codes}")

    finding = not ratelimited
    report = [{
        "endpoint": "/",
        "method": "GET",
        "role": "unauthenticated",
        "status": 200,
        "expected_status": 429,
        "finding": finding,
        "severity": "Medium",
        "test_category": "Rate Limiting",
        "note": "No rate limiting detected after 30 requests." if finding else "Rate limiting working (429 detected).",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }]

    with open("automated_test/report_ratelimit.json", "w") as f:
        json.dump(report, f, indent=2)

test_rate_limiting()
