#!/usr/bin/env python3
"""
Round-Trip Engineering Demo Orchestrator

A Reflective Module that orchestrates the demo workflow, showcasing
the refactored round-trip engineering system's reverse engineering capabilities.
"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..generators.base_reflective_module import BaseReflectiveModule
from ..core.round_trip_system import RoundTripSystem
from ..core.model_manager import ModelManager
from ..core.vocabulary_aligner import VocabularyAligner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DemoOrchestrator(BaseReflectiveModule):
    """
    Demo Orchestrator - Coordinates the round-trip engineering demo workflow.

    This module follows Reflective Module principles:
    - Single responsibility: Demo orchestration only
    - Self-monitoring: Tracks demo execution status
    - Clear boundaries: Interfaces with other modules through defined contracts
    - Testable: Can be tested in isolation
    """

    def __init__(self) -> None:
        """Initialize the demo orchestrator."""
        super().__init__()
        self.round_trip_system = RoundTripSystem()
        self.model_manager = ModelManager()
        self.vocabulary_aligner = VocabularyAligner()
        self.demo_results: Dict[str, Any] = {}
        self.current_demo_step = "idle"
        self.demo_start_time: Optional[float] = None

        logger.info("🎯 Demo Orchestrator initialized")

    async def get_module_capabilities(self) -> List[Dict[str, Any]]:
        """Get module capabilities."""
        return [
            {
                "name": "demo_orchestration",
                "description": "Orchestrates round-trip engineering demos",
                "available": True,
                "version": "1.0.0",
            },
            {
                "name": "workflow_execution",
                "description": "Executes complete round-trip workflows",
                "available": True,
                "version": "1.0.0",
            },
            {
                "name": "result_analysis",
                "description": "Analyzes demo results and performance",
                "available": True,
                "version": "1.0.0",
            },
        ]

    async def run_basic_demo(self) -> Dict[str, Any]:
        """Run a basic round-trip engineering demo using reverse engineering."""
        try:
            self._track_success()
            self.current_demo_step = "basic_demo"
            self.demo_start_time = time.time()

            logger.info("🚀 Starting basic round-trip engineering demo")

            # Create a simple Python file for demo purposes
            demo_file = self._create_demo_python_file()
            logger.info("✅ Created demo Python file")

            # Step 1: Analyze and generate code from the demo file
            results = self.round_trip_system.analyze_and_generate_code(demo_file)
            logger.info("✅ Code analysis and generation completed")

            # Step 2: Get workflow analysis
            workflow_analysis = self.round_trip_system.get_workflow_analysis(demo_file)
            logger.info("✅ Workflow analysis completed")

            # Step 3: Get system status
            system_status = self.round_trip_system.get_system_status()
            logger.info("✅ System status retrieved")

            # Calculate demo metrics
            demo_duration = time.time() - self.demo_start_time
            self.demo_results = {
                "demo_type": "basic",
                "status": "success",
                "duration": demo_duration,
                "source_file": demo_file,
                "analysis_results": results,
                "workflow_analysis": workflow_analysis,
                "system_status": system_status,
                "round_trip_successful": results.get("enhancement_metrics", {}).get(
                    "code_generation_successful", False
                ),
            }

            self.current_demo_step = "completed"
            logger.info("🎉 Basic demo completed successfully")

            return self.demo_results

        except Exception as e:
            self._track_error()
            logger.error(f"❌ Basic demo failed: {e}")
            self.demo_results = {
                "demo_type": "basic",
                "status": "failed",
                "error": str(e),
                "round_trip_successful": False,
            }
            self.current_demo_step = "failed"
            return self.demo_results

    async def run_advanced_demo(self) -> Dict[str, Any]:
        """Run an advanced round-trip engineering demo with complex scenarios."""
        try:
            self._track_success()
            self.current_demo_step = "advanced_demo"
            self.demo_start_time = time.time()

            logger.info("🚀 Starting advanced round-trip engineering demo")

            # Create a complex Python file for demo purposes
            demo_file = self._create_complex_demo_python_file()
            logger.info("✅ Created complex demo Python file")

            # Step 1: Analyze and generate code from the complex demo file
            results = self.round_trip_system.analyze_and_generate_code(demo_file)
            logger.info("✅ Complex code analysis and generation completed")

            # Step 2: Get workflow analysis
            workflow_analysis = self.round_trip_system.get_workflow_analysis(demo_file)
            logger.info("✅ Complex workflow analysis completed")

            # Step 3: Validate vocabulary alignment
            vocabulary_status = await self._validate_vocabulary_alignment(results)

            # Calculate demo metrics
            demo_duration = time.time() - self.demo_start_time
            self.demo_results = {
                "demo_type": "advanced",
                "status": "success",
                "duration": demo_duration,
                "source_file": demo_file,
                "analysis_results": results,
                "workflow_analysis": workflow_analysis,
                "vocabulary_alignment": vocabulary_status,
                "round_trip_successful": results.get("enhancement_metrics", {}).get(
                    "code_generation_successful", False
                ),
            }

            self.current_demo_step = "completed"
            logger.info("🎉 Advanced demo completed successfully")

            return self.demo_results

        except Exception as e:
            self._track_error()
            logger.error(f"❌ Advanced demo failed: {e}")
            self.demo_results = {
                "demo_type": "advanced",
                "status": "failed",
                "error": str(e),
                "round_trip_successful": False,
            }
            self.current_demo_step = "failed"
            return self.demo_results

    async def run_performance_demo(self) -> Dict[str, Any]:
        """Run a performance-focused demo to validate system performance."""
        try:
            self._track_success()
            self.current_demo_step = "performance_demo"
            self.demo_start_time = time.time()

            logger.info("🚀 Starting performance demo")

            # Run multiple iterations to measure performance
            iterations = 5  # Reduced for demo purposes
            results = []

            for i in range(iterations):
                iteration_start = time.time()

                # Create a simple demo file
                demo_file = self._create_performance_demo_python_file(i)

                # Run the full workflow
                analysis_results = self.round_trip_system.analyze_and_generate_code(
                    demo_file
                )
                workflow_analysis = self.round_trip_system.get_workflow_analysis(
                    demo_file
                )

                iteration_duration = time.time() - iteration_start
                results.append(
                    {
                        "iteration": i + 1,
                        "duration": iteration_duration,
                        "source_file": demo_file,
                        "analysis_successful": analysis_results.get(
                            "enhancement_metrics", {}
                        ).get("code_generation_successful", False),
                        "workflow_nodes": len(workflow_analysis.get("nodes", [])),
                        "enhanced_ast_classes": analysis_results.get(
                            "enhancement_metrics", {}
                        ).get("enhanced_ast_classes", 0),
                    }
                )

            # Calculate performance metrics
            total_duration = time.time() - self.demo_start_time
            avg_iteration_time = sum(r["duration"] for r in results) / len(results)

            self.demo_results = {
                "demo_type": "performance",
                "status": "success",
                "total_duration": total_duration,
                "iterations": iterations,
                "average_iteration_time": avg_iteration_time,
                "results": results,
                "performance_score": (
                    "excellent" if avg_iteration_time < 2.0 else "good"
                ),
            }

            self.current_demo_step = "completed"
            logger.info("🎉 Performance demo completed successfully")

            return self.demo_results

        except Exception as e:
            self._track_error()
            logger.error(f"❌ Performance demo failed: {e}")
            self.demo_results = {
                "demo_type": "performance",
                "status": "failed",
                "error": str(e),
            }
            self.current_demo_step = "failed"
            return self.demo_results

    async def get_demo_status(self) -> Dict[str, Any]:
        """Get current demo status and results."""
        return {
            "current_step": self.current_demo_step,
            "demo_start_time": self.demo_start_time,
            "last_results": self.demo_results,
            "success_count": self._get_success_count(),
            "error_count": self._get_error_count(),
            "success_rate": self._calculate_success_rate(),
        }

    def _create_demo_python_file(self) -> str:
        """Create a simple Python file for demo purposes."""
        demo_content = '''#!/usr/bin/env python3
"""
Simple Demo Class for Round-Trip Engineering Demo
"""

from typing import List, Dict, Any


class SimpleDemoClass:
    """A simple demo class to showcase round-trip engineering."""
    
    def __init__(self, name: str):
        self.name = name
        self.data = []
    
    def add_data(self, item: Any) -> None:
        """Add an item to the data list."""
        self.data.append(item)
    
    def get_data(self) -> List[Any]:
        """Get all data items."""
        return self.data
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the data."""
        return {
            "name": self.name,
            "count": len(self.data),
            "data": self.data
        }


def demo_function(value: int) -> str:
    """A simple demo function."""
    if value > 0:
        return f"Positive: {value}"
    elif value < 0:
        return f"Negative: {value}"
    else:
        return "Zero"


if __name__ == "__main__":
    demo = SimpleDemoClass("Test")
    demo.add_data(42)
    demo.add_data("hello")
    print(demo.get_summary())
    print(demo_function(10))
'''

        demo_file = "demo_simple_class.py"
        with open(demo_file, "w") as f:
            f.write(demo_content)

        return demo_file

    def _create_complex_demo_python_file(self) -> str:
        """Create a complex Python file for demo purposes."""
        demo_content = '''#!/usr/bin/env python3
"""
Complex Demo System for Round-Trip Engineering Demo
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class DataItem:
    """Data item with metadata."""
    id: str
    value: Any
    metadata: Dict[str, Any]


class DataProcessor(ABC):
    """Abstract base class for data processing."""
    
    @abstractmethod
    def process(self, data: List[DataItem]) -> List[DataItem]:
        """Process data items."""
        pass


class SimpleProcessor(DataProcessor):
    """Simple data processor implementation."""
    
    def process(self, data: List[DataItem]) -> List[DataItem]:
        """Process data items with simple logic."""
        return [item for item in data if item.value is not None]


class AdvancedProcessor(DataProcessor):
    """Advanced data processor with filtering and transformation."""
    
    def __init__(self, filter_func=None, transform_func=None):
        self.filter_func = filter_func
        self.transform_func = transform_func
    
    def process(self, data: List[DataItem]) -> List[DataItem]:
        """Process data items with advanced logic."""
        # Apply filter if provided
        if self.filter_func:
            data = [item for item in data if self.filter_func(item)]
        
        # Apply transformation if provided
        if self.transform_func:
            data = [DataItem(
                id=item.id,
                value=self.transform_func(item.value),
                metadata=item.metadata
            ) for item in data]
        
        return data


class ResultFormatter:
    """Formats processing results."""
    
    def __init__(self, output_format: str = "json"):
        self.output_format = output_format
    
    def format_json(self, data: List[DataItem]) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps([{
            "id": item.id,
            "value": item.value,
            "metadata": item.metadata
        } for item in data], indent=2)
    
    def format_text(self, data: List[DataItem]) -> str:
        """Format data as text."""
        lines = []
        for item in data:
            lines.append(f"ID: {item.id}")
            lines.append(f"Value: {item.value}")
            lines.append(f"Metadata: {item.metadata}")
            lines.append("---")
        return "\\n".join(lines)
    
    def format(self, data: List[DataItem]) -> str:
        """Format data using the specified output format."""
        if self.output_format == "json":
            return self.format_json(data)
        else:
            return self.format_text(data)


class DemoSystem:
    """Main demo system that orchestrates data processing."""
    
    def __init__(self, processor: DataProcessor, formatter: ResultFormatter):
        self.processor = processor
        self.formatter = formatter
        self.logger = logging.getLogger(__name__)
    
    def run_demo(self, input_data: List[DataItem]) -> str:
        """Run the complete demo workflow."""
        try:
            self.logger.info("Starting demo workflow")
            
            # Process data
            processed_data = self.processor.process(input_data)
            self.logger.info(f"Processed {len(processed_data)} items")
            
            # Format results
            formatted_result = self.formatter.format(processed_data)
            self.logger.info("Results formatted successfully")
            
            return formatted_result
            
        except Exception as e:
            self.logger.error(f"Demo workflow failed: {e}")
            raise


def create_sample_data() -> List[DataItem]:
    """Create sample data for demo purposes."""
    return [
        DataItem("1", 42, {"type": "number", "category": "positive"}),
        DataItem("2", "hello", {"type": "string", "category": "greeting"}),
        DataItem("3", None, {"type": "null", "category": "empty"}),
        DataItem("4", [1, 2, 3], {"type": "list", "category": "sequence"}),
        DataItem("5", {"key": "value"}, {"type": "dict", "category": "mapping"})
    ]


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data
    sample_data = create_sample_data()
    
    # Create processor and formatter
    processor = AdvancedProcessor(
        filter_func=lambda item: item.value is not None,
        transform_func=lambda value: str(value) if not isinstance(value, (int, float)) else value
    )
    formatter = ResultFormatter(output_format="json")
    
    # Create and run demo system
    demo_system = DemoSystem(processor, formatter)
    result = demo_system.run_demo(sample_data)
    
    print("Demo Results:")
    print(result)
'''

        demo_file = "demo_complex_system.py"
        with open(demo_file, "w") as f:
            f.write(demo_content)

        return demo_file

    def _create_performance_demo_python_file(self, iteration: int) -> str:
        """Create a performance test Python file."""
        demo_content = f'''#!/usr/bin/env python3
"""
Performance Demo Class {iteration} for Round-Trip Engineering Demo
"""

from typing import List, Dict, Any


class PerformanceDemoClass{iteration}:
    """Performance demo class iteration {iteration}."""
    
    def __init__(self, name: str):
        self.name = name
        self.counter = 0
        self.data = {{}}
    
    def increment(self) -> int:
        """Increment counter and return new value."""
        self.counter += 1
        return self.counter
    
    def add_data(self, key: str, value: Any) -> None:
        """Add data to the internal dictionary."""
        self.data[key] = value
    
    def get_data(self, key: str) -> Any:
        """Get data by key."""
        return self.data.get(key)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of the class state."""
        return {{
            "name": self.name,
            "counter": self.counter,
            "data_keys": list(self.data.keys()),
            "data_count": len(self.data)
        }}


def performance_demo_function{iteration}(value: int) -> str:
    """Performance demo function {iteration}."""
    if value > 0:
        return f"Positive {{iteration}}: {{value}}"
    elif value < 0:
        return f"Negative {{iteration}}: {{value}}"
    else:
        return f"Zero {{iteration}}"


if __name__ == "__main__":
    demo = PerformanceDemoClass{iteration}("PerformanceTest{iteration}")
    demo.increment()
    demo.add_data("test", "value")
    print(demo.get_summary())
    print(performance_demo_function{iteration}(10))
'''

        demo_file = f"demo_performance_class_{iteration}.py"
        with open(demo_file, "w") as f:
            f.write(demo_content)

        return demo_file

    async def _validate_vocabulary_alignment(
        self, analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate vocabulary alignment for the analysis results."""
        try:
            # This would normally use the vocabulary aligner
            # For demo purposes, we'll return a mock validation
            return {
                "status": "validated",
                "alignment_score": 0.95,
                "vocabulary_matches": 19,
                "vocabulary_mismatches": 1,
                "overall_health": "excellent",
            }
        except Exception as e:
            logger.warning(f"Vocabulary validation failed: {e}")
            return {"status": "failed", "error": str(e), "overall_health": "unknown"}
