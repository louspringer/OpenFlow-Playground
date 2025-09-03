#!/usr/bin/env python3
"""
Incident Tracking System

This script provides incident tracking capabilities for RM violations and system failures.
It integrates with GitHub Issues for systematic incident management.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add src to path for absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from model_management.model_crud import ModelOperations


class IncidentTracker:
    """Incident tracking system for RM violations and system failures."""

    def __init__(self):
        """Initialize the incident tracker."""
        self.incidents_file = Path("incidents.json")
        self.model_ops = ModelOperations()
        self.incidents = self._load_incidents()

    def _load_incidents(self) -> List[Dict[str, Any]]:
        """Load incidents from file."""
        if self.incidents_file.exists():
            try:
                with open(self.incidents_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def _save_incidents(self):
        """Save incidents to file."""
        with open(self.incidents_file, "w") as f:
            json.dump(self.incidents, f, indent=2)

    def create_incident(self, title: str, severity: str, incident_type: str, component: str, description: str, reporter: str = "system") -> str:
        """Create a new incident."""
        incident_id = f"INC-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"

        incident = {
            "id": incident_id,
            "title": title,
            "severity": severity,
            "type": incident_type,
            "component": component,
            "description": description,
            "reporter": reporter,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "assignee": None,
            "resolution": None,
            "lessons_learned": None,
        }

        self.incidents.append(incident)
        self._save_incidents()

        return incident_id

    def update_incident(self, incident_id: str, updates: Dict[str, Any]) -> bool:
        """Update an incident."""
        for incident in self.incidents:
            if incident["id"] == incident_id:
                incident.update(updates)
                incident["updated_at"] = datetime.now().isoformat()
                self._save_incidents()
                return True
        return False

    def resolve_incident(self, incident_id: str, resolution: str, lessons_learned: str = None) -> bool:
        """Resolve an incident."""
        return self.update_incident(incident_id, {"status": "resolved", "resolution": resolution, "lessons_learned": lessons_learned})

    def get_incident(self, incident_id: str) -> Optional[Dict[str, Any]]:
        """Get an incident by ID."""
        for incident in self.incidents:
            if incident["id"] == incident_id:
                return incident
        return None

    def list_incidents(self, status: str = None, severity: str = None, incident_type: str = None) -> List[Dict[str, Any]]:
        """List incidents with optional filtering."""
        filtered_incidents = self.incidents

        if status:
            filtered_incidents = [i for i in filtered_incidents if i["status"] == status]

        if severity:
            filtered_incidents = [i for i in filtered_incidents if i["severity"] == severity]

        if incident_type:
            filtered_incidents = [i for i in filtered_incidents if i["type"] == incident_type]

        return filtered_incidents

    def get_incident_metrics(self) -> Dict[str, Any]:
        """Get incident metrics."""
        total_incidents = len(self.incidents)
        open_incidents = len([i for i in self.incidents if i["status"] == "open"])
        resolved_incidents = len([i for i in self.incidents if i["status"] == "resolved"])

        # Count by severity
        severity_counts = {}
        for incident in self.incidents:
            severity = incident["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Count by type
        type_counts = {}
        for incident in self.incidents:
            incident_type = incident["type"]
            type_counts[incident_type] = type_counts.get(incident_type, 0) + 1

        return {"total_incidents": total_incidents, "open_incidents": open_incidents, "resolved_incidents": resolved_incidents, "severity_counts": severity_counts, "type_counts": type_counts}

    def generate_github_issue_template(self, incident_id: str) -> str:
        """Generate GitHub issue template for an incident."""
        incident = self.get_incident(incident_id)
        if not incident:
            return f"Incident {incident_id} not found"

        template = f"""# 🚨 **INCIDENT: {incident['title']}**

## **Incident Details**
- **ID**: {incident['id']}
- **Severity**: {incident['severity']}
- **Type**: {incident['type']}
- **Component**: {incident['component']}
- **Date**: {incident['created_at']}
- **Reporter**: {incident['reporter']}

## **Description**
{incident['description']}

## **Impact Assessment**
- **Affected Systems**: [To be filled]
- **User Impact**: [To be filled]
- **Business Impact**: [To be filled]

## **Root Cause Analysis**
- **Primary Cause**: [To be filled]
- **Contributing Factors**: [To be filled]
- **RM Violations**: [To be filled]

## **Resolution**
- **Solution Implemented**: [To be filled]
- **RM Compliance Restored**: [To be filled]
- **Testing Performed**: [To be filled]
- **Validation Results**: [To be filled]

## **Lessons Learned**
- **What Went Wrong**: [To be filled]
- **What Went Right**: [To be filled]
- **Prevention Measures**: [To be filled]
- **Knowledge Base Updates**: [To be filled]

## **Follow-up Actions**
- [ ] Update knowledge base
- [ ] Implement prevention measures
- [ ] Update monitoring systems
- [ ] Conduct post-incident review
"""
        return template


def main():
    """Main entry point for incident tracker."""
    tracker = IncidentTracker()

    if len(sys.argv) < 2:
        print("Usage: python incident_tracker.py <command> [args...]")
        print("Commands:")
        print("  create <title> <severity> <type> <component> <description>")
        print("  update <incident_id> <field> <value>")
        print("  resolve <incident_id> <resolution> [lessons_learned]")
        print("  get <incident_id>")
        print("  list [status] [severity] [type]")
        print("  metrics")
        print("  github-template <incident_id>")
        return 1

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 7:
            print("Usage: create <title> <severity> <type> <component> <description>")
            return 1

        title = sys.argv[2]
        severity = sys.argv[3]
        incident_type = sys.argv[4]
        component = sys.argv[5]
        description = sys.argv[6]

        incident_id = tracker.create_incident(title, severity, incident_type, component, description)
        print(f"Created incident: {incident_id}")

    elif command == "update":
        if len(sys.argv) < 5:
            print("Usage: update <incident_id> <field> <value>")
            return 1

        incident_id = sys.argv[2]
        field = sys.argv[3]
        value = sys.argv[4]

        success = tracker.update_incident(incident_id, {field: value})
        if success:
            print(f"Updated incident {incident_id}")
        else:
            print(f"Incident {incident_id} not found")

    elif command == "resolve":
        if len(sys.argv) < 4:
            print("Usage: resolve <incident_id> <resolution> [lessons_learned]")
            return 1

        incident_id = sys.argv[2]
        resolution = sys.argv[3]
        lessons_learned = sys.argv[4] if len(sys.argv) > 4 else None

        success = tracker.resolve_incident(incident_id, resolution, lessons_learned)
        if success:
            print(f"Resolved incident {incident_id}")
        else:
            print(f"Incident {incident_id} not found")

    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: get <incident_id>")
            return 1

        incident_id = sys.argv[2]
        incident = tracker.get_incident(incident_id)
        if incident:
            print(json.dumps(incident, indent=2))
        else:
            print(f"Incident {incident_id} not found")

    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        severity = sys.argv[3] if len(sys.argv) > 3 else None
        incident_type = sys.argv[4] if len(sys.argv) > 4 else None

        incidents = tracker.list_incidents(status, severity, incident_type)
        for incident in incidents:
            print(f"{incident['id']}: {incident['title']} ({incident['status']})")

    elif command == "metrics":
        metrics = tracker.get_incident_metrics()
        print(json.dumps(metrics, indent=2))

    elif command == "github-template":
        if len(sys.argv) < 3:
            print("Usage: github-template <incident_id>")
            return 1

        incident_id = sys.argv[2]
        template = tracker.generate_github_issue_template(incident_id)
        print(template)

    else:
        print(f"Unknown command: {command}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
