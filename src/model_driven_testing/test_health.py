#!/usr/bin/env python3
"""
Test Generation Health Monitor - RM Compliant

This module monitors the health of test generation operations.
"""

import time
from typing import Dict, Any


class TestGenerationHealth:
    """Monitor test generation health and performance"""

    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.last_success = None
        self.last_failure = None
        self.start_time = time.time()

    def record_success(self, tests_generated: int = 1):
        """Record a successful test generation"""
        self.success_count += 1
        self.last_success = time.time()

    def record_failure(self):
        """Record a test generation failure"""
        self.failure_count += 1
        self.last_failure = time.time()

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get current health indicators"""
        current_time = time.time()
        uptime = current_time - self.start_time

        return {
            "uptime_seconds": uptime,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.success_count / max(1, self.success_count + self.failure_count),
            "last_success_ago": current_time - self.last_success if self.last_success else None,
            "last_failure_ago": current_time - self.last_failure if self.last_failure else None,
            "status": "healthy" if self.failure_count == 0 else "degraded" if self.success_count > self.failure_count else "unhealthy",
        }
