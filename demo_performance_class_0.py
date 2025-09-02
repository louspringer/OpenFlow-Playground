#!/usr/bin/env python3
"""
Performance Demo Class 0 for Round-Trip Engineering Demo
"""

from typing import List, Dict, Any


class PerformanceDemoClass0:
    """Performance demo class iteration 0."""
    
    def __init__(self, name: str):
        self.name = name
        self.counter = 0
        self.data = {}
    
    def increment(self) -> int:
        """Increment counter and return new value."""
        self.counter += 1
        return self.counter
    
    def add_data(self, key: str, value: Any) -> None:
        """Add data to the internal dictionary."""
        self.data[key] = value
    
    def get_data(self, key: str) -> Any:
        """Get data by key."""
        return self.data.get(key)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of the class state."""
        return {
            "name": self.name,
            "counter": self.counter,
            "data_keys": list(self.data.keys()),
            "data_count": len(self.data)
        }


def performance_demo_function0(value: int) -> str:
    """Performance demo function 0."""
    if value > 0:
        return f"Positive {iteration}: {value}"
    elif value < 0:
        return f"Negative {iteration}: {value}"
    else:
        return f"Zero {iteration}"


if __name__ == "__main__":
    demo = PerformanceDemoClass0("PerformanceTest0")
    demo.increment()
    demo.add_data("test", "value")
    print(demo.get_summary())
    print(performance_demo_function0(10))
