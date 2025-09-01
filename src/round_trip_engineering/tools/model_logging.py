"""
Enhanced logging and profiling for model management operations.
"""

import logging
import time
import psutil
import os
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
from datetime import datetime
from contextlib import contextmanager

from .model_schemas import LogEntry, PerformanceMetrics


class ModelProfiler:
    """Profiler for model management operations."""

    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.process = psutil.Process(os.getpid())

    def record_operation(
        self,
        operation: str,
        duration_ms: float,
        success: bool,
        error_message: Optional[str] = None,
    ) -> PerformanceMetrics:
        """Record operation metrics."""
        try:
            memory_info = self.process.memory_info()
            memory_usage_mb = memory_info.rss / 1024 / 1024  # Convert to MB
            cpu_usage_percent = self.process.cpu_percent()
        except Exception:
            memory_usage_mb = None
            cpu_usage_percent = None

        metric = PerformanceMetrics(
            operation=operation,
            duration_ms=duration_ms,
            memory_usage_mb=memory_usage_mb,
            cpu_usage_percent=cpu_usage_percent,
            success=success,
            error_message=error_message,
        )

        self.metrics.append(metric)
        return metric

    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.metrics:
            return {"message": "No metrics recorded"}

        successful_ops = [m for m in self.metrics if m.success]
        failed_ops = [m for m in self.metrics if not m.success]

        return {
            "total_operations": len(self.metrics),
            "successful_operations": len(successful_ops),
            "failed_operations": len(failed_ops),
            "success_rate": len(successful_ops) / len(self.metrics) * 100,
            "average_duration_ms": sum(m.duration_ms for m in self.metrics)
            / len(self.metrics),
            "max_duration_ms": max(m.duration_ms for m in self.metrics),
            "min_duration_ms": min(m.duration_ms for m in self.metrics),
            "average_memory_mb": sum(m.memory_usage_mb or 0 for m in self.metrics)
            / len(self.metrics),
            "max_memory_mb": max(m.memory_usage_mb or 0 for m in self.metrics),
            "recent_operations": [
                m.dict() for m in self.metrics[-10:]
            ],  # Last 10 operations
        }


class ModelLogger:
    """Enhanced logger for model management operations."""

    def __init__(self, name: str = "model_management"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create handlers if they don't exist
        if not self.logger.handlers:
            self._setup_handlers()

        self.profiler = ModelProfiler()

    def _setup_handlers(self):
        """Setup logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for detailed logs
        file_handler = logging.FileHandler("logs/model_management.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def log_operation(
        self,
        level: str,
        message: str,
        operation: Optional[str] = None,
        model_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Log operation with structured data."""
        log_entry = LogEntry(
            level=level,
            message=message,
            operation=operation,
            target_model=model_name,  # Fixed: use target_model instead of model_name
            details=details,
        )

        # Log to standard logger
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(
            f"{message} | Operation: {operation} | Model: {model_name} | Details: {details}"
        )

        return log_entry

    def profile_operation(self, operation_name: str):
        """Decorator to profile operations."""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                success = False
                error_message = None

                try:
                    result = func(*args, **kwargs)
                    success = True
                    return result
                except Exception as e:
                    error_message = str(e)
                    raise
                finally:
                    duration_ms = (time.time() - start_time) * 1000
                    metric = self.profiler.record_operation(
                        operation_name, duration_ms, success, error_message
                    )

                    # Log the operation
                    self.log_operation(
                        "INFO" if success else "ERROR",
                        f"Operation '{operation_name}' completed",
                        operation=operation_name,
                        details={
                            "duration_ms": duration_ms,
                            "success": success,
                            "error_message": error_message,
                        },
                    )

            return wrapper

        return decorator

    @contextmanager
    def operation_context(self, operation_name: str, model_name: Optional[str] = None):
        """Context manager for operation profiling."""
        start_time = time.time()
        success = False
        error_message = None

        self.log_operation(
            "DEBUG",
            f"Starting operation: {operation_name}",
            operation=operation_name,
            model_name=model_name,
        )

        try:
            yield
            success = True
        except Exception as e:
            error_message = str(e)
            self.log_operation(
                "ERROR",
                f"Operation failed: {error_message}",
                operation=operation_name,
                model_name=model_name,
            )
            raise
        finally:
            duration_ms = (time.time() - start_time) * 1000
            metric = self.profiler.record_operation(
                operation_name, duration_ms, success, error_message
            )

            self.log_operation(
                "INFO" if success else "ERROR",
                f"Operation '{operation_name}' completed in {duration_ms:.2f}ms",
                operation=operation_name,
                model_name=model_name,
                details={
                    "duration_ms": duration_ms,
                    "success": success,
                    "error_message": error_message,
                },
            )

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        return self.profiler.get_summary()

    def export_metrics(self, filename: str = "model_management_metrics.json"):
        """Export metrics to JSON file."""
        import json
        from pathlib import Path

        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)

        metrics_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.profiler.get_summary(),
            "all_metrics": [metric.dict() for metric in self.profiler.metrics],
        }

        with open(f"logs/{filename}", "w") as f:
            json.dump(metrics_data, f, indent=2, default=str)

        self.log_operation("INFO", f"Metrics exported to logs/{filename}")
        return f"logs/{filename}"


# Global logger instance
model_logger = ModelLogger()
