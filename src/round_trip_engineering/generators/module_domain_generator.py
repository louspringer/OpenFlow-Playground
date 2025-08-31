#!/usr/bin/env python3
"""
Module & Domain Generator
Generates Python code for modules and domains from design models.
"""

import logging
from typing import Any, Dict

from .base_reflective_module import BaseReflectiveModule


class ModuleDomainGenerator(BaseReflectiveModule):
    """Generates Python code for modules and domains from design models"""

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_module_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities"""
        return {
            "code_generation": [
                "generate_module_code",
                "generate_domain_code",
                "generate_package_structure",
            ],
            "templates": [
                "get_module_template",
                "get_domain_template",
                "get_package_template",
            ],
        }

    def generate_module_code(self, component: Dict[str, Any]) -> str:
        """Generate Python module code from a component"""
        module_name = component.get("name", "generated_module")
        description = component.get("description", f"Generated module {module_name}")
        dependencies = component.get("dependencies", [])
        requirements = component.get("requirements", [])

        self.logger.info(f"🎯 Generating module code for: {module_name}")

        # Generate module structure
        code_lines = []

        # Module docstring
        code_lines.append('"""')
        code_lines.append(f"{description}")
        code_lines.append("")
        if requirements:
            code_lines.append("Requirements:")
            for req in requirements:
                code_lines.append(f"  - {req}")
            code_lines.append("")
        if dependencies:
            code_lines.append("Dependencies:")
            for dep in dependencies:
                code_lines.append(f"  - {dep}")
        code_lines.append('"""')
        code_lines.append("")

        # Import statements
        if dependencies:
            for dep in dependencies:
                code_lines.append(f"import {dep}")
            code_lines.append("")

        # Module-level variables
        code_lines.append(f"__version__ = '0.1.0'")
        code_lines.append(f"__author__ = 'Generated'")
        code_lines.append(f"__description__ = '{description}'")
        code_lines.append("")

        # Main module logic
        code_lines.append("def main():")
        code_lines.append(f'    """Main entry point for {module_name}"""')
        code_lines.append("    print(f'Running {module_name}')")
        code_lines.append("")
        code_lines.append("if __name__ == '__main__':")
        code_lines.append("    main()")

        return "\n".join(code_lines)

    def generate_domain_code(self, component: Dict[str, Any]) -> str:
        """Generate Python domain model code from a component"""
        domain_name = component.get("name", "generated_domain")
        description = component.get("description", f"Generated domain {domain_name}")
        requirements = component.get("requirements", [])
        relationships = component.get("relationships", {})

        self.logger.info(f"🎯 Generating domain code for: {domain_name}")

        # Generate domain model structure
        code_lines = []

        # Domain docstring
        code_lines.append('"""')
        code_lines.append(f"{description}")
        code_lines.append("")
        if requirements:
            code_lines.append("Domain Requirements:")
            for req in requirements:
                code_lines.append(f"  - {req}")
        code_lines.append('"""')
        code_lines.append("")

        # Import statements
        code_lines.append("from dataclasses import dataclass, field")
        code_lines.append("from typing import Any, Dict, List, Optional")
        code_lines.append("from datetime import datetime")
        code_lines.append("")

        # Domain class
        code_lines.append("@dataclass")
        code_lines.append(f"class {domain_name.title().replace('_', '')}:")
        code_lines.append(f'    """{description}"""')
        code_lines.append("")
        code_lines.append("    # Core domain properties")
        code_lines.append("    name: str")
        code_lines.append("    description: str")
        code_lines.append(
            "    created_at: datetime = field(default_factory=datetime.now)"
        )
        code_lines.append(
            "    updated_at: datetime = field(default_factory=datetime.now)"
        )
        code_lines.append("    metadata: Dict[str, Any] = field(default_factory=dict)")
        code_lines.append("")

        # Domain methods
        code_lines.append("    def validate(self) -> bool:")
        code_lines.append('        """Validate domain constraints"""')
        code_lines.append("        return bool(self.name and self.description)")
        code_lines.append("")
        code_lines.append("    def update(self, **kwargs) -> None:")
        code_lines.append('        """Update domain properties"""')
        code_lines.append("        for key, value in kwargs.items():")
        code_lines.append("            if hasattr(self, key):")
        code_lines.append("                setattr(self, key, value)")
        code_lines.append("        self.updated_at = datetime.now()")
        code_lines.append("")
        code_lines.append("    def to_dict(self) -> Dict[str, Any]:")
        code_lines.append('        """Convert domain to dictionary"""')
        code_lines.append("        return {")
        code_lines.append("            'name': self.name,")
        code_lines.append("            'description': self.description,")
        code_lines.append("            'created_at': self.created_at.isoformat(),")
        code_lines.append("            'updated_at': self.updated_at.isoformat(),")
        code_lines.append("            'metadata': self.metadata,")
        code_lines.append("        }")

        return "\n".join(code_lines)

    def generate_package_structure(self, component: Dict[str, Any]) -> str:
        """Generate package structure for a module or domain"""
        package_name = component.get("name", "generated_package")
        package_type = component.get("type", "module")

        self.logger.info(f"🎯 Generating package structure for: {package_name}")

        if package_type == "module":
            return self._generate_module_package(package_name)
        elif package_type == "domain":
            return self._generate_domain_package(package_name)
        else:
            return self._generate_generic_package(package_name)

    def _generate_module_package(self, package_name: str) -> str:
        """Generate module package structure"""
        code_lines = []

        # __init__.py content
        code_lines.append('"""')
        code_lines.append(f"{package_name} module package")
        code_lines.append('"""')
        code_lines.append("")
        code_lines.append(f"__version__ = '0.1.0'")
        code_lines.append(f"__package_name__ = '{package_name}'")
        code_lines.append("")
        code_lines.append("# Import main module components")
        code_lines.append(f"from .{package_name} import main")
        code_lines.append("")
        code_lines.append("__all__ = ['main']")

        return "\n".join(code_lines)

    def _generate_domain_package(self, package_name: str) -> str:
        """Generate domain package structure"""
        code_lines = []

        # __init__.py content
        code_lines.append('"""')
        code_lines.append(f"{package_name} domain package")
        code_lines.append('"""')
        code_lines.append("")
        code_lines.append(f"__version__ = '0.1.0'")
        code_lines.append(f"__domain_name__ = '{package_name}'")
        code_lines.append("")
        code_lines.append("# Import domain models")
        code_lines.append(
            f"from .domain_model import {package_name.title().replace('_', '')}"
        )
        code_lines.append("")
        code_lines.append(f"__all__ = ['{package_name.title().replace('_', '')}']")

        return "\n".join(code_lines)

    def _generate_generic_package(self, package_name: str) -> str:
        """Generate generic package structure"""
        code_lines = []

        # __init__.py content
        code_lines.append('"""')
        code_lines.append(f"{package_name} package")
        code_lines.append('"""')
        code_lines.append("")
        code_lines.append(f"__version__ = '0.1.0'")
        code_lines.append(f"__package_name__ = '{package_name}'")
        code_lines.append("")
        code_lines.append("# Package initialization")
        code_lines.append("def initialize():")
        code_lines.append(f'    """Initialize {package_name} package"""')
        code_lines.append("    print(f'Initializing {package_name} package')")
        code_lines.append("")
        code_lines.append("__all__ = ['initialize']")

        return "\n".join(code_lines)

    def get_module_template(self) -> str:
        """Get a template for module generation"""
        return '''"""
{module_name} module

Generated module for {description}
"""

__version__ = '0.1.0'
__author__ = 'Generated'

def main():
    """Main entry point"""
    print('Module {module_name} running')

if __name__ == '__main__':
    main()
'''

    def get_domain_template(self) -> str:
        """Get a template for domain generation"""
        return '''"""
{domain_name} domain model

Generated domain model for {description}
"""

from dataclasses import dataclass, field
from typing import Any, Dict
from datetime import datetime

@dataclass
class {domain_class}:
    """{description}"""
    
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate domain constraints"""
        return bool(self.name and self.description)
'''

    def get_package_template(self) -> str:
        """Get a template for package generation"""
        return '''"""
{package_name} package

Generated package for {description}
"""

__version__ = '0.1.0'
__package_name__ = '{package_name}'

def initialize():
    """Initialize package"""
    print(f'Initializing {package_name} package')

__all__ = ['initialize']
'''
