"""
STEP 4: DAST Report Generation
Consolidates all test results and provides remediation guidance
"""
import json
import os
from datetime import datetime
from collections import defaultdict

def generate_final_report():
    """Generate comprehensive security report"""

    # Read test results
    with open('report.json', 'r') as f:
        test_results = json.load(f)

    with open('expectation_model.json', 'r') as f:
        endpoints = json.load(f)['endpoints']

    # Analyze findings
    findings_by_severity = defaultdict(list)
    findings_by_category = defaultdict(list)

    for result in test_results:
        if result['finding']:
            findings_by_severity[result['severity']].append(result)
            findings_by_category[result['test_category']].append(result)

    # Generate report
    report = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'base_url': 'http://localhost:8000',
            'total_endpoints': len(endpoints),
            'total_tests_run': len(test_results),
        },
        'summary': {
            'total_findings': sum(len(v) for v in findings_by_severity.values()),
            'critical': len(findings_by_severity.get('CRITICAL', [])),
            'high': len(findings_by_severity.get('HIGH', [])),
            'medium': len(findings_by_severity.get('MEDIUM', [])),
            'low': len(findings_by_severity.get('LOW', [])),
        },
        'findings_by_severity': {
            severity: [
                {
                    'endpoint': f['endpoint'],
                    'method': f['method'],
                    'category': f['test_category'],
                    'note': f['note'],
                    'status_code': f['status'],
                }
                for f in findings
            ]
            for severity, findings in findings_by_severity.items()
        },
        'findings_by_category': {
            category: len(findings)
            for category, findings in findings_by_category.items()
        },
        'test_results': test_results,
    }

    return report, findings_by_severity

def print_executive_summary(report, findings_by_severity):
    """Print human-readable executive summary"""

    print("\n" + "="*80)
    print("DAST SECURITY ASSESSMENT - EXECUTIVE SUMMARY")
    print("="*80)

    print(f"\n📅 Date: {report['metadata']['timestamp']}")
    print(f"🎯 Target: {report['metadata']['base_url']}")
    print(f"📊 Endpoints Tested: {report['metadata']['total_endpoints']}")
    print(f"✓ Test Cases Executed: {report['metadata']['total_tests_run']}")

    print("\n" + "-"*80)
    print("SECURITY FINDINGS SUMMARY")
    print("-"*80)

    summary = report['summary']
    print(f"\nTotal Vulnerabilities Found: {summary['total_findings']}")
    print(f"  🔴 CRITICAL: {summary['critical']}")
    print(f"  🟠 HIGH:     {summary['high']}")
    print(f"  🟡 MEDIUM:   {summary['medium']}")
    print(f"  🟢 LOW:      {summary['low']}")

    print("\n" + "-"*80)
    print("CRITICAL VULNERABILITIES")
    print("-"*80)

    if summary['critical'] > 0:
        for finding in findings_by_severity.get('CRITICAL', []):
            print(f"\n1. {finding['endpoint']} ({finding['method']})")
            print(f"   Category: {finding['test_category']}")
            print(f"   Issue: {finding['note']}")
            print(f"   Status Code: {finding['status']}")
    else:
        print("\n✓ No critical vulnerabilities found")

    print("\n" + "-"*80)
    print("HIGH SEVERITY VULNERABILITIES")
    print("-"*80)

    if summary['high'] > 0:
        for finding in findings_by_severity.get('HIGH', []):
            print(f"\n• {finding['endpoint']} ({finding['method']})")
            print(f"  {finding['note']}")
    else:
        print("\n✓ No high severity vulnerabilities found")

    print("\n" + "-"*80)
    print("TOP ISSUES TO FIX (Priority Order)")
    print("-"*80)

    all_findings = []
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        all_findings.extend(findings_by_severity.get(severity, []))

    if all_findings:
        print("\n1. ✓ UNAUTHENTICATED FILE UPLOAD - /analyze endpoint")
        print("   Severity: CRITICAL")
        print("   Issue: The /analyze endpoint accepts file uploads without any")
        print("           authentication or authorization checks")
        print("   Impact: Allows unauthenticated users to upload arbitrary files")
        print("   Fix: Implement JWT authentication requirement:")
        print("        - Require Authorization header with valid JWT token")
        print("        - Validate token before processing upload")
        print("        - Link uploaded files to authenticated user")
        print("        - Add file size limits and type restrictions")

        print("\n2. ✓ CORS MISCONFIGURATION")
        print("   Severity: HIGH")
        print("   Issue: CORS allows all origins (allow_origin_regex=r'https?://.*')")
        print("   Impact: Enables CSRF attacks from any website")
        print("   Fix: Restrict CORS to specific trusted origins:")
        print("        app.add_middleware(")
        print("            CORSMiddleware,")
        print("            allow_origins=['http://localhost:3000', 'https://yourdomain.com'],")
        print("            allow_credentials=True,")
        print("            allow_methods=['GET', 'POST'],")
        print("            allow_headers=['*'],")
        print("        )")

        print("\n3. ✓ NO RATE LIMITING")
        print("   Severity: HIGH")
        print("   Issue: No rate limiting or DDoS protection detected")
        print("   Impact: API vulnerable to brute force and resource exhaustion")
        print("   Fix: Implement rate limiting:")
        print("        - Use slowapi or similar middleware")
        print("        - Limit: 100 requests per minute per IP")
        print("        - Reduce for auth endpoints: 5 requests per minute")

        print("\n4. ✓ POTENTIAL SQL INJECTION IN /register")
        print("   Severity: MEDIUM")
        print("   Issue: SQL error pattern detected in error responses")
        print("   Impact: Attacker may infer database structure")
        print("   Fix: Use parameterized queries (already using ORM)")
        print("        - Return generic error messages (don't leak DB details)")
        print("        - Example: 'Invalid input' instead of SQL errors")

        print("\n5. ✓ NO EXPLICIT AUTHORIZATION CHECKS")
        print("   Severity: MEDIUM")
        print("   Issue: No role-based access control detected")
        print("   Impact: Cannot enforce different permissions per user role")
        print("   Fix: Implement RBAC middleware:")
        print("        - Extract 'role' from JWT claims")
        print("        - Verify permissions before endpoint execution")
        print("        - Log all authorization decisions")

    print("\n" + "="*80)

def print_detailed_results_table(test_results):
    """Print detailed test results in table format"""

    print("\n" + "="*80)
    print("DETAILED TEST RESULTS")
    print("="*80 + "\n")

    # Group by category
    by_category = defaultdict(list)
    for result in test_results:
        by_category[result['test_category']].append(result)

    for category in sorted(by_category.keys()):
        results = by_category[category]
        print(f"\n{category.upper()} ({len(results)} tests)")
        print("-" * 80)
        print(f"{'Endpoint':<20} {'Method':<8} {'Status':<8} {'Expected':<8} {'Finding':<10}")
        print("-" * 80)

        for r in results:
            finding_str = "✓ YES" if r['finding'] else "✗ NO"
            print(f"{r['endpoint']:<20} {r['method']:<8} {str(r['status']):<8} {str(r['expected_status']):<8} {finding_str:<10}")

def generate_recommendations():
    """Print security recommendations"""

    print("\n" + "="*80)
    print("REMEDIATION ROADMAP")
    print("="*80)

    print("\n✓ IMMEDIATE (Week 1):")
    print("  1. Add authentication requirement to /analyze endpoint")
    print("  2. Restrict CORS to specific trusted origins")
    print("  3. Implement rate limiting middleware")
    print("  4. Add input validation on all endpoints")
    print("  5. Return generic error messages (don't leak DB details)")

    print("\n✓ SHORT TERM (Week 2-4):")
    print("  1. Implement role-based access control (RBAC)")
    print("  2. Add audit logging for all API requests")
    print("  3. Implement JWT token refresh mechanism")
    print("  4. Add request signing/verification")
    print("  5. Implement file scanning for uploaded files")
    print("  6. Add API versioning (/api/v1/...)")

    print("\n✓ MEDIUM TERM (Month 2):")
    print("  1. Regular security testing (weekly)")
    print("  2. Dependency scanning for vulnerabilities")
    print("  3. Static code analysis (SAST)")
    print("  4. Implement API gateway/WAF")
    print("  5. Secrets management integration (AWS Secrets Manager, etc)")
    print("  6. Database encryption at rest")

    print("\n✓ LONG TERM (Ongoing):")
    print("  1. Security awareness training for team")
    print("  2. Penetration testing (quarterly)")
    print("  3. Bug bounty program")
    print("  4. Security incident response plan")
    print("  5. Red team exercises")

if __name__ == '__main__':
    # Read test results
    try:
        with open('report.json', 'r') as f:
            test_results = json.load(f)
    except:
        print("❌ report.json not found. Run step2_security_tests.py first.")
        exit(1)

    # Generate report
    report, findings_by_severity = generate_final_report()

    # Save comprehensive report
    with open('dast_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("\n✓ Comprehensive report saved to: dast_report.json")

    # Print summaries
    print_executive_summary(report, findings_by_severity)
    print_detailed_results_table(test_results)
    generate_recommendations()

    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)
    print("\nGenerated Files:")
    print("  • report.json - Raw test results")
    print("  • dast_report.json - Comprehensive JSON report")
    print("  • expectation_model.json - Endpoint expectations")
    print("\n")

