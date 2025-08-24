#!/usr/bin/env python3
"""
Generated tests for Test_create_workflow
"""

import pytest
from pathlib import Path

from src.ghostbusters.ghostbusters_orchestrator import _create_workflow


class Test_create_workflow:
    """Generated tests for _create_workflow"""


    def test__create_workflow_import(self, ghostbustersorchestrator):
        """Test that _create_workflow function can be imported"""
        # Test that function can be imported
        from src.ghostbusters.ghostbusters_orchestrator import _create_workflow
        assert _create_workflow is not None
        assert callable(_create_workflow)

    def test__create_workflow_callable(self, ghostbustersorchestrator):
        """Test that _create_workflow function is callable"""
        # Test that function is callable
        from src.ghostbusters.ghostbusters_orchestrator import _create_workflow
        assert callable(_create_workflow)
