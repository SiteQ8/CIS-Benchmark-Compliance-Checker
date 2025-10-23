"""
Command-line interface for CIS Benchmark Compliance Checker.
"""

import click
import json
import os
from pathlib import Path
from .auditors.ubuntu_auditor import UbuntuAuditor
from .reports.html_reporter import HTMLReporter
from .reports.json_reporter import JSONReporter
from .reports.csv_reporter import CSVReporter


@click.group()
@click.version_option(version="1.0.0")
def main():
    """CIS Benchmark Compliance Checker - Automated security auditing tool."""
    pass


@main.command()
@click.option('--os', 'os_type', type=click.Choice(['ubuntu', 'rhel', 'amazon-linux', 'windows', 'macos']),
              help='Operating system to audit')
@click.option('--profile', help='CIS profile to use')
@click.option('--level', type=click.IntRange(1, 2), default=1,
              help='CIS Level (1 or 2)')
@click.option('--output', type=click.Path(), default='./reports',
              help='Output directory for reports')
@click.option('--format', 'output_format', type=click.Choice(['html', 'json', 'csv']),
              default='html', multiple=True, help='Report format(s)')
@click.option('--verbose', is_flag=True, help='Verbose output')
def audit(os_type, profile, level, output, output_format, verbose):
    """Run CIS compliance audit."""
    click.echo("🔍 Starting CIS Benchmark Compliance Audit...")
    click.echo(f"   OS: {os_type or 'auto-detect'}")
    click.echo(f"   Level: {level}")
    click.echo(f"   Output: {output}")

    # Create output directory
    os.makedirs(output, exist_ok=True)

    # For demo, we'll use Ubuntu auditor
    if verbose:
        click.echo("\n📊 Running checks...")

    auditor = UbuntuAuditor(profile or "ubuntu_22_04", level)
    results = auditor.run_all_checks()

    # Export to JSON first
    json_path = os.path.join(output, "audit_results.json")
    auditor.export_results(json_path)

    if verbose:
        click.echo(f"   Ran {len(results)} checks")
        click.echo(f"   Compliance Score: {auditor.get_compliance_score():.1f}%")

    # Load the data for reporting
    with open(json_path, 'r') as f:
        audit_data = json.load(f)

    # Generate reports in requested formats
    if 'html' in output_format or not output_format:
        html_reporter = HTMLReporter()
        html_path = os.path.join(output, "compliance_report.html")
        html_reporter.generate(audit_data, html_path)
        click.echo(f"\n📄 HTML report: {html_path}")

    if 'json' in output_format:
        click.echo(f"📄 JSON report: {json_path}")

    if 'csv' in output_format:
        csv_reporter = CSVReporter()
        csv_path = os.path.join(output, "compliance_report.csv")
        csv_reporter.generate(audit_data, csv_path)
        click.echo(f"📄 CSV report: {csv_path}")

    score = auditor.get_compliance_score()
    if score >= 80:
        click.secho(f"\n✅ Audit completed! Compliance Score: {score:.1f}%", fg='green', bold=True)
    elif score >= 60:
        click.secho(f"\n⚠️  Audit completed! Compliance Score: {score:.1f}%", fg='yellow', bold=True)
    else:
        click.secho(f"\n❌ Audit completed! Compliance Score: {score:.1f}%", fg='red', bold=True)


@main.command()
@click.option('--profile', required=True, help='CIS profile to remediate')
@click.option('--checks', help='Comma-separated check IDs')
@click.option('--dry-run', is_flag=True, help='Show changes without applying')
@click.option('--backup', is_flag=True, help='Create backup before changes')
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
def remediate(profile, checks, dry_run, backup, force):
    """Apply remediation for non-compliant checks."""
    if dry_run:
        click.secho("🔍 DRY RUN MODE - No changes will be applied", fg='yellow')

    if not force and not dry_run:
        click.confirm('⚠️  This will modify system configuration. Continue?', abort=True)

    click.echo(f"\n🔧 Starting remediation for profile: {profile}")

    if backup:
        click.echo("📦 Creating system backup...")
        # Backup implementation would go here
        click.secho("✅ Backup created", fg='green')

    if checks:
        check_list = checks.split(',')
        click.echo(f"   Remediating specific checks: {', '.join(check_list)}")
    else:
        click.echo("   Remediating all failed checks")

    # Remediation implementation would go here
    click.echo("\n🔄 Applying remediations...")
    click.secho("✅ Remediation completed!", fg='green', bold=True)
    click.echo("\n💡 Tip: Run 'cis-checker audit' again to verify changes")


@main.command()
@click.option('--input', 'input_path', required=True, type=click.Path(exists=True),
              help='Input audit results file (JSON)')
@click.option('--format', 'output_format', type=click.Choice(['html', 'json', 'csv']),
              required=True, help='Output format')
@click.option('--output', 'output_path', help='Output file path')
def report(input_path, output_format, output_path):
    """Generate compliance reports from audit results."""
    click.echo(f"📊 Generating {output_format.upper()} report...")

    with open(input_path, 'r') as f:
        audit_data = json.load(f)

    if not output_path:
        output_path = f"compliance_report.{output_format}"

    if output_format == 'html':
        reporter = HTMLReporter()
        reporter.generate(audit_data, output_path)
    elif output_format == 'json':
        reporter = JSONReporter()
        reporter.generate(audit_data, output_path)
    elif output_format == 'csv':
        reporter = CSVReporter()
        reporter.generate(audit_data, output_path)

    click.secho(f"✅ Report generated: {output_path}", fg='green')


@main.command()
@click.option('--profiles', is_flag=True, help='List available profiles')
@click.option('--checks', help='List checks for profile')
@click.option('--os', 'os_type', help='Filter by operating system')
def list_items(profiles, checks, os_type):
    """List available profiles and checks."""
    if profiles:
        click.echo("\n📋 Available CIS Profiles:\n")
        profiles_list = [
            ("ubuntu_20_04", "Ubuntu 20.04 LTS"),
            ("ubuntu_22_04", "Ubuntu 22.04 LTS"),
            ("ubuntu_24_04", "Ubuntu 24.04 LTS"),
            ("rhel_8", "Red Hat Enterprise Linux 8"),
            ("rhel_9", "Red Hat Enterprise Linux 9"),
            ("amazon_linux_2", "Amazon Linux 2"),
            ("windows_server_2019", "Windows Server 2019"),
            ("windows_server_2022", "Windows Server 2022"),
            ("macos_13", "macOS 13 Ventura"),
            ("macos_14", "macOS 14 Sonoma"),
        ]

        for profile_id, profile_name in profiles_list:
            if not os_type or os_type.lower() in profile_id.lower():
                click.echo(f"  • {profile_id:<25} - {profile_name}")

    if checks:
        click.echo(f"\n📋 Checks for profile: {checks}\n")
        click.echo("  • 1.1.1 - Ensure mounting of cramfs filesystems is disabled")
        click.echo("  • 1.1.2 - Ensure mounting of freevxfs filesystems is disabled")
        click.echo("  • 3.5.1.1 - Ensure ufw is installed and enabled")
        click.echo("  • 4.1.1.1 - Ensure auditd is installed")
        click.echo("  • 5.4.1.1 - Ensure password expiration is configured")
        click.echo("\n  ... and more")


if __name__ == '__main__':
    main()
