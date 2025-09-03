#!/usr/bin/env python3
"""
RM-Compliant Safety Check Wrapper

This wrapper implements proper RM compliance for safety checks:
- Self-Monitoring: Detects its own health status
- Operational Visibility: Reports health status externally
- Graceful Degradation: Fails gracefully without hanging
- Single Responsibility: Only handles safety check operations
"""

import sys
import time
import signal
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path


class SafetyCheckWrapper:
    """RM-compliant wrapper for safety check operations."""

    def __init__(self):
        """Initialize the safety check wrapper."""
        self.health_status = "unknown"
        self.last_check_time = None
        self.error_count = 0
        self.success_count = 0
        self.performance_history = []
        self.avg_execution_time = 0

    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status (RM Self-Monitoring)."""
        return {"status": self.health_status, "last_check": self.last_check_time, "error_count": self.error_count, "success_count": self.success_count, "is_healthy": self.health_status == "healthy"}

    def is_healthy(self) -> bool:
        """Check if safety check is healthy (RM Self-Monitoring)."""
        return self.health_status == "healthy"

    def run_safety_check(self, timeout: int = 5, fast_fail: bool = True) -> Dict[str, Any]:
        """Run safety check with timeout and error handling (RM Graceful Degradation)."""
        start_time = time.time()

        try:
            # Fast-fail mode: Skip safety check if it's known to be slow
            if fast_fail and self.health_status == "timeout":
                self.health_status = "fast_fail"
                self.error_count += 1
                self.last_check_time = time.time()
                return {"status": "fast_fail", "message": "Safety check skipped due to known performance issues", "execution_time": 0.001}

            # Set up timeout handler
            def timeout_handler(signum, frame):
                raise TimeoutError("Safety check timed out")

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

            # Run safety check
            result = subprocess.run(["uv", "run", "safety", "check"], capture_output=True, text=True, timeout=timeout)

            signal.alarm(0)  # Cancel timeout

            execution_time = time.time() - start_time
            self.performance_history.append(execution_time)
            self.avg_execution_time = sum(self.performance_history) / len(self.performance_history)

            if result.returncode == 0:
                self.health_status = "healthy"
                self.success_count += 1
                return {"status": "success", "output": result.stdout, "vulnerabilities": self._parse_vulnerabilities(result.stdout), "execution_time": execution_time}
            else:
                self.health_status = "degraded"
                self.error_count += 1
                return {"status": "error", "output": result.stderr, "returncode": result.returncode, "execution_time": execution_time}

        except TimeoutError:
            execution_time = time.time() - start_time
            self.health_status = "timeout"
            self.error_count += 1
            self.last_check_time = time.time()
            self.performance_history.append(execution_time)
            self.avg_execution_time = sum(self.performance_history) / len(self.performance_history)
            return {"status": "timeout", "message": f"Safety check timed out after {timeout} seconds", "execution_time": execution_time}
        except Exception as e:
            execution_time = time.time() - start_time
            self.health_status = "error"
            self.error_count += 1
            self.last_check_time = time.time()
            self.performance_history.append(execution_time)
            self.avg_execution_time = sum(self.performance_history) / len(self.performance_history)
            return {"status": "error", "message": str(e), "execution_time": execution_time}
        finally:
            if self.last_check_time is None:
                self.last_check_time = time.time()

    def _parse_vulnerabilities(self, output: str) -> int:
        """Parse vulnerability count from safety check output."""
        try:
            lines = output.split("\n")
            for line in lines:
                if "vulnerability" in line.lower():
                    # Extract number from line
                    import re

                    numbers = re.findall(r"\d+", line)
                    if numbers:
                        return int(numbers[0])
            return 0
        except:
            return 0

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators (RM Self-Reporting)."""
        return {
            "health_status": self.health_status,
            "last_check_time": self.last_check_time,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "success_rate": self.success_count / (self.success_count + self.error_count) if (self.success_count + self.error_count) > 0 else 0,
            "is_operational": self.health_status in ["healthy", "degraded"],
        }


def main():
    """Main entry point for safety check wrapper."""
    wrapper = SafetyCheckWrapper()

    # Check if we should run safety check or just report status
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        status = wrapper.get_health_status()
        print(f"Safety Check Status: {status['status']}")
        print(f"Healthy: {status['is_healthy']}")
        print(f"Last Check: {status['last_check']}")
        print(f"Error Count: {status['error_count']}")
        print(f"Success Count: {status['success_count']}")
        return 0

    # Run safety check
    result = wrapper.run_safety_check()

    if result["status"] == "success":
        print("✅ Safety check completed successfully")
        if result["vulnerabilities"] > 0:
            print(f"⚠️  Found {result['vulnerabilities']} vulnerabilities")
        return 0
    elif result["status"] == "timeout":
        print("⏰ Safety check timed out")
        return 1
    else:
        print(f"❌ Safety check failed: {result.get('message', 'Unknown error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
