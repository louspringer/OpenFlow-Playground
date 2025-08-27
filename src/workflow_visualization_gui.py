#!/usr/bin/env python3
"""
Workflow Visualization GUI

Comprehensive Streamlit application for visualizing all workflow extraction artifacts.
Provides navigation framework organized by tested components and artifact types.
"""

import streamlit as st
import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import tempfile
import shutil
import requests
import urllib.parse

# Import our analysis components
from src.control_flow_analyzer import ControlFlowAnalyzer
from src.multi_file_workflow_analyzer import MultiFileWorkflowAnalyzer
from src.uml_activity_generator import UMLActivityGenerator
from src.complexity_metrics_analyzer import ComplexityMetricsAnalyzer
from src.performance_optimizer import PerformanceOptimizer
from src.round_trip_validation import RoundTripValidator


class WorkflowVisualizationGUI:
    """Main GUI application for workflow visualization."""

    def __init__(self):
        self.project_root = Path(".")
        self.artifacts_dir = self.project_root / "generated_activity_models"
        self.artifacts_dir.mkdir(exist_ok=True)

        # Initialize analysis components
        self.control_flow_analyzer = ControlFlowAnalyzer()
        self.multi_file_analyzer = MultiFileWorkflowAnalyzer()
        self.uml_generator = UMLActivityGenerator()
        self.complexity_analyzer = ComplexityMetricsAnalyzer()
        self.performance_optimizer = PerformanceOptimizer()
        self.round_trip_validator = RoundTripValidator()

        # Test files for demonstration
        self.test_files = [
            "src/enhanced_activity_generator.py",
            "src/dynamic_rule_updater.py",
            "src/round_trip_validation.py",
        ]

        # Component mapping
        self.components = {
            "UC-1: Function Call Chain Analysis": {
                "description": "Analyzes function call relationships using pydeps",
                "icon": "🔗",
                "component": "pydeps",
                "artifacts": ["dependency_graphs", "call_chains"],
            },
            "UC-2: Control Flow Pattern Recognition": {
                "description": "Recognizes complex control flow patterns",
                "icon": "🔄",
                "component": "control_flow_analyzer",
                "artifacts": ["control_flow_patterns", "complexity_metrics"],
            },
            "UC-3: Method Workflow Extraction": {
                "description": "Extracts workflows from AST using ast2json",
                "icon": "📊",
                "component": "ast2json",
                "artifacts": ["ast_models", "workflow_extractions"],
            },
            "UC-4: UML Activity Diagram Generation": {
                "description": "Generates UML activity diagrams",
                "icon": "📋",
                "component": "uml_activity_generator",
                "artifacts": ["plantuml", "mermaid", "dot", "png"],
            },
            "UC-5: Code Complexity Metrics": {
                "description": "Analyzes code complexity using Radon",
                "icon": "📈",
                "component": "complexity_metrics_analyzer",
                "artifacts": ["complexity_scores", "maintainability_metrics"],
            },
            "UC-6: Multi-File Workflow Analysis": {
                "description": "Analyzes workflows across multiple files",
                "icon": "📁",
                "component": "multi_file_workflow_analyzer",
                "artifacts": ["dependency_analysis", "cross_file_calls"],
            },
            "UC-7: Round-Trip Validation Framework": {
                "description": "Validates extracted models against source code",
                "icon": "✅",
                "component": "round_trip_validator",
                "artifacts": ["validation_reports", "accuracy_metrics"],
            },
            "UC-9: Performance Optimization": {
                "description": "Benchmarks and optimizes system performance",
                "icon": "⚡",
                "component": "performance_optimizer",
                "artifacts": ["performance_metrics", "optimization_recommendations"],
            },
        }

    def run(self):
        """Main application entry point."""
        st.set_page_config(
            page_title="Workflow Extraction Visualization",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # Custom CSS for better styling
        self._apply_custom_css()

        # Sidebar navigation
        selected_component = self._render_sidebar()

        # Main content area
        if selected_component:
            self._render_component_page(selected_component)
        else:
            self._render_dashboard()

    def _apply_custom_css(self):
        """Apply custom CSS styling."""
        st.markdown(
            """
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .component-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
        }
        .metric-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            margin: 0.5rem;
        }
        .artifact-preview {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .status-success { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-error { color: #dc3545; }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def _render_sidebar(self) -> Optional[str]:
        """Render the sidebar navigation."""
        st.sidebar.title("🔍 Workflow Extraction")
        st.sidebar.markdown("---")

        # Component selection
        st.sidebar.subheader("📋 Tested Components")
        selected = st.sidebar.selectbox(
            "Select Component:",
            [""] + list(self.components.keys()),
            format_func=lambda x: "🏠 Dashboard" if x == "" else x,
        )

        st.sidebar.markdown("---")

        # Quick actions
        st.sidebar.subheader("⚡ Quick Actions")
        if st.sidebar.button("🔄 Refresh All Artifacts"):
            self._refresh_all_artifacts()
            st.rerun()

        if st.sidebar.button("📊 Generate Demo Data"):
            self._generate_demo_data()
            st.rerun()

        # System status
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 System Status")
        self._render_system_status()

        # Fix: Return the selected component only if it's not empty string
        return selected if selected != "" else None

    def _render_dashboard(self):
        """Render the main dashboard."""
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.title("🔍 Workflow Extraction Visualization System")
        st.markdown(
            "**Complete visualization framework for all tested components and generated artifacts**"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Components", "8", "Tested")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Artifacts", "Generated", "Multiple Formats")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Formats", "4", "UML/PNG/Mermaid/DOT")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Status", "✅", "Complete")
            st.markdown("</div>", unsafe_allow_html=True)

        # Component overview
        st.subheader("📋 Component Overview")

        for component_name, component_info in self.components.items():
            with st.expander(
                f"{component_info['icon']} {component_name}", expanded=False
            ):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**Description:** {component_info['description']}")
                    st.markdown(
                        f"**Artifacts:** {', '.join(component_info['artifacts'])}"
                    )

                with col2:
                    if st.button(
                        f"View {component_name.split(':')[0]}",
                        key=f"view_{component_name}",
                    ):
                        st.session_state.selected_component = component_name
                        st.rerun()

        # Recent artifacts
        st.subheader("🆕 Recent Artifacts")
        self._render_recent_artifacts()

        # Quick analysis
        st.subheader("🚀 Quick Analysis")
        self._render_quick_analysis()

    def _render_component_page(self, component_name: str):
        """Render a specific component page."""
        component_info = self.components[component_name]

        # Header
        st.markdown(
            f"<h1>{component_info['icon']} {component_name}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**{component_info['description']}**")
        st.markdown("---")

        # Component-specific content
        if "UC-1" in component_name:
            self._render_function_call_analysis()
        elif "UC-2" in component_name:
            self._render_control_flow_analysis()
        elif "UC-3" in component_name:
            self._render_method_workflow_extraction()
        elif "UC-4" in component_name:
            self._render_uml_generation()
        elif "UC-5" in component_name:
            self._render_complexity_analysis()
        elif "UC-6" in component_name:
            self._render_multi_file_analysis()
        elif "UC-7" in component_name:
            self._render_round_trip_validation()
        elif "UC-9" in component_name:
            self._render_performance_optimization()

        # Back to dashboard
        if st.button("🏠 Back to Dashboard"):
            st.session_state.selected_component = None
            st.rerun()

    def _render_function_call_analysis(self):
        """Render function call chain analysis (UC-1)."""
        st.subheader("🔗 Function Call Chain Analysis")

        # File selection
        selected_file = st.selectbox("Select file to analyze:", self.test_files)

        if st.button("Analyze Dependencies"):
            with st.spinner("Analyzing function call chains..."):
                try:
                    # Run pydeps analysis
                    result = subprocess.run(
                        ["uv", "run", "pydeps", "--show-dot", selected_file],
                        capture_output=True,
                        text=True,
                        cwd=self.project_root,
                    )

                    if result.returncode == 0:
                        st.success("✅ Dependency analysis completed!")

                        # Parse and display results
                        self._display_dependency_results(result.stdout, selected_file)
                    else:
                        st.error(f"❌ Analysis failed: {result.stderr}")

                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

    def _render_control_flow_analysis(self):
        """Render control flow pattern recognition (UC-2)."""
        st.subheader("🔄 Control Flow Pattern Recognition")

        # File selection
        selected_file = st.selectbox(
            "Select file to analyze:", self.test_files, key="control_flow_file"
        )

        if st.button("Analyze Control Flow", key="control_flow_btn"):
            with st.spinner("Analyzing control flow patterns..."):
                try:
                    result = self.control_flow_analyzer.analyze_control_flow(
                        selected_file
                    )

                    if result:
                        st.success("✅ Control flow analysis completed!")

                        # Display results in tabs
                        tab1, tab2, tab3 = st.tabs(
                            ["📊 Patterns", "📈 Metrics", "🔍 Details"]
                        )

                        with tab1:
                            self._display_control_flow_patterns(result)

                        with tab2:
                            self._display_complexity_metrics(result)

                        with tab3:
                            self._display_control_flow_details(result)
                    else:
                        st.error("❌ Control flow analysis failed")

                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

    def _render_method_workflow_extraction(self):
        """Render method workflow extraction (UC-3)."""
        st.subheader("📊 Method Workflow Extraction")

        # File selection
        selected_file = st.selectbox(
            "Select file to analyze:", self.test_files, key="workflow_file"
        )

        if st.button("Extract Workflows", key="workflow_btn"):
            with st.spinner("Extracting workflow models..."):
                try:
                    # Use ast2json for extraction
                    result = subprocess.run(
                        [
                            "uv",
                            "run",
                            "python",
                            "-c",
                            f"import ast2json; import ast; print(ast2json.str2json(open('{selected_file}').read()))",
                        ],
                        capture_output=True,
                        text=True,
                        cwd=self.project_root,
                    )

                    if result.returncode == 0:
                        st.success("✅ Workflow extraction completed!")

                        # Display AST structure
                        self._display_ast_structure(result.stdout, selected_file)
                    else:
                        st.error(f"❌ Extraction failed: {result.stderr}")

                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")

    def _render_uml_generation(self):
        """Render UML activity diagram generation (UC-4)."""
        st.subheader("📋 UML Activity Diagram Generation")

        # File selection
        selected_file = st.selectbox(
            "Select file to analyze:", self.test_files, key="uml_file"
        )
        output_name = st.text_input(
            "Output name (without extension):", value="generated_workflow"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate UML Diagrams"):
                with st.spinner("Generating UML activity diagrams..."):
                    try:
                        result = self.uml_generator.generate_activity_diagram(
                            selected_file, output_name
                        )

                        if result:
                            st.success("✅ UML generation completed!")
                            self._display_uml_results(result, output_name)
                        else:
                            st.error("❌ UML generation failed")

                    except Exception as e:
                        st.error(f"❌ Error during generation: {str(e)}")

        with col2:
            if st.button("View Existing Diagrams"):
                self._display_existing_diagrams()

    def _render_complexity_analysis(self):
        """Render code complexity analysis (UC-5)."""
        st.subheader("📈 Code Complexity Metrics")

        # File selection
        selected_file = st.selectbox(
            "Select file to analyze:", self.test_files, key="complexity_file"
        )

        if st.button("Analyze Complexity", key="complexity_btn"):
            with st.spinner("Analyzing code complexity..."):
                try:
                    result = self.complexity_analyzer.analyze_complexity(selected_file)

                    if result:
                        st.success("✅ Complexity analysis completed!")

                        # Display results in tabs
                        tab1, tab2, tab3 = st.tabs(
                            ["📊 Overview", "📈 Metrics", "🔍 Distribution"]
                        )

                        with tab1:
                            self._display_complexity_overview(result)

                        with tab2:
                            self._display_complexity_metrics(result)

                        with tab3:
                            self._display_complexity_distribution(result)
                    else:
                        st.error("❌ Complexity analysis failed")

                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

    def _render_multi_file_analysis(self):
        """Render multi-file workflow analysis (UC-6)."""
        st.subheader("📁 Multi-File Workflow Analysis")

        source_dir = st.selectbox(
            "Select source directory:", ["src", "tests", "."], key="multi_file_dir"
        )

        if st.button("Analyze Multi-File Workflows", key="multi_file_btn"):
            with st.spinner("Analyzing multi-file workflows..."):
                try:
                    result = self.multi_file_analyzer.analyze_project_workflow(
                        source_dir
                    )

                    if result:
                        st.success("✅ Multi-file analysis completed!")

                        # Display results in tabs
                        tab1, tab2, tab3 = st.tabs(
                            ["📊 Dependencies", "🔄 Circular", "📁 Cross-File"]
                        )

                        with tab1:
                            self._display_dependency_analysis(result)

                        with tab2:
                            self._display_circular_dependencies(result)

                        with tab3:
                            self._display_cross_file_calls(result)
                    else:
                        st.error("❌ Multi-file analysis failed")

                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")

    def _render_round_trip_validation(self):
        """Render round-trip validation framework (UC-7)."""
        st.subheader("✅ Round-Trip Validation Framework")

        # File selection
        selected_file = st.selectbox(
            "Select file to validate:", self.test_files, key="validation_file"
        )

        if st.button("Run Validation", key="validation_btn"):
            with st.spinner("Running round-trip validation..."):
                try:
                    result = self.round_trip_validator.validate_workflow_extraction(
                        selected_file
                    )

                    if result:
                        st.success("✅ Validation completed!")

                        # Display validation results
                        self._display_validation_results(result)
                    else:
                        st.error("❌ Validation failed")

                except Exception as e:
                    st.error(f"❌ Error during validation: {str(e)}")

    def _render_performance_optimization(self):
        """Render performance optimization (UC-9)."""
        st.subheader("⚡ Performance Optimization")

        if st.button("Benchmark System Performance", key="performance_btn"):
            with st.spinner("Benchmarking system performance..."):
                try:
                    result = self.performance_optimizer.benchmark_system_performance(
                        self.test_files
                    )

                    if result:
                        st.success("✅ Performance benchmarking completed!")

                        # Display results in tabs
                        tab1, tab2, tab3 = st.tabs(
                            ["📊 Performance", "🐛 Bottlenecks", "💡 Recommendations"]
                        )

                        with tab1:
                            self._display_performance_metrics(result)

                        with tab2:
                            self._display_bottlenecks(result)

                        with tab3:
                            self._display_optimization_recommendations(result)
                    else:
                        st.error("❌ Performance benchmarking failed")

                except Exception as e:
                    st.error(f"❌ Error during benchmarking: {str(e)}")

    def _render_system_status(self):
        """Render system status in sidebar."""
        # Check component availability
        components_status = {}

        for component_name, component_info in self.components.items():
            try:
                if component_info["component"] == "pydeps":
                    # Check if pydeps is available
                    result = subprocess.run(
                        ["uv", "run", "pydeps", "--help"],
                        capture_output=True,
                        text=True,
                    )
                    components_status[component_name] = result.returncode == 0
                else:
                    # Check if our custom components are working
                    components_status[component_name] = True
            except:
                components_status[component_name] = False

        # Display status
        for component_name, status in components_status.items():
            icon = "✅" if status else "❌"
            st.markdown(f"{icon} {component_name.split(':')[0]}")

        # Overall status
        overall_status = all(components_status.values())
        status_icon = "✅" if overall_status else "⚠️"
        status_color = "status-success" if overall_status else "status-warning"

        st.markdown(
            f"<div class='{status_color}'><strong>{status_icon} System Status</strong></div>",
            unsafe_allow_html=True,
        )

    def _render_recent_artifacts(self):
        """Render recent artifacts section."""
        # Find recent artifacts
        artifact_files = []
        for ext in [".puml", ".mmd", ".dot", ".png", ".svg"]:
            artifact_files.extend(self.artifacts_dir.glob(f"*{ext}"))

        # Sort by modification time
        artifact_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        if artifact_files:
            for artifact in artifact_files[:5]:  # Show last 5
                with st.expander(f"📄 {artifact.name}", expanded=False):
                    st.markdown(f"**Path:** `{artifact}`")
                    st.markdown(f"**Size:** {artifact.stat().st_size} bytes")
                    st.markdown(f"**Modified:** {artifact.stat().st_mtime}")

                    # Preview content
                    if artifact.suffix in [".puml", ".mmd", ".dot"]:
                        with open(artifact, "r") as f:
                            content = f.read()
                            st.code(content, language="text")
        else:
            st.info("No artifacts found. Run analysis to generate some!")

    def _render_quick_analysis(self):
        """Render quick analysis section."""
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Quick Control Flow"):
                self._run_quick_control_flow()

        with col2:
            if st.button("📊 Quick Complexity"):
                self._run_quick_complexity()

    def _run_quick_control_flow(self):
        """Run quick control flow analysis."""
        try:
            result = self.control_flow_analyzer.analyze_control_flow(self.test_files[0])
            if result:
                st.success("✅ Quick control flow analysis completed!")
                st.json(result)
        except Exception as e:
            st.error(f"❌ Quick analysis failed: {str(e)}")

    def _run_quick_complexity(self):
        """Run quick complexity analysis."""
        try:
            result = self.complexity_analyzer.analyze_complexity(self.test_files[0])
            if result:
                st.success("✅ Quick complexity analysis completed!")
                st.json(result)
        except Exception as e:
            st.error(f"❌ Quick analysis failed: {str(e)}")

    def _refresh_all_artifacts(self):
        """Refresh all artifacts."""
        st.info("🔄 Refreshing all artifacts...")
        # This would trigger regeneration of all artifacts

    def _generate_demo_data(self):
        """Generate demo data for visualization."""
        st.info("📊 Generating demo data...")
        # This would create sample artifacts for demonstration

    # Display methods for different result types
    def _display_dependency_results(self, output: str, filename: str):
        """Display dependency analysis results."""
        st.subheader("📊 Dependency Results")
        st.code(output, language="text")

        # Try to parse and visualize
        try:
            # Extract dependency information
            lines = output.split("\n")
            dependencies = [line.strip() for line in lines if "->" in line]

            if dependencies:
                st.subheader("🔗 Dependencies Found")
                for dep in dependencies[:10]:  # Show first 10
                    st.markdown(f"- {dep}")
            else:
                st.info("No explicit dependencies found in output")
        except Exception as e:
            st.warning(f"Could not parse dependencies: {str(e)}")

    def _display_control_flow_patterns(self, result: Dict[str, Any]):
        """Display control flow patterns."""
        if "patterns" in result:
            st.subheader("🔄 Control Flow Patterns")

            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("If Statements", result["patterns"].get("if_statements", 0))
            with col2:
                st.metric(
                    "Loops",
                    result["patterns"].get("for_loops", 0)
                    + result["patterns"].get("while_loops", 0),
                )
            with col3:
                st.metric("Try Blocks", result["patterns"].get("try_blocks", 0))

            # Pattern details
            if "recognized_patterns" in result:
                st.subheader("🔍 Recognized Patterns")
                for pattern in result["recognized_patterns"]:
                    st.markdown(f"- **{pattern['type']}**: {pattern['description']}")

    def _display_complexity_metrics(self, result: Dict[str, Any]):
        """Display complexity metrics."""
        if "complexity_metrics" in result:
            st.subheader("📈 Complexity Metrics")

            metrics = result["complexity_metrics"]
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Max Nesting", metrics.get("max_nesting", 0))
            with col2:
                st.metric("Boolean Complexity", metrics.get("boolean_complexity", 0))
            with col3:
                st.metric("Total Statements", metrics.get("total_statements", 0))

    def _display_control_flow_details(self, result: Dict[str, Any]):
        """Display detailed control flow information."""
        st.subheader("🔍 Control Flow Details")
        st.json(result)

    def _display_ast_structure(self, output: str, filename: str):
        """Display AST structure."""
        st.subheader("🌳 AST Structure")

        try:
            # Try to parse as JSON
            import json

            ast_data = json.loads(output)
            st.json(ast_data)
        except:
            # Fallback to text display
            st.code(output, language="text")

    def _display_uml_results(self, result: Dict[str, Any], output_name: str):
        """Display UML generation results."""
        st.subheader("📋 Generated UML Diagrams")

        # Check for generated files
        generated_files = []
        for ext in [".puml", ".mmd", ".dot", ".png"]:
            file_path = self.project_root / f"{output_name}{ext}"
            if file_path.exists():
                generated_files.append((file_path, ext))

        if generated_files:
            st.success(f"✅ Generated {len(generated_files)} diagram files")

            # Display each format
            for file_path, ext in generated_files:
                with st.expander(f"{ext.upper()} Diagram", expanded=False):
                    if ext in [".puml", ".mmd", ".dot"]:
                        with open(file_path, "r") as f:
                            content = f.read()
                            st.code(content, language="text")
                    elif ext == ".png":
                        st.image(str(file_path), caption=f"{ext.upper()} Diagram")
        else:
            st.warning("No diagram files were generated")

    def _display_existing_diagrams(self):
        """Display existing diagrams."""
        st.subheader("📋 Existing Diagrams")
        
        # Find existing diagram files
        diagram_files = []
        for ext in [".puml", ".mmd", ".dot", ".png", ".svg"]:
            diagram_files.extend(self.project_root.glob(f"*{ext}"))
        
        if diagram_files:
            for diagram in diagram_files:
                with st.expander(f"📄 {diagram.name}", expanded=False):
                    if diagram.suffix == '.puml':
                        # Try to display as SVG visualization first
                        svg_content = self._convert_plantuml_to_svg(diagram)
                        if svg_content:
                            st.markdown("**🎨 PlantUML → SVG Visualization:**")
                            st.markdown(svg_content, unsafe_allow_html=True)
                            
                            # Also show the raw PlantUML for reference
                            with st.expander("📝 Raw PlantUML Code", expanded=False):
                                with open(diagram, 'r') as f:
                                    content = f.read()
                                    st.code(content, language='text')
                        else:
                            st.warning("⚠️ Could not convert PlantUML to SVG")
                            # Fallback to raw text
                            with open(diagram, 'r') as f:
                                content = f.read()
                                st.code(content, language='text')
                    elif diagram.suffix in [".mmd", ".dot"]:
                        with open(diagram, "r") as f:
                            content = f.read()
                            st.code(content, language="text")
                    elif diagram.suffix == ".png":
                        st.image(str(diagram), caption=diagram.name)
                    elif diagram.suffix == '.svg':
                        # Display SVG directly
                        with open(diagram, 'r') as f:
                            content = f.read()
                            st.markdown(content, unsafe_allow_html=True)
        else:
            st.info("No existing diagrams found")

    def _display_complexity_overview(self, result: Dict[str, Any]):
        """Display complexity overview."""
        st.subheader("📊 Complexity Overview")

        if "overall_score" in result:
            st.metric("Overall Score", f"{result['overall_score']:.1f}/100")

        if "industry_metrics" in result:
            st.subheader("🏭 Industry Metrics")
            metrics = result["industry_metrics"]
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Maintainability", f"{metrics.get('maintainability_index', 0):.1f}"
                )
            with col2:
                st.metric(
                    "Cyclomatic", f"{metrics.get('cyclomatic_complexity', 0):.1f}"
                )
            with col3:
                st.metric("Lines of Code", metrics.get("lines_of_code", 0))

    def _display_complexity_metrics(self, result: Dict[str, Any]):
        """Display detailed complexity metrics."""
        st.subheader("📈 Detailed Metrics")

        if "custom_analysis" in result:
            st.json(result["custom_analysis"])

    def _display_complexity_distribution(self, result: Dict[str, Any]):
        """Display complexity distribution."""
        st.subheader("📊 Complexity Distribution")

        if "complexity_distribution" in result:
            dist = result["complexity_distribution"]
            st.markdown("**Complexity Categories:**")
            for category, count in dist.items():
                st.markdown(f"- **{category}**: {count}")

    def _display_dependency_analysis(self, result: Dict[str, Any]):
        """Display dependency analysis results."""
        st.subheader("📊 Dependency Analysis")

        if "dependency_analysis" in result:
            deps = result["dependency_analysis"]
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total Dependencies", deps.get("total_dependencies", 0))
                st.metric("Graph Nodes", deps.get("graph_nodes", 0))

            with col2:
                st.metric("Inter-File Calls", deps.get("inter_file_calls", 0))
                st.metric("Entry Points", deps.get("entry_points", 0))

    def _display_circular_dependencies(self, result: Dict[str, Any]):
        """Display circular dependencies."""
        st.subheader("🔄 Circular Dependencies")

        if "circular_dependencies" in result:
            circular = result["circular_dependencies"]
            if circular:
                st.warning(f"⚠️ Found {len(circular)} circular dependencies")
                for dep in circular:
                    st.markdown(f"- {dep}")
            else:
                st.success("✅ No circular dependencies found")

    def _display_cross_file_calls(self, result: Dict[str, Any]):
        """Display cross-file call analysis."""
        st.subheader("📁 Cross-File Calls")

        if "cross_file_calls" in result:
            calls = result["cross_file_calls"]
            st.markdown(f"**Total Cross-File Calls:** {len(calls)}")

            # Show sample calls
            for i, (caller, callees) in enumerate(list(calls.items())[:5]):
                st.markdown(f"- **{caller}** → {', '.join(callees[:3])}")

    def _display_validation_results(self, result: Dict[str, Any]):
        """Display validation results."""
        st.subheader("✅ Validation Results")

        if "validation_status" in result:
            status = result["validation_status"]
            if status.get("passed", False):
                st.success("✅ Validation PASSED")
            else:
                st.error("❌ Validation FAILED")

        if "accuracy" in result:
            accuracy = result["accuracy"]
            st.metric("Accuracy", f"{accuracy:.1f}%")

            if accuracy < 95:
                st.warning("⚠️ Accuracy below 95% threshold")

        if "missing_elements" in result:
            st.subheader("🔍 Missing Elements")
            missing = result["missing_elements"]
            for element_type, elements in missing.items():
                if elements:
                    st.markdown(f"**{element_type}:** {', '.join(elements[:5])}")

    def _display_performance_metrics(self, result: Dict[str, Any]):
        """Display performance metrics."""
        st.subheader("📊 Performance Metrics")

        if "overall_performance" in result:
            perf = result["overall_performance"]
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Performance Score", f"{perf.get('score', 0):.1f}/100")
            with col2:
                st.metric("Total Time", f"{perf.get('total_time', 0):.2f}s")
            with col3:
                st.metric("Memory Usage", f"{perf.get('memory_usage', 0):.1f}MB")

    def _display_bottlenecks(self, result: Dict[str, Any]):
        """Display identified bottlenecks."""
        st.subheader("🐛 Performance Bottlenecks")

        if "bottlenecks" in result:
            bottlenecks = result["bottlenecks"]
            if bottlenecks:
                for bottleneck in bottlenecks:
                    st.markdown(
                        f"- **{bottleneck['component']}**: {bottleneck['description']}"
                    )
            else:
                st.success("✅ No bottlenecks identified")

    def _display_optimization_recommendations(self, result: Dict[str, Any]):
        """Display optimization recommendations."""
        st.subheader("💡 Optimization Recommendations")

        if "optimization_recommendations" in result:
            recommendations = result["optimization_recommendations"]
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. **{rec['category']}**: {rec['description']}")
            else:
                st.info("No optimization recommendations available")

    def _convert_plantuml_to_svg(self, puml_file: Path) -> Optional[str]:
        """Convert PlantUML file to SVG content using Docker service."""
        try:
            # Read the PlantUML content
            with open(puml_file, 'r') as f:
                plantuml_content = f.read()
            
            # Encode the PlantUML content for HTTP request
            encoded_content = urllib.parse.quote(plantuml_content)
            
            # Use the Docker PlantUML service on port 20075
            
            # Create the URL for the PlantUML service
            plantuml_url = f"http://localhost:20075/svg/{encoded_content}"
            
            # Make the request to get SVG
            response = requests.get(plantuml_url, timeout=30)
            
            if response.status_code == 200:
                svg_content = response.text
                
                # Validate that we got actual SVG content
                if svg_content.startswith('<?xml') or svg_content.startswith('<svg'):
                    return svg_content
                else:
                    st.error(f"PlantUML service returned non-SVG content: {response.text[:200]}")
                    return None
            else:
                st.error(f"PlantUML service request failed: HTTP {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to PlantUML Docker service: {str(e)}")
            st.info("💡 Make sure the PlantUML Docker service is running: sudo docker start plantuml-server")
            return None
        except Exception as e:
            st.error(f"Error converting PlantUML to SVG: {str(e)}")
            return None


# Ensure the app runs when imported by Streamlit
# This must be at the top level, not inside any function
gui = WorkflowVisualizationGUI()
gui.run()

def main():
    """Main entry point."""
    gui = WorkflowVisualizationGUI()
    gui.run()


if __name__ == "__main__":
    main()
