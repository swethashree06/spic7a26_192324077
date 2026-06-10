import requests
import json
import os
import time

with open("input.json", "r") as f:
    config = json.load(f)

BASE_URL = config.get("baseUrl", "http://localhost:8000")
USER_EMAIL = config.get("user_email")

report = []

def log_test(endpoint, method, role, status, expected, finding, severity, category, note):
    report.append({
        "endpoint": endpoint,
        "method": method,
        "role": role,
        "status": status,
        "expected_status": expected,
        "finding": finding,
        "severity": severity,
        "test_category": category,
        "note": note,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

def test_unauthenticated_analyze():
    # Testing /analyze without any auth - the current code doesn't seem to check for it.
    url = f"{BASE_URL}/analyze"
    # Need a dummy file
    files = {'file': ('test.txt', 'This is a test resume content with python and java keywords.')}
    try:
        start = time.time()
        res = requests.post(url, files=files, timeout=10)
        elapsed = (time.time() - start) * 1000

        # Expected: If it's private data, should be 401.
        # Current code uses hardcoded user_id=1 and doesn't check for headers.
        is_finding = res.status_code == 200
        log_test("/analyze", "POST", "unauthenticated", res.status_code, 401, is_finding, "High" if is_finding else "Low", "AuthN Bypass",
                 "Endpoint processed resume and saved to DB (user_id:1) without authentication." if is_finding else "Access denied as expected.")
    except Exception as e:
        log_test("/analyze", "POST", "unauthenticated", 0, 401, False, "Info", "Network Error", str(e))

def test_auth_endpoints():
    # GET / is public
    url = f"{BASE_URL}/"
    res = requests.get(url)
    log_test("/", "GET", "unauthenticated", res.status_code, 200, res.status_code != 200, "Low", "Basic Connectivity", "Public home page")

test_unauthenticated_analyze()
test_auth_endpoints()

with open("automated_test/report_auth.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"Auth tests completed. {len(report)} results written to automated_test/report_auth.json")
