#!/usr/bin/env python3
"""
🎯 Kiro Agent Live Fire Dashboard
Real-time Streamlit visualization of Kiro Agent coordination
"""

import streamlit as st
import asyncio
import aiohttp
import json
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
import queue

# Configure Streamlit
st.set_page_config(page_title="🎯 Kiro Agent Live Fire Dashboard", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")


class KiroDataStreamer:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.data_queue = queue.Queue()
        self.running = False
        self.session = None

    async def start_streaming(self):
        """Start async data streaming"""
        self.running = True
        self.session = aiohttp.ClientSession()

        while self.running:
            try:
                # Get status
                async with self.session.get(f"{self.base_url}/status") as resp:
                    status = await resp.json()

                # Get tasks
                async with self.session.get(f"{self.base_url}/tasks") as resp:
                    tasks = await resp.json()

                # Get metrics
                async with self.session.get(f"{self.base_url}/metrics") as resp:
                    metrics_text = await resp.text()

                # Parse metrics
                metrics = self._parse_metrics(metrics_text)

                # Create data point
                data_point = {"timestamp": datetime.now(), "status": status, "tasks": tasks, "metrics": metrics}

                # Add to queue
                self.data_queue.put(data_point)

                await asyncio.sleep(2)  # Update every 2 seconds

            except Exception as e:
                st.error(f"Streaming error: {e}")
                await asyncio.sleep(5)

    def _parse_metrics(self, metrics_text: str) -> Dict[str, float]:
        """Parse Prometheus metrics text"""
        metrics = {}
        for line in metrics_text.strip().split("\n"):
            if line.startswith("kiro_agent_") and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        metrics[parts[0]] = float(parts[1])
                    except ValueError:
                        pass
        return metrics

    def stop_streaming(self):
        """Stop data streaming"""
        self.running = False
        if self.session:
            asyncio.create_task(self.session.close())

    def get_latest_data(self):
        """Get latest data from queue"""
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None


# Initialize session state
if "streamer" not in st.session_state:
    st.session_state.streamer = KiroDataStreamer()
if "data_history" not in st.session_state:
    st.session_state.data_history = []
if "streaming" not in st.session_state:
    st.session_state.streaming = False


def start_streaming():
    """Start the data streaming"""
    if not st.session_state.streaming:
        st.session_state.streaming = True

        # Start streaming in background thread
        def run_streaming():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(st.session_state.streamer.start_streaming())

        thread = threading.Thread(target=run_streaming, daemon=True)
        thread.start()


def stop_streaming():
    """Stop the data streaming"""
    st.session_state.streaming = False
    st.session_state.streamer.stop_streaming()


# Main dashboard
st.title("🎯 Kiro Agent Live Fire Dashboard")
st.markdown("Real-time monitoring of multi-agent coordination system")

# Sidebar controls
with st.sidebar:
    st.header("🎮 Controls")

    if st.button("🚀 Start Live Fire", disabled=st.session_state.streaming):
        start_streaming()
        st.success("Live fire started!")

    if st.button("🛑 Stop Live Fire", disabled=not st.session_state.streaming):
        stop_streaming()
        st.info("Live fire stopped!")

    st.markdown("---")
    st.markdown("### 📊 Connection Status")
    if st.session_state.streaming:
        st.success("🟢 Streaming Active")
    else:
        st.warning("🟡 Ready to Start")

# Get latest data
latest_data = st.session_state.streamer.get_latest_data()
if latest_data:
    st.session_state.data_history.append(latest_data)
    # Keep only last 100 data points
    if len(st.session_state.data_history) > 100:
        st.session_state.data_history = st.session_state.data_history[-100:]

# Main dashboard content
if latest_data:
    status = latest_data["status"]
    tasks = latest_data["tasks"]
    metrics = latest_data["metrics"]

    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="🤖 Registered Agents", value=status["coordinator"]["registered_agents"], delta=None)

    with col2:
        st.metric(label="📋 Active Tasks", value=status["coordinator"]["active_tasks"], delta=None)

    with col3:
        st.metric(label="🔄 Coordination Cycles", value=status["coordinator"]["stats"]["coordination_cycles"], delta=None)

    with col4:
        st.metric(label="✅ Tasks Completed", value=status["coordinator"]["stats"]["tasks_completed"], delta=None)

    with col5:
        st.metric(label="❌ Tasks Failed", value=status["coordinator"]["stats"]["tasks_failed"], delta=None)

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Task Activity Over Time")
        if len(st.session_state.data_history) > 1:
            # Create time series data
            timestamps = [d["timestamp"] for d in st.session_state.data_history]
            active_tasks = [d["status"]["coordinator"]["active_tasks"] for d in st.session_state.data_history]
            completed_tasks = [d["status"]["coordinator"]["stats"]["tasks_completed"] for d in st.session_state.data_history]

            df = pd.DataFrame({"Time": timestamps, "Active Tasks": active_tasks, "Completed Tasks": completed_tasks})

            fig = px.line(df, x="Time", y=["Active Tasks", "Completed Tasks"], title="Task Activity Timeline")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Collecting data for timeline...")

    with col2:
        st.subheader("🎯 Task Status Distribution")
        if tasks["tasks"]:
            task_types = {}
            for task in tasks["tasks"]:
                task_type = task.get("type", "unknown")
                task_types[task_type] = task_types.get(task_type, 0) + 1

            if task_types:
                fig = px.pie(values=list(task_types.values()), names=list(task_types.keys()), title="Task Types Distribution")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No tasks to display")
        else:
            st.info("📊 No active tasks")

    # Active tasks table
    st.subheader("📋 Live Fire Tasks")
    if tasks["tasks"]:
        task_data = []
        for task in tasks["tasks"]:
            task_data.append(
                {
                    "🎯 Task ID": task.get("task_id", "unknown"),
                    "📝 Type": task.get("type", "unknown"),
                    "📄 Description": task.get("description", "No description")[:100] + "...",
                    "⚡ Status": task.get("status", "unknown"),
                    "🤖 Assigned Agent": task.get("assigned_agent", "None"),
                }
            )

        df_tasks = pd.DataFrame(task_data)
        st.dataframe(df_tasks, use_container_width=True)
    else:
        st.info("📭 No active tasks")

    # Metrics details
    st.subheader("📊 System Metrics")
    if metrics:
        metrics_data = []
        for metric_name, value in metrics.items():
            display_name = metric_name.replace("kiro_agent_", "").replace("_", " ").title()
            metrics_data.append({"📈 Metric": display_name, "🔢 Value": value, "📊 Raw Name": metric_name})

        df_metrics = pd.DataFrame(metrics_data)
        st.dataframe(df_metrics, use_container_width=True)
    else:
        st.info("📊 No metrics available")

    # Coordination cycles chart
    if len(st.session_state.data_history) > 1:
        st.subheader("🔄 Coordination Activity")
        timestamps = [d["timestamp"] for d in st.session_state.data_history]
        cycles = [d["status"]["coordinator"]["stats"]["coordination_cycles"] for d in st.session_state.data_history]

        df_cycles = pd.DataFrame({"Time": timestamps, "Coordination Cycles": cycles})

        fig = px.area(df_cycles, x="Time", y="Coordination Cycles", title="Coordination Cycles Over Time")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

else:
    # No data available
    st.info("🎯 Ready to start live fire exercise!")
    st.markdown(
        """
    ### 🚀 Getting Started
    
    1. **Start Live Fire**: Click the "🚀 Start Live Fire" button in the sidebar
    2. **Monitor Real-time**: Watch the dashboard update with live data
    3. **Analyze Performance**: Use the charts and metrics to understand system behavior
    
    ### 📊 What You'll See
    
    - **🤖 Agent Status**: Number of registered agents and their activity
    - **📋 Task Management**: Active tasks and their progress
    - **🔄 Coordination**: Real-time coordination cycle monitoring
    - **📈 Performance**: Historical trends and system health
    """
    )

# Auto-refresh
if st.session_state.streaming:
    time.sleep(2)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("🎯 **Kiro Agent Live Fire Dashboard** | Built with Streamlit & Plotly")
