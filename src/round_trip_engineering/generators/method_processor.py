#!/usr/bin/env python3
"""
Method Completer
Focused on completing incomplete method source code with proper structure.
"""

import logging
from typing import Any, Dict, List

from .base_reflective_module import BaseReflectiveModule

logger = logging.getLogger(__name__)


class MethodCompleter(BaseReflectiveModule):
    """Complete incomplete method source code with proper structure."""

    def complete_method_source(self, method_source: str) -> str:
        """Complete incomplete method source code with proper return statements and try blocks."""
        try:
            start_time = self._get_last_operation_time()
            logger.info(f"🔧 Attempting to complete incomplete method source...")
            logger.info(f"  - Original source length: {len(method_source)} chars")

            lines = method_source.split("\n")
            completed_lines = []
            fixes_applied = 0

            logger.info(f"  - Processing {len(lines)} lines...")

            # Track try block state
            in_try_block = False
            try_indent = 0

            for i, line in enumerate(lines):
                line_content = line.strip()
                original_line = line
                logger.debug(f"    Line {i + 1}: {repr(line_content)}")

                # Check for try block start
                if line_content.startswith("try:"):
                    in_try_block = True
                    try_indent = len(line) - len(line.lstrip())
                    logger.info(f"  🔧 Found try block start at line {i + 1}")
                    completed_lines.append(original_line)
                    continue

                # Check for incomplete try blocks (missing except/finally)
                if in_try_block and line_content.startswith("}") and not line_content.startswith("return"):
                    # End of dictionary, ensure it's properly returned
                    logger.info(f"  🔧 Found dictionary end at line {i + 1}: {line_content}")
                    completed_lines.append(original_line)
                    if not any("return" in prev_line for prev_line in completed_lines[-3:]):
                        logger.info(f"  ✅ Adding return statement after dictionary")
                        completed_lines.append("        return result")
                        fixes_applied += 1
                    continue

                # Check for incomplete dictionary literals
                if line_content.startswith('"operation_name"') or line_content.startswith('"nodes"'):
                    # This looks like an incomplete dictionary literal
                    logger.info(f"  🔧 Found incomplete dictionary at line {i + 1}: {line_content}")
                    # Add proper return statement
                    if i > 0 and not lines[i - 1].strip().startswith("return"):
                        logger.info(f"  ✅ Adding return statement before dictionary")
                        completed_lines.append("        return {")
                        fixes_applied += 1
                    completed_lines.append(original_line)
                    continue

                # Check if we're at the end of a method and need to close try block
                if in_try_block and (i == len(lines) - 1 or (i < len(lines) - 1 and lines[i + 1].strip().startswith("def"))):
                    # We're at the end of the method or next line is a new method
                    # Need to close the try block
                    logger.info(f"  🔧 Closing incomplete try block at end of method")
                    completed_lines.append(f"{' ' * try_indent}except Exception as e:")
                    completed_lines.append(f'{" " * (try_indent + 4)}logger.error(f"❌ Error in {lines[0].split("(")[0].split()[-1]}: {{e}}")')
                    completed_lines.append(f"{' ' * (try_indent + 4)}return None")
                    fixes_applied += 1
                    in_try_block = False

                completed_lines.append(original_line)

            completed_source = "\n".join(completed_lines)

            # Track success
            self._track_success()
            operation_time = self._get_last_operation_time() - start_time

            logger.info(f"  ✅ Method completion finished:")
            logger.info(f"    - Fixes applied: {fixes_applied}")
            logger.info(f"    - Completed source length: {len(completed_source)} chars")
            logger.info(f"    - Completion time: {operation_time:.3f}s")

            return completed_source

        except Exception as e:
            # Track error
            self._track_error()
            logger.error(f"  ❌ Exception during method completion: {e}")
            # If we can't fix it, return the original
            return method_source

    async def get_module_capabilities(self) -> List[Any]:
        """Get module capabilities."""
        try:
            return [
                {
                    "name": "method_completion",
                    "description": "Complete incomplete method source code with proper structure",
                    "available": self._check_operational_state(),
                    "version": "1.0.0",
                    "details": {
                        "try_block_completion": True,
                        "return_statement_fixing": True,
                        "dictionary_completion": True,
                    },
                },
                {
                    "name": "reflective_module_interface",
                    "description": "ReflectiveModule operational monitoring interface",
                    "available": True,
                    "version": "1.0.0",
                    "details": {"interface": "BaseReflectiveModule"},
                },
            ]
        except Exception as e:
            logger.error(f"❌ Failed to get capabilities: {e}")
            return []
