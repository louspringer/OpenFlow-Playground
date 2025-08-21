#!/usr/bin/env python3
"""
Generated tests for Test_calculate_confidence
"""

from pathlib import Path

import pytest

from src.ghostbusters.ghostbusters_orchestrator import _calculate_confidence


class Test_calculate_confidence:
    """Generated tests for _calculate_confidence"""

    def test__calculate_confidence_import(self, ghostbustersorchestrator):
        """Test that _calculate_confidence function can be imported"""
        # Test that function can be imported
        from src.ghostbusters.ghostbusters_orchestrator import _calculate_confidence

        assert _calculate_confidence is not None
        assert callable(_calculate_confidence)

    def test__calculate_confidence_callable(self, ghostbustersorchestrator):
        """Test that _calculate_confidence function is callable"""
        # Test that function is callable
        from src.ghostbusters.ghostbusters_orchestrator import _calculate_confidence

        assert callable(_calculate_confidence)
