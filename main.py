#!/usr/bin/env python3
"""
Main entry point for Cloud Run deployment.
Now uses beast-ai-dev-agent package.
"""

# Import from the beast-ai-dev-agent package
from beast_ai_dev_agent import CloudRunKiroAgent

if __name__ == '__main__':
    agent = CloudRunKiroAgent()
    agent.run()
