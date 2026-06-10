"""
STEP 3a: Hardcoded Credentials Scanner
Scans the codebase for committed secrets and credentials
"""
import os
import re
import json
from pathlib import Path

class CredentialsScanner:
    def __init__(self):
        self.findings = []
        self.patterns = {
            'AWS_ACCESS_KEY': r'AKIA[0-9A-Z]{16}',
            'AWS_SECRET_KEY': r'aws_secret_access_key.*[=:]\s*[\'"]?([A-Za-z0-9/+=]{40})[\'"]?',
            'Private_Key': r'-----BEGIN (RSA|DSA|EC) PRIVATE KEY-----',
            'API_Key': r'api[_-]?key["\']?\s*[:=]\s*["\']?([A-Za-z0-9\-_]{20,})["\']?',
            'JWT_Token': r'Bearer\s+eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
            'Password_Assignment': r'password["\']?\s*[:=]\s*["\']?([A-Za-z0-9!@#$%^&*]{8,})["\']?',
            'Token_Assignment': r'token["\']?\s*[:=]\s*["\']?([A-Za-z0-9\-_.]{20,})["\']?',
        }

    def scan_file(self, filepath):
        """Scan a single file for secrets"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for pattern_name, pattern in self.patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Skip test files and comments
                    if 'test' in filepath.lower() or 'example' in filepath.lower():
                        continue

                    self.findings.append({
                        'file': filepath,
                        'pattern': pattern_name,
                        'match': match.group(0)[:100],  # First 100 chars
                        'line_num': content[:match.start()].count('\n') + 1
                    })
        except:
            pass

    def scan_directory(self, root_path):
        """Recursively scan directory for secrets"""
        skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'build', 'dist', '.pytest_cache'}
        skip_extensions = {'.pyc', '.class', '.jar', '.exe', '.dll', '.so'}

        for dirpath, dirnames, filenames in os.walk(root_path):
            # Remove skip directories
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]

            for filename in filenames:
                if not any(filename.endswith(ext) for ext in skip_extensions):
                    filepath = os.path.join(dirpath, filename)
                    self.scan_file(filepath)

    def print_report(self):
        """Print findings"""
        print("\n" + "="*80)
        print("HARDCODED CREDENTIALS SCANNER")
        print("="*80)

        if not self.findings:
            print("\n✓ No obvious hardcoded secrets detected in scanned files")
            print("\nNote: This scan looks for common patterns. Manual review recommended.")
            return

        print(f"\n⚠ Found {len(self.findings)} potential secrets:\n")

        for i, finding in enumerate(self.findings, 1):
            print(f"{i}. {finding['file']} (line {finding['line_num']})")
            print(f"   Pattern: {finding['pattern']}")
            print(f"   Match: {finding['match'][:80]}")
            print()

if __name__ == '__main__':
    scanner = CredentialsScanner()

    # Scan backend
    backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app')
    webapp_path = os.path.join(os.path.dirname(__file__), '..', 'webapp')

    print("Scanning for hardcoded credentials...")
    for path in [backend_path, app_path, webapp_path]:
        if os.path.exists(path):
            print(f"  Scanning: {path}")
            scanner.scan_directory(path)

    scanner.print_report()

