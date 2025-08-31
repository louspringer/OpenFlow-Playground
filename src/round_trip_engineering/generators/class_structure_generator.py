#!/usr/bin/env python3
"""
Class Structure Generator
Focused on generating class structure (name, bases, docstring) from enhanced AST data.
"""

import logging
from typing import Any, Dict, List

from .base_reflective_module import BaseReflectiveModule

logger = logging.getLogger(__name__)


class ClassStructureGenerator(BaseReflectiveModule):
    """Generate class structure from enhanced AST data."""

    def generate_class_structure(
        self, class_name: str, enhanced_ast: Dict[str, Any]
    ) -> str:
        """Generate class structure with proper inheritance and docstring."""
        try:
            start_time = self._get_last_operation_time()
            logger.info(f"🔍 Generating class structure for {class_name}")

            # Extract inheritance information
            bases = enhanced_ast.get("bases", [])
            docstring = enhanced_ast.get("docstring", "")

            # Build class definition with preserved inheritance
            class_def = f"class {class_name}"
            if bases:
                class_def += f"({', '.join(bases)})"
            else:
                # Add Reflective Module as base class if no other bases
                class_def += "(ReflectiveModule)"
            class_def += ":"

            # Add preserved docstring if available, or default if none
            if docstring:
                class_def += f'\n    """\n    {docstring}\n    """\n'
            else:
                # Add default docstring when none is provided
                class_def += f'\n    """Generated class {class_name}"""\n'

            # Track success
            self._track_success()
            operation_time = self._get_last_operation_time() - start_time

            logger.info(
                f"✅ Generated class structure for {class_name} in {operation_time:.3f}s"
            )
            return class_def

        except Exception as e:
            # Track error
            self._track_error()
            logger.error(f"❌ Failed to generate class structure for {class_name}: {e}")

            # Fallback to basic structure
            return f'class {class_name}(ReflectiveModule):\n    """Generated class {class_name}"""\n'

    async def get_module_capabilities(self) -> List[Any]:
        """Get module capabilities."""
        try:
            return [
                {
                    "name": "class_structure_generation",
                    "description": "Generate class structure (name, bases, docstring) from enhanced AST data",
                    "available": self._check_operational_state(),
                    "version": "1.0.0",
                    "details": {
                        "enhanced_ast_support": True,
                        "inheritance_preservation": True,
                        "docstring_preservation": True,
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
