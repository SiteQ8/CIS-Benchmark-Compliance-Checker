"""
CSV report generator for CIS compliance audits.
"""

import csv
from typing import Dict


class CSVReporter:
    """Generate CSV compliance reports."""

    def generate(self, audit_data: Dict, output_path: str) -> str:
        """Generate CSV report from audit results."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Check ID', 'Title', 'Status', 'Severity', 'Description', 'Remediation'])

            for result in audit_data.get('results', []):
                writer.writerow([
                    result.get('check_id', ''),
                    result.get('title', ''),
                    result.get('status', ''),
                    result.get('severity', ''),
                    result.get('description', ''),
                    result.get('remediation', '')
                ])

        return output_path
