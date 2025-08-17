#!/usr/bin/env python3
"""
Mass Reverse Engineering System - Process all Python artifacts in parallel
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional

from enhanced_reverse_engineer import EnhancedReverseEngineer


class MassReverseEngineeringSystem:
    """System for mass reverse engineering of Python artifacts"""

    def __init__(self, workspace_path: str = ".") -> None:
        self.workspace_path = Path(workspace_path)
        self.results: dict[str, Any] = {}
        self.errors: list[dict[str, Any]] = []
        self.stats = {
            "total_files": 0,
            "successful": 0,
            "failed": 0,
            "processing_time": 0,
        }

    def discover_python_files(
        self, exclude_patterns: Optional[list[str]] = None
    ) -> list[Path]:
        """Discover all Python files in the workspace"""
        if exclude_patterns is None:
            exclude_patterns = [
                "__pycache__",
                ".git",
                ".mypy_cache",
                "venv",
                "env",
                "node_modules",
                "*.pyc",
                "*.pyo",
            ]

        python_files = []

        for file_path in self.workspace_path.rglob("*.py"):
            # Check if file should be excluded
            should_exclude = False
            for pattern in exclude_patterns:
                if pattern in str(file_path):
                    should_exclude = True
                    break

            if not should_exclude:
                python_files.append(file_path)

        return python_files

    def reverse_engineer_single_file(self, file_path: Path) -> dict[str, Any]:
        """Reverse engineer a single Python file"""
        try:
            start_time = time.time()

            # Create fresh instance for each file
            reverse_engineer = EnhancedReverseEngineer()

            # Run reverse engineering
            model = reverse_engineer.reverse_engineer(str(file_path))

            processing_time = time.time() - start_time

            if model:
                return {
                    "status": "success",
                    "file_path": str(file_path),
                    "model": model,
                    "processing_time": processing_time,
                    "file_size": file_path.stat().st_size,
                    "lines": model.get("file_structure", {}).get("total_lines", 0),
                }
            else:
                return {
                    "status": "failed",
                    "file_path": str(file_path),
                    "error": "No model generated",
                    "processing_time": processing_time,
                }

        except Exception as e:
            return {
                "status": "error",
                "file_path": str(file_path),
                "error": str(e),
                "processing_time": 0,
            }

    def process_all_files(self, max_workers: int = 4) -> None:
        """Process all Python files in parallel"""
        print("🚀 Mass Reverse Engineering System")
        print("=" * 60)

        # Discover Python files
        print("🔍 Discovering Python files...")
        python_files = self.discover_python_files()
        self.stats["total_files"] = len(python_files)

        print(f"   📁 Found {len(python_files)} Python files")

        # Process files in parallel
        print(f"\n⚡ Processing files with {max_workers} workers...")
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            future_to_file = {
                executor.submit(self.reverse_engineer_single_file, file_path): file_path
                for file_path in python_files
            }

            # Process completed jobs
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                result = future.result()

                if result["status"] == "success":
                    self.results[str(file_path)] = result
                    self.stats["successful"] += 1
                    print(f"   ✅ {file_path.name} - {result['lines']} lines")
                else:
                    self.errors.append(result)
                    self.stats["failed"] += 1
                    print(
                        f"   ❌ {file_path.name} - {result.get('error', 'Unknown error')}"
                    )

        self.stats["processing_time"] = time.time() - start_time

        # Generate summary
        self._generate_summary()

    def _generate_summary(self) -> None:
        """Generate comprehensive summary of results"""
        print(f"\n📊 Mass Reverse Engineering Summary")
        print("=" * 60)

        print(f"   📁 Total Files: {self.stats['total_files']}")
        print(f"   ✅ Successful: {self.stats['successful']}")
        print(f"   ❌ Failed: {self.stats['failed']}")
        print(f"   ⏱️  Total Time: {self.stats['processing_time']:.2f}s")
        print(
            f"   🚀 Average Time: {self.stats['processing_time'] / self.stats['total_files']:.3f}s/file"
        )

        if self.stats["successful"] > 0:
            success_rate = (self.stats["successful"] / self.stats["total_files"]) * 100
            print(f"   🎯 Success Rate: {success_rate:.1f}%")

        # Show file statistics
        if self.results:
            print(f"\n📈 File Statistics:")

            # Lines of code
            total_lines = sum(result["lines"] for result in self.results.values())
            avg_lines = total_lines / len(self.results)
            print(f"   📏 Total Lines: {total_lines:,}")
            print(f"   📊 Average Lines: {avg_lines:.1f}")

            # File sizes
            total_size = sum(result["file_size"] for result in self.results.values())
            avg_size = total_size / len(self.results)
            print(f"   💾 Total Size: {total_size:,} bytes")
            print(f"   📊 Average Size: {avg_size:.1f} bytes")

            # Processing times
            total_time = sum(
                result["processing_time"] for result in self.results.values()
            )
            avg_time = total_time / len(self.results)
            print(f"   ⏱️  Total Processing: {total_time:.2f}s")
            print(f"   📊 Average Processing: {avg_time:.3f}s")

        # Show errors if any
        if self.errors:
            print(f"\n❌ Errors Encountered:")
            for error in self.errors:
                print(
                    f"   • {error['file_path']}: {error.get('error', 'Unknown error')}"
                )

    def save_results(
        self, output_dir: str = "mass_reverse_engineering_results"
    ) -> None:
        """Save all results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"\n💾 Saving results to {output_dir}/...")

        # Save summary
        summary = {
            "stats": self.stats,
            "total_files": len(self.results),
            "successful_files": list(self.results.keys()),
            "failed_files": [error["file_path"] for error in self.errors],
        }

        with open(output_path / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        # Save individual models
        models_dir = output_path / "models"
        models_dir.mkdir(exist_ok=True)

        for file_path, result in self.results.items():
            # Create safe filename
            safe_name = Path(file_path).name.replace(".py", "_model.json")
            model_file = models_dir / safe_name

            with open(model_file, "w") as f:
                json.dump(result["model"], f, indent=2)

        # Save errors
        if self.errors:
            with open(output_path / "errors.json", "w") as f:
                json.dump(self.errors, f, indent=2)

        print(f"   ✅ Summary: {output_path / 'summary.json'}")
        print(f"   📁 Models: {output_path / 'models/'}")
        if self.errors:
            print(f"   ❌ Errors: {output_path / 'errors.json'}")

    def generate_clean_models(self) -> dict[str, Any]:
        """Generate clean, error-free models for all successful files"""
        print(f"\n🧹 Generating Clean Models...")

        clean_models = {}

        for file_path, result in self.results.items():
            if result["status"] == "success":
                model = result["model"]

                # Clean the model (remove any problematic fields)
                clean_model = self._clean_model(model)
                clean_models[file_path] = clean_model

        print(f"   ✅ Generated {len(clean_models)} clean models")
        return clean_models

    def _clean_model(self, model: dict[str, Any]) -> dict[str, Any]:
        """Clean a model to ensure it's error-free"""
        # Create a clean copy with only essential fields
        clean_model = {
            "system_name": model.get("system_name", ""),
            "description": model.get("description", ""),
            "purpose": model.get("purpose", ""),
            "graph_api_level": model.get("graph_api_level", 1),
            "projection_system": model.get("projection_system", "reverse_engineered"),
            "components": {},
            "module_functions": [],
            "imports": model.get("imports", []),
            "file_structure": model.get("file_structure", {}),
        }

        # Clean components
        for comp_name, comp_data in model.get("components", {}).items():
            clean_comp = {
                "responsibility": comp_data.get("responsibility", ""),
                "methods": [],
                "line_number": comp_data.get("line_number", 0),
            }

            # Clean methods
            for method in comp_data.get("methods", []):
                if isinstance(method, dict):
                    clean_method = {
                        "name": method.get("name", ""),
                        "signature": method.get("signature", ""),
                        "docstring": method.get("docstring", ""),
                        "return_type": method.get("return_type", "Any"),
                        "parameters": method.get("parameters", []),
                    }
                    clean_comp["methods"].append(clean_method)

            clean_model["components"][comp_name] = clean_comp

        # Clean module functions
        for func in model.get("module_functions", []):
            if isinstance(func, dict):
                clean_func = {
                    "name": func.get("name", ""),
                    "signature": func.get("signature", ""),
                    "docstring": func.get("docstring", ""),
                    "return_type": func.get("return_type", "Any"),
                    "parameters": func.get("parameters", []),
                }
                clean_model["module_functions"].append(clean_func)

        return clean_model


def main() -> None:
    """Main function to run mass reverse engineering"""

    # Create the system
    system = MassReverseEngineeringSystem(".")

    # Process all files
    system.process_all_files(max_workers=4)

    # Save results
    system.save_results()

    # Generate clean models
    clean_models = system.generate_clean_models()

    print(f"\n🎯 Mass Reverse Engineering Complete!")
    print(f"   📊 Processed {system.stats['total_files']} files")
    print(
        f"   ✅ Success Rate: {(system.stats['successful'] / system.stats['total_files']) * 100:.1f}%"
    )
    print(f"   🧹 Generated {len(clean_models)} clean models")


if __name__ == "__main__":
    main()
