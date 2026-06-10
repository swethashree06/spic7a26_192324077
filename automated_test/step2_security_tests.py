"""
STEP 2 & 3: Comprehensive Security Testing Suite
Tests for: AuthN/AuthZ, IDOR, Token Tampering, Injection, Rate Limiting
"""
import json
import requests
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple
import threading
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from config import CONFIG

class DastSecurityTester:
    def __init__(self):
        self.base_url = CONFIG.get_base_url()
        self.user_email = CONFIG.get_user_email()
        self.test_results = []
        self.tokens = {}
        self.rate_limit_results = defaultdict(list)

    def log_result(self, endpoint: str, method: str, role: str, status: int,
                   expected: int, finding: bool, severity: str, response_time: float,
                   category: str, note: str):
        """Log a single test result"""
        self.test_results.append({
            'endpoint': endpoint,
            'method': method,
            'role': role,
            'status': status,
            'expected_status': expected,
            'finding': finding,
            'severity': severity,
            'response_time_ms': round(response_time * 1000, 2),
            'test_category': category,
            'note': note,
            'timestamp': datetime.now().isoformat()
        })

    # ========== AUTH TESTS ==========

    def test_auth_bypass_no_token(self):
        """Test 1: AuthN Bypass - Access protected endpoints without token"""
        print("\n[TEST 1] Authentication Bypass - No Token")
        print("-" * 70)

        # Test unauthenticated access to /analyze
        url = f"{self.base_url}/analyze"
        try:
            headers = {'Content-Type': 'application/json'}

            # Try with a dummy file in the body - this endpoint expects file upload
            start = time.time()
            resp = requests.post(url, headers=headers, timeout=5)
            elapsed = time.time() - start

            status = resp.status_code
            finding = status in [200, 201, 204]  # Success codes = vulnerability
            severity = "CRITICAL" if finding else "INFO"

            note = "No auth required - file upload endpoint accepts unauthenticated requests"
            self.log_result('/analyze', 'POST', 'public', status, 401, finding, severity, elapsed, 'AuthN Bypass', note)

            print(f"  POST /analyze (no token)")
            print(f"    Status: {status} | Expected: 401 | Finding: {finding} | Severity: {severity}")
            print(f"    Response time: {elapsed*1000:.2f}ms")

        except Exception as e:
            print(f"  ERROR: {e}")

    def test_auth_bypass_malformed_token(self):
        """Test 2: AuthN Bypass - Malformed/Invalid token"""
        print("\n[TEST 2] Authentication Bypass - Malformed Token")
        print("-" * 70)

        url = f"{self.base_url}/analyze"

        malformed_tokens = [
            ("empty", ""),
            ("garbage", "not.a.jwt"),
            ("expired", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"),
        ]

        for token_name, token_value in malformed_tokens:
            try:
                headers = {'Content-Type': 'application/json'}
                if token_value:
                    headers['Authorization'] = f'Bearer {token_value}'

                start = time.time()
                resp = requests.post(url, headers=headers, timeout=5)
                elapsed = time.time() - start

                status = resp.status_code
                finding = status in [200, 201, 204]
                severity = "CRITICAL" if finding else "INFO"

                note = f"Malformed token ({token_name}) - should return 401"
                self.log_result('/analyze', 'POST', f'invalid_{token_name}', status, 401, finding, severity, elapsed, 'AuthN Bypass', note)

                print(f"  POST /analyze (malformed: {token_name})")
                print(f"    Status: {status} | Finding: {'✓ VULNERABLE' if finding else 'Protected'}")

            except Exception as e:
                print(f"  ERROR ({token_name}): {e}")

    # ========== REGISTER & LOGIN TESTS ==========

    def test_register_user(self):
        """Test 3: Register a test user for further testing"""
        print("\n[TEST 3] User Registration")
        print("-" * 70)

        url = f"{self.base_url}/register"
        timestamp = int(time.time())
        test_email = f"dasttest_{timestamp}@mailinator.com"
        test_password = "TestPassword123!"

        payload = {
            "full_name": f"DAST Test User {timestamp}",
            "email": test_email,
            "password": test_password
        }

        try:
            start = time.time()
            resp = requests.post(url, json=payload, timeout=10)
            elapsed = time.time() - start

            status = resp.status_code
            note = f"Registered user: {test_email}"

            print(f"  POST /register")
            print(f"    Status: {status}")
            print(f"    Response time: {elapsed*1000:.2f}ms")
            print(f"    Email: {test_email}")

            self.log_result('/register', 'POST', 'public', status, 200, False, 'INFO', elapsed, 'Registration', note)

            return test_email, test_password

        except Exception as e:
            print(f"  ERROR: {e}")
            return None, None

    def test_login_user(self, email: str, password: str):
        """Test 4: Login user and obtain JWT token"""
        print("\n[TEST 4] User Login")
        print("-" * 70)

        url = f"{self.base_url}/login"
        payload = {"email": email, "password": password}

        try:
            start = time.time()
            resp = requests.post(url, json=payload, timeout=10)
            elapsed = time.time() - start

            status = resp.status_code
            print(f"  POST /login")
            print(f"    Status: {status}")
            print(f"    Response time: {elapsed*1000:.2f}ms")

            self.log_result('/login', 'POST', 'user', status, 200, False, 'INFO', elapsed, 'Authentication', f"Logged in: {email}")

            if status == 200:
                data = resp.json()
                token = data.get('token', '')
                if token:
                    self.tokens['user'] = token
                    # Show token preview (first/last 10 chars)
                    token_preview = f"{token[:10]}...{token[-10:]}"
                    print(f"    Token obtained: {token_preview}")
                    return token

            return None

        except Exception as e:
            print(f"  ERROR: {e}")
            return None

    # ========== TOKEN TAMPERING TESTS ==========

    def test_token_tampering(self):
        """Test 5: JWT Token Tampering - modify claims without re-signing"""
        print("\n[TEST 5] JWT Token Tampering")
        print("-" * 70)

        if 'user' not in self.tokens:
            print("  ⚠ Skipped: No valid user token available")
            return

        token = self.tokens['user']

        # Try to tamper with JWT (flip signature)
        try:
            parts = token.split('.')
            if len(parts) == 3:
                header, payload, signature = parts

                # Flip a bit in the signature
                tampered_sig = ''.join(chr(ord(c) ^ 1) if c.isalpha() else c for c in signature[:20]).ljust(len(signature), '0')
                tampered_token = f"{header}.{payload}.{tampered_sig}"

                url = f"{self.base_url}/analyze"
                headers = {
                    'Authorization': f'Bearer {tampered_token}',
                    'Content-Type': 'application/json'
                }

                start = time.time()
                resp = requests.post(url, headers=headers, timeout=5)
                elapsed = time.time() - start

                status = resp.status_code
                # If tampered token is accepted, it's vulnerable
                finding = status in [200, 201, 204]
                severity = "CRITICAL" if finding else "INFO"

                note = "Tampered JWT signature - server should reject"
                self.log_result('/analyze', 'POST', 'tampered', status, 401, finding, severity, elapsed, 'Token Tampering', note)

                print(f"  POST /analyze (tampered JWT)")
                print(f"    Status: {status} | Expected: 401 | Finding: {finding}")

        except Exception as e:
            print(f"  ERROR: {e}")

    # ========== INJECTION TESTS ==========

    def test_sql_injection_detection(self):
        """Test 6: SQLi Detection - probe for SQL error patterns"""
        print("\n[TEST 6] SQL Injection Detection")
        print("-" * 70)

        sqli_payloads = [
            ("Single Quote", "' OR '1'='1"),
            ("Union Select", "' UNION SELECT NULL--"),
            ("Comment", "'; DROP TABLE users--"),
        ]

        for payload_name, payload in sqli_payloads:
            # Note: Without specific query parameters, we can't directly inject
            # But we can test via register endpoint
            url = f"{self.base_url}/register"
            test_data = {
                "full_name": f"Test {payload_name}",
                "email": f"{payload}@test.com",
                "password": "Test123!"
            }

            try:
                start = time.time()
                resp = requests.post(url, json=test_data, timeout=5)
                elapsed = time.time() - start

                status = resp.status_code
                body = resp.text

                # Look for SQL error patterns
                sql_errors = ['SQL', 'syntax', 'database', 'mysql', 'postgres', 'table not found']
                has_sql_error = any(err.lower() in body.lower() for err in sql_errors)

                finding = has_sql_error
                severity = "HIGH" if finding else "INFO"

                note = f"SQLi probe ({payload_name}) - checking for error patterns"
                self.log_result('/register', 'POST', 'public', status, 400, finding, severity, elapsed, 'Injection Detection', note)

                if finding:
                    print(f"  ⚠ Found SQL error pattern in {payload_name} response")

            except Exception as e:
                pass

    # ========== RATE LIMITING TESTS ==========

    def test_rate_limiting(self, endpoint: str = "/", burst_count: int = 30):
        """Test 7: Rate Limiting - burst requests to detect limits"""
        print(f"\n[TEST 7] Rate Limiting - Burst Test ({burst_count} requests)")
        print("-" * 70)

        url = f"{self.base_url}{endpoint}"
        status_codes = []
        response_times = []

        print(f"  Sending {burst_count} rapid requests to {endpoint}...")

        for i in range(burst_count):
            try:
                start = time.time()
                resp = requests.get(url, timeout=5)
                elapsed = time.time() - start
                status_codes.append(resp.status_code)
                response_times.append(elapsed)

                if i % 10 == 0:
                    print(f"    {i+1}/{burst_count} requests sent...", end='\r')

            except Exception as e:
                status_codes.append(0)
                response_times.append(0)

            time.sleep(0.05)  # Small delay between requests

        # Analyze results
        rate_limited = any(code in [429, 503] for code in status_codes)
        avg_time = sum(response_times) / len(response_times) if response_times else 0

        severity = "WARNING" if rate_limited else "CRITICAL"
        note = f"No rate limit detected" if not rate_limited else f"Rate limit detected at ~{status_codes.index(429) if 429 in status_codes else '?'} requests"

        self.log_result(endpoint, 'GET', 'burst', 200, 200, not rate_limited, severity, avg_time, 'Rate Limiting', note)

        print(f"\n  Results:")
        print(f"    Total requests: {burst_count}")
        print(f"    Avg response time: {avg_time*1000:.2f}ms")
        print(f"    Rate limit detected: {rate_limited}")
        print(f"    Status codes: {set(status_codes)}")

    # ========== UNAUTHENTICATED FILE UPLOAD TEST ==========

    def test_unauthenticated_file_upload(self):
        """Test 8: IDOR/Unauth Upload - Upload file without authentication"""
        print("\n[TEST 8] Unauthenticated File Upload")
        print("-" * 70)

        url = f"{self.base_url}/analyze"

        # Create a simple test file
        test_content = b"""
        Python Developer

        Skills: Python, Django, FastAPI, PostgreSQL, Redis
        Experience: 5 years
        Projects:
        - Built REST APIs
        - Machine Learning pipeline
        - Data analysis tools
        """

        try:
            files = {'file': ('test_resume.txt', test_content, 'text/plain')}
            headers = {}  # No auth header

            start = time.time()
            resp = requests.post(url, files=files, headers=headers, timeout=10)
            elapsed = time.time() - start

            status = resp.status_code
            finding = status in [200, 201]
            severity = "CRITICAL" if finding else "INFO"

            note = "Unauthenticated file upload accepted - potential IDOR/abuse"
            self.log_result('/analyze', 'POST', 'public', status, 401, finding, severity, elapsed, 'Unauthenticated Access', note)

            print(f"  POST /analyze (file upload, no auth)")
            print(f"    Status: {status} | Expected: 401 | Finding: {finding}")
            if status in [200, 201]:
                print(f"    ⚠ VULNERABILITY: File accepted without authentication!")
                if status == 200:
                    try:
                        resp_data = resp.json()
                        print(f"    Response preview: {str(resp_data)[:200]}")
                    except:
                        pass

        except Exception as e:
            print(f"  ERROR: {e}")

    # ========== CORS TEST ==========

    def test_cors_misconfiguration(self):
        """Test 9: CORS Misconfiguration - test origin validation"""
        print("\n[TEST 9] CORS Misconfiguration")
        print("-" * 70)

        url = f"{self.base_url}/"

        # Test with malicious origin
        headers = {
            'Origin': 'http://attacker.com',
            'Access-Control-Request-Method': 'POST'
        }

        try:
            start = time.time()
            resp = requests.options(url, headers=headers, timeout=5)
            elapsed = time.time() - start

            cors_header = resp.headers.get('Access-Control-Allow-Origin', '')
            finding = cors_header != ''
            severity = "HIGH" if finding else "INFO"

            note = f"CORS allows: {cors_header if cors_header else 'Restricted'}"
            self.log_result('/', 'OPTIONS', 'public', resp.status_code, 200, finding, severity, elapsed, 'CORS', note)

            print(f"  OPTIONS / (from attacker.com)")
            print(f"    CORS Allow-Origin: {cors_header if cors_header else '(not set)'}")
            if finding:
                print(f"    ⚠ CORS allows external origins!")

        except Exception as e:
            print(f"  ERROR: {e}")

    def run_all_tests(self):
        """Run all security tests"""
        print("\n" + "="*80)
        print("SKILLSYNC AI - DAST SECURITY TESTING SUITE")
        print("="*80)

        # AuthN tests
        self.test_auth_bypass_no_token()
        self.test_auth_bypass_malformed_token()

        # Create user and login
        email, password = self.test_register_user()
        if email and password:
            self.test_login_user(email, password)

        # Token tampering
        self.test_token_tampering()

        # Injection tests
        self.test_sql_injection_detection()

        # Rate limiting
        self.test_rate_limiting("/", burst_count=30)

        # File upload
        self.test_unauthenticated_file_upload()

        # CORS
        self.test_cors_misconfiguration()

    def save_report(self):
        """Save test results to report.json"""
        with open('report.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)

        print(f"\n✓ Report saved: report.json ({len(self.test_results)} test cases)")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)

        total = len(self.test_results)
        findings = sum(1 for r in self.test_results if r['finding'])
        critical = sum(1 for r in self.test_results if r['severity'] == 'CRITICAL')
        high = sum(1 for r in self.test_results if r['severity'] == 'HIGH')

        print(f"\n📊 Tests Run: {total}")
        print(f"🚨 Findings: {findings}")
        print(f"  CRITICAL: {critical}")
        print(f"  HIGH: {high}")

        print("\n" + "-"*80)
        print("Tests by Category:")
        for category in set(r['test_category'] for r in self.test_results):
            count = sum(1 for r in self.test_results if r['test_category'] == category)
            print(f"  ✓ {category}: {count} tests")

if __name__ == '__main__':
    tester = DastSecurityTester()
    tester.run_all_tests()
    tester.save_report()
    tester.print_summary()

    print("\n" + "="*80)
    print("Detailed results saved in: report.json")
    print("="*80 + "\n")

