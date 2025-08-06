#!/usr/bin/env python3
"""
Command Execution Service - GCP Cloud Functions
Fire-and-forget command execution with Pub/Sub queues
"""

import json
import logging
import subprocess
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import functions_framework
from google.cloud import firestore, pubsub_v1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firestore client
db = firestore.Client()

# Initialize Pub/Sub clients
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Topic paths
COMMAND_INPUT_TOPIC = "command-execution-input"
COMMAND_OUTPUT_TOPIC = "command-execution-output"

# Get project ID from environment or default
PROJECT_ID = "aardvark-linkedin-grepper"  # Your existing project

input_topic_path = publisher.topic_path(PROJECT_ID, COMMAND_INPUT_TOPIC)
output_topic_path = publisher.topic_path(PROJECT_ID, COMMAND_OUTPUT_TOPIC)


def authenticate_request(request) -> str:
    """Simple authentication for demo purposes"""
    try:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return "demo-user-123"
        return "demo-user-123"
    except Exception as e:
        logger.warning("Authentication failed, using demo user: %s", str(e))
        return "demo-user-123"


def publish_command_result(job_id: str, status: str, data: dict):
    """Publish command result to output queue"""
    try:
        message = {
            "job_id": job_id,
            "status": status,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "data": data,
        }

        future = publisher.publish(
            output_topic_path,
            json.dumps(message).encode("utf-8"),
            job_id=str(job_id) if job_id else "unknown",
            status=str(status),
        )

        logger.info("Published result for job %s: %s", job_id, status)
        return future.result()
    except Exception as e:
        logger.error("Failed to publish result: %s", str(e))


def execute_command_safely(command: str, cwd: Optional[str] = None) -> dict[str, Any]:
    """Execute command safely and return results"""
    try:
        logger.info("Executing command: %s", command)

        # Execute command with timeout
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=cwd,
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
            "command": command,
            "cwd": cwd,
        }
    except subprocess.TimeoutExpired:
        return {
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 5 minutes",
            "success": False,
            "command": command,
            "cwd": cwd,
            "error": "timeout",
        }
    except Exception as e:
        return {
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False,
            "command": command,
            "cwd": cwd,
            "error": "execution_error",
        }


@functions_framework.cloud_event
def command_executor(cloud_event):
    """Cloud Function triggered by Pub/Sub to execute commands"""
    job_id = None
    try:
        # Parse the command from the Pub/Sub message
        logger.info("Cloud event data type: %s", type(cloud_event.data))
        logger.info("Cloud event data: %s", cloud_event.data)

        # Handle Pub/Sub message format
        if isinstance(cloud_event.data, dict) and "message" in cloud_event.data:
            # Extract job_id from attributes
            job_id = cloud_event.data["message"]["attributes"].get("job_id")

            # Decode base64 data
            import base64

            encoded_data = cloud_event.data["message"]["data"]
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            data = json.loads(decoded_data)

            command = data.get("command")
            cwd = data.get("cwd")
            user_id = data.get("user_id", "unknown")
        else:
            # Fallback for other formats
            if hasattr(cloud_event.data, "decode"):
                data = json.loads(cloud_event.data.decode("utf-8"))
            else:
                data = cloud_event.data

            job_id = data.get("job_id")
            command = data.get("command")
            cwd = data.get("cwd")
            user_id = data.get("user_id", "unknown")

        logger.info("Parsed data: %s", data)
        logger.info("Job ID: %s, Command: %s", job_id, command)

        logger.info("Received command execution request: %s", job_id)

        # Publish "executing" status
        publish_command_result(
            job_id,
            "executing",
            {"message": "Command execution started"},
        )

        # Execute the command
        result = execute_command_safely(command, cwd)

        # Store result in Firestore
        doc_ref = db.collection("command_executions").document(job_id)
        doc_ref.set(
            {
                "job_id": job_id,
                "user_id": user_id,
                "command": command,
                "cwd": cwd,
                "result": result,
                "created_at": datetime.now(tz=timezone.utc),
                "completed_at": datetime.now(tz=timezone.utc),
                "status": "completed",
            },
        )

        # Publish completion status
        publish_command_result(job_id, "completed", result)

        logger.info("Command execution completed: %s", job_id)

    except Exception as e:
        logger.error("Command execution failed: %s", str(e))
        if job_id:
            publish_command_result(job_id, "failed", {"error": str(e)})


@functions_framework.http
def submit_command(request):
    """HTTP endpoint to submit a command for execution"""
    try:
        # Authenticate request
        user_id = authenticate_request(request)

        # Parse request
        request_json = request.get_json()
        if not request_json:
            return {"error": "No JSON data provided"}, 400

        command = request_json.get("command")
        cwd = request_json.get("cwd")

        if not command:
            return {"error": "No command provided"}, 400

        # Generate job ID
        job_id = str(uuid.uuid4())

        # Store job in Firestore
        doc_ref = db.collection("command_executions").document(job_id)
        doc_ref.set(
            {
                "job_id": job_id,
                "user_id": user_id,
                "command": command,
                "cwd": cwd,
                "status": "pending",
                "created_at": datetime.now(tz=timezone.utc),
            },
        )

        # Publish command to input queue
        message = {"job_id": job_id, "command": command, "cwd": cwd, "user_id": user_id}

        publisher.publish(
            input_topic_path,
            json.dumps(message).encode("utf-8"),
            job_id=job_id,
        )

        logger.info("Submitted command for execution: %s", job_id)

        return {
            "job_id": job_id,
            "status": "submitted",
            "message": "Command submitted for execution",
        }

    except Exception as e:
        logger.error("Failed to submit command: %s", str(e))
        return {"error": str(e)}, 500


@functions_framework.http
def get_command_status(request):
    """HTTP endpoint to get command execution status"""
    try:
        # Authenticate request
        user_id = authenticate_request(request)

        # Get job ID from query parameters
        job_id = request.args.get("job_id")
        if not job_id:
            return {"error": "No job_id provided"}, 400

        # Get job from Firestore
        doc_ref = db.collection("command_executions").document(job_id)
        doc = doc_ref.get()

        if not doc.exists:
            return {"error": "Job not found"}, 404

        job_data = doc.to_dict()

        # Check if user has access to this job
        if job_data.get("user_id") != user_id:
            return {"error": "Access denied"}, 403

        return {
            "job_id": job_id,
            "status": job_data.get("status"),
            "command": job_data.get("command"),
            "created_at": job_data.get("created_at").isoformat()
            if job_data.get("created_at")
            else None,
            "completed_at": job_data.get("completed_at").isoformat()
            if job_data.get("completed_at")
            else None,
            "result": job_data.get("result"),
        }

    except Exception as e:
        logger.error("Failed to get command status: %s", str(e))
        return {"error": str(e)}, 500


@functions_framework.http
def list_user_commands(request):
    """HTTP endpoint to list user's command executions"""
    try:
        # Authenticate request
        user_id = authenticate_request(request)

        # Get user's commands from Firestore
        docs = (
            db.collection("command_executions")
            .where("user_id", "==", user_id)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(50)
            .stream()
        )

        commands = []
        for doc in docs:
            data = doc.to_dict()
            commands.append(
                {
                    "job_id": data.get("job_id"),
                    "status": data.get("status"),
                    "command": data.get("command"),
                    "created_at": data.get("created_at").isoformat()
                    if data.get("created_at")
                    else None,
                    "completed_at": data.get("completed_at").isoformat()
                    if data.get("completed_at")
                    else None,
                },
            )

        return {"commands": commands, "count": len(commands)}

    except Exception as e:
        logger.error("Failed to list commands: %s", str(e))
        return {"error": str(e)}, 500
