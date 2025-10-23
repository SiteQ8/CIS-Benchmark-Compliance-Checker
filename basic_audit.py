#!/usr/bin/env python3
"""
Basic audit example for CIS Benchmark Compliance Checker.
"""

from cis_checker.auditors.ubuntu_auditor import UbuntuAuditor


def main():
    print("Starting CIS Benchmark Audit...\n")

    # Create auditor instance
    auditor = UbuntuAuditor(profile="ubuntu_22_04", level=1)

    # Run all checks
    print("Running compliance checks...")
    results = auditor.run_all_checks()

    # Display summary
    print(f"\nCompleted {len(results)} checks")
    print(f"Compliance Score: {auditor.get_compliance_score():.1f}%\n")

    # Display results
    for result in results:
        status_icon = "✅" if result.status == "pass" else "❌"
        print(f"{status_icon} [{result.check_id}] {result.title}")
        if result.status == "fail":
            print(f"   Remediation: {result.remediation}")

    # Export results
    auditor.export_results("audit_results.json")
    print("\nResults exported to audit_results.json")


if __name__ == "__main__":
    main()
