#!/usr/bin/env python3
"""
Generated tests for Test__init__
"""

from pathlib import Path

import pytest

from src.ghostbusters.ghostbusters_orchestrator import __init__


class Test__init__:
    """Generated tests for __init__"""

    def test___init___import(self, ghostbustersorchestrator):
        """Test that __init__ function can be imported"""
        # Test that function can be imported
        from src.ghostbusters.ghostbusters_orchestrator import __init__

        assert __init__ is not None
        assert callable(__init__)

    def test___init___callable(self, ghostbustersorchestrator):
        """Test that __init__ function is callable"""
        # Test that function is callable
        from src.ghostbusters.ghostbusters_orchestrator import __init__

        assert callable(__init__)
