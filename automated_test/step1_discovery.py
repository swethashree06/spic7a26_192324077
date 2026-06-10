"""
STEP 1: Endpoint Discovery
Analyzes the FastAPI backend to discover all routes and their access rules.
"""
import json
import requests
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from config import CONFIG

class EndpointDiscovery:
    def __init__(self):
        self.base_url = CONFIG.get_base_url()
        self.endpoints = []

    def add_endpoint(self, method: str, path: str, access_level: str,
                     auth_required: bool, roles: list = None, notes: str = ""):
        """Add a discovered endpoint to the list"""
        self.endpoints.append({
            'method': method,
            'path': path,
            'access_level': access_level,
            'auth_required': auth_required,
            'roles': roles or [],
            'notes': notes
        })

    def discover_from_code(self):
        """Discover endpoints from FastAPI source code analysis"""

        # Public endpoints (no auth required)
        self.add_endpoint('GET', '/', 'public', False, [],
            'Home endpoint - returns status and domain count')

        self.add_endpoint('POST', '/register', 'public', False, [],
            'User registration - public, creates new account')

        self.add_endpoint('POST', '/login', 'public', False, [],
            'User authentication - public, returns JWT token')

        self.add_endpoint('POST', '/google-login', 'public', False, [],
            'Google OAuth login - public, exchanges Google ID token')

        # Protected/Unprotected endpoints
        self.add_endpoint('POST', '/analyze', 'requires-investigation', False, [],
            'Resume analysis - NO EXPLICIT AUTH CHECK IN CODE - POTENTIAL VULNERABILITY')

    def verify_endpoints_live(self):
        """Test if endpoints actually respond"""
        print("\n🔍 Verifying endpoint availability...\n")
        verified = []

        for ep in self.endpoints:
            try:
                if ep['method'] == 'GET':
                    resp = requests.get(f"{self.base_url}{ep['path']}", timeout=3)
                    status = resp.status_code
                    verified.append({**ep, 'live': True, 'status': status})
                    print(f"  ✓ {ep['method']:6} {ep['path']:20} -> {status}")
                elif ep['method'] == 'POST':
                    # Don't actually POST without proper data
                    verified.append({**ep, 'live': 'not-tested', 'status': None})
                    print(f"  ? {ep['method']:6} {ep['path']:20} -> Not tested (POST)")
            except Exception as e:
                verified.append({**ep, 'live': False, 'error': str(e)})
                print(f"  ✗ {ep['method']:6} {ep['path']:20} -> ERROR: {e}")

        return verified

    def print_report(self):
        """Print discovered endpoints report"""
        print("\n" + "="*80)
        print("STEP 1: ENDPOINT DISCOVERY REPORT")
        print("="*80)

        print(f"\n📍 Base URL: {self.base_url}")
        print(f"📊 Total Endpoints Discovered: {len(self.endpoints)}")
        print("\n" + "-"*80)
        print(f"{'METHOD':<8} {'PATH':<25} {'ACCESS':<20} {'AUTH':<8} {'NOTES':<20}")
        print("-"*80)

        for ep in self.endpoints:
            auth_str = "✓ YES" if ep['auth_required'] else "✗ NO"
            print(f"{ep['method']:<8} {ep['path']:<25} {ep['access_level']:<20} {auth_str:<8} {ep['notes'][:20]:<20}")

        print("\n" + "="*80)
        print("\nKEY FINDINGS:")
        print("  • Total public endpoints: 4")
        print("  • Total protected endpoints: 0")
        print("  • Unverified endpoints: 1 (/analyze - NO EXPLICIT AUTH)")
        print("\n⚠  SECURITY CONCERNS IDENTIFIED:")
        print("  1. /analyze endpoint has NO auth check - POTENTIAL IDOR/Unauthenticated Access vulnerability")
        print("  2. CORS allows all origins - broad attack surface")
        print("  3. No rate limiting detected in source")
        print("\n" + "="*80)

    def save_expectation_model(self):
        """Save endpoint expectations to file for later comparison"""
        model = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'endpoints': self.endpoints
        }

        with open('expectation_model.json', 'w') as f:
            json.dump(model, f, indent=2)

        print(f"\n✓ Expectation model saved to: expectation_model.json")

if __name__ == '__main__':
    discovery = EndpointDiscovery()

    print("\n" + "="*80)
    print("SKILLSYNC AI - DAST ENDPOINT DISCOVERY")
    print("="*80)

    # Discover endpoints from code
    discovery.discover_from_code()

    # Verify live
    discovery.verify_endpoints_live()

    # Print report
    discovery.print_report()

    # Save expectations
    discovery.save_expectation_model()

    print("\n✓ Ready for security testing. Review discoveries above before proceeding.\n")

