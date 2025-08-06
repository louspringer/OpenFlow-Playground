#!/usr/bin/env python3
"""
Tests for Command Execution Service
"""

import os

# Import the service functions
import sys
import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, patch

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "src", "command_execution_service"),
)

from main import (
    authenticate_request,
    execute_command_safely,
    get_command_status,
    list_user_commands,
    publish_command_result,
    submit_command,
)


class TestCommandExecutionService(unittest.TestCase):
    """Test cases for Command Execution Service"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_request = Mock()
        self.mock_request.headers = {"Authorization": "Bearer test-token"}
        self.mock_request.get_json.return_value = {
            "command": "echo 'test'",
            "cwd": "/tmp",
        }
        self.mock_request.args = {"job_id": "test-job-id"}

    def test_authenticate_request(self):
        """Test authentication function"""
        # Test with valid auth header
        user_id = authenticate_request(self.mock_request)
        self.assertEqual(user_id, "demo-user-123")

        # Test without auth header
        self.mock_request.headers = {}
        user_id = authenticate_request(self.mock_request)
        self.assertEqual(user_id, "demo-user-123")

    @patch("main.publisher")
    def test_publish_command_result(self, mock_publisher):
        """Test publishing command results"""
        mock_future = Mock()
        mock_publisher.publish.return_value = mock_future
        mock_future.result.return_value = "message-id"

        result = publish_command_result("test-job", "completed", {"data": "test"})

        mock_publisher.publish.assert_called_once()
        self.assertEqual(result, "message-id")

    @patch("subprocess.run")
    def test_execute_command_safely_success(self, mock_run):
        """Test successful command execution"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = execute_command_safely("echo 'test'", "/tmp")

        self.assertTrue(result["success"])
        self.assertEqual(result["return_code"], 0)
        self.assertEqual(result["stdout"], "test output")
        self.assertEqual(result["command"], "echo 'test'")
        self.assertEqual(result["cwd"], "/tmp")

    @patch("subprocess.run")
    def test_execute_command_safely_failure(self, mock_run):
        """Test failed command execution"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "command not found"
        mock_run.return_value = mock_result

        result = execute_command_safely("invalid-command", "/tmp")

        self.assertFalse(result["success"])
        self.assertEqual(result["return_code"], 1)
        self.assertEqual(result["stderr"], "command not found")

    @patch("subprocess.run")
    def test_execute_command_safely_timeout(self, mock_run):
        """Test command execution timeout"""
        mock_run.side_effect = Exception("timeout")

        result = execute_command_safely("sleep 10", "/tmp")

        self.assertFalse(result["success"])
        self.assertEqual(result["return_code"], -1)
        self.assertIn("error", result)

    @patch("main.db")
    @patch("main.publisher")
    def test_submit_command(self, mock_publisher, mock_db):
        """Test command submission"""
        mock_doc_ref = Mock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref

        result = submit_command(self.mock_request)

        # Check that job was stored in Firestore
        mock_db.collection.assert_called_with("command_executions")
        mock_doc_ref.set.assert_called_once()

        # Check response
        self.assertIn("job_id", result[0])
        self.assertEqual(result[0]["status"], "submitted")
        self.assertEqual(result[1], 200)

    @patch("main.db")
    def test_get_command_status(self, mock_db):
        """Test getting command status"""
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {
            "job_id": "test-job-id",
            "user_id": "demo-user-123",
            "status": "completed",
            "command": "echo 'test'",
            "created_at": datetime.now(tz=timezone.utc),
            "completed_at": datetime.now(tz=timezone.utc),
            "result": {"return_code": 0, "stdout": "test"},
        }

        mock_doc_ref = Mock()
        mock_doc_ref.get.return_value = mock_doc
        mock_db.collection.return_value.document.return_value = mock_doc_ref

        result = get_command_status(self.mock_request)

        self.assertEqual(result[0]["job_id"], "test-job-id")
        self.assertEqual(result[0]["status"], "completed")
        self.assertEqual(result[1], 200)

    @patch("main.db")
    def test_list_user_commands(self, mock_db):
        """Test listing user commands"""
        mock_docs = [
            Mock(
                to_dict=lambda: {
                    "job_id": f"job-{i}",
                    "status": "completed",
                    "command": f"echo 'test {i}'",
                    "created_at": datetime.now(tz=timezone.utc),
                    "completed_at": datetime.now(tz=timezone.utc),
                },
            )
            for i in range(3)
        ]

        mock_query = Mock()
        mock_query.stream.return_value = mock_docs
        mock_db.collection.return_value.where.return_value.order_by.return_value.limit.return_value = mock_query

        result = list_user_commands(self.mock_request)

        self.assertEqual(result[0]["count"], 3)
        self.assertEqual(len(result[0]["commands"]), 3)
        self.assertEqual(result[1], 200)


if __name__ == "__main__":
    unittest.main()
