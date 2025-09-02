#!/usr/bin/env python3
"""
Simple Demo Class for Round-Trip Engineering Demo
"""

from typing import List, Dict, Any


class SimpleDemoClass:
    """A simple demo class to showcase round-trip engineering."""
    
    def __init__(self, name: str):
        self.name = name
        self.data = []
    
    def add_data(self, item: Any) -> None:
        """Add an item to the data list."""
        self.data.append(item)
    
    def get_data(self) -> List[Any]:
        """Get all data items."""
        return self.data
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the data."""
        return {
            "name": self.name,
            "count": len(self.data),
            "data": self.data
        }


def demo_function(value: int) -> str:
    """A simple demo function."""
    if value > 0:
        return f"Positive: {value}"
    elif value < 0:
        return f"Negative: {value}"
    else:
        return "Zero"


if __name__ == "__main__":
    demo = SimpleDemoClass("Test")
    demo.add_data(42)
    demo.add_data("hello")
    print(demo.get_summary())
    print(demo_function(10))
