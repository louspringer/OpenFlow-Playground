#!/usr/bin/env python3
"""
Generated tests for Test_create_delusion
"""

import pytest
from pathlib import Path

from src.ghostbusters.ghostbusters_orchestrator import _create_delusion


class Test_create_delusion:
    """Generated tests for _create_delusion"""


    def test__create_delusion_import(self, ghostbustersorchestrator):
        """Test that _create_delusion function can be imported"""
        # Test that function can be imported
        from src.ghostbusters.ghostbusters_orchestrator import _create_delusion
        assert _create_delusion is not None
        assert callable(_create_delusion)

    def test__create_delusion_callable(self, ghostbustersorchestrator):
        """Test that _create_delusion function is callable"""
        # Test that function is callable
        from src.ghostbusters.ghostbusters_orchestrator import _create_delusion
        assert callable(_create_delusion)
