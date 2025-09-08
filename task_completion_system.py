#!/usr/bin/env python3
"""
Task Completion System - Beast Mode integration with screen recording
"""

import redis
import json
import time
import subprocess
import os
from datetime import datetime
from typing import Optional, Dict, Any, List


class TaskCompletionSystem:
    """Handles task completion notifications with screen recording"""

    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=0):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.recordings_dir = "recordings"
        self.ensure_recordings_dir()

    def ensure_recordings_dir(self):
        """Create recordings directory if it doesn't exist"""
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)

    def start_screen_recording(self, task_name: str) -> str:
        """Start screen recording for a task"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        recording_path = f"{self.recordings_dir}/task_{task_name}_{timestamp}.mp4"

        # Start recording in background (macOS using ffmpeg)
        cmd = ["ffmpeg", "-f", "avfoundation", "-i", "1:0", "-t", "300", "-y", recording_path]  # Screen:Audio  # 5 minute max  # Overwrite

        try:
            # Start recording process
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return recording_path, process
        except Exception as e:
            print(f"Failed to start screen recording: {e}")
            return None, None

    def stop_screen_recording(self, process):
        """Stop screen recording process"""
        if process:
            process.terminate()
            process.wait()

    def send_beast_message(self, message: Dict[str, Any]):
        """Send message to beast network"""
        try:
            self.redis_client.lpush("beast_mode_messages", json.dumps(message))
            print(f"📤 Sent beast message: {message.get('subject', 'No subject')}")
        except Exception as e:
            print(f"Failed to send beast message: {e}")

    def send_cinque_notification(self, message: str):
        """Send Cinque notification (placeholder for now)"""
        # TODO: Implement actual Cinque integration
        print(f"🔔 Cinque notification: {message}")

    def complete_task(self, task_name: str, status: str, sender: str, details: Optional[Dict[str, Any]] = None, recording_path: Optional[str] = None, duration: Optional[float] = None):
        """Complete a task and send notifications"""

        # Create task completion message
        message = {
            "message_id": f"task_{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "sender": sender,
            "message_type": "task_completion",
            "priority": "critical" if status == "failure" else "high",
            "timestamp": time.time(),
            "subject": f"Task Completed: {task_name}",
            "content": f"Task '{task_name}' completed with status: {status}",
            "task_name": task_name,
            "task_status": status,
            "task_duration": duration,
            "details": details,
            "screen_recording": recording_path,
            "tags": ["task", "completion", status],
            "requires_response": status == "failure",
        }

        # Send to beast network
        self.send_beast_message(message)

        # Send Cinque notification
        cinque_msg = f"Task {task_name} completed: {status}"
        if recording_path:
            cinque_msg += f" (Recording: {recording_path})"
        self.send_cinque_notification(cinque_msg)

        return message

    def execute_task_with_recording(self, task_name: str, task_function, sender: str, *args, **kwargs):
        """Execute a task with automatic screen recording"""

        print(f"🎬 Starting task: {task_name}")

        # Start screen recording
        recording_path, recording_process = self.start_screen_recording(task_name)

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
            # Stop recording
            self.stop_screen_recording(recording_process)

            # Calculate duration
            duration = time.time() - start_time

            # Complete the task
            message = self.complete_task(task_name=task_name, status=status, sender=sender, details=error_details, recording_path=recording_path, duration=duration)

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
    task_system = TaskCompletionSystem()

    # Example: Execute a successful task
    print("=== Testing Successful Task ===")
    result, message = task_system.execute_task_with_recording(task_name="example_success_task", task_function=example_task, sender="TEST_AGENT")

    print(f"Result: {result}")
    print(f"Message: {message}")

    # Example: Execute a failing task
    print("\n=== Testing Failing Task ===")
    try:
        result, message = task_system.execute_task_with_recording(task_name="example_failing_task", task_function=example_failing_task, sender="TEST_AGENT")
    except:
        pass  # Expected to fail

    print(f"Message: {message}")
