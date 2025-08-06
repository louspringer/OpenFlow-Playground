#!/usr/bin/env python3
"""
Command Execution Service Client
Python client for fire-and-forget command execution
"""

import time
from typing import Any, Optional

import requests


class CommandExecutionClient:
    """Client for the Command Execution Service"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the client

        Args:
            base_url: Base URL of the service (e.g., https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def submit_command(self, command: str, cwd: Optional[str] = None) -> dict[str, Any]:
        """
        Submit a command for execution

        Args:
            command: Command to execute
            cwd: Working directory (optional)

        Returns:
            Dict with job_id and status
        """
        url = f"{self.base_url}/submit-command"
        data = {"command": command, "cwd": cwd}

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_status(self, job_id: str) -> dict[str, Any]:
        """
        Get the status of a command execution

        Args:
            job_id: Job ID returned from submit_command

        Returns:
            Dict with job status and results
        """
        url = f"{self.base_url}/get-command-status"
        params = {"job_id": job_id}

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def list_commands(self) -> dict[str, Any]:
        """
        List user's command executions

        Returns:
            Dict with list of commands
        """
        url = f"{self.base_url}/list-user-commands"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(
        self,
        job_id: str,
        timeout: int = 300,
        poll_interval: int = 5,
    ) -> dict[str, Any]:
        """
        Wait for command completion

        Args:
            job_id: Job ID to wait for
            timeout: Maximum time to wait in seconds
            poll_interval: How often to check status in seconds

        Returns:
            Final job status and results
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_status(job_id)

            if status.get("status") in ["completed", "failed"]:
                return status

            time.sleep(poll_interval)

        raise TimeoutError(f"Command execution timed out after {timeout} seconds")

    def execute_and_wait(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 300,
    ) -> dict[str, Any]:
        """
        Submit command and wait for completion

        Args:
            command: Command to execute
            cwd: Working directory (optional)
            timeout: Maximum time to wait in seconds

        Returns:
            Final job status and results
        """
        # Submit the command
        result = self.submit_command(command, cwd)
        job_id = result["job_id"]

        print(f"🚀 Submitted command: {command}")
        print(f"📋 Job ID: {job_id}")

        # Wait for completion
        return self.wait_for_completion(job_id, timeout)


def main():
    """Example usage of the Command Execution Client"""

    # Initialize client
    client = CommandExecutionClient(
        base_url="https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net",
    )

    # Example 1: Fire and forget
    print("🔥 Fire and forget example:")
    result = client.submit_command("ls -la", "/tmp")
    print(f"Job ID: {result['job_id']}")
    print(f"Status: {result['status']}")

    # Example 2: Wait for completion
    print("\n⏳ Wait for completion example:")
    try:
        final_result = client.execute_and_wait("echo 'Hello from cloud!'", timeout=60)
        print(f"Final Status: {final_result['status']}")
        if final_result.get("result"):
            print(f"Return Code: {final_result['result']['return_code']}")
            print(f"STDOUT: {final_result['result']['stdout']}")
            if final_result["result"]["stderr"]:
                print(f"STDERR: {final_result['result']['stderr']}")
    except TimeoutError as e:
        print(f"❌ {e}")

    # Example 3: List user commands
    print("\n📋 List user commands:")
    commands = client.list_commands()
    print(f"Found {commands['count']} commands")
    for cmd in commands["commands"][:5]:  # Show first 5
        print(f"  {cmd['job_id']}: {cmd['command']} ({cmd['status']})")


if __name__ == "__main__":
    main()
