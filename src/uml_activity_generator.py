#!/usr/bin/env python3
"""
UML Activity Diagram Generation System

Addresses UC-4 low risk use case for generating UML activity diagrams from extracted workflows.
This system integrates control flow analysis with diagram generation using PlantUML/Graphviz.
"""

import ast
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
import subprocess
import tempfile
import os
from src.control_flow_analyzer import ControlFlowAnalyzer


class UMLActivityGenerator:
    """Generates UML activity diagrams from Python workflow analysis."""
    
    def __init__(self, output_format: str = "plantuml"):
        self.output_format = output_format
        self.control_flow_analyzer = ControlFlowAnalyzer()
        self.diagram_cache = {}
        
    def generate_activity_diagram(self, source_file: str, output_file: str = None) -> Dict[str, Any]:
        """
        Generate UML activity diagram from Python source file.
        
        Args:
            source_file: Path to source Python file
            output_file: Optional output file path
            
        Returns:
            Generation results with diagram content and metadata
        """
        try:
            # Analyze control flow
            control_flow = self.control_flow_analyzer.analyze_control_flow(source_file)
            
            if not control_flow['analysis_success']:
                return {
                    'success': False,
                    'error': f"Control flow analysis failed: {control_flow.get('error', 'Unknown error')}"
                }
            
            # Generate PlantUML diagram
            plantuml_content = self._generate_plantuml_diagram(control_flow)
            
            # Generate Mermaid diagram (alternative format)
            mermaid_content = self._generate_mermaid_diagram(control_flow)
            
            # Generate Graphviz DOT format
            dot_content = self._generate_dot_diagram(control_flow)
            
            # Save diagrams if output file specified
            if output_file:
                self._save_diagrams(output_file, plantuml_content, mermaid_content, dot_content)
            
            # Generate visual output if PlantUML is available
            visual_output = self._generate_visual_output(plantuml_content, output_file)
            
            result = {
                'success': True,
                'source_file': source_file,
                'output_file': output_file,
                'plantuml': plantuml_content,
                'mermaid': mermaid_content,
                'dot': dot_content,
                'visual_output': visual_output,
                'control_flow_summary': {
                    'total_patterns': sum(len(patterns) for patterns in control_flow['patterns'].values()),
                    'recognized_patterns': sum(len(patterns) for patterns in control_flow['recognized_patterns'].values()),
                    'complexity': control_flow['complexity']
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_plantuml_diagram(self, control_flow: Dict[str, Any]) -> str:
        """Generate PlantUML activity diagram."""
        plantuml = []
        plantuml.append("@startuml")
        plantuml.append("!theme plain")
        plantuml.append("title Python Workflow Activity Diagram")
        plantuml.append("")
        
        # Add start activity
        plantuml.append("start")
        
        # Generate main workflow
        self._add_plantuml_workflow(plantuml, control_flow)
        
        # Add end activity
        plantuml.append("stop")
        plantuml.append("@enduml")
        
        return "\n".join(plantuml)
    
    def _add_plantuml_workflow(self, plantuml: List[str], control_flow: Dict[str, Any]):
        """Add workflow elements to PlantUML diagram."""
        patterns = control_flow['patterns']
        recognized = control_flow['recognized_patterns']
        
        # Add function definitions as activities
        for func in patterns.get('functions', []):
            plantuml.append(f":{func['name']};")
        
        # Add control flow patterns
        self._add_plantuml_control_flow(plantuml, patterns)
        
        # Add recognized patterns
        self._add_plantuml_recognized_patterns(plantuml, recognized)
    
    def _add_plantuml_control_flow(self, plantuml: List[str], patterns: Dict[str, Any]):
        """Add control flow elements to PlantUML diagram."""
        # Add if statements
        for if_stmt in patterns.get('if_statements', []):
            condition = f"if ({if_stmt.get('test_complexity', 0)} complexity) then"
            plantuml.append(condition)
            plantuml.append("  :Process condition;")
            plantuml.append("else")
            plantuml.append("  :Handle else case;")
            plantuml.append("endif")
        
        # Add loops
        for loop in patterns.get('for_loops', []):
            plantuml.append(f"while (Loop: {loop.get('target', 'item')}) is (has items)")
            plantuml.append("  :Process item;")
            plantuml.append("endwhile (no more items)")
        
        for while_loop in patterns.get('while_loops', []):
            plantuml.append(f"while (While loop) is (condition true)")
            plantuml.append("  :Process loop body;")
            plantuml.append("endwhile (condition false)")
        
        # Add try blocks
        for try_block in patterns.get('try_blocks', []):
            plantuml.append(":Try block;")
            if try_block.get('handlers', 0) > 0:
                plantuml.append(":Handle exceptions;")
            if try_block.get('finalbody_complexity', 0) > 0:
                plantuml.append(":Finally block;")
    
    def _add_plantuml_recognized_patterns(self, plantuml: List[str], recognized: Dict[str, Any]):
        """Add recognized patterns to PlantUML diagram."""
        # Add guard clauses
        if recognized.get('guard_clauses'):
            plantuml.append(":Guard clause check;")
            plantuml.append("if (condition met) then")
            plantuml.append("  :Early return;")
            plantuml.append("  stop")
            plantuml.append("endif")
        
        # Add early returns
        if recognized.get('early_returns'):
            plantuml.append(":Early return check;")
            plantuml.append("if (early return condition) then")
            plantuml.append("  :Return early;")
            plantuml.append("  stop")
            plantuml.append("endif")
        
        # Add complex loops
        if recognized.get('complex_loops'):
            plantuml.append(":Complex loop processing;")
            plantuml.append("while (complex condition) is (processing)")
            plantuml.append("  :Process complex logic;")
            plantuml.append("  if (break condition) then")
            plantuml.append("    break")
            plantuml.append("  endif")
            plantuml.append("endwhile (complete)")
    
    def _generate_mermaid_diagram(self, control_flow: Dict[str, Any]) -> str:
        """Generate Mermaid activity diagram."""
        mermaid = []
        mermaid.append("graph TD")
        mermaid.append("    A[Start] --> B[Python Workflow]")
        
        # Add workflow elements
        patterns = control_flow['patterns']
        recognized = control_flow['recognized_patterns']
        
        # Add functions
        for i, func in enumerate(patterns.get('functions', [])[:5]):  # Limit to first 5
            mermaid.append(f"    B --> C{i}[{func['name']}]")
        
        # Add control flow
        if patterns.get('if_statements'):
            mermaid.append("    B --> D{If Statement}")
            mermaid.append("    D -->|True| E[Process True]")
            mermaid.append("    D -->|False| F[Process False]")
        
        if patterns.get('for_loops'):
            mermaid.append("    B --> G[For Loop]")
            mermaid.append("    G --> H[Process Items]")
            mermaid.append("    H --> G")
        
        # Add end
        mermaid.append("    E --> I[End]")
        mermaid.append("    F --> I")
        mermaid.append("    H --> I")
        
        return "\n".join(mermaid)
    
    def _generate_dot_diagram(self, control_flow: Dict[str, Any]) -> str:
        """Generate Graphviz DOT diagram."""
        dot = []
        dot.append("digraph PythonWorkflow {")
        dot.append("    rankdir=TB;")
        dot.append("    node [shape=box, style=filled, fillcolor=lightblue];")
        dot.append("    edge [color=black];")
        dot.append("")
        
        # Add nodes
        dot.append("    start [shape=oval, fillcolor=green, label=\"Start\"];")
        
        patterns = control_flow['patterns']
        recognized = control_flow['recognized_patterns']
        
        # Add function nodes
        for func in patterns.get('functions', [])[:10]:  # Limit to first 10
            func_id = func['name'].replace('-', '_').replace(' ', '_')
            dot.append(f"    {func_id} [label=\"{func['name']}\"];")
        
        # Add control flow nodes
        if patterns.get('if_statements'):
            dot.append("    if_stmt [shape=diamond, fillcolor=yellow, label=\"If Statement\"];")
        
        if patterns.get('for_loops'):
            dot.append("    for_loop [shape=box, fillcolor=orange, label=\"For Loop\"];")
        
        if patterns.get('while_loops'):
            dot.append("    while_loop [shape=box, fillcolor=orange, label=\"While Loop\"];")
        
        dot.append("    end [shape=oval, fillcolor=red, label=\"End\"];")
        dot.append("")
        
        # Add edges
        dot.append("    start -> if_stmt;")
        
        # Connect functions
        func_nodes = [f for f in patterns.get('functions', [])[:10]]
        for i, func in enumerate(func_nodes):
            func_id = func['name'].replace('-', '_').replace(' ', '_')
            if i == 0:
                dot.append(f"    start -> {func_id};")
            else:
                prev_func = func_nodes[i-1]
                prev_id = prev_func['name'].replace('-', '_').replace(' ', '_')
                dot.append(f"    {prev_id} -> {func_id};")
        
        # Connect control flow
        if func_nodes:
            last_func = func_nodes[-1]
            last_id = last_func['name'].replace('-', '_').replace(' ', '_')
            dot.append(f"    {last_id} -> end;")
        else:
            dot.append("    if_stmt -> end;")
        
        dot.append("}")
        
        return "\n".join(dot)
    
    def _save_diagrams(self, base_output_file: str, plantuml: str, mermaid: str, dot: str):
        """Save diagrams to files."""
        base_path = Path(base_output_file).stem
        
        # Save PlantUML
        plantuml_file = f"{base_path}.puml"
        with open(plantuml_file, 'w') as f:
            f.write(plantuml)
        
        # Save Mermaid
        mermaid_file = f"{base_path}.mmd"
        with open(mermaid_file, 'w') as f:
            f.write(mermaid)
        
        # Save DOT
        dot_file = f"{base_path}.dot"
        with open(dot_file, 'w') as f:
            f.write(dot)
    
    def _generate_visual_output(self, plantuml_content: str, output_file: str = None) -> Dict[str, Any]:
        """Generate visual output using PlantUML if available."""
        try:
            # Check if PlantUML is available
            result = subprocess.run(
                ["plantuml", "-version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # PlantUML is available, generate PNG
                if output_file:
                    base_path = Path(output_file).stem
                    png_file = f"{base_path}.png"
                    
                    # Create temporary PlantUML file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as f:
                        f.write(plantuml_content)
                        temp_file = f.name
                    
                    # Generate PNG
                    subprocess.run([
                        "plantuml", "-tpng", temp_file
                    ], cwd=os.path.dirname(temp_file))
                    
                    # Clean up temp file
                    os.unlink(temp_file)
                    
                    return {
                        'success': True,
                        'png_file': png_file,
                        'plantuml_available': True
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No output file specified for PNG generation',
                        'plantuml_available': True
                    }
            else:
                return {
                    'success': False,
                    'error': 'PlantUML not available',
                    'plantuml_available': False
                }
                
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'PlantUML command not found',
                'plantuml_available': False
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'plantuml_available': False
            }
    
    def generate_project_diagrams(self, source_dir: str = "src", output_dir: str = "diagrams") -> Dict[str, Any]:
        """
        Generate activity diagrams for all Python files in a directory.
        
        Args:
            source_dir: Directory containing Python files
            output_dir: Directory to save generated diagrams
            
        Returns:
            Batch generation results
        """
        source_path = Path(source_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        python_files = list(source_path.rglob("*.py"))
        results = []
        
        for python_file in python_files[:5]:  # Limit to first 5 files for testing
            try:
                output_file = output_path / f"{python_file.stem}_workflow"
                result = self.generate_activity_diagram(str(python_file), str(output_file))
                result['source_file'] = str(python_file)
                result['output_file'] = str(output_file)
                results.append(result)
                
            except Exception as e:
                results.append({
                    'success': False,
                    'source_file': str(python_file),
                    'error': str(e)
                })
        
        return {
            'total_files': len(python_files),
            'processed_files': len(results),
            'successful_generations': len([r for r in results if r['success']]),
            'failed_generations': len([r for r in results if not r['success']]),
            'results': results
        }


def test_uml_generator():
    """Test the UML activity diagram generator."""
    generator = UMLActivityGenerator()
    
    # Test with a single file
    test_file = "src/enhanced_activity_generator.py"
    output_file = "test_workflow"
    
    print("Testing UML Activity Diagram Generation:")
    print("=" * 50)
    
    # Generate diagram
    result = generator.generate_activity_diagram(test_file, output_file)
    
    if result['success']:
        print(f"✅ Diagram generation successful!")
        print(f"Source file: {result['source_file']}")
        print(f"Output file: {result['output_file']}")
        
        print(f"\nControl Flow Summary:")
        summary = result['control_flow_summary']
        print(f"  Total Patterns: {summary['total_patterns']}")
        print(f"  Recognized Patterns: {summary['recognized_patterns']}")
        print(f"  Complexity: {summary['complexity']}")
        
        print(f"\nGenerated Files:")
        print(f"  PlantUML: {output_file}.puml")
        print(f"  Mermaid: {output_file}.mmd")
        print(f"  DOT: {output_file}.dot")
        
        if result['visual_output']['success']:
            print(f"  PNG: {result['visual_output']['png_file']}")
        else:
            print(f"  PNG: Not generated ({result['visual_output']['error']})")
        
        # Show sample PlantUML content
        print(f"\nSample PlantUML Content:")
        plantuml_lines = result['plantuml'].split('\n')[:10]
        for line in plantuml_lines:
            print(f"  {line}")
        if len(result['plantuml'].split('\n')) > 10:
            print(f"  ... ({len(result['plantuml'].split('\n')) - 10} more lines)")
        
    else:
        print(f"❌ Diagram generation failed: {result['error']}")
    
    return result


if __name__ == "__main__":
    test_uml_generator()
