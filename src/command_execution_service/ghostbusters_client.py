#!/usr/bin/env python3
"""
Ghostbusters Client for Command Execution Service
Queue Ghostbusters analysis through the fire-and-forget system
"""

from typing import Any, Optional

from .client import CommandExecutionClient
from .ghostbusters_integration import create_ghostbusters_command


class GhostbustersClient:
    """Client for queuing Ghostbusters analysis through command execution service"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the Ghostbusters client

        Args:
            base_url: Base URL of the command execution service
            api_key: Optional API key for authentication
        """
        self.command_client = CommandExecutionClient(base_url, api_key)

    def queue_analysis(self, project_path: str = ".") -> dict[str, Any]:
        """
        Queue a full Ghostbusters analysis

        Args:
            project_path: Path to project to analyze

        Returns:
            Dict with job_id and status
        """
        command = create_ghostbusters_command("analysis", project_path=project_path)
        return self.command_client.submit_command(command, cwd=project_path)

    def queue_agent(self, agent_name: str, project_path: str = ".") -> dict[str, Any]:
        """
        Queue a specific Ghostbusters agent

        Args:
            agent_name: Name of agent (security, code_quality, test, build, architecture, model)
            project_path: Path to project to analyze

        Returns:
            Dict with job_id and status
        """
        command = create_ghostbusters_command(
            "agent",
            agent_name=agent_name,
            project_path=project_path,
        )
        return self.command_client.submit_command(command, cwd=project_path)

    def queue_recovery(
        self,
        recovery_type: str,
        target_files: list[str],
        project_path: str = ".",
    ) -> dict[str, Any]:
        """
        Queue a Ghostbusters recovery operation

        Args:
            recovery_type: Type of recovery (syntax, indentation, imports, types)
            target_files: List of files to fix
            project_path: Path to project

        Returns:
            Dict with job_id and status
        """
        command = create_ghostbusters_command(
            "recovery",
            recovery_type=recovery_type,
            target_files=target_files,
            project_path=project_path,
        )
        return self.command_client.submit_command(command, cwd=project_path)

    def wait_for_analysis(self, job_id: str, timeout: int = 600) -> dict[str, Any]:
        """
        Wait for Ghostbusters analysis completion

        Args:
            job_id: Job ID from queue_analysis
            timeout: Maximum time to wait in seconds

        Returns:
            Final analysis results
        """
        return self.command_client.wait_for_completion(job_id, timeout)

    def wait_for_agent(self, job_id: str, timeout: int = 300) -> dict[str, Any]:
        """
        Wait for Ghostbusters agent completion

        Args:
            job_id: Job ID from queue_agent
            timeout: Maximum time to wait in seconds

        Returns:
            Final agent results
        """
        return self.command_client.wait_for_completion(job_id, timeout)

    def wait_for_recovery(self, job_id: str, timeout: int = 300) -> dict[str, Any]:
        """
        Wait for Ghostbusters recovery completion

        Args:
            job_id: Job ID from queue_recovery
            timeout: Maximum time to wait in seconds

        Returns:
            Final recovery results
        """
        return self.command_client.wait_for_completion(job_id, timeout)

    def run_full_analysis(
        self,
        project_path: str = ".",
        timeout: int = 600,
    ) -> dict[str, Any]:
        """
        Run full Ghostbusters analysis and wait for completion

        Args:
            project_path: Path to project to analyze
            timeout: Maximum time to wait in seconds

        Returns:
            Complete analysis results
        """
        print(f"🔍 Queuing Ghostbusters analysis for: {project_path}")
        result = self.queue_analysis(project_path)
        job_id = result["job_id"]
        print(f"📋 Job ID: {job_id}")

        print("⏳ Waiting for analysis completion...")
        return self.wait_for_analysis(job_id, timeout)

    def run_agent_analysis(
        self,
        agent_name: str,
        project_path: str = ".",
        timeout: int = 300,
    ) -> dict[str, Any]:
        """
        Run specific Ghostbusters agent and wait for completion

        Args:
            agent_name: Name of agent to run
            project_path: Path to project to analyze
            timeout: Maximum time to wait in seconds

        Returns:
            Agent analysis results
        """
        print(f"🔍 Queuing Ghostbusters {agent_name} agent for: {project_path}")
        result = self.queue_agent(agent_name, project_path)
        job_id = result["job_id"]
        print(f"📋 Job ID: {job_id}")

        print(f"⏳ Waiting for {agent_name} agent completion...")
        return self.wait_for_agent(job_id, timeout)

    def run_recovery_operation(
        self,
        recovery_type: str,
        target_files: list[str],
        project_path: str = ".",
        timeout: int = 300,
    ) -> dict[str, Any]:
        """
        Run Ghostbusters recovery and wait for completion

        Args:
            recovery_type: Type of recovery to run
            target_files: List of files to fix
            project_path: Path to project
            timeout: Maximum time to wait in seconds

        Returns:
            Recovery operation results
        """
        print(f"🔧 Queuing Ghostbusters {recovery_type} recovery for: {target_files}")
        result = self.queue_recovery(recovery_type, target_files, project_path)
        job_id = result["job_id"]
        print(f"📋 Job ID: {job_id}")

        print(f"⏳ Waiting for {recovery_type} recovery completion...")
        return self.wait_for_recovery(job_id, timeout)

    def get_status(self, job_id: str) -> dict[str, Any]:
        """
        Get status of a Ghostbusters job

        Args:
            job_id: Job ID to check

        Returns:
            Job status and results
        """
        return self.command_client.get_status(job_id)

    def list_jobs(self) -> dict[str, Any]:
        """
        List all Ghostbusters jobs

        Returns:
            List of jobs
        """
        return self.command_client.list_commands()


def main():
    """Example usage of the Ghostbusters Client"""

    # Initialize client
    client = GhostbustersClient(
        base_url="https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net",
    )

    print("🎯 Ghostbusters Command Execution Client")
    print("=" * 50)

    # Example 1: Queue full analysis
    print("\n🔥 Fire and forget - Full analysis:")
    result = client.queue_analysis(".")
    print(f"Job ID: {result['job_id']}")
    print(f"Status: {result['status']}")

    # Example 2: Queue specific agent
    print("\n🔥 Fire and forget - Security agent:")
    result = client.queue_agent("security", ".")
    print(f"Job ID: {result['job_id']}")
    print(f"Status: {result['status']}")

    # Example 3: Wait for completion
    print("\n⏳ Wait for completion - Full analysis:")
    try:
        final_result = client.run_full_analysis(".", timeout=300)
        print(f"Final Status: {final_result['status']}")
        if final_result.get("result"):
            print(f"Success: {final_result['result']['success']}")
            print(f"Return Code: {final_result['result']['return_code']}")
            if final_result["result"]["stdout"]:
                print(f"STDOUT: {final_result['result']['stdout'][:200]}...")
            if final_result["result"]["stderr"]:
                print(f"STDERR: {final_result['result']['stderr']}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 4: Run specific agent
    print("\n🔍 Run security agent:")
    try:
        agent_result = client.run_agent_analysis("security", ".", timeout=120)
        print(f"Agent Status: {agent_result['status']}")
        if agent_result.get("result"):
            print(f"Success: {agent_result['result']['success']}")
            if agent_result["result"]["stdout"]:
                print(f"Agent Output: {agent_result['result']['stdout']}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 5: List jobs
    print("\n📋 List Ghostbusters jobs:")
    try:
        jobs = client.list_jobs()
        print(f"Found {jobs['count']} jobs")
        for job in jobs["commands"][:3]:  # Show first 3
            print(f"  {job['job_id']}: {job['command'][:50]}... ({job['status']})")
    except Exception as e:
        print(f"❌ Error listing jobs: {e}")


if __name__ == "__main__":
    main()
