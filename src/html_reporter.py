"""
HTML report generator for CIS compliance audits.
"""

from typing import List, Dict
from datetime import datetime
from jinja2 import Template
import os


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIS Compliance Report - {{ profile }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 16px; }
        .score-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .score-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-box {
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-box h3 { font-size: 36px; margin-bottom: 5px; }
        .stat-box p { color: #666; font-size: 14px; }
        .stat-pass { background: #d4edda; color: #155724; }
        .stat-fail { background: #f8d7da; color: #721c24; }
        .stat-skip { background: #fff3cd; color: #856404; }
        .stat-total { background: #d1ecf1; color: #0c5460; }
        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: conic-gradient(
                #28a745 0deg {{ score_degrees }}deg,
                #e9ecef {{ score_degrees }}deg 360deg
            );
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
        }
        .score-inner {
            width: 120px;
            height: 120px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        .score-value { font-size: 36px; font-weight: bold; color: #333; }
        .score-label { font-size: 12px; color: #666; }
        .check-item {
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .check-pass { border-color: #28a745; }
        .check-fail { border-color: #dc3545; }
        .check-skip { border-color: #ffc107; }
        .check-error { border-color: #6c757d; }
        .check-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .check-id { 
            font-weight: bold; 
            color: #667eea;
            font-size: 14px;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .badge-pass { background: #d4edda; color: #155724; }
        .badge-fail { background: #f8d7da; color: #721c24; }
        .badge-skip { background: #fff3cd; color: #856404; }
        .badge-error { background: #e2e3e5; color: #383d41; }
        .severity-badge {
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 10px;
            margin-left: 10px;
        }
        .severity-critical { background: #dc3545; color: white; }
        .severity-high { background: #fd7e14; color: white; }
        .severity-medium { background: #ffc107; color: #000; }
        .severity-low { background: #17a2b8; color: white; }
        .remediation {
            margin-top: 10px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 3px solid #007bff;
        }
        .remediation strong { color: #007bff; }
        .remediation code {
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
        .section-title {
            font-size: 24px;
            margin: 40px 0 20px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ CIS Compliance Report</h1>
            <p><strong>Profile:</strong> {{ profile }} | <strong>Level:</strong> {{ level }}</p>
            <p><strong>Generated:</strong> {{ timestamp }}</p>
        </div>

        <div class="score-card">
            <h2 style="text-align: center; margin-bottom: 10px;">Compliance Score</h2>
            <div class="score-circle">
                <div class="score-inner">
                    <div class="score-value">{{ compliance_score }}%</div>
                    <div class="score-label">COMPLIANCE</div>
                </div>
            </div>

            <div class="score-grid">
                <div class="stat-box stat-total">
                    <h3>{{ total_checks }}</h3>
                    <p>Total Checks</p>
                </div>
                <div class="stat-box stat-pass">
                    <h3>{{ passed_checks }}</h3>
                    <p>Passed</p>
                </div>
                <div class="stat-box stat-fail">
                    <h3>{{ failed_checks }}</h3>
                    <p>Failed</p>
                </div>
                <div class="stat-box stat-skip">
                    <h3>{{ skipped_checks }}</h3>
                    <p>Skipped</p>
                </div>
            </div>
        </div>

        <h2 class="section-title">📋 Detailed Check Results</h2>
        {% for check in results %}
        <div class="check-item check-{{ check.status }}">
            <div class="check-header">
                <div>
                    <span class="check-id">{{ check.check_id }}</span>
                    <span class="severity-badge severity-{{ check.severity }}">{{ check.severity }}</span>
                </div>
                <span class="status-badge badge-{{ check.status }}">{{ check.status }}</span>
            </div>
            <h3 style="margin-bottom: 10px; color: #333;">{{ check.title }}</h3>
            {% if check.description %}
            <p style="color: #666; font-size: 14px;">{{ check.description }}</p>
            {% endif %}
            {% if check.status == 'fail' and check.remediation %}
            <div class="remediation">
                <strong>🔧 Remediation:</strong><br>
                <code>{{ check.remediation }}</code>
            </div>
            {% endif %}
        </div>
        {% endfor %}

        <div class="footer">
            <p>Generated by CIS Benchmark Compliance Checker</p>
            <p>For more information, visit <a href="https://github.com/SiteQ8/CIS-Benchmark-Compliance-Checker">GitHub Repository</a></p>
        </div>
    </div>
</body>
</html>
"""


class HTMLReporter:
    """Generate HTML compliance reports."""

    def __init__(self):
        self.template = Template(HTML_TEMPLATE)

    def generate(self, audit_data: Dict, output_path: str) -> str:
        """Generate HTML report from audit results."""
        compliance_score = int(audit_data.get("compliance_score", 0))

        html_content = self.template.render(
            profile=audit_data.get("profile", "Unknown"),
            level=audit_data.get("level", 1),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            compliance_score=compliance_score,
            score_degrees=int(compliance_score * 3.6),  # Convert to degrees
            total_checks=audit_data.get("total_checks", 0),
            passed_checks=audit_data.get("passed", 0),
            failed_checks=audit_data.get("failed", 0),
            skipped_checks=audit_data.get("skipped", 0),
            results=audit_data.get("results", [])
        )

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path
