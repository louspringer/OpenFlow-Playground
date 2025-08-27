#!/usr/bin/env python3
"""
Launch script for Workflow Visualization GUI

Simple launcher that starts the Streamlit application.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit GUI application."""
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Check if Streamlit is available
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Launch the Streamlit app
    print("🚀 Launching Workflow Visualization GUI...")
    print("📱 The GUI will open in your default web browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    # Run Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "src/workflow_visualization_gui.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main()
