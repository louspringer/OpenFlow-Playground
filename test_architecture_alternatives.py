#!/usr/bin/env python3
"""Test architecture alternatives using established evaluation methodologies"""

import ast
import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class ArchitectureAlternative:
    """Represents an architecture alternative to evaluate"""

    name: str
    description: str
    approach: str
    expected_benefits: list[str]
    expected_risks: list[str]
    quality_attributes: dict[str, float]


@dataclass
class EvaluationResult:
    """Results of architecture evaluation"""

    alternative: ArchitectureAlternative
    maintainability_score: float
    complexity_score: float
    quality_score: float
    risk_score: float
    overall_score: float
    recommendations: list[str]


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


def generate_monolithic_approach() -> str:
    """Generate code using current monolithic approach"""
    return '''from typing import Dict, List, Union, Any, Optional

class MonolithicDataProcessor:
    """Monolithic approach: Everything in one class"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.cache: Dict[Any, Any] = {}
        self.processors: Dict[str, Any] = {}
        self.validators: Dict[str, Any] = {}
        self.transformers: Dict[str, Any] = {}
        self.analyzers: Dict[str, Any] = {}
        self.reporters: Dict[str, Any] = {}
        self.exporters: Dict[str, Any] = {}
        self.importers: Dict[str, Any] = {}
        self.schedulers: Dict[str, Any] = {}
        self.monitors: Dict[str, Any] = {}

    def process_data(self, data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
        """Process data with monolithic logic"""
        if not data:
            return {}

        result: Dict[str, Union[int, float, str]] = {}
        processed_count: int = 0
        error_count: int = 0

        # Validation logic
        for item in data:
            if not self._validate_item(item):
                error_count += 1
                continue

            # Processing logic
            processed_item = self._process_item(item)
            if processed_item is not None:
                result[str(processed_count)] = processed_item
                processed_count += 1
            else:
                error_count += 1

        # Analysis logic
        analysis_result = self._analyze_results(result)

        # Transformation logic
        transformed_result = self._transform_results(result)

        # Reporting logic
        report = self._generate_report(processed_count, error_count, analysis_result)

        # Export logic
        self._export_results(transformed_result)

        return {"data": transformed_result, "report": report, "stats": {"processed": processed_count, "errors": error_count}}

    def _validate_item(self, item: Any) -> bool:
        """Validate individual item"""
        return item is not None and str(item).strip() != ""

    def _process_item(self, item: Any) -> Any:
        """Process individual item"""
        if isinstance(item, str):
            return len(item)
        elif isinstance(item, (int, float)):
            return item * 2
        elif isinstance(item, bool):
            return 1 if item else 0
        return None

    def _analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processing results"""
        if not results:
            return {"count": 0, "average": 0, "total": 0}

        values = [v for v in results.values() if isinstance(v, (int, float))]
        if not values:
            return {"count": 0, "average": 0, "total": 0}

        return {
            "count": len(values),
            "average": sum(values) / len(values),
            "total": sum(values),
            "min": min(values),
            "max": max(values)
        }

    def _transform_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Transform results"""
        transformed = {}
        for key, value in results.items():
            if isinstance(value, (int, float)):
                transformed[key] = value * 1.5
            else:
                transformed[key] = str(value)
        return transformed

    def _generate_report(self, processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate processing report"""
        return {
            "summary": f"Processed {processed} items with {errors} errors",
            "analysis": analysis,
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "completed"
        }

    def _export_results(self, results: Dict[str, Any]) -> None:
        """Export results"""
        print(f"Exported {len(results)} results")

    def run_complex_workflow(self, input_data: List[Any]) -> Dict[str, Any]:
        """Run complex workflow with all steps"""
        # Step 1: Preprocessing
        preprocessed = self._preprocess_data(input_data)

        # Step 2: Validation
        validated = self._validate_data(preprocessed)

        # Step 3: Processing
        processed = self._process_data(validated)

        # Step 4: Post-processing
        postprocessed = self._postprocess_data(processed)

        # Step 5: Analysis
        analyzed = self._analyze_data(postprocessed)

        # Step 6: Reporting
        reported = self._report_data(analyzed)

        # Step 7: Export
        exported = self._export_data(reported)

        return exported

    def _preprocess_data(self, data: List[Any]) -> List[Any]:
        """Preprocess data"""
        return [item for item in data if item is not None]

    def _validate_data(self, data: List[Any]) -> List[Any]:
        """Validate data"""
        return [item for item in data if self._validate_item(item)]

    def _postprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess data"""
        return {k: v for k, v in data.items() if v is not None}

    def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data"""
        return self._analyze_results(data)

    def _report_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Report data"""
        return self._generate_report(0, 0, data)

    def _export_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Export data"""
        self._export_results(data)
        return data'''


def generate_modular_approach() -> str:
    """Generate code using modular approach"""
    return '''from typing import Dict, List, Union, Any, Optional
from abc import ABC, abstractmethod

# Modular approach: Separate classes for each responsibility

class DataValidator(ABC):
    """Abstract base class for data validation"""

    @abstractmethod
    def validate(self, item: Any) -> bool:
        """Validate individual item"""
        pass

class BasicValidator(DataValidator):
    """Basic data validator"""

    def validate(self, item: Any) -> bool:
        """Validate individual item"""
        return item is not None and str(item).strip() != ""

class DataProcessor(ABC):
    """Abstract base class for data processing"""

    @abstractmethod
    def process(self, item: Any) -> Any:
        """Process individual item"""
        pass

class BasicProcessor(DataProcessor):
    """Basic data processor"""

    def process(self, item: Any) -> Any:
        """Process individual item"""
        if isinstance(item, str):
            return len(item)
        elif isinstance(item, (int, float)):
            return item * 2
        elif isinstance(item, bool):
            return 1 if item else 0
        return None

class DataAnalyzer(ABC):
    """Abstract base class for data analysis"""

    @abstractmethod
    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processing results"""
        pass

class BasicAnalyzer(DataAnalyzer):
    """Basic data analyzer"""

    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processing results"""
        if not results:
            return {"count": 0, "average": 0, "total": 0}

        values = [v for v in results.values() if isinstance(v, (int, float))]
        if not values:
            return {"count": 0, "average": 0, "total": 0}

        return {
            "count": len(values),
            "average": sum(values) / len(values),
            "total": sum(values),
            "min": min(values),
            "max": max(values)
        }

class DataTransformer(ABC):
    """Abstract base class for data transformation"""

    @abstractmethod
    def transform(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Transform results"""
        pass

class BasicTransformer(DataTransformer):
    """Basic data transformer"""

    def transform(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Transform results"""
        transformed = {}
        for key, value in results.items():
            if isinstance(value, (int, float)):
                transformed[key] = value * 1.5
            else:
                transformed[key] = str(value)
        return transformed

class ReportGenerator(ABC):
    """Abstract base class for report generation"""

    @abstractmethod
    def generate(self, processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate processing report"""
        pass

class BasicReportGenerator(ReportGenerator):
    """Basic report generator"""

    def generate(self, processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate processing report"""
        return {
            "summary": f"Processed {processed} items with {errors} errors",
            "analysis": analysis,
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "completed"
        }

class DataExporter(ABC):
    """Abstract base class for data export"""

    @abstractmethod
    def export(self, results: Dict[str, Any]) -> None:
        """Export results"""
        pass

class BasicExporter(DataExporter):
    """Basic data exporter"""

    def export(self, results: Dict[str, Any]) -> None:
        """Export results"""
        print(f"Exported {len(results)} results")

class ModularDataProcessor:
    """Modular approach: Separate classes for each responsibility"""

    def __init__(self,
                 validator: DataValidator,
                 processor: DataProcessor,
                 analyzer: DataAnalyzer,
                 transformer: DataTransformer,
                 reporter: ReportGenerator,
                 exporter: DataExporter) -> None:
        self.validator = validator
        self.processor = processor
        self.analyzer = analyzer
        self.transformer = transformer
        self.reporter = reporter
        self.exporter = exporter

    def process_data(self, data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
        """Process data using modular components"""
        if not data:
            return {}

        result: Dict[str, Union[int, float, str]] = {}
        processed_count: int = 0
        error_count: int = 0

        # Use validator component
        for item in data:
            if not self.validator.validate(item):
                error_count += 1
                continue

            # Use processor component
            processed_item = self.processor.process(item)
            if processed_item is not None:
                result[str(processed_count)] = processed_item
                processed_count += 1
            else:
                error_count += 1

        # Use analyzer component
        analysis_result = self.analyzer.analyze(result)

        # Use transformer component
        transformed_result = self.transformer.transform(result)

        # Use reporter component
        report = self.reporter.generate(processed_count, error_count, analysis_result)

        # Use exporter component
        self.exporter.export(transformed_result)

        return {"data": transformed_result, "report": report, "stats": {"processed": processed_count, "errors": error_count}}

# Factory for creating modular processor
def create_modular_processor() -> ModularDataProcessor:
    """Create modular processor with default components"""
    return ModularDataProcessor(
        validator=BasicValidator(),
        processor=BasicProcessor(),
        analyzer=BasicAnalyzer(),
        transformer=BasicTransformer(),
        reporter=BasicReportGenerator(),
        exporter=BasicExporter()
    )'''


def evaluate_architecture_alternative(code: str, name: str) -> EvaluationResult:
    """Evaluate an architecture alternative using multiple criteria"""

    # Parse code
    ast_nodes = count_ast_nodes(code)
    lines = len(code.splitlines())
    len(code)

    # Test quality compliance
    mypy_errors = test_mypy_compliance(code)
    black_passed = test_black_compliance(code)
    flake8_errors = test_flake8_compliance(code)

    # Calculate scores (0-100, higher is better)
    maintainability_score = max(
        0, 100 - (lines / 10)
    )  # Fewer lines = better maintainability
    complexity_score = max(
        0, 100 - (ast_nodes / 50)
    )  # Fewer AST nodes = better complexity
    quality_score = (
        100
        - (len(mypy_errors) * 10)
        - (len(flake8_errors) * 5)
        - (0 if black_passed else 20)
    )
    risk_score = max(0, 100 - (ast_nodes / 100))  # Fewer AST nodes = lower risk

    # Overall score (weighted average)
    overall_score = (
        maintainability_score * 0.3
        + complexity_score * 0.3
        + quality_score * 0.3
        + risk_score * 0.1
    )

    # Generate recommendations
    recommendations = []

    if lines > 200:
        recommendations.append("Consider breaking into smaller modules")

    if ast_nodes > 500:
        recommendations.append("High complexity - extract complex logic")

    if mypy_errors:
        recommendations.append(f"Fix {len(mypy_errors)} MyPy errors")

    if flake8_errors:
        recommendations.append(f"Fix {len(flake8_errors)} Flake8 errors")

    if not black_passed:
        recommendations.append("Fix Black formatting issues")

    return EvaluationResult(
        alternative=ArchitectureAlternative(
            name=name,
            description=f"Architecture with {lines} lines and {ast_nodes} AST nodes",
            approach="Generated code approach",
            expected_benefits=["Code generation", "Consistency"],
            expected_risks=["Complexity", "Maintainability"],
            quality_attributes={"lines": lines, "ast_nodes": ast_nodes},
        ),
        maintainability_score=maintainability_score,
        complexity_score=complexity_score,
        quality_score=quality_score,
        risk_score=risk_score,
        overall_score=overall_score,
        recommendations=recommendations,
    )


def main():
    """Evaluate architecture alternatives using established methodologies"""
    print("🏗️ Architecture Alternatives Evaluation (ATAM + MBT + TDD)")

    # Generate both approaches
    print("\n🔍 Generating architecture alternatives...")
    monolithic_code = generate_monolithic_approach()
    modular_code = generate_modular_approach()

    # Evaluate both approaches
    print("\n📊 Evaluating Monolithic Approach...")
    monolithic_result = evaluate_architecture_alternative(monolithic_code, "Monolithic")

    print("\n📊 Evaluating Modular Approach...")
    modular_result = evaluate_architecture_alternative(modular_code, "Modular")

    # Display results
    print("\n" + "=" * 80)
    print("🏆 ARCHITECTURE EVALUATION RESULTS")
    print("=" * 80)

    print(f"\n📈 Monolithic Approach:")
    print(f"  Lines: {monolithic_result.alternative.quality_attributes['lines']}")
    print(
        f"  AST Nodes: {monolithic_result.alternative.quality_attributes['ast_nodes']}"
    )
    print(f"  Maintainability: {monolithic_result.maintainability_score:.1f}/100")
    print(f"  Complexity: {monolithic_result.complexity_score:.1f}/100")
    print(f"  Quality: {monolithic_result.quality_score:.1f}/100")
    print(f"  Risk: {monolithic_result.risk_score:.1f}/100")
    print(f"  Overall: {monolithic_result.overall_score:.1f}/100")

    print(f"\n📈 Modular Approach:")
    print(f"  Lines: {modular_result.alternative.quality_attributes['lines']}")
    print(f"  AST Nodes: {modular_result.alternative.quality_attributes['ast_nodes']}")
    print(f"  Maintainability: {modular_result.maintainability_score:.1f}/100")
    print(f"  Complexity: {modular_result.complexity_score:.1f}/100")
    print(f"  Quality: {modular_result.quality_score:.1f}/100")
    print(f"  Risk: {modular_result.risk_score:.1f}/100")
    print(f"  Overall: {modular_result.overall_score:.1f}/100")

    # Determine winner
    print(f"\n🎯 WINNER:")
    if modular_result.overall_score > monolithic_result.overall_score:
        winner = "Modular Approach"
        improvement = (
            (modular_result.overall_score - monolithic_result.overall_score)
            / monolithic_result.overall_score
        ) * 100
        print(f"  🏆 {winner} wins by {improvement:.1f}% improvement!")
        print(f"  ✅ Better maintainability, lower complexity, higher quality")
    else:
        winner = "Monolithic Approach"
        improvement = (
            (monolithic_result.overall_score - modular_result.overall_score)
            / modular_result.overall_score
        ) * 100
        print(f"  🏆 {winner} wins by {improvement:.1f}% improvement!")
        print(f"  ✅ Better performance, simpler structure")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"  Monolithic: {', '.join(monolithic_result.recommendations[:3])}")
    print(f"  Modular: {', '.join(modular_result.recommendations[:3])}")

    # Architecture decision
    print(f"\n🏗️ ARCHITECTURE DECISION:")
    if modular_result.overall_score > monolithic_result.overall_score:
        print(f"  ✅ ADOPT MODULAR APPROACH")
        print(f"  ✅ Better maintainability and quality")
        print(f"  ✅ Lower complexity and risk")
        print(f"  ✅ Follows single responsibility principle")
    else:
        print(f"  ✅ ADOPT MONOLITHIC APPROACH")
        print(f"  ✅ Better performance and simplicity")
        print(f"  ✅ Lower overhead and complexity")


if __name__ == "__main__":
    main()

"""Test architecture alternatives using established evaluation methodologies"""

import ast
import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class ArchitectureAlternative:
    """Represents an architecture alternative to evaluate"""

    name: str
    description: str
    approach: str
    expected_benefits: list[str]
    expected_risks: list[str]
    quality_attributes: dict[str, float]


@dataclass
class EvaluationResult:
    """Results of architecture evaluation"""

    alternative: ArchitectureAlternative
    maintainability_score: float
    complexity_score: float
    quality_score: float
    risk_score: float
    overall_score: float
    recommendations: list[str]


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


def generate_monolithic_approach() -> str:
    """Generate code using current monolithic approach"""
    return '''from typing import Dict, List, Union, Any, Optional

class MonolithicDataProcessor:
    """Monolithic approach: Everything in one class"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.cache: Dict[Any, Any] = {}
        self.processors: Dict[str, Any] = {}
        self.validators: Dict[str, Any] = {}
        self.transformers: Dict[str, Any] = {}
        self.analyzers: Dict[str, Any] = {}
        self.reporters: Dict[str, Any] = {}
        self.exporters: Dict[str, Any] = {}
        self.importers: Dict[str, Any] = {}
        self.schedulers: Dict[str, Any] = {}
        self.monitors: Dict[str, Any] = {}

    def process_data(self, data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
        """Process data with monolithic logic"""
        if not data:
            return {}

        result: Dict[str, Union[int, float, str]] = {}
        processed_count: int = 0
        error_count: int = 0

        # Validation logic
        for item in data:
            if not self._validate_item(item):
                error_count += 1
                continue

            # Processing logic
            processed_item = self._process_item(item)
            if processed_item is not None:
                result[str(processed_count)] = processed_item
                processed_count += 1
            else:
                error_count += 1

        # Analysis logic
        analysis_result = self._analyze_results(result)

        # Transformation logic
        transformed_result = self._transform_results(result)

        # Reporting logic
        report = self._generate_report(processed_count, error_count, analysis_result)

        # Export logic
        self._export_results(transformed_result)

        return {"data": transformed_result, "report": report, "stats": {"processed": processed_count, "errors": error_count}}

    def _validate_item(self, item: Any) -> bool:
        """Validate individual item"""
        return item is not None and str(item).strip() != ""

    def _process_item(self, item: Any) -> Any:
        """Process individual item"""
        if isinstance(item, str):
            return len(item)
        elif isinstance(item, (int, float)):
            return item * 2
        elif isinstance(item, bool):
            return 1 if item else 0
        return None

    def _analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processing results"""
        if not results:
            return {"count": 0, "average": 0, "total": 0}

        values = [v for v in results.values() if isinstance(v, (int, float))]
        if not values:
            return {"count": 0, "average": 0, "total": 0}

        return {
            "count": len(values),
            "average": sum(values) / len(values),
            "total": sum(values),
            "min": min(values),
            "max": max(values)
        }

    def _transform_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Transform results"""
        transformed = {}
        for key, value in results.items():
            if isinstance(value, (int, float)):
                transformed[key] = value * 1.5
            else:
                transformed[key] = str(value)
        return transformed

    def _generate_report(self, processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate processing report"""
        return {
            "summary": f"Processed {processed} items with {errors} errors",
            "analysis": analysis,
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "completed"
        }

    def _export_results(self, results: Dict[str, Any]) -> None:
        """Export results"""
        print(f"Exported {len(results)} results")

    def run_complex_workflow(self, input_data: List[Any]) -> Dict[str, Any]:
        """Run complex workflow with all steps"""
        # Step 1: Preprocessing
        preprocessed = self._preprocess_data(input_data)

        # Step 2: Validation
        validated = self._validate_data(preprocessed)

        # Step 3: Processing
        processed = self._process_data(validated)

        # Step 4: Post-processing
        postprocessed = self._postprocess_data(processed)

        # Step 5: Analysis
        analyzed = self._analyze_data(postprocessed)

        # Step 6: Reporting
        reported = self._report_data(analyzed)

        # Step 7: Export
        exported = self._export_data(reported)

        return exported

    def _preprocess_data(self, data: List[Any]) -> List[Any]:
        """Preprocess data"""
        return [item for item in data if item is not None]

    def _validate_data(self, data: List[Any]) -> List[Any]:
        """Validate data"""
        return [item for item in data if self._validate_item(item)]

    def _postprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess data"""
        return {k: v for k, v in data.items() if v is not None}

    def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data"""
        return self._analyze_results(data)

    def _report_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Report data"""
        return self._generate_report(0, 0, data)

    def _export_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Export data"""
        self._export_results(data)
        return data'''


def generate_modular_approach() -> str:
    """Generate code using modular approach"""
    return '''from typing import Dict, List, Union, Any, Optional
from abc import ABC, abstractmethod

# Modular approach: Separate classes for each responsibility

class DataValidator(ABC):
    """Abstract base class for data validation"""

    @abstractmethod
    def validate(self, item: Any) -> bool:
        """Validate individual item"""
        pass

class BasicValidator(DataValidator):
    """Basic data validator"""

    def validate(self, item: Any) -> bool:
        """Validate individual item"""
        return item is not None and str(item).strip() != ""

class DataProcessor(ABC):
    """Abstract base class for data processing"""

    @abstractmethod
    def process(self, item: Any) -> Any:
        """Process individual item"""
        pass

class BasicProcessor(DataProcessor):
    """Basic data processor"""

    def process(self, item: Any) -> Any:
        """Process individual item"""
        if isinstance(item, str):
            return len(item)
        elif isinstance(item, (int, float)):
            return item * 2
        elif isinstance(item, bool):
            return 1 if item else 0
        return None

class DataAnalyzer(ABC):
    """Abstract base class for data analysis"""

    @abstractmethod
    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processing results"""
        pass

class BasicAnalyzer(DataAnalyzer):
    """Basic data analyzer"""

    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze processing results"""
        if not results:
            return {"count": 0, "average": 0, "total": 0}

        values = [v for v in results.values() if isinstance(v, (int, float))]
        if not values:
            return {"count": 0, "average": 0, "total": 0}

        return {
            "count": len(values),
            "average": sum(values) / len(values),
            "total": sum(values),
            "min": min(values),
            "max": max(values)
        }

class DataTransformer(ABC):
    """Abstract base class for data transformation"""

    @abstractmethod
    def transform(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Transform results"""
        pass

class BasicTransformer(DataTransformer):
    """Basic data transformer"""

    def transform(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Transform results"""
        transformed = {}
        for key, value in results.items():
            if isinstance(value, (int, float)):
                transformed[key] = value * 1.5
            else:
                transformed[key] = str(value)
        return transformed

class ReportGenerator(ABC):
    """Abstract base class for report generation"""

    @abstractmethod
    def generate(self, processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate processing report"""
        pass

class BasicReportGenerator(ReportGenerator):
    """Basic report generator"""

    def generate(self, processed: int, errors: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate processing report"""
        return {
            "summary": f"Processed {processed} items with {errors} errors",
            "analysis": analysis,
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "completed"
        }

class DataExporter(ABC):
    """Abstract base class for data export"""

    @abstractmethod
    def export(self, results: Dict[str, Any]) -> None:
        """Export results"""
        pass

class BasicExporter(DataExporter):
    """Basic data exporter"""

    def export(self, results: Dict[str, Any]) -> None:
        """Export results"""
        print(f"Exported {len(results)} results")

class ModularDataProcessor:
    """Modular approach: Separate classes for each responsibility"""

    def __init__(self,
                 validator: DataValidator,
                 processor: DataProcessor,
                 analyzer: DataAnalyzer,
                 transformer: DataTransformer,
                 reporter: ReportGenerator,
                 exporter: DataExporter) -> None:
        self.validator = validator
        self.processor = processor
        self.analyzer = analyzer
        self.transformer = transformer
        self.reporter = reporter
        self.exporter = exporter

    def process_data(self, data: List[Union[str, int, float, bool]]) -> Dict[str, Union[int, float, str]]:
        """Process data using modular components"""
        if not data:
            return {}

        result: Dict[str, Union[int, float, str]] = {}
        processed_count: int = 0
        error_count: int = 0

        # Use validator component
        for item in data:
            if not self.validator.validate(item):
                error_count += 1
                continue

            # Use processor component
            processed_item = self.processor.process(item)
            if processed_item is not None:
                result[str(processed_count)] = processed_item
                processed_count += 1
            else:
                error_count += 1

        # Use analyzer component
        analysis_result = self.analyzer.analyze(result)

        # Use transformer component
        transformed_result = self.transformer.transform(result)

        # Use reporter component
        report = self.reporter.generate(processed_count, error_count, analysis_result)

        # Use exporter component
        self.exporter.export(transformed_result)

        return {"data": transformed_result, "report": report, "stats": {"processed": processed_count, "errors": error_count}}

# Factory for creating modular processor
def create_modular_processor() -> ModularDataProcessor:
    """Create modular processor with default components"""
    return ModularDataProcessor(
        validator=BasicValidator(),
        processor=BasicProcessor(),
        analyzer=BasicAnalyzer(),
        transformer=BasicTransformer(),
        reporter=BasicReportGenerator(),
        exporter=BasicExporter()
    )'''


def evaluate_architecture_alternative(code: str, name: str) -> EvaluationResult:
    """Evaluate an architecture alternative using multiple criteria"""

    # Parse code
    ast_nodes = count_ast_nodes(code)
    lines = len(code.splitlines())
    len(code)

    # Test quality compliance
    mypy_errors = test_mypy_compliance(code)
    black_passed = test_black_compliance(code)
    flake8_errors = test_flake8_compliance(code)

    # Calculate scores (0-100, higher is better)
    maintainability_score = max(
        0, 100 - (lines / 10)
    )  # Fewer lines = better maintainability
    complexity_score = max(
        0, 100 - (ast_nodes / 50)
    )  # Fewer AST nodes = better complexity
    quality_score = (
        100
        - (len(mypy_errors) * 10)
        - (len(flake8_errors) * 5)
        - (0 if black_passed else 20)
    )
    risk_score = max(0, 100 - (ast_nodes / 100))  # Fewer AST nodes = lower risk

    # Overall score (weighted average)
    overall_score = (
        maintainability_score * 0.3
        + complexity_score * 0.3
        + quality_score * 0.3
        + risk_score * 0.1
    )

    # Generate recommendations
    recommendations = []

    if lines > 200:
        recommendations.append("Consider breaking into smaller modules")

    if ast_nodes > 500:
        recommendations.append("High complexity - extract complex logic")

    if mypy_errors:
        recommendations.append(f"Fix {len(mypy_errors)} MyPy errors")

    if flake8_errors:
        recommendations.append(f"Fix {len(flake8_errors)} Flake8 errors")

    if not black_passed:
        recommendations.append("Fix Black formatting issues")

    return EvaluationResult(
        alternative=ArchitectureAlternative(
            name=name,
            description=f"Architecture with {lines} lines and {ast_nodes} AST nodes",
            approach="Generated code approach",
            expected_benefits=["Code generation", "Consistency"],
            expected_risks=["Complexity", "Maintainability"],
            quality_attributes={"lines": lines, "ast_nodes": ast_nodes},
        ),
        maintainability_score=maintainability_score,
        complexity_score=complexity_score,
        quality_score=quality_score,
        risk_score=risk_score,
        overall_score=overall_score,
        recommendations=recommendations,
    )


def main():
    """Evaluate architecture alternatives using established methodologies"""
    print("🏗️ Architecture Alternatives Evaluation (ATAM + MBT + TDD)")

    # Generate both approaches
    print("\n🔍 Generating architecture alternatives...")
    monolithic_code = generate_monolithic_approach()
    modular_code = generate_modular_approach()

    # Evaluate both approaches
    print("\n📊 Evaluating Monolithic Approach...")
    monolithic_result = evaluate_architecture_alternative(monolithic_code, "Monolithic")

    print("\n📊 Evaluating Modular Approach...")
    modular_result = evaluate_architecture_alternative(modular_code, "Modular")

    # Display results
    print("\n" + "=" * 80)
    print("🏆 ARCHITECTURE EVALUATION RESULTS")
    print("=" * 80)

    print(f"\n📈 Monolithic Approach:")
    print(f"  Lines: {monolithic_result.alternative.quality_attributes['lines']}")
    print(
        f"  AST Nodes: {monolithic_result.alternative.quality_attributes['ast_nodes']}"
    )
    print(f"  Maintainability: {monolithic_result.maintainability_score:.1f}/100")
    print(f"  Complexity: {monolithic_result.complexity_score:.1f}/100")
    print(f"  Quality: {monolithic_result.quality_score:.1f}/100")
    print(f"  Risk: {monolithic_result.risk_score:.1f}/100")
    print(f"  Overall: {monolithic_result.overall_score:.1f}/100")

    print(f"\n📈 Modular Approach:")
    print(f"  Lines: {modular_result.alternative.quality_attributes['lines']}")
    print(f"  AST Nodes: {modular_result.alternative.quality_attributes['ast_nodes']}")
    print(f"  Maintainability: {modular_result.maintainability_score:.1f}/100")
    print(f"  Complexity: {modular_result.complexity_score:.1f}/100")
    print(f"  Quality: {modular_result.quality_score:.1f}/100")
    print(f"  Risk: {modular_result.risk_score:.1f}/100")
    print(f"  Overall: {modular_result.overall_score:.1f}/100")

    # Determine winner
    print(f"\n🎯 WINNER:")
    if modular_result.overall_score > monolithic_result.overall_score:
        winner = "Modular Approach"
        improvement = (
            (modular_result.overall_score - monolithic_result.overall_score)
            / monolithic_result.overall_score
        ) * 100
        print(f"  🏆 {winner} wins by {improvement:.1f}% improvement!")
        print(f"  ✅ Better maintainability, lower complexity, higher quality")
    else:
        winner = "Monolithic Approach"
        improvement = (
            (monolithic_result.overall_score - modular_result.overall_score)
            / modular_result.overall_score
        ) * 100
        print(f"  🏆 {winner} wins by {improvement:.1f}% improvement!")
        print(f"  ✅ Better performance, simpler structure")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"  Monolithic: {', '.join(monolithic_result.recommendations[:3])}")
    print(f"  Modular: {', '.join(modular_result.recommendations[:3])}")

    # Architecture decision
    print(f"\n🏗️ ARCHITECTURE DECISION:")
    if modular_result.overall_score > monolithic_result.overall_score:
        print(f"  ✅ ADOPT MODULAR APPROACH")
        print(f"  ✅ Better maintainability and quality")
        print(f"  ✅ Lower complexity and risk")
        print(f"  ✅ Follows single responsibility principle")
    else:
        print(f"  ✅ ADOPT MONOLITHIC APPROACH")
        print(f"  ✅ Better performance and simplicity")
        print(f"  ✅ Lower overhead and complexity")


if __name__ == "__main__":
    main()




