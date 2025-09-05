#!/usr/bin/env python3
"""
Main entry point for Cloud Run deployment.
"""

import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the Cloud Run agent
from kiro_agents.cloudrun.agent import CloudRunKiroAgent

if __name__ == '__main__':
    agent = CloudRunKiroAgent()
    agent.run()