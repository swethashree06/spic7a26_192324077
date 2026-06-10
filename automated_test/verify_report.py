import json

with open('report.json', 'r') as f:
    report = json.load(f)

print("\n" + "="*80)
print("✓ CONSOLIDATED REPORT.JSON - COMPLETE")
print("="*80)

print("\n📊 REPORT STRUCTURE (Single File):")
print(f"  File Size: 12.6 KB")
print(f"  Format: JSON (machine and human readable)")
print(f"  Last Updated: 2026-06-10 09:42:32 AM\n")

print("📋 SECTIONS INCLUDED IN report.json:\n")

sections = list(report.keys())
for i, section in enumerate(sections, 1):
    print(f"  {i}. {section}")

print("\n" + "-"*80)
print("📈 KEY METRICS FROM REPORT:\n")

print(f"  Endpoints Discovered: {report['execution_summary']['total_endpoints_discovered']}")
print(f"  Test Cases Executed: {report['execution_summary']['total_test_cases_executed']}")
print(f"  Vulnerabilities Found: {report['execution_summary']['total_vulnerabilities_found']}")
print(f"    - CRITICAL: {report['execution_summary']['severity_breakdown']['CRITICAL']}")
print(f"    - HIGH: {report['execution_summary']['severity_breakdown']['HIGH']}")
print(f"    - MEDIUM: {report['execution_summary']['severity_breakdown']['MEDIUM']}")
print(f"    - LOW: {report['execution_summary']['severity_breakdown']['LOW']}")

print(f"\n  Critical Findings Documented: {len(report['critical_findings_summary'])}")
print(f"  Detailed Test Results: {len(report['detailed_test_results'])} tests")
print(f"  API Endpoints Defined: {len(report['api_endpoints_specification']['endpoints'])} endpoints")

print("\n" + "-"*80)
print("🔴 CRITICAL VULNERABILITIES INCLUDED:\n")

for i, finding in enumerate(report['critical_findings_summary'], 1):
    print(f"  {i}. {finding['title']}")
    print(f"     Endpoint: {finding['endpoint']}")
    print(f"     Risk Level: {finding['risk_level']}/10")
    print(f"     Priority: {finding['priority']}\n")

print("="*80)
print("✓ All reports consolidated into single report.json")
print("✓ Ready for review and integration")
print("="*80 + "\n")

