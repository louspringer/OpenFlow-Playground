#!/usr/bin/env python3
"""
Ghostbusters Integration for Command Execution Service
Allows queuing Ghostbusters analysis through the fire-and-forget system
"""

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def run_ghostbusters_analysis(project_path: str = ".") -> dict[str, Any]:
    """
    Run Ghostbusters analysis and return results

    Args:
        project_path: Path to project to analyze

    Returns:
        Dict with analysis results
    """
    try:
        logger.info("Starting Ghostbusters analysis for: %s", project_path)

        # Change to project directory
        original_cwd = Path.cwd()
        project_dir = Path(project_path).resolve()

        if not project_dir.exists():
            return {
                "success": False,
                "error": f"Project path does not exist: {project_path}",
                "stdout": "",
                "stderr": f"Directory not found: {project_path}",
            }

        # Run Ghostbusters using the proper Python script
        cmd = [sys.executable, "scripts/call_ghostbusters_properly.py"]

        logger.info("Executing command: %s", " ".join(cmd))

        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "cwd": str(project_dir),
            "project_path": project_path,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": "Ghostbusters analysis timed out after 5 minutes",
            "command": " ".join(cmd) if "cmd" in locals() else "ghostbusters",
            "cwd": str(project_dir) if "project_dir" in locals() else project_path,
            "error": "timeout",
        }
    except Exception as e:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "command": "ghostbusters",
            "cwd": project_path,
            "error": "execution_error",
        }


def run_ghostbusters_specific_agent(
    agent_name: str,
    project_path: str = ".",
) -> dict[str, Any]:
    """
    Run a specific Ghostbusters agent

    Args:
        agent_name: Name of agent to run (security, code_quality, test, build, architecture, model)
        project_path: Path to project to analyze

    Returns:
        Dict with agent results
    """
    try:
        logger.info("Running Ghostbusters agent %s for: %s", agent_name, project_path)

        # Validate agent name
        valid_agents = [
            "security",
            "code_quality",
            "test",
            "build",
            "architecture",
            "model",
        ]
        if agent_name not in valid_agents:
            return {
                "success": False,
                "error": f"Invalid agent name: {agent_name}. Valid agents: {valid_agents}",
                "stdout": "",
                "stderr": f"Invalid agent: {agent_name}",
            }

        # Create Python command to run specific agent
        agent_code = f"""
import asyncio
from src.ghostbusters.agents import {agent_name.title().replace('_', '')}Expert

async def run_agent():
    expert = {agent_name.title().replace('_', '')}Expert()
    result = await expert.detect_delusions('{project_path}')
    print(f"Agent: {agent_name}")
    print(f"Delusions found: {{len(result.delusions)}}")
    for delusion in result.delusions:
        print(f"  - {{delusion.get('description', 'No description')}}")
    return result

if __name__ == "__main__":
    asyncio.run(run_agent())
"""

        # Write temporary script
        temp_script = Path(f"/tmp/ghostbusters_{agent_name}.py")
        temp_script.write_text(agent_code)

        # Run the agent
        cmd = [sys.executable, str(temp_script)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Clean up
        temp_script.unlink(missing_ok=True)

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "agent": agent_name,
            "project_path": project_path,
        }

    except Exception as e:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "command": f"ghostbusters_agent_{agent_name}",
            "agent": agent_name,
            "project_path": project_path,
            "error": "execution_error",
        }


def run_ghostbusters_recovery(
    recovery_type: str,
    target_files: list[str],
    project_path: str = ".",
) -> dict[str, Any]:
    """
    Run Ghostbusters recovery engine

    Args:
        recovery_type: Type of recovery (syntax, indentation, imports, types)
        target_files: List of files to fix
        project_path: Path to project

    Returns:
        Dict with recovery results
    """
    try:
        logger.info(
            "Running Ghostbusters recovery %s for files: %s",
            recovery_type,
            target_files,
        )

        # Validate recovery type
        valid_recoveries = ["syntax", "indentation", "imports", "types"]
        if recovery_type not in valid_recoveries:
            return {
                "success": False,
                "error": f"Invalid recovery type: {recovery_type}. Valid types: {valid_recoveries}",
                "stdout": "",
                "stderr": f"Invalid recovery type: {recovery_type}",
            }

        # Create Python command to run recovery
        recovery_code = f"""
import asyncio
from src.ghostbusters.recovery import {recovery_type.title().replace('_', '')}RecoveryEngine

async def run_recovery():
    engine = {recovery_type.title().replace('_', '')}RecoveryEngine()
    result = await engine.execute_recovery({{
        'target_files': {target_files},
        'project_path': '{project_path}'
    }})
    print(f"Recovery: {recovery_type}")
    print(f"Files processed: {{len(result.fixed_files) if hasattr(result, 'fixed_files') else 'Unknown'}}")
    return result

if __name__ == "__main__":
    asyncio.run(run_recovery())
"""

        # Write temporary script
        temp_script = Path(f"/tmp/ghostbusters_recovery_{recovery_type}.py")
        temp_script.write_text(recovery_code)

        # Run the recovery
        cmd = [sys.executable, str(temp_script)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Clean up
        temp_script.unlink(missing_ok=True)

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "recovery_type": recovery_type,
            "target_files": target_files,
            "project_path": project_path,
        }

    except Exception as e:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "command": f"ghostbusters_recovery_{recovery_type}",
            "recovery_type": recovery_type,
            "target_files": target_files,
            "project_path": project_path,
            "error": "execution_error",
        }


def create_ghostbusters_command(command_type: str, **kwargs) -> str:
    """
    Create a Ghostbusters command string for the command execution service

    Args:
        command_type: Type of command (analysis, agent, recovery)
        **kwargs: Additional parameters

    Returns:
        Command string to execute
    """
    if command_type == "analysis":
        project_path = kwargs.get("project_path", ".")
        return f"python -c \"import sys; sys.path.append('.'); from src.command_execution_service.ghostbusters_integration import run_ghostbusters_analysis; import json; result = run_ghostbusters_analysis('{project_path}'); print(json.dumps(result, indent=2))\""

    elif command_type == "agent":
        agent_name = kwargs.get("agent_name")
        project_path = kwargs.get("project_path", ".")
        if not agent_name:
            raise ValueError("agent_name is required for agent command")
        return f"python -c \"import sys; sys.path.append('.'); from src.command_execution_service.ghostbusters_integration import run_ghostbusters_specific_agent; import json; result = run_ghostbusters_specific_agent('{agent_name}', '{project_path}'); print(json.dumps(result, indent=2))\""

    elif command_type == "recovery":
        recovery_type = kwargs.get("recovery_type")
        target_files = kwargs.get("target_files", [])
        project_path = kwargs.get("project_path", ".")
        if not recovery_type:
            raise ValueError("recovery_type is required for recovery command")
        files_str = json.dumps(target_files)
        return f"python -c \"import sys; sys.path.append('.'); from src.command_execution_service.ghostbusters_integration import run_ghostbusters_recovery; import json; result = run_ghostbusters_recovery('{recovery_type}', {files_str}, '{project_path}'); print(json.dumps(result, indent=2))\""

    else:
        raise ValueError(f"Unknown command type: {command_type}")


if __name__ == "__main__":
    """Test the Ghostbusters integration"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ghostbusters_integration.py <command_type> [args...]")
        print("Command types:")
        print("  analysis [project_path]")
        print("  agent <agent_name> [project_path]")
        print("  recovery <recovery_type> <target_files> [project_path]")
        sys.exit(1)

    command_type = sys.argv[1]

    if command_type == "analysis":
        project_path = sys.argv[2] if len(sys.argv) > 2 else "."
        result = run_ghostbusters_analysis(project_path)
        print(json.dumps(result, indent=2))

    elif command_type == "agent":
        if len(sys.argv) < 3:
            print("Error: agent_name required")
            sys.exit(1)
        agent_name = sys.argv[2]
        project_path = sys.argv[3] if len(sys.argv) > 3 else "."
        result = run_ghostbusters_specific_agent(agent_name, project_path)
        print(json.dumps(result, indent=2))

    elif command_type == "recovery":
        if len(sys.argv) < 3:
            print("Error: recovery_type required")
            sys.exit(1)
        recovery_type = sys.argv[2]
        target_files = sys.argv[3].split(",") if len(sys.argv) > 3 else []
        project_path = sys.argv[4] if len(sys.argv) > 4 else "."
        result = run_ghostbusters_recovery(recovery_type, target_files, project_path)
        print(json.dumps(result, indent=2))

    else:
        print(f"Error: Unknown command type: {command_type}")
        sys.exit(1)
