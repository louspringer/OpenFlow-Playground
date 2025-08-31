#!/usr/bin/env python3
"""
Round-Trip Engineering Streamlit Demo App

A Streamlit application that showcases the refactored round-trip engineering system
with interactive demos, real-time monitoring, and performance visualization.
"""

import asyncio
import json
import streamlit as st
import time
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add src to path for imports
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from .demo_orchestrator import DemoOrchestrator

# Configure Streamlit page
st.set_page_config(
    page_title="Round-Trip Engineering Demo",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .demo-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .info-message {
        color: #17a2b8;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "demo_orchestrator" not in st.session_state:
    st.session_state.demo_orchestrator = DemoOrchestrator()
if "demo_results" not in st.session_state:
    st.session_state.demo_results = {}
if "current_demo" not in st.session_state:
    st.session_state.current_demo = None


def main():
    """Main Streamlit application."""

    # Header
    st.markdown(
        '<h1 class="main-header">🔄 Round-Trip Engineering Demo</h1>',
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.header("🎯 Demo Controls")

        # Demo selection
        demo_type = st.selectbox(
            "Select Demo Type",
            ["Basic Demo", "Advanced Demo", "Performance Demo", "All Demos"],
        )

        # Run button
        if st.button("🚀 Run Demo", type="primary"):
            st.session_state.current_demo = demo_type
            run_demo(demo_type)

        # Status
        st.header("📊 System Status")
        display_system_status()

        # Navigation
        st.header("🧭 Navigation")
        page = st.selectbox(
            "Select Page",
            [
                "Demo Dashboard",
                "Performance Analysis",
                "Generated Code",
                "System Architecture",
            ],
        )

    # Main content based on navigation
    if page == "Demo Dashboard":
        show_demo_dashboard()
    elif page == "Performance Analysis":
        show_performance_analysis()
    elif page == "Generated Code":
        show_generated_code()
    elif page == "System Architecture":
        show_system_architecture()


def run_demo(demo_type: str):
    """Run the selected demo type."""
    try:
        with st.spinner(f"Running {demo_type}..."):
            if demo_type == "Basic Demo":
                result = asyncio.run(
                    st.session_state.demo_orchestrator.run_basic_demo()
                )
            elif demo_type == "Advanced Demo":
                result = asyncio.run(
                    st.session_state.demo_orchestrator.run_advanced_demo()
                )
            elif demo_type == "Performance Demo":
                result = asyncio.run(
                    st.session_state.demo_orchestrator.run_performance_demo()
                )
            elif demo_type == "All Demos":
                result = run_all_demos()
            else:
                st.error(f"Unknown demo type: {demo_type}")
                return

            st.session_state.demo_results[demo_type] = result
            st.success(f"✅ {demo_type} completed successfully!")

    except Exception as e:
        st.error(f"❌ Demo failed: {e}")


def run_all_demos():
    """Run all demo types sequentially."""
    results = {}

    # Basic Demo
    with st.spinner("Running Basic Demo..."):
        results["Basic Demo"] = asyncio.run(
            st.session_state.demo_orchestrator.run_basic_demo()
        )

    # Advanced Demo
    with st.spinner("Running Advanced Demo..."):
        results["Advanced Demo"] = asyncio.run(
            st.session_state.demo_orchestrator.run_advanced_demo()
        )

    # Performance Demo
    with st.spinner("Running Performance Demo..."):
        results["Performance Demo"] = asyncio.run(
            st.session_state.demo_orchestrator.run_performance_demo()
        )

    return results


def display_system_status():
    """Display system status in sidebar."""
    try:
        status = asyncio.run(st.session_state.demo_orchestrator.get_module_status())

        # Status indicator
        if status.status.value == "available":
            st.success("🟢 System Available")
        elif status.status.value == "partially_available":
            st.warning("🟡 System Partially Available")
        else:
            st.error("🔴 System Not Available")

        # Health indicators
        st.metric(
            "Success Rate", f"{status.health_indicators.get('success_rate', 0):.1%}"
        )
        st.metric("Success Count", status.health_indicators.get("success_count", 0))
        st.metric("Error Count", status.health_indicators.get("error_count", 0))

    except Exception as e:
        st.error(f"Status Error: {e}")


def show_demo_dashboard():
    """Show the main demo dashboard."""
    st.header("🎯 Demo Dashboard")

    # Demo results display
    if st.session_state.demo_results:
        for demo_name, results in st.session_state.demo_results.items():
            with st.expander(f"📊 {demo_name} Results", expanded=True):
                display_demo_results(results)
    else:
        st.info("👆 Select a demo type and click 'Run Demo' to get started!")

    # Quick demo buttons
    st.header("⚡ Quick Demos")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Basic Demo", use_container_width=True):
            run_demo("Basic Demo")

    with col2:
        if st.button("🚀 Advanced Demo", use_container_width=True):
            run_demo("Advanced Demo")

    with col3:
        if st.button("🚀 Performance Demo", use_container_width=True):
            run_demo("Performance Demo")


def display_demo_results(results: Dict[str, Any]):
    """Display demo results in an organized way."""
    if results.get("status") == "success":
        st.success("✅ Demo completed successfully!")

        # Basic metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            if "duration" in results:
                st.metric("Duration", f"{results['duration']:.3f}s")

        with col2:
            if "components_count" in results:
                st.metric("Components", results["components_count"])

        with col3:
            if "generated_files_count" in results:
                st.metric("Files Generated", results["generated_files_count"])

        # Detailed results
        if "generated_files" in results:
            st.subheader("📁 Generated Files")
            for filename in results["generated_files"]:
                st.code(filename, language="text")

        # Performance results
        if results.get("demo_type") == "performance":
            display_performance_results(results)

        # Vocabulary alignment
        if "vocabulary_alignment" in results:
            display_vocabulary_alignment(results["vocabulary_alignment"])

        # Raw results
        with st.expander("🔍 Raw Results"):
            st.json(results)

    else:
        st.error("❌ Demo failed!")
        if "error" in results:
            st.error(f"Error: {results['error']}")


def display_performance_results(results: Dict[str, Any]):
    """Display performance demo results."""
    st.subheader("📈 Performance Metrics")

    # Performance score
    if "performance_score" in results:
        score = results["performance_score"]
        if score == "excellent":
            st.success(f"🏆 Performance Score: {score}")
        else:
            st.info(f"📊 Performance Score: {score}")

    # Performance chart
    if "results" in results:
        df_data = []
        for result in results["results"]:
            df_data.append(
                {
                    "Iteration": result["iteration"],
                    "Duration (s)": result["duration"],
                    "Components": result["components"],
                    "Files Generated": result["files_generated"],
                }
            )

        # Duration chart
        fig = px.line(
            df_data,
            x="Iteration",
            y="Duration (s)",
            title="Performance Over Iterations",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Duration", f"{results.get('total_duration', 0):.3f}s")
        with col2:
            st.metric("Iterations", results.get("iterations", 0))
        with col3:
            st.metric("Avg Time", f"{results.get('average_iteration_time', 0):.3f}s")


def display_vocabulary_alignment(alignment: Dict[str, Any]):
    """Display vocabulary alignment results."""
    st.subheader("🔤 Vocabulary Alignment")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Status", alignment.get("status", "unknown"))

    with col2:
        if "alignment_score" in alignment:
            score = alignment["alignment_score"]
            if score > 0.9:
                st.success(f"Score: {score:.1%}")
            elif score > 0.7:
                st.warning(f"Score: {score:.1%}")
            else:
                st.error(f"Score: {score:.1%}")

    with col3:
        st.metric("Matches", alignment.get("vocabulary_matches", 0))

    with col4:
        st.metric("Mismatches", alignment.get("vocabulary_mismatches", 0))

    # Health indicator
    health = alignment.get("overall_health", "unknown")
    if health == "excellent":
        st.success(f"🏆 Overall Health: {health}")
    elif health == "good":
        st.info(f"✅ Overall Health: {health}")
    else:
        st.warning(f"⚠️ Overall Health: {health}")


def show_performance_analysis():
    """Show performance analysis page."""
    st.header("📈 Performance Analysis")

    if not st.session_state.demo_results:
        st.info("👆 Run some demos first to see performance analysis!")
        return

    # Performance comparison chart
    performance_data = []
    for demo_name, results in st.session_state.demo_results.items():
        if results.get("status") == "success" and "duration" in results:
            performance_data.append(
                {
                    "Demo": demo_name,
                    "Duration (s)": results["duration"],
                    "Type": results.get("demo_type", "unknown"),
                }
            )

    if performance_data:
        fig = px.bar(
            performance_data,
            x="Demo",
            y="Duration (s)",
            title="Demo Performance Comparison",
            color="Type",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Performance insights
        st.subheader("💡 Performance Insights")

        durations = [d["Duration (s)"] for d in performance_data]
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Duration", f"{avg_duration:.3f}s")
        with col2:
            st.metric("Fastest Demo", f"{min_duration:.3f}s")
        with col3:
            st.metric("Slowest Demo", f"{max_duration:.3f}s")

    # System health over time
    st.subheader("🏥 System Health Trends")
    try:
        status = asyncio.run(st.session_state.demo_orchestrator.get_module_status())

        # Create a simple health chart
        health_data = {
            "Success Rate": status.health_indicators.get("success_rate", 0),
            "Success Count": status.health_indicators.get("success_count", 0),
            "Error Count": status.health_indicators.get("error_count", 0),
        }

        fig = go.Figure(
            data=[go.Bar(x=list(health_data.keys()), y=list(health_data.values()))]
        )
        fig.update_layout(title="Current System Health Metrics")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Could not load system health: {e}")


def show_generated_code():
    """Show generated code page."""
    st.header("📝 Generated Code")

    if not st.session_state.demo_results:
        st.info("👆 Run some demos first to see generated code!")
        return

    # Find generated files
    generated_files = []
    for demo_name, results in st.session_state.demo_results.items():
        if results.get("status") == "success" and "generated_files" in results:
            for filename in results["generated_files"]:
                generated_files.append(
                    {"demo": demo_name, "filename": filename, "results": results}
                )

    if generated_files:
        st.subheader(f"📁 Generated Files ({len(generated_files)})")

        for file_info in generated_files:
            with st.expander(f"📄 {file_info['filename']} ({file_info['demo']})"):
                # Try to read the actual generated file
                try:
                    file_path = Path(file_info["filename"])
                    if file_path.exists():
                        with open(file_path, "r") as f:
                            code_content = f.read()

                        st.code(code_content, language="python")

                        # File info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("File Size", f"{len(code_content)} chars")
                        with col2:
                            st.metric("Lines", len(code_content.split("\n")))
                        with col3:
                            st.metric("Demo", file_info["demo"])
                    else:
                        st.warning("Generated file not found on disk")
                        st.info(
                            "This is normal for demo purposes - files are generated in memory"
                        )

                except Exception as e:
                    st.error(f"Error reading file: {e}")
    else:
        st.info("No generated files found in demo results")


def show_system_architecture():
    """Show system architecture page."""
    st.header("🏗️ System Architecture")

    # Architecture overview
    st.subheader("🎯 Reflective Module Architecture")

    st.markdown(
        """
    The Round-Trip Engineering system follows **Reflective Module principles**:
    
    ### 🔄 Core Principles
    - **Self-Monitoring**: Each module reports its own status and health
    - **Single Responsibility**: Each module has one clear, focused purpose
    - **Clear Boundaries**: Well-defined interfaces between modules
    - **Testability**: Modules can be tested in isolation
    - **Operational Visibility**: Real-time monitoring and debugging support
    
    ### 🏗️ Module Structure
    - **DemoOrchestrator**: Coordinates demo workflows (this module)
    - **RoundTripSystem**: Main system orchestrator
    - **ModelManager**: Handles model creation and persistence
    - **VocabularyAligner**: Manages domain vocabulary alignment
    - **CodeGenerator**: Generates code from models
    - **ClassGenerator**: Generates class structures
    - **MethodProcessor**: Processes method implementations
    """
    )

    # Module capabilities
    st.subheader("🔧 Module Capabilities")

    try:
        capabilities = asyncio.run(
            st.session_state.demo_orchestrator.get_module_capabilities()
        )

        for capability in capabilities:
            with st.expander(f"📋 {capability['name']}"):
                st.write(f"**Description**: {capability['description']}")
                st.write(
                    f"**Available**: {'✅ Yes' if capability['available'] else '❌ No'}"
                )
                st.write(f"**Version**: {capability['version']}")

    except Exception as e:
        st.error(f"Could not load module capabilities: {e}")

    # System status
    st.subheader("📊 Current System Status")
    display_system_status()


if __name__ == "__main__":
    main()
