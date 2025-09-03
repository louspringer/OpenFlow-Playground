#!/usr/bin/env python3
"""Generated tests for BaseExpert"""

import pytest
from src.ghostbusters.agents.base_expert import BaseExpert


class TestBaseExpert:
    """Generated tests for BaseExpert"""

    def test_baseexpert_initialization(self):
        """Test that BaseExpert initializes correctly"""
        instance = BaseExpert()
        assert instance is not None
        assert isinstance(instance, BaseExpert)
