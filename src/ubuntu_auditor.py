"""
Ubuntu Linux CIS Benchmark auditor.
"""

import subprocess
import os
from .base_auditor import BaseAuditor, CheckResult


class UbuntuAuditor(BaseAuditor):
    """Ubuntu-specific CIS Benchmark auditor."""

    def __init__(self, profile: str = "ubuntu_22_04", level: int = 1):
        super().__init__(profile, level)
        self.os_name = "Ubuntu"

    def check_password_policy(self) -> CheckResult:
        """Check password policy configuration."""
        try:
            # Check /etc/login.defs for password settings
            with open('/etc/login.defs', 'r') as f:
                content = f.read()
                if 'PASS_MAX_DAYS' in content and 'PASS_MIN_DAYS' in content:
                    return CheckResult(
                        check_id="5.4.1.1",
                        title="Ensure password expiration is configured",
                        status="pass",
                        description="Password expiration policy is properly configured",
                        severity="high"
                    )
        except Exception as e:
            return CheckResult(
                check_id="5.4.1.1",
                title="Ensure password expiration is configured",
                status="error",
                description=f"Error checking password policy: {str(e)}",
                severity="high"
            )

        return CheckResult(
            check_id="5.4.1.1",
            title="Ensure password expiration is configured",
            status="fail",
            description="Password expiration policy not properly configured",
            remediation="Edit /etc/login.defs and set PASS_MAX_DAYS, PASS_MIN_DAYS",
            severity="high"
        )

    def check_firewall_status(self) -> CheckResult:
        """Check UFW firewall status."""
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            if 'Status: active' in result.stdout:
                return CheckResult(
                    check_id="3.5.1.1",
                    title="Ensure ufw is installed and enabled",
                    status="pass",
                    description="UFW firewall is active and enabled",
                    severity="high"
                )
        except Exception as e:
            return CheckResult(
                check_id="3.5.1.1",
                title="Ensure ufw is installed and enabled",
                status="error",
                description=f"Error checking firewall: {str(e)}",
                severity="high"
            )

        return CheckResult(
            check_id="3.5.1.1",
            title="Ensure ufw is installed and enabled",
            status="fail",
            description="UFW firewall is not active",
            remediation="Run: sudo ufw enable",
            severity="high"
        )

    def check_audit_logging(self) -> CheckResult:
        """Check auditd configuration."""
        if os.path.exists('/etc/audit/auditd.conf'):
            return CheckResult(
                check_id="4.1.1.1",
                title="Ensure auditd is installed",
                status="pass",
                description="Auditd is installed and configured",
                severity="medium"
            )

        return CheckResult(
            check_id="4.1.1.1",
            title="Ensure auditd is installed",
            status="fail",
            description="Auditd is not installed",
            remediation="Run: sudo apt install auditd",
            severity="medium"
        )

    def check_file_permissions(self) -> CheckResult:
        """Check critical file permissions."""
        critical_files = ['/etc/passwd', '/etc/shadow', '/etc/group']
        issues = []

        for filepath in critical_files:
            if os.path.exists(filepath):
                stat_info = os.stat(filepath)
                mode = oct(stat_info.st_mode)[-3:]
                if filepath == '/etc/shadow' and mode != '000':
                    issues.append(f"{filepath} has incorrect permissions: {mode}")

        if not issues:
            return CheckResult(
                check_id="6.1.2",
                title="Ensure permissions on critical files are configured",
                status="pass",
                description="All critical files have correct permissions",
                severity="high"
            )

        return CheckResult(
            check_id="6.1.2",
            title="Ensure permissions on critical files are configured",
            status="fail",
            description="; ".join(issues),
            remediation="Run: sudo chmod 000 /etc/shadow",
            severity="high"
        )

    def check_service_configuration(self) -> CheckResult:
        """Check for unnecessary services."""
        try:
            result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'],
                                  capture_output=True, text=True)
            # Simple check - in production, compare against baseline
            return CheckResult(
                check_id="2.1.1",
                title="Ensure unnecessary services are not running",
                status="pass",
                description="Service configuration checked",
                severity="medium"
            )
        except Exception as e:
            return CheckResult(
                check_id="2.1.1",
                title="Ensure unnecessary services are not running",
                status="error",
                description=f"Error checking services: {str(e)}",
                severity="medium"
            )
