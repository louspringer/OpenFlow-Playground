"""
Duplication Cleaner Module

This module removes duplicate method definitions and return statements from generated code
to prevent the "hairball" of code duplication that was causing issues.
"""

import logging
from typing import List, Set

logger = logging.getLogger(__name__)


class DuplicationCleaner:
    """Removes duplications from generated code."""

    def __init__(self):
        """Initialize the duplication cleaner."""
        logger.info("✅ Duplication cleaner initialized")

    def clean_code(self, code: str) -> str:
        """
        Clean generated code by removing duplications.

        Args:
            code: Generated code that may contain duplications

        Returns:
            Cleaned code without duplications
        """
        try:
            import traceback

            # REAL profiling: track call stack
            stack_trace = traceback.format_stack()
            logger.info("🧹 Cleaning generated code for duplications...")
            logger.info(f"📞 CALL STACK: Called from {len(stack_trace)} levels:")
            for i, frame in enumerate(stack_trace[-5:]):  # Show last 5 frames
                logger.info(f"   Frame {i}: {frame.strip()}")

            lines = code.split("\n")
            cleaned_lines = []
            seen_methods: Set[str] = set()
            seen_returns: Set[str] = set()

            logger.info(f"🔍 Starting duplication cleaning: {len(lines)} lines")

            # SIMPLE APPROACH: Process each line once, no complex loop control
            current_method = None
            method_has_return = False

            # Use a simple for loop with a flag to skip duplicate method bodies
            skip_until_next_method = False
            for line in lines:
                line_stripped = line.strip()

                # Check for duplicate method definitions
                if line_stripped.startswith("def ") and "(" in line_stripped:
                    # Extract full method signature including parameters
                    method_start = line_stripped.find("def ") + 4
                    method_end = line_stripped.find(":", method_start)
                    if method_end == -1:
                        method_end = len(line_stripped)

                    method_signature = line_stripped[method_start:method_end].strip()

                    if method_signature in seen_methods:
                        logger.warning(
                            f"⚠️ Removing duplicate method: {method_signature}"
                        )
                        # Set flag to skip until next method
                        skip_until_next_method = True
                        current_method = None
                        method_has_return = False
                        continue
                    else:
                        # This is a new method, start processing it
                        seen_methods.add(method_signature)
                        current_method = method_signature
                        method_has_return = False
                        skip_until_next_method = False
                        cleaned_lines.append(line)

                # Skip all lines if we're in a duplicate method body
                elif skip_until_next_method:
                    continue

                # Check for return statements (including unreachable ones)
                elif line_stripped.startswith("return "):
                    if current_method and method_has_return:
                        logger.warning(
                            f"⚠️ Removing unreachable return in {current_method}: {line_stripped}"
                        )
                        # Skip this unreachable return - don't add it to cleaned_lines
                        continue
                    else:
                        method_has_return = True
                        # This is the first return in the method, add it to cleaned lines
                        cleaned_lines.append(line)

                # Add all other lines (class definition, method bodies, etc.)
                else:
                    cleaned_lines.append(line)

            cleaned_code = "\n".join(cleaned_lines)

            # Verify cleaning was effective
            original_lines = len(code.split("\n"))
            cleaned_lines_count = len(cleaned_code.split("\n"))

            if original_lines != cleaned_lines_count:
                logger.info(
                    f"✅ Code cleaning complete: {original_lines} → {cleaned_lines_count} lines"
                )
            else:
                logger.info("✅ Code cleaning complete: No duplications found")

            return cleaned_code

        except Exception as e:
            logger.error(f"❌ Code cleaning failed: {e}")
            return code

    def clean_method_duplications(self, code: str) -> str:
        """
        Clean only method duplications.

        Args:
            code: Code with potential method duplications

        Returns:
            Code with method duplications removed
        """
        try:
            lines = code.split("\n")
            cleaned_lines = []
            seen_methods: Set[str] = set()

            i = 0
            while i < len(lines):
                line = lines[i].strip()

                if line.startswith("def ") and "(" in line:
                    method_signature = line.split("(")[0].replace("def ", "").strip()
                    if method_signature in seen_methods:
                        logger.warning(
                            f"⚠️ Removing duplicate method: {method_signature}"
                        )
                        # Skip until next method or end of class
                        while i < len(lines) and not lines[i].strip().startswith(
                            "def "
                        ):
                            i += 1
                        continue
                    else:
                        seen_methods.add(method_signature)

                cleaned_lines.append(lines[i])
                i += 1

            return "\n".join(cleaned_lines)

        except Exception as e:
            logger.error(f"❌ Method duplication cleaning failed: {e}")
            return code

    def clean_return_duplications(self, code: str) -> str:
        """
        Clean only return statement duplications.

        Args:
            code: Code with potential return duplications

        Returns:
            Code with return duplications removed
        """
        try:
            lines = code.split("\n")
            cleaned_lines = []
            seen_returns: Set[str] = set()

            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith("return "):
                    if stripped_line in seen_returns:
                        logger.warning(f"⚠️ Removing duplicate return: {stripped_line}")
                        continue
                    else:
                        seen_returns.add(stripped_line)

                cleaned_lines.append(line)

            return "\n".join(cleaned_lines)

        except Exception as e:
            logger.error(f"❌ Return duplication cleaning failed: {e}")
            return code
