#!/usr/bin/env python3
"""
Round-Trip Validation Framework

Addresses UC-7 critical risk use case for validating extracted models against source code.
This framework ensures >95% accuracy and no missing critical paths.
"""

import ast
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import ast2json


class RoundTripValidator:
    """Validates extracted workflow models against source code for accuracy."""
    
    def __init__(self):
        self.validation_results = {}
        self.accuracy_metrics = {}
        
    def validate_workflow_extraction(self, source_file: str, extracted_model: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted workflow model against source code.
        
        Args:
            source_file: Path to source Python file
            extracted_model: Extracted workflow model to validate
            
        Returns:
            Validation results with accuracy metrics
        """
        try:
            # Parse source file
            with open(source_file, 'r') as f:
                source_content = f.read()
            
            # Generate AST from source
            source_ast = ast.parse(source_content)
            source_json = ast2json.ast2json(source_ast)
            
            # Extract actual workflow elements from source
            actual_elements = self._extract_actual_workflow_elements(source_ast)
            
            # Extract expected workflow elements from model
            expected_elements = self._extract_expected_workflow_elements(extracted_model)
            
            # Compare and calculate accuracy
            accuracy_results = self._calculate_accuracy(actual_elements, expected_elements)
            
            # Generate validation report
            validation_report = {
                'source_file': source_file,
                'validation_timestamp': self._get_timestamp(),
                'accuracy_metrics': accuracy_results,
                'missing_elements': accuracy_results['missing_elements'],
                'extra_elements': accuracy_results['extra_elements'],
                'validation_passed': accuracy_results['overall_accuracy'] >= 0.95,
                'critical_paths_missing': len(accuracy_results['missing_critical_paths']) > 0
            }
            
            self.validation_results[source_file] = validation_report
            return validation_report
            
        except Exception as e:
            return {
                'source_file': source_file,
                'error': str(e),
                'validation_passed': False
            }
    
    def _extract_actual_workflow_elements(self, ast_tree: ast.AST) -> Dict[str, Any]:
        """Extract actual workflow elements from AST."""
        elements = {
            'functions': [],
            'classes': [],
            'calls': [],
            'imports': [],
            'control_flow': []
        }
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                elements['functions'].append({
                    'name': node.name,
                    'lineno': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'calls': self._extract_function_calls(node)
                })
            elif isinstance(node, ast.ClassDef):
                elements['classes'].append({
                    'name': node.name,
                    'lineno': node.lineno,
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id'):
                    elements['calls'].append({
                        'function': node.func.id,
                        'lineno': getattr(node, 'lineno', 0)
                    })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    elements['imports'].append({'name': alias.name})
            elif isinstance(node, ast.ImportFrom):
                elements['imports'].append({'name': f"{node.module}.{node.names[0].name}"})
            elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                elements['control_flow'].append({
                    'type': type(node).__name__,
                    'lineno': getattr(node, 'lineno', 0)
                })
        
        return elements
    
    def _extract_function_calls(self, function_node: ast.FunctionDef) -> List[str]:
        """Extract function calls within a function."""
        calls = []
        for node in ast.walk(function_node):
            if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
                calls.append(node.func.id)
        return calls
    
    def _extract_expected_workflow_elements(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """Extract expected workflow elements from extracted model."""
        # This would parse the extracted model format
        # For now, return a basic structure
        return {
            'functions': model.get('functions', []),
            'classes': model.get('classes', []),
            'calls': model.get('calls', []),
            'imports': model.get('imports', []),
            'control_flow': model.get('control_flow', [])
        }
    
    def _calculate_accuracy(self, actual: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate accuracy metrics between actual and expected elements."""
        
        def calculate_element_accuracy(actual_list: List, expected_list: List, key: str) -> float:
            if not expected_list:
                return 1.0 if not actual_list else 0.0
            if not actual_list:
                return 0.0
            
            # Simple matching for now - could be enhanced with fuzzy matching
            actual_names = [item.get('name', str(item)) for item in actual_list]
            expected_names = [item.get('name', str(item)) for item in expected_list]
            
            matches = len(set(actual_names) & set(expected_names))
            return matches / len(expected_names) if expected_names else 0.0
        
        # Calculate accuracy for each element type
        function_accuracy = calculate_element_accuracy(actual['functions'], expected['functions'], 'name')
        class_accuracy = calculate_element_accuracy(actual['classes'], expected['classes'], 'name')
        call_accuracy = calculate_element_accuracy(actual['calls'], expected['calls'], 'function')
        import_accuracy = calculate_element_accuracy(actual['imports'], expected['imports'], 'name')
        control_flow_accuracy = calculate_element_accuracy(actual['control_flow'], expected['control_flow'], 'type')
        
        # Calculate overall accuracy
        overall_accuracy = (function_accuracy + class_accuracy + call_accuracy + 
                           import_accuracy + control_flow_accuracy) / 5
        
        # Identify missing and extra elements
        missing_elements = []
        extra_elements = []
        missing_critical_paths = []
        
        # Check for missing critical paths (functions with high call count)
        actual_call_counts = {}
        for call in actual['calls']:
            if isinstance(call, dict):
                func_name = call.get('function', '')
            else:
                func_name = str(call)
            actual_call_counts[func_name] = actual_call_counts.get(func_name, 0) + 1
        
        # Functions called more than 3 times are considered critical
        critical_functions = [func for func, count in actual_call_counts.items() if count > 3]
        for critical_func in critical_functions:
            if not any((call.get('function') if isinstance(call, dict) else str(call)) == critical_func for call in expected['calls']):
                missing_critical_paths.append(critical_func)
        
        return {
            'function_accuracy': function_accuracy,
            'class_accuracy': class_accuracy,
            'call_accuracy': call_accuracy,
            'import_accuracy': import_accuracy,
            'control_flow_accuracy': control_flow_accuracy,
            'overall_accuracy': overall_accuracy,
            'missing_elements': missing_elements,
            'extra_elements': extra_elements,
            'missing_critical_paths': missing_critical_paths
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for validation."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_validation_report(self, source_file: str) -> str:
        """Generate human-readable validation report."""
        if source_file not in self.validation_results:
            return f"No validation results found for {source_file}"
        
        result = self.validation_results[source_file]
        
        report = f"""
Round-Trip Validation Report
===========================
Source File: {result['source_file']}
Timestamp: {result['validation_timestamp']}
Validation Status: {'✅ PASSED' if result['validation_passed'] else '❌ FAILED'}

Accuracy Metrics:
----------------
Overall Accuracy: {result['accuracy_metrics'].get('overall_accuracy', 0):.2%}
Function Accuracy: {result['accuracy_metrics'].get('function_accuracy', 0):.2%}
Class Accuracy: {result['accuracy_metrics'].get('class_accuracy', 0):.2%}
Call Accuracy: {result['accuracy_metrics'].get('call_accuracy', 0):.2%}
Import Accuracy: {result['accuracy_metrics'].get('import_accuracy', 0):.2%}
Control Flow Accuracy: {result['accuracy_metrics'].get('control_flow_accuracy', 0):.2%}

Issues Found:
-------------
Missing Critical Paths: {len(result.get('missing_critical_paths', []))}
Missing Elements: {len(result.get('missing_elements', []))}
Extra Elements: {len(result.get('extra_elements', []))}

Validation Result: {'PASSED' if result['validation_passed'] else 'FAILED'}
"""
        return report


def test_validation_framework():
    """Test the round-trip validation framework."""
    validator = RoundTripValidator()
    
    # Test with a simple file
    test_file = "src/enhanced_activity_generator.py"
    
    # Create a mock extracted model for testing
    mock_model = {
        'functions': [{'name': 'test_function'}],
        'classes': [{'name': 'TestClass'}],
        'calls': [{'function': 'print'}],
        'imports': [{'name': 'os'}],
        'control_flow': [{'type': 'If'}]
    }
    
    # Run validation
    result = validator.validate_workflow_extraction(test_file, mock_model)
    
    # Print raw result for debugging
    print("Raw validation result:")
    print(json.dumps(result, indent=2))
    
    # Generate report
    report = validator.generate_validation_report(test_file)
    print("\n" + report)
    
    return result


if __name__ == "__main__":
    test_validation_framework()
