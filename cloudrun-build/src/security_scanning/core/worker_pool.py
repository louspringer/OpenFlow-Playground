"""
Multi-Threaded Worker Pool for Security Scanning

This module uses proven libraries for robust task management:
- concurrent.futures for thread pool management
- tenacity for retry logic with exponential backoff
- asyncio for async task coordination
- psutil for system monitoring
"""

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import psutil

try:
    from tenacity import (
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False
    logging.warning("tenacity not available, using basic retry logic")

logger = logging.getLogger(__name__)


class WorkerPool:
    """
    High-performance multi-threaded worker pool using proven libraries

    Features:
    - ThreadPoolExecutor for robust thread management
    - Tenacity for retry logic with exponential backoff
    - Automatic CPU core detection and optimization
    - Performance monitoring and metrics
    - Graceful error handling and task abandonment
    """

    def __init__(self, max_workers: Optional[int] = None, enable_monitoring: bool = True):
        """
        Initialize the worker pool

        Args:
            max_workers: Maximum number of worker threads (auto-detected if None)
            enable_monitoring: Enable performance monitoring
        """
        self.max_workers = max_workers or self._get_optimal_worker_count()
        self.enable_monitoring = enable_monitoring

        # Thread pool executor
        self.executor = None
        self.monitor_thread = None
        self.shutdown_event = threading.Event()

        # Performance metrics
        self.metrics = {
            "tasks_submitted": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "tasks_retried": 0,
            "tasks_abandoned": 0,
            "start_time": None,
            "cpu_usage": [],
            "memory_usage": [],
        }

        logger.info(f"Initialized worker pool with {self.max_workers} workers")

    def _get_optimal_worker_count(self) -> int:
        """Determine optimal number of workers based on system resources"""
        cpu_count = psutil.cpu_count(logical=True)
        memory_gb = psutil.virtual_memory().total / (1024**3)

        # Target ~80% CPU utilization for security scanning
        # Security scanning is I/O bound with some CPU work, so we can use more workers
        optimal_workers = int(cpu_count * 3.2)  # 3.2x CPU cores for ~80% utilization

        # Adjust based on available memory (each worker needs ~25MB for security scanning)
        max_memory_workers = int(memory_gb * 6)  # Allow more memory usage for better throughput

        # Use the higher of the two for better CPU utilization
        optimal_workers = max(optimal_workers, max_memory_workers)

        # Cap at reasonable maximum to prevent system overload
        optimal_workers = min(optimal_workers, 24)

        # Ensure minimum of 8 workers for good parallelism on 4-core systems
        optimal_workers = max(8, optimal_workers)

        logger.info(f"System: {cpu_count} CPU cores, {memory_gb:.1f}GB RAM")
        logger.info(f"Target ~80% CPU utilization with {optimal_workers} workers")

        return optimal_workers

    def start(self):
        """Start the worker pool and monitoring"""
        if self.executor is not None:
            logger.warning("Worker pool already started")
            return

        logger.info("Starting worker pool...")

        # Start the thread pool executor
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="SecurityScanner")

        # Start monitoring if enabled
        if self.enable_monitoring:
            self.monitor_thread = threading.Thread(target=self._monitor_performance, daemon=True, name="PerformanceMonitor")
            self.monitor_thread.start()

        self.metrics["start_time"] = time.time()
        logger.info("Worker pool started successfully")

    def stop(self):
        """Stop the worker pool gracefully"""
        if self.executor is None:
            return

        logger.info("Stopping worker pool...")

        # Signal shutdown
        self.shutdown_event.set()

        # Shutdown executor
        self.executor.shutdown(wait=True)
        self.executor = None

        # Wait for monitor thread
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5.0)

        logger.info("Worker pool stopped")

    def process_files(
        self,
        files: list[Path],
        worker_func: Callable[[Path], Any],
        show_progress: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Process a list of files using the worker pool

        Args:
            files: List of file paths to process
            worker_func: Function to apply to each file
            show_progress: Show progress updates

        Returns:
            List of worker results
        """
        if not files:
            return []

        logger.info(f"Processing {len(files)} files with {self.max_workers} workers")

        # Create retry wrapper if tenacity is available
        if TENACITY_AVAILABLE:
            retry_wrapper = self._create_tenacity_retry(worker_func)
        else:
            retry_wrapper = self._create_basic_retry(worker_func)

        # Submit all tasks to executor
        results = []
        completed = 0
        total = len(files)

        # Submit work to executor in batches of 4
        # This keeps each thread busy longer and reduces context switching overhead
        batch_size = 4
        file_batches = [files[i : i + batch_size] for i in range(0, len(files), batch_size)]

        future_to_batch = {}
        for batch in file_batches:
            future = self.executor.submit(self._process_batch, retry_wrapper, batch)
            future_to_batch[future] = batch
            self.metrics["tasks_submitted"] += 1

        # Collect results from batches
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            batch_size = len(batch)
            completed += batch_size

            try:
                batch_results = future.result()
                # Flatten batch results into individual results
                if isinstance(batch_results, list):
                    results.extend(batch_results)
                else:
                    results.append(batch_results)
                self.metrics["tasks_completed"] += batch_size

            except Exception as e:
                logger.error(f"Batch failed permanently for {len(batch)} files: {e}")
                self.metrics["tasks_failed"] += batch_size
                self.metrics["tasks_abandoned"] += batch_size

                # Add error results for each file in the batch
                for file_path in batch:
                    results.append(
                        {
                            "file_path": str(file_path),
                            "success": False,
                            "error": str(e),
                            "retry_count": 3,  # Max retries attempted
                            "abandoned": True,
                        }
                    )

            # Show progress
            if show_progress and completed % 10 == 0:
                progress = (completed / total) * 100
                logger.info(f"Progress: {progress:.1f}% ({completed}/{total})")

        # Calculate final metrics
        self._update_metrics()

        logger.info(f"Completed processing {len(files)} files")
        logger.info(
            f"Tasks: {self.metrics['tasks_submitted']} submitted, {self.metrics['tasks_completed']} completed, {self.metrics['tasks_failed']} failed, {self.metrics['tasks_abandoned']} abandoned"
        )

        return results

    def _create_tenacity_retry(self, worker_func: Callable[[Path], Any]):
        """Create retry wrapper using tenacity library"""

        @retry(
            stop=stop_after_attempt(3),  # Three strikes and you're out
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type((Exception,)),
            before_sleep=lambda retry_state: logger.warning(f"Retrying {retry_state.fn.__name__} after {retry_state.attempt_number} attempts"),
        )
        def retry_wrapper(file_path: Path):
            start_time = time.time()
            try:
                result = worker_func(file_path)
                processing_time = time.time() - start_time

                # Add metadata to result
                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, dict):
                            item["processing_time"] = processing_time
                            item["file_path"] = str(file_path)
                            item["success"] = True
                else:
                    result = {
                        "data": result,
                        "processing_time": processing_time,
                        "file_path": str(file_path),
                        "success": True,
                    }

                return result

            except Exception as e:
                processing_time = time.time() - start_time
                logger.error(f"Task failed for {file_path}: {e}")
                raise

        return retry_wrapper

    def _create_basic_retry(self, worker_func: Callable[[Path], Any]):
        """Create basic retry wrapper without tenacity"""

        def retry_wrapper(file_path: Path):
            start_time = time.time()
            last_error = None

            for attempt in range(3):  # Three strikes and you're out
                try:
                    result = worker_func(file_path)
                    processing_time = time.time() - start_time

                    # Add metadata to result
                    if isinstance(result, list):
                        for item in result:
                            if isinstance(item, dict):
                                item["processing_time"] = processing_time
                                item["file_path"] = str(file_path)
                                item["success"] = True
                                item["retry_count"] = attempt
                    else:
                        result = {
                            "data": result,
                            "processing_time": processing_time,
                            "file_path": str(file_path),
                            "success": True,
                            "retry_count": attempt,
                        }

                    return result

                except Exception as e:
                    last_error = e
                    if attempt < 2:  # Not the last attempt
                        logger.warning(f"Task failed for {file_path} (attempt {attempt + 1}/3): {e}")
                        self.metrics["tasks_retried"] += 1
                        time.sleep(min(2**attempt, 5))  # Exponential backoff, max 5s
                    else:
                        logger.error(f"Task failed permanently for {file_path} after 3 attempts: {e}")
                        raise last_error

            # This should never be reached
            raise last_error or Exception("Task failed for unknown reason")

        return retry_wrapper

    def _process_batch(self, worker_func: Callable[[Path], Any], batch: list[Path]) -> list[Any]:
        """
        Process a batch of files using the worker function

        Args:
            worker_func: Function to apply to each file
            batch: List of file paths to process

        Returns:
            List of results from processing the batch
        """
        batch_results = []

        for file_path in batch:
            try:
                result = worker_func(file_path)
                batch_results.append(result)
            except Exception as e:
                logger.error(f"File processing failed in batch for {file_path}: {e}")
                # Add error result for this file
                batch_results.append(
                    {
                        "file_path": str(file_path),
                        "success": False,
                        "error": str(e),
                        "retry_count": 0,  # No retries at batch level
                        "abandoned": False,
                    }
                )

        return batch_results

    def _monitor_performance(self):
        """Monitor system performance and worker pool metrics"""
        while not self.shutdown_event.is_set():
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1.0)
                memory = psutil.virtual_memory()

                self.metrics["cpu_usage"].append(cpu_percent)
                self.metrics["memory_usage"].append(memory.percent)

                # Keep only last 100 measurements
                if len(self.metrics["cpu_usage"]) > 100:
                    self.metrics["cpu_usage"] = self.metrics["cpu_usage"][-100:]
                    self.metrics["memory_usage"] = self.metrics["memory_usage"][-100:]

                # Log performance every 10 seconds
                if len(self.metrics["cpu_usage"]) % 10 == 0:
                    avg_cpu = sum(self.metrics["cpu_usage"][-10:]) / 10
                    avg_memory = sum(self.metrics["memory_usage"][-10:]) / 10
                    logger.debug(f"Performance: CPU {avg_cpu:.1f}%, Memory {avg_memory:.1f}%")

                time.sleep(1.0)

            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                time.sleep(5.0)

    def _update_metrics(self):
        """Update performance metrics"""
        if self.metrics["start_time"]:
            elapsed = time.time() - self.metrics["start_time"]
            if elapsed > 0:
                self.metrics["throughput"] = self.metrics["tasks_completed"] / elapsed

    def get_performance_summary(self) -> dict[str, Any]:
        """Get a summary of performance metrics"""
        self._update_metrics()

        # Calculate current CPU and memory usage
        current_cpu = psutil.cpu_percent()
        current_memory = psutil.virtual_memory().percent

        # Calculate averages
        avg_cpu = sum(self.metrics["cpu_usage"]) / len(self.metrics["cpu_usage"]) if self.metrics["cpu_usage"] else 0
        avg_memory = sum(self.metrics["memory_usage"]) / len(self.metrics["memory_usage"]) if self.metrics["memory_usage"] else 0

        return {
            "worker_count": self.max_workers,
            "tasks_submitted": self.metrics["tasks_submitted"],
            "tasks_completed": self.metrics["tasks_completed"],
            "tasks_failed": self.metrics["tasks_failed"],
            "tasks_retried": self.metrics["tasks_retried"],
            "tasks_abandoned": self.metrics["tasks_abandoned"],
            "success_rate": (self.metrics["tasks_completed"] - self.metrics["tasks_failed"]) / max(1, self.metrics["tasks_submitted"]),
            "throughput": self.metrics.get("throughput", 0),
            "current_cpu_usage": current_cpu,
            "current_memory_usage": current_memory,
            "average_cpu_usage": avg_cpu,
            "average_memory_usage": avg_memory,
            "elapsed_time": (time.time() - self.metrics["start_time"] if self.metrics["start_time"] else 0),
        }

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


def create_worker_pool(max_workers: Optional[int] = None, enable_monitoring: bool = True) -> WorkerPool:
    """
    Factory function to create a worker pool with optimal settings

    Args:
        max_workers: Maximum number of workers (auto-detected if None)
        enable_monitoring: Enable performance monitoring

    Returns:
        Configured worker pool instance
    """
    return WorkerPool(max_workers=max_workers, enable_monitoring=enable_monitoring)
