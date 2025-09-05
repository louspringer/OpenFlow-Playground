#!/usr/bin/env python3
"""
Method Validator
Focused on validating method source code for basic Python syntax.
"""

import ast
import logging
from typing import Any, Dict, List

from .base_reflective_module import BaseReflectiveModule

logger = logging.getLogger(__name__)


class MethodValidator(BaseReflectiveModule):
    """Validate method source code for basic Python syntax."""

    def is_valid_method_source(self, method_source: str) -> bool:
        """Validate that method source code has basic Python syntax."""
        try:
            start_time = self._get_last_operation_time()
            logger.info(f"🔍 Validating method source code...")
            logger.info(f"  - Source length: {len(method_source)} chars")

            # Basic validation: check for common syntax issues
            source = method_source.strip()

            # Must start with 'def' or 'async def'
            if not (source.startswith("def ") or source.startswith("async def ")):
                logger.warning(f"  ❌ Method doesn't start with 'def' or 'async def': {repr(source[:50])}")
                self._track_error()
                return False

            # Must have proper indentation (4 spaces) - but be smarter about docstrings
            lines = source.split("\n")
            logger.info(f"  - Method has {len(lines)} lines")

            # Skip docstring lines when checking indentation
            in_docstring = False
            docstring_quotes = None

            for i, line in enumerate(lines[1:], 1):  # Skip first line (def statement)
                stripped_line = line.strip()

                # Check for docstring start/end
                if '"""' in stripped_line or "'''" in stripped_line:
                    if not in_docstring:
                        # Starting docstring
                        in_docstring = True
                        if '"""' in stripped_line:
                            docstring_quotes = '"""'
                        else:
                            docstring_quotes = "'''"
                        # Check if docstring ends on same line
                        if stripped_line.count(docstring_quotes) >= 2:
                            in_docstring = False
                    else:
                        # Ending docstring
                        if docstring_quotes in stripped_line:
                            in_docstring = False
                        continue

                # Skip indentation check for docstring lines
                if in_docstring:
                    continue

                # Only check indentation for non-empty, non-docstring lines
                if stripped_line and not line.startswith("    "):
                    logger.warning(f"  ❌ Line {i + 1} has improper indentation: {repr(line)}")
                    self._track_error()
                    return False

            # Must have at least one method body line
            if len(lines) < 2:
                logger.warning(f"  ❌ Method has insufficient lines: {len(lines)}")
                self._track_error()
                return False

            # Check for basic Python syntax - be more lenient for partial implementations
            try:
                logger.info(f"  - Testing AST parsing...")
                # Try to parse as a complete method in class context
                # Need to properly indent the method body for class context
                class_source = f"class Test:\n    {source.replace(chr(10), chr(10) + '    ')}"
                logger.info(f"  - Class source: {repr(class_source)}")
                ast.parse(class_source)
                logger.info(f"  ✅ Method passes AST parsing")

                # Track success
                self._track_success()
                operation_time = self._get_last_operation_time() - start_time
                logger.info(f"✅ Method validation completed in {operation_time:.3f}s")
                return True

            except SyntaxError as e:
                logger.warning(f"  ❌ Method fails AST parsing: {e}")
                logger.warning(f"  - Syntax error details: {e.msg} at line {e.lineno}")
                self._track_error()
                return False

        except Exception as e:
            self._track_error()
            logger.error(f"  ❌ Exception during validation: {e}")
            return False

    async def get_module_capabilities(self) -> List[Any]:
        """Get module capabilities."""
        try:
            return [
                {
                    "name": "method_validation",
                    "description": "Validate method source code for basic Python syntax",
                    "available": self._check_operational_state(),
                    "version": "1.0.0",
                    "details": {
                        "ast_parsing": True,
                        "indentation_check": True,
                        "syntax_validation": True,
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
