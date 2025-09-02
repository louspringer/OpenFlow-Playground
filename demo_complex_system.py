#!/usr/bin/env python3
"""
Complex Demo System for Round-Trip Engineering Demo
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class DataItem:
    """Data item with metadata."""
    id: str
    value: Any
    metadata: Dict[str, Any]


class DataProcessor(ABC):
    """Abstract base class for data processing."""
    
    @abstractmethod
    def process(self, data: List[DataItem]) -> List[DataItem]:
        """Process data items."""
        pass


class SimpleProcessor(DataProcessor):
    """Simple data processor implementation."""
    
    def process(self, data: List[DataItem]) -> List[DataItem]:
        """Process data items with simple logic."""
        return [item for item in data if item.value is not None]


class AdvancedProcessor(DataProcessor):
    """Advanced data processor with filtering and transformation."""
    
    def __init__(self, filter_func=None, transform_func=None):
        self.filter_func = filter_func
        self.transform_func = transform_func
    
    def process(self, data: List[DataItem]) -> List[DataItem]:
        """Process data items with advanced logic."""
        # Apply filter if provided
        if self.filter_func:
            data = [item for item in data if self.filter_func(item)]
        
        # Apply transformation if provided
        if self.transform_func:
            data = [DataItem(
                id=item.id,
                value=self.transform_func(item.value),
                metadata=item.metadata
            ) for item in data]
        
        return data


class ResultFormatter:
    """Formats processing results."""
    
    def __init__(self, output_format: str = "json"):
        self.output_format = output_format
    
    def format_json(self, data: List[DataItem]) -> str:
        """Format data as JSON string."""
        import json
        return json.dumps([{
            "id": item.id,
            "value": item.value,
            "metadata": item.metadata
        } for item in data], indent=2)
    
    def format_text(self, data: List[DataItem]) -> str:
        """Format data as text."""
        lines = []
        for item in data:
            lines.append(f"ID: {item.id}")
            lines.append(f"Value: {item.value}")
            lines.append(f"Metadata: {item.metadata}")
            lines.append("---")
        return "\n".join(lines)
    
    def format(self, data: List[DataItem]) -> str:
        """Format data using the specified output format."""
        if self.output_format == "json":
            return self.format_json(data)
        else:
            return self.format_text(data)


class DemoSystem:
    """Main demo system that orchestrates data processing."""
    
    def __init__(self, processor: DataProcessor, formatter: ResultFormatter):
        self.processor = processor
        self.formatter = formatter
        self.logger = logging.getLogger(__name__)
    
    def run_demo(self, input_data: List[DataItem]) -> str:
        """Run the complete demo workflow."""
        try:
            self.logger.info("Starting demo workflow")
            
            # Process data
            processed_data = self.processor.process(input_data)
            self.logger.info(f"Processed {len(processed_data)} items")
            
            # Format results
            formatted_result = self.formatter.format(processed_data)
            self.logger.info("Results formatted successfully")
            
            return formatted_result
            
        except Exception as e:
            self.logger.error(f"Demo workflow failed: {e}")
            raise


def create_sample_data() -> List[DataItem]:
    """Create sample data for demo purposes."""
    return [
        DataItem("1", 42, {"type": "number", "category": "positive"}),
        DataItem("2", "hello", {"type": "string", "category": "greeting"}),
        DataItem("3", None, {"type": "null", "category": "empty"}),
        DataItem("4", [1, 2, 3], {"type": "list", "category": "sequence"}),
        DataItem("5", {"key": "value"}, {"type": "dict", "category": "mapping"})
    ]


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data
    sample_data = create_sample_data()
    
    # Create processor and formatter
    processor = AdvancedProcessor(
        filter_func=lambda item: item.value is not None,
        transform_func=lambda value: str(value) if not isinstance(value, (int, float)) else value
    )
    formatter = ResultFormatter(output_format="json")
    
    # Create and run demo system
    demo_system = DemoSystem(processor, formatter)
    result = demo_system.run_demo(sample_data)
    
    print("Demo Results:")
    print(result)
