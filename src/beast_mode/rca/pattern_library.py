"""
Pattern Library

Manages root cause analysis patterns and learning.
"""

import logging
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class PatternLibrary:
    """Manages RCA patterns and learning."""

    def __init__(self, library_path: str = None):
        """Initialize the pattern library."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.library_path = Path(library_path) if library_path else None
        self.patterns = self._load_patterns()

    def get_patterns(self) -> List[Dict[str, Any]]:
        """Get all patterns in the library."""
        return self.patterns

    def add_pattern(self, pattern: Dict[str, Any]) -> None:
        """Add a new pattern to the library."""
        self.patterns.append(pattern)
        self._save_patterns()
        self.logger.info(f"Added pattern: {pattern.get('id')}")

    def _load_patterns(self) -> List[Dict[str, Any]]:
        """Load patterns from storage."""
        if self.library_path and self.library_path.exists():
            try:
                with open(self.library_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load patterns: {str(e)}")
        return []

    def _save_patterns(self) -> None:
        """Save patterns to storage."""
        if self.library_path:
            try:
                self.library_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.library_path, "w") as f:
                    json.dump(self.patterns, f, indent=2)
            except Exception as e:
                self.logger.error(f"Failed to save patterns: {str(e)}")
