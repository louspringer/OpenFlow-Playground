#!/usr/bin/env python3
"""
Beast Mode Message Schema - Simple structured message format for easy parsing
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class BeastModeMessage:
    """Structured Beast Mode message for easy parsing"""

    # Core message fields
    message_id: str
    sender: str
    recipient: Optional[str] = None
    message_type: str = "notification"  # task_completion, question, error_report, etc.
    priority: str = "normal"  # low, normal, high, critical
    timestamp: str = ""

    # Content fields
    subject: str = ""
    content: str = ""
    details: Optional[Dict[str, Any]] = None

    # Task-specific fields
    task_name: Optional[str] = None
    task_status: Optional[str] = None  # success, failure, in_progress, cancelled
    task_duration: Optional[float] = None

    # Media and evidence fields
    screen_recording: Optional[str] = None
    screenshots: Optional[List[str]] = None
    log_files: Optional[List[str]] = None
    error_traceback: Optional[str] = None

    # Coordination fields
    requires_response: bool = False
    response_deadline: Optional[str] = None
    related_message_id: Optional[str] = None

    # Metadata
    tags: Optional[List[str]] = None
    environment: Optional[str] = None
    version: str = "1.0"

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "BeastModeMessage":
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls(**data)


def create_task_completion_message(
    task_name: str, status: str, sender: str, details: Optional[Dict[str, Any]] = None, screen_recording: Optional[str] = None, duration: Optional[float] = None
) -> BeastModeMessage:
    """Create a structured task completion message"""

    message_id = f"task_{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    priority = "critical" if status == "failure" else "high"

    return BeastModeMessage(
        message_id=message_id,
        sender=sender,
        message_type="task_completion",
        priority=priority,
        subject=f"Task Completed: {task_name}",
        content=f"Task '{task_name}' completed with status: {status}",
        task_name=task_name,
        task_status=status,
        task_duration=duration,
        details=details,
        screen_recording=screen_recording,
        tags=["task", "completion", status],
        requires_response=status == "failure",
    )


def create_question_message(question: str, sender: str, recipient: str, priority: str = "normal") -> BeastModeMessage:
    """Create a structured question message"""

    message_id = f"question_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return BeastModeMessage(
        message_id=message_id,
        sender=sender,
        recipient=recipient,
        message_type="question",
        priority=priority,
        subject="Question",
        content=question,
        requires_response=True,
        tags=["question", "coordination"],
    )


def create_error_report_message(error_description: str, sender: str, error_traceback: Optional[str] = None, screenshots: Optional[List[str]] = None) -> BeastModeMessage:
    """Create a structured error report message"""

    message_id = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return BeastModeMessage(
        message_id=message_id,
        sender=sender,
        message_type="error_report",
        priority="critical",
        subject="Error Report",
        content=error_description,
        error_traceback=error_traceback,
        screenshots=screenshots,
        tags=["error", "report", "critical"],
        requires_response=True,
    )


# Example usage and testing
if __name__ == "__main__":
    # Example task completion message
    task_msg = create_task_completion_message(
        task_name="deploy_to_production",
        status="success",
        sender="DEPLOYMENT_AGENT",
        details={"deployment_id": "deploy_123", "version": "v1.2.3"},
        screen_recording="recordings/deploy_to_production_20250106_143022.mp4",
        duration=45.2,
    )

    print("Task Completion Message:")
    print(task_msg.to_json())

    # Example question message
    question_msg = create_question_message(question="How did you configure your listener to run as a daemon?", sender="BEAST_MODE_ORCHESTRATOR", recipient="TIDB")

    print("\nQuestion Message:")
    print(question_msg.to_json())
