#!/usr/bin/env python3
"""Test if simple approaches can achieve the same goals as complex model-driven systems"""

import ast
import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Approach:
    """Represents a different approach to achieving our goals"""

    name: str
    description: str
    code: str
    expected_benefits: list[str]
    expected_risks: list[str]


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception:
        return 0


def test_mypy_compliance(code: str) -> list[str]:
    """Test if code passes MyPy validation"""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [
                "uv",
                "run",
                "mypy",
                "--show-error-codes",
                "--no-error-summary",
                temp_file,
            ],
            capture_output=True,
            text=True,
        )

        os.unlink(temp_file)

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"MyPy test failed: {e}"]


def test_black_compliance(code: str) -> bool:
    """Test if code passes Black formatting"""
    try:
        result = subprocess.run(
            ["uv", "run", "black", "--check", "-"],
            input=code,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def test_flake8_compliance(code: str) -> list[str]:
    """Test if code passes Flake8 validation"""
    try:
        result = subprocess.run(
            ["uv", "run", "flake8", "--select=F401,E302,E305,W291,W292", "-"],
            input=code,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Flake8 test failed: {e}"]


def generate_complex_model_driven() -> str:
    """Generate code using our current complex model-driven approach"""
    return '''from typing import Dict, List, Union, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import yaml
import toml

@dataclass
class ModelConfiguration:
    """Complex model configuration"""
    name: str
    version: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    validation_rules: List[Dict[str, Any]] = field(default_factory=list)
    transformation_pipeline: List[Dict[str, Any]] = field(default_factory=list)
    quality_gates: List[Dict[str, Any]] = field(default_factory=list)
    testing_strategies: List[Dict[str, Any]] = field(default_factory=list)

class ModelDrivenCodeGenerator(ABC):
    """Abstract base class for model-driven code generation"""

    def __init__(self, config: ModelConfiguration):
        self.config = config
        self.model_registry: Dict[str, Any] = {}
        self.generation_history: List[Dict[str, Any]] = []
        self.validation_results: Dict[str, Any] = {}
        self.quality_metrics: Dict[str, Any] = {}

    @abstractmethod
    def generate_code(self, model: Dict[str, Any]) -> str:
        """Generate code from model"""
        pass

    def validate_model(self, model: Dict[str, Any]) -> bool:
        """Validate model against configuration"""
        # Complex validation logic
        validation_passed = True
        for rule in self.config.validation_rules:
            if not self._apply_validation_rule(model, rule):
                validation_passed = False
                self.validation_results[rule['name']] = False

        return validation_passed

    def _apply_validation_rule(self, model: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Apply individual validation rule"""
        rule_type = rule.get('type', 'basic')
        if rule_type == 'required_fields':
            return all(field in model for field in rule.get('fields', []))
        elif rule_type == 'type_check':
            return self._check_field_types(model, rule.get('field_types', {}))
        elif rule_type == 'constraint_check':
            return self._check_constraints(model, rule.get('constraints', {}))
        return True

    def _check_field_types(self, model: Dict[str, Any], field_types: Dict[str, str]) -> bool:
        """Check field types in model"""
        for field, expected_type in field_types.items():
            if field in model:
                actual_type = type(model[field]).__name__
                if actual_type != expected_type:
                    return False
        return True

    def _check_constraints(self, model: Dict[str, Any], constraints: Dict[str, Any]) -> bool:
        """Check constraints in model"""
        for field, constraint in constraints.items():
            if field in model:
                value = model[field]
                if constraint.get('min') and value < constraint['min']:
                    return False
                if constraint.get('max') and value > constraint['max']:
                    return False
                if constraint.get('pattern') and not re.match(constraint['pattern'], str(value)):
                    return False
        return True

    def run_quality_gates(self, generated_code: str) -> Dict[str, Any]:
        """Run quality gates on generated code"""
        results = {}
        for gate in self.config.quality_gates:
            gate_name = gate['name']
            if gate['type'] == 'mypy':
                results[gate_name] = self._run_mypy_check(generated_code)
            elif gate['type'] == 'flake8':
                results[gate_name] = self._run_flake8_check(generated_code)
            elif gate['type'] == 'black':
                results[gate_name] = self._run_black_check(generated_code)
            elif gate['type'] == 'ast_complexity':
                results[gate_name] = self._check_ast_complexity(generated_code)

        return results

    def _run_mypy_check(self, code: str) -> Dict[str, Any]:
        """Run MyPy check on code"""
        # Complex MyPy integration
        return {"passed": True, "errors": [], "warnings": []}

    def _run_flake8_check(self, code: str) -> Dict[str, Any]:
        """Run Flake8 check on code"""
        # Complex Flake8 integration
        return {"passed": True, "errors": [], "warnings": []}

    def _run_black_check(self, code: str) -> Dict[str, Any]:
        """Run Black check on code"""
        # Complex Black integration
        return {"passed": True, "errors": [], "warnings": []}

    def _check_ast_complexity(self, code: str) -> Dict[str, Any]:
        """Check AST complexity of code"""
        try:
            tree = ast.parse(code)
            node_count = len(list(ast.walk(tree)))
            return {
                "passed": node_count < 1000,
                "node_count": node_count,
                "threshold": 1000
            }
        except Exception:
            return {"passed": False, "error": "Parse failed"}

class ComplexDataProcessor:
    """Complex data processor using model-driven approach"""

    def __init__(self, config: ModelConfiguration):
        self.config = config
        self.generator = ModelDrivenCodeGenerator(config)
        self.cache: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {}

    def process_data(self, data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
        """Process data using complex model-driven approach"""
        # Complex preprocessing with model validation
        preprocessed_data = self._preprocess_with_model(data)

        # Complex validation using model rules
        if not self._validate_with_model(preprocessed_data):
            raise ValueError("Data validation failed against model")

        # Complex processing with model-driven transformations
        processed_data = self._process_with_model(preprocessed_data)

        # Complex post-processing with quality gates
        final_data = self._postprocess_with_quality_gates(processed_data)

        # Update metrics
        self._update_metrics(final_data)

        return final_data

    def _preprocess_with_model(self, data: List[Any]) -> List[Any]:
        """Preprocess data using model rules"""
        # Complex preprocessing logic
        return [item for item in data if item is not None]

    def _validate_with_model(self, data: List[Any]) -> bool:
        """Validate data using model rules"""
        # Complex validation logic
        return len(data) > 0

    def _process_with_model(self, data: List[Any]) -> Dict[str, Any]:
        """Process data using model-driven approach"""
        # Complex processing logic
        result = {}
        for i, item in enumerate(data):
            if isinstance(item, str):
                result[str(i)] = len(item)
            elif isinstance(item, (int, float)):
                result[str(i)] = item * 2
            elif isinstance(item, bool):
                result[str(i)] = 1 if item else 0
        return result

    def _postprocess_with_quality_gates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess data with quality gates"""
        # Complex postprocessing logic
        return data

    def _update_metrics(self, data: Dict[str, Any]) -> None:
        """Update processing metrics"""
        # Complex metrics tracking
        self.metrics['processed_count'] = len(data)
        self.metrics['last_processed'] = "2024-01-01T00:00:00Z"'''


def generate_simple_functional() -> str:
    """Generate code using simple functional approach"""
    return '''from typing import Dict, List, Union

def process_data(data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
    """Process data using simple functional approach"""
    if not data:
        return {}

    result = {}
    for i, item in enumerate(data):
        if isinstance(item, str):
            result[str(i)] = len(item)
        elif isinstance(item, (int, float)):
            result[str(i)] = item * 2
        elif isinstance(item, bool):
            result[str(i)] = 1 if item else 0

    return result

def analyze_data(data: Dict[str, Union[int, float, str]]) -> Dict[str, Union[int, float, str]]:
    """Analyze data using simple approach"""
    if not data:
        return {"count": 0, "total": 0, "average": 0}

    numeric_values = [v for v in data.values() if isinstance(v, (int, float))]
    if not numeric_values:
        return {"count": 0, "total": 0, "average": 0}

    return {
        "count": len(numeric_values),
        "total": sum(numeric_values),
        "average": sum(numeric_values) / len(numeric_values)
    }

def validate_data(data: List[Any]) -> List[Any]:
    """Validate data using simple approach"""
    return [item for item in data if item is not None and str(item).strip() != ""]

def transform_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform data using simple approach"""
    return {k: v * 1.5 if isinstance(v, (int, float)) else str(v) for k, v in data.items()}

def generate_report(processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate report using simple approach"""
    return {
        "summary": f"Processed {processed} items with {errors} errors",
        "analysis": analysis,
        "timestamp": "2024-01-01T00:00:00Z",
        "status": "completed"
    }

def export_data(data: Dict[str, Any]) -> None:
    """Export data using simple approach"""
    print(f"Exported {len(data)} results")

# Simple workflow function
def run_simple_workflow(input_data: List[Any]) -> Dict[str, Any]:
    """Run simple workflow"""
    # Step 1: Validate
    validated = validate_data(input_data)

    # Step 2: Process
    processed = process_data(validated)

    # Step 3: Analyze
    analyzed = analyze_data(processed)

    # Step 4: Transform
    transformed = transform_data(processed)

    # Step 5: Report
    reported = generate_report(len(processed), len(input_data) - len(validated), analyzed)

    # Step 6: Export
    export_data(transformed)

    return {"data": transformed, "report": reported}'''


def generate_minimal_working() -> str:
    """Generate minimal working code that achieves the same goals"""
    return '''def process_data(data):
    """Minimal working data processor"""
    result = {}
    for i, item in enumerate(data):
        if item is not None:
            if isinstance(item, str):
                result[str(i)] = len(item)
            elif isinstance(item, (int, float)):
                result[str(i)] = item * 2
            elif isinstance(item, bool):
                result[str(i)] = 1 if item else 0
    return result

def analyze_data(data):
    """Minimal working data analyzer"""
    if not data:
        return {"count": 0, "total": 0, "average": 0}

    values = [v for v in data.values() if isinstance(v, (int, float))]
    if not values:
        return {"count": 0, "total": 0, "average": 0}

    return {
        "count": len(values),
        "total": sum(values),
        "average": sum(values) / len(values)
    }

def run_workflow(data):
    """Minimal working workflow"""
    processed = process_data(data)
    analyzed = analyze_data(processed)
    return {"data": processed, "analysis": analyzed}'''


def evaluate_approach(approach: Approach) -> dict[str, Any]:
    """Evaluate an approach using multiple criteria"""

    # Parse code
    ast_nodes = count_ast_nodes(approach.code)
    lines = len(approach.code.splitlines())
    characters = len(approach.code)

    # Test quality compliance
    mypy_errors = test_mypy_compliance(approach.code)
    black_passed = test_black_compliance(approach.code)
    flake8_errors = test_flake8_compliance(approach.code)

    # Calculate scores (0-100, higher is better)
    maintainability_score = max(0, 100 - (lines / 5))  # Fewer lines = better maintainability
    complexity_score = max(0, 100 - (ast_nodes / 20))  # Fewer AST nodes = better complexity
    quality_score = 100 - (len(mypy_errors) * 10) - (len(flake8_errors) * 5) - (0 if black_passed else 20)
    simplicity_score = max(0, 100 - (ast_nodes / 10))  # Fewer AST nodes = better simplicity

    # Overall score (weighted average)
    overall_score = maintainability_score * 0.3 + complexity_score * 0.3 + quality_score * 0.2 + simplicity_score * 0.2

    return {
        "name": approach.name,
        "lines": lines,
        "ast_nodes": ast_nodes,
        "characters": characters,
        "maintainability_score": maintainability_score,
        "complexity_score": complexity_score,
        "quality_score": quality_score,
        "simplicity_score": simplicity_score,
        "overall_score": overall_score,
        "mypy_errors": len(mypy_errors),
        "flake8_errors": len(flake8_errors),
        "black_passed": black_passed,
        "recommendations": approach.expected_benefits,
    }


def main():
    """Test if simple approaches can achieve the same goals"""
    print("🧪 Testing: Can Simple Approaches Achieve the Same Goals?")

    # Define our approaches
    approaches = [
        Approach(
            name="Complex Model-Driven",
            description="Our current complex model-driven approach with validation, quality gates, etc.",
            code=generate_complex_model_driven(),
            expected_benefits=[
                "Full validation",
                "Quality gates",
                "Extensible",
                "Enterprise-ready",
            ],
            expected_risks=[
                "Complexity",
                "Maintenance",
                "Learning curve",
                "Over-engineering",
            ],
        ),
        Approach(
            name="Simple Functional",
            description="Simple functional approach with clean interfaces",
            code=generate_simple_functional(),
            expected_benefits=[
                "Simple",
                "Maintainable",
                "Easy to understand",
                "Quick to implement",
            ],
            expected_risks=["Limited features", "Less extensible", "Manual testing"],
        ),
        Approach(
            name="Minimal Working",
            description="Minimal working code that achieves the same goals",
            code=generate_minimal_working(),
            expected_benefits=["Minimal", "Working", "Fast", "Simple"],
            expected_risks=["No validation", "No quality gates", "Limited features"],
        ),
    ]

    # Evaluate all approaches
    print("\n🔍 Evaluating approaches...")
    results = []
    for approach in approaches:
        result = evaluate_approach(approach)
        results.append(result)
        print(f"  {approach.name}: {result['overall_score']:.1f}/100")

    # Sort by overall score
    results.sort(key=lambda x: x["overall_score"], reverse=True)

    # Display detailed results
    print("\n" + "=" * 80)
    print("🏆 APPROACH EVALUATION RESULTS")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['name']}: {result['overall_score']:.1f}/100")
        print(f"   Lines: {result['lines']}, AST: {result['ast_nodes']}, Chars: {result['characters']}")
        print(f"   Maintainability: {result['maintainability_score']:.1f}/100")
        print(f"   Complexity: {result['complexity_score']:.1f}/100")
        print(f"   Quality: {result['quality_score']:.1f}/100")
        print(f"   Simplicity: {result['simplicity_score']:.1f}/100")
        print(f"   MyPy errors: {result['mypy_errors']}")
        print(f"   Flake8 errors: {result['flake8_errors']}")
        print(f"   Black passed: {result['black_passed']}")

    # Determine winner
    winner = results[0]
    print(f"\n🎯 WINNER: {winner['name']} ({winner['overall_score']:.1f}/100)")

    # Challenge our assumptions
    print(f"\n🤔 CHALLENGING OUR ASSUMPTIONS:")
    if winner["name"] == "Minimal Working":
        print("  🚨 MINIMAL WORKING CODE WINS!")
        print("  🚨 Our complex requirements are OVER-ENGINEERING!")
        print("  🚨 We should abandon model-driven complexity!")
    elif winner["name"] == "Simple Functional":
        print("  ⚠️ SIMPLE FUNCTIONAL APPROACH WINS!")
        print("  ⚠️ Our model-driven approach is TOO COMPLEX!")
        print("  ⚠️ We need to simplify our requirements!")
    else:
        print("  ✅ COMPLEX MODEL-DRIVEN APPROACH WINS!")
        print("  ✅ Our complexity is justified!")
        print("  ✅ We should keep our current approach!")

    # The real question
    print(f"\n🎯 THE REAL QUESTION:")
    print("  'Are we over-engineering our requirements when simple approaches work better?'")
    print("  'Should we abandon complex model-driven systems for simple, working code?'")
    print("  'Are our core requirements actually counterproductive?'")


if __name__ == "__main__":
    main()

"""Test if simple approaches can achieve the same goals as complex model-driven systems"""

import ast
import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Approach:
    """Represents a different approach to achieving our goals"""

    name: str
    description: str
    code: str
    expected_benefits: list[str]
    expected_risks: list[str]


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception:
        return 0


def test_mypy_compliance(code: str) -> list[str]:
    """Test if code passes MyPy validation"""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [
                "uv",
                "run",
                "mypy",
                "--show-error-codes",
                "--no-error-summary",
                temp_file,
            ],
            capture_output=True,
            text=True,
        )

        os.unlink(temp_file)

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"MyPy test failed: {e}"]


def test_black_compliance(code: str) -> bool:
    """Test if code passes Black formatting"""
    try:
        result = subprocess.run(
            ["uv", "run", "black", "--check", "-"],
            input=code,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def test_flake8_compliance(code: str) -> list[str]:
    """Test if code passes Flake8 validation"""
    try:
        result = subprocess.run(
            ["uv", "run", "flake8", "--select=F401,E302,E305,W291,W292", "-"],
            input=code,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return []
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Flake8 test failed: {e}"]


def generate_complex_model_driven() -> str:
    """Generate code using our current complex model-driven approach"""
    return '''from typing import Dict, List, Union, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import yaml
import toml

@dataclass
class ModelConfiguration:
    """Complex model configuration"""
    name: str
    version: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    validation_rules: List[Dict[str, Any]] = field(default_factory=list)
    transformation_pipeline: List[Dict[str, Any]] = field(default_factory=list)
    quality_gates: List[Dict[str, Any]] = field(default_factory=list)
    testing_strategies: List[Dict[str, Any]] = field(default_factory=list)

class ModelDrivenCodeGenerator(ABC):
    """Abstract base class for model-driven code generation"""

    def __init__(self, config: ModelConfiguration):
        self.config = config
        self.model_registry: Dict[str, Any] = {}
        self.generation_history: List[Dict[str, Any]] = []
        self.validation_results: Dict[str, Any] = {}
        self.quality_metrics: Dict[str, Any] = {}

    @abstractmethod
    def generate_code(self, model: Dict[str, Any]) -> str:
        """Generate code from model"""
        pass

    def validate_model(self, model: Dict[str, Any]) -> bool:
        """Validate model against configuration"""
        # Complex validation logic
        validation_passed = True
        for rule in self.config.validation_rules:
            if not self._apply_validation_rule(model, rule):
                validation_passed = False
                self.validation_results[rule['name']] = False

        return validation_passed

    def _apply_validation_rule(self, model: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Apply individual validation rule"""
        rule_type = rule.get('type', 'basic')
        if rule_type == 'required_fields':
            return all(field in model for field in rule.get('fields', []))
        elif rule_type == 'type_check':
            return self._check_field_types(model, rule.get('field_types', {}))
        elif rule_type == 'constraint_check':
            return self._check_constraints(model, rule.get('constraints', {}))
        return True

    def _check_field_types(self, model: Dict[str, Any], field_types: Dict[str, str]) -> bool:
        """Check field types in model"""
        for field, expected_type in field_types.items():
            if field in model:
                actual_type = type(model[field]).__name__
                if actual_type != expected_type:
                    return False
        return True

    def _check_constraints(self, model: Dict[str, Any], constraints: Dict[str, Any]) -> bool:
        """Check constraints in model"""
        for field, constraint in constraints.items():
            if field in model:
                value = model[field]
                if constraint.get('min') and value < constraint['min']:
                    return False
                if constraint.get('max') and value > constraint['max']:
                    return False
                if constraint.get('pattern') and not re.match(constraint['pattern'], str(value)):
                    return False
        return True

    def run_quality_gates(self, generated_code: str) -> Dict[str, Any]:
        """Run quality gates on generated code"""
        results = {}
        for gate in self.config.quality_gates:
            gate_name = gate['name']
            if gate['type'] == 'mypy':
                results[gate_name] = self._run_mypy_check(generated_code)
            elif gate['type'] == 'flake8':
                results[gate_name] = self._run_flake8_check(generated_code)
            elif gate['type'] == 'black':
                results[gate_name] = self._run_black_check(generated_code)
            elif gate['type'] == 'ast_complexity':
                results[gate_name] = self._check_ast_complexity(generated_code)

        return results

    def _run_mypy_check(self, code: str) -> Dict[str, Any]:
        """Run MyPy check on code"""
        # Complex MyPy integration
        return {"passed": True, "errors": [], "warnings": []}

    def _run_flake8_check(self, code: str) -> Dict[str, Any]:
        """Run Flake8 check on code"""
        # Complex Flake8 integration
        return {"passed": True, "errors": [], "warnings": []}

    def _run_black_check(self, code: str) -> Dict[str, Any]:
        """Run Black check on code"""
        # Complex Black integration
        return {"passed": True, "errors": [], "warnings": []}

    def _check_ast_complexity(self, code: str) -> Dict[str, Any]:
        """Check AST complexity of code"""
        try:
            tree = ast.parse(code)
            node_count = len(list(ast.walk(tree)))
            return {
                "passed": node_count < 1000,
                "node_count": node_count,
                "threshold": 1000
            }
        except Exception:
            return {"passed": False, "error": "Parse failed"}

class ComplexDataProcessor:
    """Complex data processor using model-driven approach"""

    def __init__(self, config: ModelConfiguration):
        self.config = config
        self.generator = ModelDrivenCodeGenerator(config)
        self.cache: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {}

    def process_data(self, data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
        """Process data using complex model-driven approach"""
        # Complex preprocessing with model validation
        preprocessed_data = self._preprocess_with_model(data)

        # Complex validation using model rules
        if not self._validate_with_model(preprocessed_data):
            raise ValueError("Data validation failed against model")

        # Complex processing with model-driven transformations
        processed_data = self._process_with_model(preprocessed_data)

        # Complex post-processing with quality gates
        final_data = self._postprocess_with_quality_gates(processed_data)

        # Update metrics
        self._update_metrics(final_data)

        return final_data

    def _preprocess_with_model(self, data: List[Any]) -> List[Any]:
        """Preprocess data using model rules"""
        # Complex preprocessing logic
        return [item for item in data if item is not None]

    def _validate_with_model(self, data: List[Any]) -> bool:
        """Validate data using model rules"""
        # Complex validation logic
        return len(data) > 0

    def _process_with_model(self, data: List[Any]) -> Dict[str, Any]:
        """Process data using model-driven approach"""
        # Complex processing logic
        result = {}
        for i, item in enumerate(data):
            if isinstance(item, str):
                result[str(i)] = len(item)
            elif isinstance(item, (int, float)):
                result[str(i)] = item * 2
            elif isinstance(item, bool):
                result[str(i)] = 1 if item else 0
        return result

    def _postprocess_with_quality_gates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess data with quality gates"""
        # Complex postprocessing logic
        return data

    def _update_metrics(self, data: Dict[str, Any]) -> None:
        """Update processing metrics"""
        # Complex metrics tracking
        self.metrics['processed_count'] = len(data)
        self.metrics['last_processed'] = "2024-01-01T00:00:00Z"'''


def generate_simple_functional() -> str:
    """Generate code using simple functional approach"""
    return '''from typing import Dict, List, Union

def process_data(data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
    """Process data using simple functional approach"""
    if not data:
        return {}

    result = {}
    for i, item in enumerate(data):
        if isinstance(item, str):
            result[str(i)] = len(item)
        elif isinstance(item, (int, float)):
            result[str(i)] = item * 2
        elif isinstance(item, bool):
            result[str(i)] = 1 if item else 0

    return result

def analyze_data(data: Dict[str, Union[int, float, str]]) -> Dict[str, Union[int, float, str]]:
    """Analyze data using simple approach"""
    if not data:
        return {"count": 0, "total": 0, "average": 0}

    numeric_values = [v for v in data.values() if isinstance(v, (int, float))]
    if not numeric_values:
        return {"count": 0, "total": 0, "average": 0}

    return {
        "count": len(numeric_values),
        "total": sum(numeric_values),
        "average": sum(numeric_values) / len(numeric_values)
    }

def validate_data(data: List[Any]) -> List[Any]:
    """Validate data using simple approach"""
    return [item for item in data if item is not None and str(item).strip() != ""]

def transform_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform data using simple approach"""
    return {k: v * 1.5 if isinstance(v, (int, float)) else str(v) for k, v in data.items()}

def generate_report(processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate report using simple approach"""
    return {
        "summary": f"Processed {processed} items with {errors} errors",
        "analysis": analysis,
        "timestamp": "2024-01-01T00:00:00Z",
        "status": "completed"
    }

def export_data(data: Dict[str, Any]) -> None:
    """Export data using simple approach"""
    print(f"Exported {len(data)} results")

# Simple workflow function
def run_simple_workflow(input_data: List[Any]) -> Dict[str, Any]:
    """Run simple workflow"""
    # Step 1: Validate
    validated = validate_data(input_data)

    # Step 2: Process
    processed = process_data(validated)

    # Step 3: Analyze
    analyzed = analyze_data(processed)

    # Step 4: Transform
    transformed = transform_data(processed)

    # Step 5: Report
    reported = generate_report(len(processed), len(input_data) - len(validated), analyzed)

    # Step 6: Export
    export_data(transformed)

    return {"data": transformed, "report": reported}'''


def generate_minimal_working() -> str:
    """Generate minimal working code that achieves the same goals"""
    return '''def process_data(data):
    """Minimal working data processor"""
    result = {}
    for i, item in enumerate(data):
        if item is not None:
            if isinstance(item, str):
                result[str(i)] = len(item)
            elif isinstance(item, (int, float)):
                result[str(i)] = item * 2
            elif isinstance(item, bool):
                result[str(i)] = 1 if item else 0
    return result

def analyze_data(data):
    """Minimal working data analyzer"""
    if not data:
        return {"count": 0, "total": 0, "average": 0}

    values = [v for v in data.values() if isinstance(v, (int, float))]
    if not values:
        return {"count": 0, "total": 0, "average": 0}

    return {
        "count": len(values),
        "total": sum(values),
        "average": sum(values) / len(values)
    }

def run_workflow(data):
    """Minimal working workflow"""
    processed = process_data(data)
    analyzed = analyze_data(processed)
    return {"data": processed, "analysis": analyzed}'''


def evaluate_approach(approach: Approach) -> dict[str, Any]:
    """Evaluate an approach using multiple criteria"""

    # Parse code
    ast_nodes = count_ast_nodes(approach.code)
    lines = len(approach.code.splitlines())
    characters = len(approach.code)

    # Test quality compliance
    mypy_errors = test_mypy_compliance(approach.code)
    black_passed = test_black_compliance(approach.code)
    flake8_errors = test_flake8_compliance(approach.code)

    # Calculate scores (0-100, higher is better)
    maintainability_score = max(0, 100 - (lines / 5))  # Fewer lines = better maintainability
    complexity_score = max(0, 100 - (ast_nodes / 20))  # Fewer AST nodes = better complexity
    quality_score = 100 - (len(mypy_errors) * 10) - (len(flake8_errors) * 5) - (0 if black_passed else 20)
    simplicity_score = max(0, 100 - (ast_nodes / 10))  # Fewer AST nodes = better simplicity

    # Overall score (weighted average)
    overall_score = maintainability_score * 0.3 + complexity_score * 0.3 + quality_score * 0.2 + simplicity_score * 0.2

    return {
        "name": approach.name,
        "lines": lines,
        "ast_nodes": ast_nodes,
        "characters": characters,
        "maintainability_score": maintainability_score,
        "complexity_score": complexity_score,
        "quality_score": quality_score,
        "simplicity_score": simplicity_score,
        "overall_score": overall_score,
        "mypy_errors": len(mypy_errors),
        "flake8_errors": len(flake8_errors),
        "black_passed": black_passed,
        "recommendations": approach.expected_benefits,
    }


def main():
    """Test if simple approaches can achieve the same goals"""
    print("🧪 Testing: Can Simple Approaches Achieve the Same Goals?")

    # Define our approaches
    approaches = [
        Approach(
            name="Complex Model-Driven",
            description="Our current complex model-driven approach with validation, quality gates, etc.",
            code=generate_complex_model_driven(),
            expected_benefits=[
                "Full validation",
                "Quality gates",
                "Extensible",
                "Enterprise-ready",
            ],
            expected_risks=[
                "Complexity",
                "Maintenance",
                "Learning curve",
                "Over-engineering",
            ],
        ),
        Approach(
            name="Simple Functional",
            description="Simple functional approach with clean interfaces",
            code=generate_simple_functional(),
            expected_benefits=[
                "Simple",
                "Maintainable",
                "Easy to understand",
                "Quick to implement",
            ],
            expected_risks=["Limited features", "Less extensible", "Manual testing"],
        ),
        Approach(
            name="Minimal Working",
            description="Minimal working code that achieves the same goals",
            code=generate_minimal_working(),
            expected_benefits=["Minimal", "Working", "Fast", "Simple"],
            expected_risks=["No validation", "No quality gates", "Limited features"],
        ),
    ]

    # Evaluate all approaches
    print("\n🔍 Evaluating approaches...")
    results = []
    for approach in approaches:
        result = evaluate_approach(approach)
        results.append(result)
        print(f"  {approach.name}: {result['overall_score']:.1f}/100")

    # Sort by overall score
    results.sort(key=lambda x: x["overall_score"], reverse=True)

    # Display detailed results
    print("\n" + "=" * 80)
    print("🏆 APPROACH EVALUATION RESULTS")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['name']}: {result['overall_score']:.1f}/100")
        print(f"   Lines: {result['lines']}, AST: {result['ast_nodes']}, Chars: {result['characters']}")
        print(f"   Maintainability: {result['maintainability_score']:.1f}/100")
        print(f"   Complexity: {result['complexity_score']:.1f}/100")
        print(f"   Quality: {result['quality_score']:.1f}/100")
        print(f"   Simplicity: {result['simplicity_score']:.1f}/100")
        print(f"   MyPy errors: {result['mypy_errors']}")
        print(f"   Flake8 errors: {result['flake8_errors']}")
        print(f"   Black passed: {result['black_passed']}")

    # Determine winner
    winner = results[0]
    print(f"\n🎯 WINNER: {winner['name']} ({winner['overall_score']:.1f}/100)")

    # Challenge our assumptions
    print(f"\n🤔 CHALLENGING OUR ASSUMPTIONS:")
    if winner["name"] == "Minimal Working":
        print("  🚨 MINIMAL WORKING CODE WINS!")
        print("  🚨 Our complex requirements are OVER-ENGINEERING!")
        print("  🚨 We should abandon model-driven complexity!")
    elif winner["name"] == "Simple Functional":
        print("  ⚠️ SIMPLE FUNCTIONAL APPROACH WINS!")
        print("  ⚠️ Our model-driven approach is TOO COMPLEX!")
        print("  ⚠️ We need to simplify our requirements!")
    else:
        print("  ✅ COMPLEX MODEL-DRIVEN APPROACH WINS!")
        print("  ✅ Our complexity is justified!")
        print("  ✅ We should keep our current approach!")

    # The real question
    print(f"\n🎯 THE REAL QUESTION:")
    print("  'Are we over-engineering our requirements when simple approaches work better?'")
    print("  'Should we abandon complex model-driven systems for simple, working code?'")
    print("  'Are our core requirements actually counterproductive?'")


if __name__ == "__main__":
    main()
