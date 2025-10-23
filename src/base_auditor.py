"""
Base auditor class for CIS Benchmark compliance checking.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import json


class CheckResult:
    """Represents the result of a single CIS check."""

    def __init__(self, check_id: str, title: str, status: str, 
                 description: str = "", remediation: str = "", 
                 severity: str = "medium"):
        self.check_id = check_id
        self.title = title
        self.status = status  # pass, fail, skip, error
        self.description = description
        self.remediation = remediation
        self.severity = severity
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "check_id": self.check_id,
            "title": self.title,
            "status": self.status,
            "description": self.description,
            "remediation": self.remediation,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat()
        }


class BaseAuditor(ABC):
    """Abstract base class for OS-specific auditors."""

    def __init__(self, profile: str, level: int = 1):
        self.profile = profile
        self.level = level
        self.results: List[CheckResult] = []

    @abstractmethod
    def check_password_policy(self) -> CheckResult:
        """Check password policy compliance."""
        pass

    @abstractmethod
    def check_firewall_status(self) -> CheckResult:
        """Check firewall configuration."""
        pass

    @abstractmethod
    def check_audit_logging(self) -> CheckResult:
        """Check audit logging configuration."""
        pass

    @abstractmethod
    def check_file_permissions(self) -> CheckResult:
        """Check critical file permissions."""
        pass

    @abstractmethod
    def check_service_configuration(self) -> CheckResult:
        """Check service configurations."""
        pass

    def run_all_checks(self) -> List[CheckResult]:
        """Run all compliance checks."""
        self.results = []
        self.results.append(self.check_password_policy())
        self.results.append(self.check_firewall_status())
        self.results.append(self.check_audit_logging())
        self.results.append(self.check_file_permissions())
        self.results.append(self.check_service_configuration())
        return self.results

    def get_compliance_score(self) -> float:
        """Calculate compliance score percentage."""
        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r.status == "pass")
        return (passed / len(self.results)) * 100

    def export_results(self, filepath: str):
        """Export results to JSON file."""
        data = {
            "profile": self.profile,
            "level": self.level,
            "compliance_score": self.get_compliance_score(),
            "total_checks": len(self.results),
            "passed": sum(1 for r in self.results if r.status == "pass"),
            "failed": sum(1 for r in self.results if r.status == "fail"),
            "skipped": sum(1 for r in self.results if r.status == "skip"),
            "timestamp": datetime.now().isoformat(),
            "results": [r.to_dict() for r in self.results]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
