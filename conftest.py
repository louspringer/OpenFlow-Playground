#!/usr/bin/env python3
"""
Pytest configuration file to fix import issues.

This file ensures that the current directory is in the Python path
so that imports like 'from src.module import X' work correctly.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))
    print(f"✅ Added {current_dir} to Python path for pytest")
