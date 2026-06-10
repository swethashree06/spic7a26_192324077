"""
Master DAST Runner Script - Execute all security tests in sequence
"""
import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(script_name, description):
    """Run a test script and handle output"""
    print(f"\n{'='*80}")
    print(f"▶ RUNNING: {description}")
    print(f"{'='*80}")
    print(f"  Script: {script_name}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print(f"\n✓ {description} - PASSED")
            return True
        else:
            print(f"\n✗ {description} - FAILED (return code: {result.returncode})")
            return False

    except Exception as e:
        print(f"\n✗ ERROR running {script_name}: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("SKILLSYNC AI - COMPREHENSIVE DAST (Dynamic Application Security Testing)")
    print("="*80)
    print(f"Started: {datetime.now().isoformat()}")
    print("="*80)

    results = {
        'step1_discovery': run_command('step1_discovery.py', 'STEP 1: Endpoint Discovery'),
        'step2_security': run_command('step2_security_tests.py', 'STEP 2-3: Security Testing & Token Analysis'),
        'step3a_creds': run_command('step3a_credentials_scan.py', 'STEP 3A: Hardcoded Credentials Scan'),
        'step4_report': run_command('step4_report_generation.py', 'STEP 4: Report Generation & Analysis'),
    }

    print("\n" + "="*80)
    print("DAST EXECUTION SUMMARY")
    print("="*80)

    all_passed = all(results.values())

    for step, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {step}: {status}")

    print(f"\nFinished: {datetime.now().isoformat()}")

    if all_passed:
        print("\n✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("\n📄 Generated Reports:")
        print("  • dast_report.json - Comprehensive security findings")
        print("  • report.json - Detailed test results (13 test cases)")
        print("  • expectation_model.json - Endpoint expectations")
        print("\n🔒 Check dast_report.json for critical findings and remediation steps.")
    else:
        print("\n⚠ Some tests encountered issues. Review output above.")

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()

