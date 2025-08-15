#!/usr/bin/env python3
"""
Ghostbusters Agents Module

This module provides specialized investigation agents for different quality analysis domains.
"""

from .issue_detector import IssueDetector
from .quality_analyzer import QualityAnalyzer
from .recommendation_engine import RecommendationEngine

__all__ = ["QualityAnalyzer", "IssueDetector", "RecommendationEngine"]
