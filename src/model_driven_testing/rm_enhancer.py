#!/usr/bin/env python3
"""
RM Compliance: Auto-enhancement system for Python implementations

This module provides automatic logging and profiling enhancement based on RM principles.
"""

import functools
import logging
import time

logger = logging.getLogger(__name__)


class RMEnhancer:
    """RM Compliance: Automatically infers and adds logging/profiling to Python implementations"""

    @staticmethod
    def should_enhance_method(method_name: str, class_name: str = None) -> bool:
        """RM Inference: Determine if method should be enhanced based on context"""
        # Always enhance core RM methods
        if method_name.startswith("get_rm_") or method_name.startswith("_rm_"):
            return True

        # Enhance methods that suggest complexity
        complexity_indicators = ["generate", "extract", "parse", "analyze", "validate", "transform"]
        if any(indicator in method_name.lower() for indicator in complexity_indicators):
            return True

        # Enhance methods in test generation domain
        if class_name and "test" in class_name.lower():
            return True

        return False

    @staticmethod
    def create_profiling_decorator(method_name: str, class_name: str = None) -> callable:
        """RM Inference: Create context-aware profiling decorator"""
        if not RMEnhancer.should_enhance_method(method_name, class_name):
            return lambda func: func  # No-op decorator

        def profile_method(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                context = f"{class_name}.{method_name}" if class_name else method_name

                logger.debug(f"🚀 RM-Enhanced: Starting {context}")
                logger.debug(f"   Args: {args[1:] if args else 'None'}")
                logger.debug(f"   Kwargs: {kwargs}")

                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time

                    # RM Inference: Log based on execution time
                    if execution_time > 1.0:
                        logger.warning(f"🐌 RM-Performance: {context} took {execution_time:.4f}s (slow)")
                    elif execution_time > 0.1:
                        logger.info(f"📊 RM-Performance: {context} took {execution_time:.4f}s")
                    else:
                        logger.debug(f"⚡ RM-Performance: {context} took {execution_time:.4f}s (fast)")

                    return result

                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"❌ RM-Error: {context} failed after {execution_time:.4f}s")
                    logger.error(f"   Exception: {type(e).__name__}: {e}")
                    raise
                finally:
                    execution_time = time.time() - start_time
                    logger.debug(f"📊 RM-Complete: {context} total time: {execution_time:.4f}s")

            return wrapper

        return profile_method


def rm_enhance(func):
    """RM Inference: Automatically enhance methods with logging/profiling based on context"""
    # Infer method name and class name from the function
    method_name = func.__name__
    class_name = func.__qualname__.split(".")[0] if "." in func.__qualname__ else None

    # RM Inference: Automatically determine enhancement level
    return RMEnhancer.create_profiling_decorator(method_name, class_name)(func)
