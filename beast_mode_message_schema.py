#!/usr/bin/env python3
"""
Beast Mode Message Schema - Structured message format for easy parsing
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    TASK_COMPLETION = "task_completion"
    TASK_START = "task_start"
    ERROR_REPORT = "error_report"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    QUESTION = "question"
    RESPONSE = "response"
    NOTIFICATION = "notification"


class TaskStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"
    WARNING = "warning"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class BeastModeMessage(BaseModel):
    """Structured Beast Mode message for easy parsing"""

    # Core message fields
    message_id: str = Field(..., description="Unique message identifier")
    sender: str = Field(..., description="Agent or system that sent the message")
    recipient: Optional[str] = Field(None, description="Target recipient (None for broadcast)")
    message_type: MessageType = Field(..., description="Type of message")
    priority: Priority = Field(default=Priority.NORMAL, description="Message priority")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")

    # Content fields
    subject: str = Field(..., description="Brief subject/title")
    content: str = Field(..., description="Main message content")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional structured details")

    # Task-specific fields (for task_completion, task_start, etc.)
    task_name: Optional[str] = Field(None, description="Name of the task")
    task_status: Optional[TaskStatus] = Field(None, description="Status of the task")
    task_duration: Optional[float] = Field(None, description="Task duration in seconds")

    # Media and evidence fields
    screen_recording: Optional[str] = Field(None, description="Path to screen recording")
    screenshots: Optional[List[str]] = Field(None, description="List of screenshot paths")
    log_files: Optional[List[str]] = Field(None, description="List of log file paths")
    error_traceback: Optional[str] = Field(None, description="Error traceback if applicable")

    # Coordination fields
    requires_response: bool = Field(default=False, description="Whether this message requires a response")
    response_deadline: Optional[datetime] = Field(None, description="Deadline for response")
    related_message_id: Optional[str] = Field(None, description="ID of related message")

    # Metadata
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    environment: Optional[str] = Field(None, description="Environment (dev, staging, prod)")
    version: str = Field(default="1.0", description="Message schema version")


def create_task_completion_message(
    task_name: str, status: TaskStatus, sender: str, details: Optional[Dict[str, Any]] = None, screen_recording: Optional[str] = None, duration: Optional[float] = None
) -> BeastModeMessage:
    """Create a structured task completion message"""

    return BeastModeMessage(
        message_id=f"task_{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        sender=sender,
        message_type=MessageType.TASK_COMPLETION,
        priority=Priority.HIGH if status == TaskStatus.FAILURE else Priority.NORMAL,
        subject=f"Task Completed: {task_name}",
        content=f"Task '{task_name}' completed with status: {status.value}",
        task_name=task_name,
        task_status=status,
        task_duration=duration,
        details=details,
        screen_recording=screen_recording,
        tags=["task", "completion", status.value],
        requires_response=status == TaskStatus.FAILURE,
    )


def create_question_message(question: str, sender: str, recipient: str, priority: Priority = Priority.NORMAL) -> BeastModeMessage:
    """Create a structured question message"""

    return BeastModeMessage(
        message_id=f"question_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        sender=sender,
        recipient=recipient,
        message_type=MessageType.QUESTION,
        priority=priority,
        subject="Question",
        content=question,
        requires_response=True,
        tags=["question", "coordination"],
    )


def create_error_report_message(error_description: str, sender: str, error_traceback: Optional[str] = None, screenshots: Optional[List[str]] = None) -> BeastModeMessage:
    """Create a structured error report message"""

    return BeastModeMessage(
        message_id=f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        sender=sender,
        message_type=MessageType.ERROR_REPORT,
        priority=Priority.CRITICAL,
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
        status=TaskStatus.SUCCESS,
        sender="DEPLOYMENT_AGENT",
        details={"deployment_id": "deploy_123", "version": "v1.2.3"},
        screen_recording="recordings/deploy_to_production_20250106_143022.mp4",
        duration=45.2,
    )

    print("Task Completion Message:")
    print(task_msg.model_dump_json(indent=2))

    # Example question message
    question_msg = create_question_message(question="How did you configure your listener to run as a daemon?", sender="BEAST_MODE_ORCHESTRATOR", recipient="TIDB")

    print("\nQuestion Message:")
    print(question_msg.model_dump_json(indent=2))
