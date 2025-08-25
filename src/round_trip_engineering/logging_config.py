"""
Logging Configuration for Round-Trip Engineering

This module provides comprehensive logging configuration for profiling,
debugging, and monitoring the round-trip engineering system.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
import time
from typing import Optional, Dict, Any
from functools import wraps


class ProfilingLogger:
    """Logger that tracks performance metrics and provides profiling information."""

    def __init__(self, name: str):
        """Initialize the profiling logger."""
        self.logger = logging.getLogger(name)
        self.start_times: Dict[str, float] = {}
        self.performance_metrics: Dict[str, Dict[str, float]] = {}

    def start_timer(self, operation: str) -> None:
        """Start timing an operation."""
        self.start_times[operation] = time.time()
        self.logger.info(f"⏱️ START: {operation}")

    def end_timer(
        self, operation: str, metadata: Optional[Dict[str, Any]] = None
    ) -> float:
        """End timing an operation and log the duration."""
        if operation not in self.start_times:
            self.logger.warning(f"⚠️ Timer for {operation} was never started")
            return 0.0

        duration = time.time() - self.start_times[operation]

        # Store performance metrics
        if operation not in self.performance_metrics:
            self.performance_metrics[operation] = {}

        self.performance_metrics[operation]["duration"] = duration
        if metadata:
            self.performance_metrics[operation].update(metadata)

        # Log completion with duration
        metadata_str = f" | {metadata}" if metadata else ""
        self.logger.info(
            f"⏱️ END: {operation} | Duration: {duration:.4f}s{metadata_str}"
        )

        # Clean up start time
        del self.start_times[operation]

        return duration

    def get_performance_summary(self) -> Dict[str, Dict[str, float]]:
        """Get a summary of all performance metrics."""
        return self.performance_metrics.copy()

    def log_performance_summary(self) -> None:
        """Log a summary of all performance metrics."""
        if not self.performance_metrics:
            self.logger.info("📊 No performance metrics recorded")
            return

        self.logger.info("📊 PERFORMANCE SUMMARY:")
        for operation, metrics in self.performance_metrics.items():
            duration = metrics.get("duration", 0.0)
            self.logger.info(f"  {operation}: {duration:.4f}s")

            # Log additional metrics
            for key, value in metrics.items():
                if key != "duration":
                    self.logger.info(f"    {key}: {value}")


def profile_operation(operation_name: str):
    """Decorator to profile operations with automatic timing."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get logger from the first argument (self) if it's a method
            if args and hasattr(args[0], "logger"):
                logger = args[0].logger
            else:
                logger = logging.getLogger(func.__module__)

            # Start timing
            start_time = time.time()
            logger.info(f"⏱️ START: {operation_name}")

            try:
                # Execute the function
                result = func(*args, **kwargs)

                # End timing
                duration = time.time() - start_time
                logger.info(
                    f"⏱️ END: {operation_name} | Duration: {duration:.4f}s | Success"
                )

                return result

            except Exception as e:
                # Log error with timing
                duration = time.time() - start_time
                logger.error(
                    f"⏱️ END: {operation_name} | Duration: {duration:.4f}s | Error: {e}"
                )
                raise

        return wrapper

    return decorator


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_profiling: bool = True,
    enable_console: bool = True,
) -> None:
    """
    Setup comprehensive logging for the round-trip engineering system.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        enable_profiling: Enable performance profiling
        enable_console: Enable console output
    """
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s"
    )

    simple_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)

    # File handler for detailed logging
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)

    # Rotating file handler for logs directory
    rotating_handler = logging.handlers.RotatingFileHandler(
        logs_dir / f"round_trip_engineering_{datetime.now().strftime('%Y%m%d')}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(rotating_handler)

    # Performance profiling handler
    if enable_profiling:
        profiling_handler = logging.FileHandler(
            logs_dir / f"profiling_{datetime.now().strftime('%Y%m%d')}.log"
        )
        profiling_handler.setLevel(logging.INFO)
        profiling_handler.setFormatter(detailed_formatter)

        # Create profiling logger
        profiling_logger = logging.getLogger("profiling")
        profiling_logger.addHandler(profiling_handler)
        profiling_logger.setLevel(logging.INFO)

    # Set specific logger levels
    logging.getLogger("src.round_trip_engineering").setLevel(logging.DEBUG)

    logging.info("✅ Logging system initialized")
    logging.info(f"📊 Log level: {log_level.upper()}")
    logging.info(f"📁 Logs directory: {logs_dir.absolute()}")
    if log_file:
        logging.info(f"📄 Detailed log file: {log_file}")
    if enable_profiling:
        logging.info("📊 Performance profiling enabled")


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)


def log_data_transformation(
    logger: logging.Logger,
    operation: str,
    input_data: Any,
    output_data: Any,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log data transformation details for debugging.

    Args:
        logger: Logger instance
        operation: Name of the transformation operation
        input_data: Input data structure
        output_data: Output data structure
        metadata: Additional metadata about the transformation
    """
    logger.info(f"🔄 DATA TRANSFORMATION: {operation}")

    # Log input structure
    if hasattr(input_data, "__len__"):
        logger.debug(
            f"  📥 Input: {type(input_data).__name__} with {len(input_data)} items"
        )
    else:
        logger.debug(f"  📥 Input: {type(input_data).__name__}")

    # Log output structure
    if hasattr(output_data, "__len__"):
        logger.debug(
            f"  📤 Output: {type(output_data).__name__} with {len(output_data)} items"
        )
    else:
        logger.debug(f"  📤 Output: {type(output_data).__name__}")

    # Log metadata
    if metadata:
        for key, value in metadata.items():
            logger.debug(f"  📊 {key}: {value}")

    logger.debug(f"✅ Transformation {operation} completed")


def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    operation: str,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log errors with full context for debugging.

    Args:
        logger: Logger instance
        error: The exception that occurred
        operation: Name of the operation that failed
        context: Additional context about the failure
    """
    logger.error(f"❌ ERROR in {operation}: {type(error).__name__}: {error}")

    if context:
        logger.error(f"  📋 Context: {context}")

    # Log the full traceback for debugging
    import traceback

    logger.debug(f"  🔍 Full traceback:\n{traceback.format_exc()}")
