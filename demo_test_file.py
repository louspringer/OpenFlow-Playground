#!/usr/bin/env python3
"""Demo Python file for round-trip engineering testing."""

class DemoClass:
    """A simple demo class."""
    
    def __init__(self, value: str):
        """Initialize with a value."""
        self.value = value
    
    def get_value(self) -> str:
        """Get the stored value."""
        return self.value
    
    def set_value(self, new_value: str) -> None:
        """Set a new value."""
        self.value = new_value
