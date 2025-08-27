#!/usr/bin/env python3
"""
Code Complexity Metrics Analyzer

Addresses UC-5 low risk use case for comprehensive code complexity analysis.
This system integrates Radon complexity analysis with custom metrics and validation.
"""

import ast
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
import subprocess
import statistics
from collections import defaultdict


class ComplexityMetricsAnalyzer:
    """Analyzes code complexity using multiple metrics and tools."""
    
    def __init__(self):
        self.metrics_cache = {}
        self.radon_results = {}
        self.custom_metrics = {}
        
    def analyze_complexity(self, source_file: str) -> Dict[str, Any]:
        """
        Analyze code complexity using multiple approaches.
        
        Args:
            source_file: Path to source Python file
            
        Returns:
            Comprehensive complexity analysis results
        """
        try:
            # Parse source file
            with open(source_file, 'r') as f:
                source_content = f.read()
            
            # Generate AST from source
            source_ast = ast.parse(source_content)
            
            # Analyze with Radon
            radon_analysis = self._analyze_with_radon(source_file)
            
            # Custom AST-based complexity analysis
            custom_analysis = self._analyze_ast_complexity(source_ast)
            
            # Calculate industry standard metrics
            industry_metrics = self._calculate_industry_metrics(radon_analysis, custom_analysis)
            
            # Generate complexity report
            complexity_report = self._generate_complexity_report(
                source_file, radon_analysis, custom_analysis, industry_metrics
            )
            
            analysis_result = {
                'source_file': source_file,
                'analysis_success': True,
                'radon_analysis': radon_analysis,
                'custom_analysis': custom_analysis,
                'industry_metrics': industry_metrics,
                'complexity_report': complexity_report,
                'overall_complexity_score': self._calculate_overall_complexity_score(
                    radon_analysis, custom_analysis
                )
            }
            
            return analysis_result
            
        except Exception as e:
            return {
                'source_file': source_file,
                'error': str(e),
                'analysis_success': False
            }
    
    def _analyze_with_radon(self, source_file: str) -> Dict[str, Any]:
        """Analyze complexity using Radon."""
        try:
            # Run Radon complexity analysis
            result = subprocess.run(
                ["uv", "run", "radon", "cc", source_file, "-j"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse JSON output
                radon_data = json.loads(result.stdout)
                return {
                    'success': True,
                    'data': radon_data,
                    'raw_output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'return_code': result.returncode
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_ast_complexity(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """Analyze complexity using custom AST analysis."""
        complexity_metrics = {
            'function_complexity': {},
            'class_complexity': {},
            'overall_metrics': {
                'total_functions': 0,
                'total_classes': 0,
                'total_lines': 0,
                'total_statements': 0,
                'max_nesting': 0,
                'total_imports': 0,
                'total_variables': 0
            },
            'complexity_distribution': {
                'low': 0,      # 1-5
                'medium': 0,   # 6-10
                'high': 0,     # 11-20
                'very_high': 0 # 21+
            }
        }
        
        # Analyze functions
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                func_complexity = self._calculate_function_complexity(node)
                complexity_metrics['function_complexity'][node.name] = func_complexity
                complexity_metrics['overall_metrics']['total_functions'] += 1
                
                # Categorize complexity
                self._categorize_complexity(func_complexity['cyclomatic'], complexity_metrics['complexity_distribution'])
            
            elif isinstance(node, ast.ClassDef):
                class_complexity = self._calculate_class_complexity(node)
                complexity_metrics['class_complexity'][node.name] = class_complexity
                complexity_metrics['overall_metrics']['total_classes'] += 1
            
            elif isinstance(node, ast.stmt):
                complexity_metrics['overall_metrics']['total_statements'] += 1
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                complexity_metrics['overall_metrics']['total_imports'] += 1
            
            elif isinstance(node, ast.Assign):
                complexity_metrics['overall_metrics']['total_variables'] += 1
        
        # Calculate overall metrics
        complexity_metrics['overall_metrics']['total_lines'] = self._count_lines(ast_tree)
        complexity_metrics['overall_metrics']['max_nesting'] = self._calculate_max_nesting(ast_tree)
        
        return complexity_metrics
    
    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> Dict[str, Any]:
        """Calculate complexity metrics for a function."""
        complexity = {
            'name': func_node.name,
            'lineno': getattr(func_node, 'lineno', 0),
            'cyclomatic': 1,  # Base complexity
            'nesting_depth': 0,
            'parameters': len(func_node.args.args),
            'local_variables': 0,
            'function_calls': 0,
            'control_structures': 0,
            'exception_handlers': 0
        }
        
        # Calculate cyclomatic complexity
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity['cyclomatic'] += 1
                complexity['control_structures'] += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity['cyclomatic'] += 1
                complexity['exception_handlers'] += 1
            elif isinstance(node, ast.Call):
                complexity['function_calls'] += 1
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                complexity['local_variables'] += 1
        
        # Calculate nesting depth
        complexity['nesting_depth'] = self._calculate_nesting_depth(func_node)
        
        return complexity
    
    def _calculate_class_complexity(self, class_node: ast.ClassDef) -> Dict[str, Any]:
        """Calculate complexity metrics for a class."""
        complexity = {
            'name': class_node.name,
            'lineno': getattr(class_node, 'lineno', 0),
            'methods': 0,
            'attributes': 0,
            'inheritance_depth': 0,
            'total_complexity': 0,
            'method_complexities': []
        }
        
        # Count methods and calculate their complexity
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                complexity['methods'] += 1
                method_complexity = self._calculate_function_complexity(node)
                complexity['method_complexities'].append(method_complexity)
                complexity['total_complexity'] += method_complexity['cyclomatic']
            
            elif isinstance(node, ast.Assign):
                complexity['attributes'] += 1
        
        # Calculate inheritance depth
        if class_node.bases:
            complexity['inheritance_depth'] = 1  # Simplified for now
        
        return complexity
    
    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """Calculate nesting depth of a node."""
        depth = 0
        current = node
        
        while hasattr(current, 'parent'):
            if isinstance(current.parent, (ast.If, ast.For, ast.While, ast.Try)):
                depth += 1
            current = current.parent
        
        return depth
    
    def _calculate_max_nesting(self, ast_tree: ast.AST) -> int:
        """Calculate maximum nesting level in the AST."""
        max_nesting = 0
        
        def calculate_nesting(node, current_depth=0):
            nonlocal max_nesting
            max_nesting = max(max_nesting, current_depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                    calculate_nesting(child, current_depth + 1)
                else:
                    calculate_nesting(child, current_depth)
        
        calculate_nesting(ast_tree)
        return max_nesting
    
    def _count_lines(self, ast_tree: ast.AST) -> int:
        """Count total lines in the AST."""
        max_line = 0
        for node in ast.walk(ast_tree):
            if hasattr(node, 'lineno'):
                max_line = max(max_line, node.lineno)
        return max_line
    
    def _categorize_complexity(self, complexity_value: int, distribution: Dict[str, int]):
        """Categorize complexity into distribution buckets."""
        if complexity_value <= 5:
            distribution['low'] += 1
        elif complexity_value <= 10:
            distribution['medium'] += 1
        elif complexity_value <= 20:
            distribution['high'] += 1
        else:
            distribution['very_high'] += 1
    
    def _calculate_industry_metrics(self, radon_analysis: Dict[str, Any], custom_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate industry standard complexity metrics."""
        industry_metrics = {
            'maintainability_index': 0,
            'technical_debt_ratio': 0,
            'code_smell_density': 0,
            'complexity_per_function': 0,
            'complexity_per_class': 0,
            'nesting_depth_score': 0,
            'overall_quality_score': 0
        }
        
        if custom_analysis['overall_metrics']['total_functions'] > 0:
            # Calculate average complexity per function
            total_complexity = sum(
                func['cyclomatic'] for func in custom_analysis['function_complexity'].values()
            )
            industry_metrics['complexity_per_function'] = (
                total_complexity / custom_analysis['overall_metrics']['total_functions']
            )
        
        if custom_analysis['overall_metrics']['total_classes'] > 0:
            # Calculate average complexity per class
            total_class_complexity = sum(
                cls['total_complexity'] for cls in custom_analysis['class_complexity'].values()
            )
            industry_metrics['complexity_per_class'] = (
                total_class_complexity / custom_analysis['overall_metrics']['total_classes']
            )
        
        # Calculate maintainability index (simplified)
        # Higher is better, max 100
        base_score = 100
        
        # Deduct for high complexity
        if industry_metrics['complexity_per_function'] > 10:
            base_score -= 20
        elif industry_metrics['complexity_per_function'] > 5:
            base_score -= 10
        
        # Deduct for high nesting
        max_nesting = custom_analysis['overall_metrics']['max_nesting']
        if max_nesting > 5:
            base_score -= 20
        elif max_nesting > 3:
            base_score -= 10
        
        # Deduct for very high complexity functions
        very_high_count = custom_analysis['complexity_distribution']['very_high']
        if very_high_count > 0:
            base_score -= very_high_count * 5
        
        industry_metrics['maintainability_index'] = max(0, base_score)
        
        # Calculate nesting depth score (lower is better)
        industry_metrics['nesting_depth_score'] = max(0, 10 - max_nesting)
        
        # Calculate overall quality score
        industry_metrics['overall_quality_score'] = (
            industry_metrics['maintainability_index'] * 0.4 +
            industry_metrics['nesting_depth_score'] * 0.3 +
            (100 - industry_metrics['complexity_per_function'] * 2) * 0.3
        )
        industry_metrics['overall_quality_score'] = max(0, min(100, industry_metrics['overall_quality_score']))
        
        return industry_metrics
    
    def _calculate_overall_complexity_score(self, radon_analysis: Dict[str, Any], custom_analysis: Dict[str, Any]) -> float:
        """Calculate overall complexity score (0-100, lower is better)."""
        if not radon_analysis.get('success'):
            return 100.0  # Worst case if Radon fails
        
        # Base score from custom analysis
        base_score = 0
        
        # Function complexity contribution (40%)
        if custom_analysis['overall_metrics']['total_functions'] > 0:
            avg_func_complexity = sum(
                func['cyclomatic'] for func in custom_analysis['function_complexity'].values()
            ) / custom_analysis['overall_metrics']['total_functions']
            base_score += min(100, avg_func_complexity * 5) * 0.4
        
        # Nesting depth contribution (30%)
        max_nesting = custom_analysis['overall_metrics']['max_nesting']
        base_score += min(100, max_nesting * 10) * 0.3
        
        # Control structure density contribution (30%)
        total_statements = custom_analysis['overall_metrics']['total_statements']
        if total_statements > 0:
            control_structures = sum(
                func['control_structures'] for func in custom_analysis['function_complexity'].values()
            )
            control_density = (control_structures / total_statements) * 100
            base_score += min(100, control_density * 2) * 0.3
        
        return min(100, base_score)
    
    def _generate_complexity_report(self, source_file: str, radon_analysis: Dict[str, Any], 
                                  custom_analysis: Dict[str, Any], industry_metrics: Dict[str, Any]) -> str:
        """Generate human-readable complexity report."""
        report = f"""
Code Complexity Analysis Report
==============================
Source File: {source_file}

Overall Metrics:
---------------
Total Functions: {custom_analysis['overall_metrics']['total_functions']}
Total Classes: {custom_analysis['overall_metrics']['total_classes']}
Total Lines: {custom_analysis['overall_metrics']['total_lines']}
Total Statements: {custom_analysis['overall_metrics']['total_statements']}
Maximum Nesting: {custom_analysis['overall_metrics']['max_nesting']}
Total Imports: {custom_analysis['overall_metrics']['total_imports']}
Total Variables: {custom_analysis['overall_metrics']['total_variables']}

Complexity Distribution:
-----------------------
Low Complexity (1-5): {custom_analysis['complexity_distribution']['low']}
Medium Complexity (6-10): {custom_analysis['complexity_distribution']['medium']}
High Complexity (11-20): {custom_analysis['complexity_distribution']['high']}
Very High Complexity (21+): {custom_analysis['complexity_distribution']['very_high']}

Industry Metrics:
----------------
Maintainability Index: {industry_metrics['maintainability_index']:.1f}/100
Complexity per Function: {industry_metrics['complexity_per_function']:.2f}
Complexity per Class: {industry_metrics['complexity_per_class']:.2f}
Nesting Depth Score: {industry_metrics['nesting_depth_score']:.1f}/10
Overall Quality Score: {industry_metrics['overall_quality_score']:.1f}/100

Radon Analysis:
---------------
Status: {'✅ Success' if radon_analysis.get('success') else '❌ Failed'}
"""
        
        if radon_analysis.get('success'):
            report += f"Data Available: Yes\n"
        else:
            report += f"Error: {radon_analysis.get('error', 'Unknown error')}\n"
        
        return report
    
    def analyze_project_complexity(self, source_dir: str = "src") -> Dict[str, Any]:
        """
        Analyze complexity for all Python files in a directory.
        
        Args:
            source_dir: Directory containing Python files
            
        Returns:
            Project-wide complexity analysis
        """
        source_path = Path(source_dir)
        python_files = list(source_path.rglob("*.py"))
        
        project_metrics = {
            'total_files': len(python_files),
            'analyzed_files': 0,
            'failed_files': 0,
            'overall_complexity_score': 0,
            'file_complexity_scores': [],
            'complexity_distribution': defaultdict(int),
            'maintainability_scores': []
        }
        
        for python_file in python_files[:10]:  # Limit to first 10 files for testing
            try:
                result = self.analyze_complexity(str(python_file))
                if result['analysis_success']:
                    project_metrics['analyzed_files'] += 1
                    project_metrics['file_complexity_scores'].append(result['overall_complexity_score'])
                    project_metrics['maintainability_scores'].append(
                        result['industry_metrics']['maintainability_index']
                    )
                    
                    # Aggregate complexity distribution
                    custom_analysis = result['custom_analysis']
                    for category, count in custom_analysis['complexity_distribution'].items():
                        project_metrics['complexity_distribution'][category] += count
                else:
                    project_metrics['failed_files'] += 1
                    
            except Exception as e:
                project_metrics['failed_files'] += 1
        
        # Calculate project-wide metrics
        if project_metrics['file_complexity_scores']:
            project_metrics['overall_complexity_score'] = statistics.mean(project_metrics['file_complexity_scores'])
        
        if project_metrics['maintainability_scores']:
            project_metrics['average_maintainability'] = statistics.mean(project_metrics['maintainability_scores'])
        
        return project_metrics


def test_complexity_analyzer():
    """Test the complexity metrics analyzer."""
    analyzer = ComplexityMetricsAnalyzer()
    
    # Test with a single file
    test_file = "src/enhanced_activity_generator.py"
    
    print("Testing Code Complexity Analysis:")
    print("=" * 50)
    
    # Run analysis
    result = analyzer.analyze_complexity(test_file)
    
    if result['analysis_success']:
        print(f"✅ Complexity analysis successful!")
        print(f"Source file: {result['source_file']}")
        print(f"Overall complexity score: {result['overall_complexity_score']:.2f}/100")
        
        print(f"\nIndustry Metrics:")
        industry = result['industry_metrics']
        print(f"  Maintainability Index: {industry['maintainability_index']:.1f}/100")
        print(f"  Overall Quality Score: {industry['overall_quality_score']:.1f}/100")
        print(f"  Complexity per Function: {industry['complexity_per_function']:.2f}")
        print(f"  Nesting Depth Score: {industry['nesting_depth_score']:.1f}/10")
        
        print(f"\nCustom Analysis:")
        custom = result['custom_analysis']
        overall = custom['overall_metrics']
        print(f"  Total Functions: {overall['total_functions']}")
        print(f"  Total Classes: {overall['total_classes']}")
        print(f"  Total Lines: {overall['total_lines']}")
        print(f"  Max Nesting: {overall['max_nesting']}")
        
        print(f"\nComplexity Distribution:")
        dist = custom['complexity_distribution']
        print(f"  Low (1-5): {dist['low']}")
        print(f"  Medium (6-10): {dist['medium']}")
        print(f"  High (11-20): {dist['high']}")
        print(f"  Very High (21+): {dist['very_high']}")
        
        # Show detailed report
        print(f"\nDetailed Report:")
        print(result['complexity_report'])
        
    else:
        print(f"❌ Complexity analysis failed: {result.get('error', 'Unknown error')}")
    
    return result


if __name__ == "__main__":
    test_complexity_analyzer()
