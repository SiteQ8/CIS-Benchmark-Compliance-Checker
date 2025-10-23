"""
Unit tests for auditor classes.
"""

import pytest
from src.auditors.base_auditor import BaseAuditor, CheckResult
from src.auditors.ubuntu_auditor import UbuntuAuditor


def test_check_result_creation():
    """Test CheckResult object creation."""
    result = CheckResult(
        check_id="1.1.1",
        title="Test check",
        status="pass",
        description="Test description",
        severity="high"
    )

    assert result.check_id == "1.1.1"
    assert result.title == "Test check"
    assert result.status == "pass"
    assert result.severity == "high"


def test_check_result_to_dict():
    """Test CheckResult to dictionary conversion."""
    result = CheckResult(
        check_id="1.1.1",
        title="Test check",
        status="pass"
    )

    result_dict = result.to_dict()
    assert isinstance(result_dict, dict)
    assert "check_id" in result_dict
    assert "timestamp" in result_dict


def test_ubuntu_auditor_creation():
    """Test UbuntuAuditor instantiation."""
    auditor = UbuntuAuditor("ubuntu_22_04", level=1)
    assert auditor.profile == "ubuntu_22_04"
    assert auditor.level == 1


def test_compliance_score_calculation():
    """Test compliance score calculation."""
    auditor = UbuntuAuditor("ubuntu_22_04")
    auditor.results = [
        CheckResult("1.1.1", "Test 1", "pass"),
        CheckResult("1.1.2", "Test 2", "pass"),
        CheckResult("1.1.3", "Test 3", "fail"),
        CheckResult("1.1.4", "Test 4", "fail"),
    ]

    score = auditor.get_compliance_score()
    assert score == 50.0  # 2 passed out of 4


if __name__ == "__main__":
    pytest.main([__file__])
