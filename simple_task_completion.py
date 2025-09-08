#!/usr/bin/env python3
"""
Simple Task Completion System - Beast Mode integration without screen recording
"""

import redis
import json
import time
import os
from datetime import datetime
from typing import Optional, Dict, Any


class SimpleTaskCompletion:
    """Simple task completion notifications for Beast Mode"""

    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=0):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    def send_beast_message(self, message: Dict[str, Any]):
        """Send message to beast network"""
        try:
            self.redis_client.lpush("beast_mode_messages", json.dumps(message))
            print(f"📤 Sent beast message: {message.get('subject', 'No subject')}")
        except Exception as e:
            print(f"Failed to send beast message: {e}")

    def send_cinque_notification(self, message: str):
        """Send Cinque notification (placeholder)"""
        print(f"🔔 Cinque notification: {message}")

    def complete_task(self, task_name: str, status: str, sender: str, details: Optional[Dict[str, Any]] = None, duration: Optional[float] = None):
        """Complete a task and send notifications"""

        # Create simple task completion message
        message = {
            "sender": sender,
            "message_type": "task_completion",
            "timestamp": time.time(),
            "subject": f"Task Completed: {task_name}",
            "content": f"Task '{task_name}' completed with status: {status}",
            "task_name": task_name,
            "task_status": status,
            "task_duration": duration,
            "details": details,
            "tags": ["task", "completion", status],
        }

        # Send to beast network
        self.send_beast_message(message)

        # Send Cinque notification
        cinque_msg = f"Task {task_name} completed: {status}"
        self.send_cinque_notification(cinque_msg)

        return message

    def execute_task(self, task_name: str, task_function, sender: str, *args, **kwargs):
        """Execute a task with automatic completion notification"""

        print(f"🚀 Starting task: {task_name}")

        start_time = time.time()
        status = "success"
        error_details = None

        try:
            # Execute the task
            result = task_function(*args, **kwargs)
            print(f"✅ Task completed successfully: {task_name}")

        except Exception as e:
            status = "failure"
            error_details = {"error": str(e), "error_type": type(e).__name__}
            print(f"❌ Task failed: {task_name} - {e}")
            result = None

        finally:
            # Calculate duration
            duration = time.time() - start_time

            # Complete the task
            message = self.complete_task(task_name=task_name, status=status, sender=sender, details=error_details, duration=duration)

            return result, message


# Example usage
def example_task():
    """Example task function"""
    print("Doing some work...")
    time.sleep(2)
    print("Work completed!")
    return "success"


def example_failing_task():
    """Example failing task"""
    print("Doing some work...")
    time.sleep(1)
    raise Exception("Something went wrong!")


if __name__ == "__main__":
    # Initialize the system
    task_system = SimpleTaskCompletion()

    # Example: Execute a successful task
    print("=== Testing Successful Task ===")
    result, message = task_system.execute_task(task_name="example_success_task", task_function=example_task, sender="TEST_AGENT")

    print(f"Result: {result}")
    print(f"Message sent to beast network")

    # Example: Execute a failing task
    print("\n=== Testing Failing Task ===")
    try:
        result, message = task_system.execute_task(task_name="example_failing_task", task_function=example_failing_task, sender="TEST_AGENT")
    except:
        pass  # Expected to fail

    print(f"Message sent to beast network")
