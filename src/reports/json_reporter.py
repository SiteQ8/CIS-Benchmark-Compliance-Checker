"""
JSON report generator for CIS compliance audits.
"""

import json
from typing import Dict


class JSONReporter:
    """Generate JSON compliance reports."""

    def generate(self, audit_data: Dict, output_path: str) -> str:
        """Generate JSON report from audit results."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(audit_data, f, indent=2, ensure_ascii=False)
        return output_path
