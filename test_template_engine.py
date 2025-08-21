#!/usr/bin/env python3
"""Test template engine vs current code generation approaches"""

import ast


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except:
        return 0


def generate_with_current_approach() -> str:
    """Generate code using our current complex approach"""
    return '''from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
import logging
import subprocess

@dataclass
class ComplexFunction:
    """Complex function with many features"""
    name: str
    parameters: List[str]
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    body: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    type_hints: Dict[str, str] = field(default_factory=dict)
    validation_rules: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Post-initialization processing"""
        self._validate_parameters()
        self._setup_logging()

    def _validate_parameters(self) -> None:
        """Validate function parameters"""
        if not self.parameters:
            raise ValueError("Parameters cannot be empty")

    def _setup_logging(self) -> None:
        """Setup logging for the function"""
        self.logger = logging.getLogger(f"{__name__}.{self.name}")

    def generate_code(self) -> str:
        """Generate the actual code"""
        lines = []

        # Add decorators
        for decorator in self.decorators:
            lines.append(f"@{decorator}")

        # Function signature
        param_str = ", ".join([f"{p}: {self.type_hints.get(p, 'Any')}" for p in self.parameters])
        signature = f"def {self.name}({param_str})"
        if self.return_type:
            signature += f" -> {self.return_type}"
        signature += ":"
        lines.append(signature)

        # Docstring
        if self.docstring:
            lines.append(f'    """{self.docstring}"""')

        # Body
        for line in self.body:
            lines.append(f"    {line}")

        return "\\n".join(lines)'''


def generate_with_simple_template() -> str:
    """Generate code using simple template approach"""
    return '''def simple_function(name, parameters, body):
    """Simple function generation"""
    param_str = ", ".join(parameters)
    return f"""def {name}({param_str}):
    {body}"""'''


def main():
    """Compare template approaches"""
    print("🔍 Template Engine vs Current Approach Comparison:")

    # Test current approach
    current_code = generate_with_current_approach()
    current_nodes = count_ast_nodes(current_code)

    # Test simple template
    simple_code = generate_with_simple_template()
    simple_nodes = count_ast_nodes(simple_code)

    print(f"Current approach: {current_nodes} nodes")
    print(f"Simple template: {simple_nodes} nodes")
    print(f"Difference: {current_nodes - simple_nodes} nodes")
    print(f"Complexity ratio: {current_nodes / simple_nodes:.2f}x")

    if simple_nodes < current_nodes:
        print("✅ Simple templates REDUCE complexity")
    else:
        print("❌ Simple templates don't help")


if __name__ == "__main__":
    main()

"""Test template engine vs current code generation approaches"""

import ast


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except:
        return 0


def generate_with_current_approach() -> str:
    """Generate code using our current complex approach"""
    return '''from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path
import logging
import subprocess

@dataclass
class ComplexFunction:
    """Complex function with many features"""
    name: str
    parameters: List[str]
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    body: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    type_hints: Dict[str, str] = field(default_factory=dict)
    validation_rules: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Post-initialization processing"""
        self._validate_parameters()
        self._setup_logging()

    def _validate_parameters(self) -> None:
        """Validate function parameters"""
        if not self.parameters:
            raise ValueError("Parameters cannot be empty")

    def _setup_logging(self) -> None:
        """Setup logging for the function"""
        self.logger = logging.getLogger(f"{__name__}.{self.name}")

    def generate_code(self) -> str:
        """Generate the actual code"""
        lines = []

        # Add decorators
        for decorator in self.decorators:
            lines.append(f"@{decorator}")

        # Function signature
        param_str = ", ".join([f"{p}: {self.type_hints.get(p, 'Any')}" for p in self.parameters])
        signature = f"def {self.name}({param_str})"
        if self.return_type:
            signature += f" -> {self.return_type}"
        signature += ":"
        lines.append(signature)

        # Docstring
        if self.docstring:
            lines.append(f'    """{self.docstring}"""')

        # Body
        for line in self.body:
            lines.append(f"    {line}")

        return "\\n".join(lines)'''


def generate_with_simple_template() -> str:
    """Generate code using simple template approach"""
    return '''def simple_function(name, parameters, body):
    """Simple function generation"""
    param_str = ", ".join(parameters)
    return f"""def {name}({param_str}):
    {body}"""'''


def main():
    """Compare template approaches"""
    print("🔍 Template Engine vs Current Approach Comparison:")

    # Test current approach
    current_code = generate_with_current_approach()
    current_nodes = count_ast_nodes(current_code)

    # Test simple template
    simple_code = generate_with_simple_template()
    simple_nodes = count_ast_nodes(simple_code)

    print(f"Current approach: {current_nodes} nodes")
    print(f"Simple template: {simple_nodes} nodes")
    print(f"Difference: {current_nodes - simple_nodes} nodes")
    print(f"Complexity ratio: {current_nodes / simple_nodes:.2f}x")

    if simple_nodes < current_nodes:
        print("✅ Simple templates REDUCE complexity")
    else:
        print("❌ Simple templates don't help")


if __name__ == "__main__":
    main()




