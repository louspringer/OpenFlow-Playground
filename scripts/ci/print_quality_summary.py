#!/usr/bin/env python3
"""
Print quality gate summary for GitHub Actions step summary.

Reads quality report JSON and outputs formatted markdown to stdout.
"""

import json
import sys
from pathlib import Path


def print_quality_summary(report_path: str) -> int:
    """Print quality summary from report file."""
    try:
        with open(report_path) as f:
            report = json.load(f)
        
        print(f"**Overall Score**: {report.get('overall_score', 'N/A')}")
        print(f"**Quality Status**: {report.get('quality_status', 'N/A')}")
        print(f"**Can Proceed**: {report.get('can_proceed', 'N/A')}")
        
        if 'gate_summary' in report:
            gates = report['gate_summary']
            print(f"**Total Gates**: {gates.get('total_gates', 0)}")
            print(f"**Failed Gates**: {gates.get('failed_gates', 0)}")
        
        return 0
        
    except Exception as e:
        print(f"**Error**: Could not read quality report: {e}")
        return 1


if __name__ == "__main__":
    report_path = sys.argv[1] if len(sys.argv) > 1 else "quality-report.json"
    sys.exit(print_quality_summary(report_path))

