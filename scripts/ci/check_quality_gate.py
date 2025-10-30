#!/usr/bin/env python3
"""
Check quality gate decision - exit with error if quality fails.

Used in CI when FAIL_ON_QUALITY=true.
"""

import json
import sys


def check_quality_gate(report_path: str) -> int:
    """Check quality gate and exit with status code."""
    try:
        with open(report_path) as f:
            report = json.load(f)
        
        if not report.get('can_proceed', False):
            print(f"❌ Quality gates failed!")
            print(f"Overall score: {report.get('overall_score', 'N/A')}")
            print(f"Threshold: {report.get('quality_threshold', 'N/A')}")
            return 1
        else:
            print(f"✅ Quality gates passed!")
            print(f"Overall score: {report.get('overall_score', 'N/A')}")
            return 0
            
    except Exception as e:
        print(f"Error reading quality report: {e}")
        return 1


if __name__ == "__main__":
    report_path = sys.argv[1] if len(sys.argv) > 1 else "quality-report.json"
    sys.exit(check_quality_gate(report_path))

