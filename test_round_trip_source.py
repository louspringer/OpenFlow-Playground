#!/usr/bin/env python3
"""
Test file for round-trip engineering demonstration.
This file contains multiple classes with various methods to test the system.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataProcessor:
    """Processes data with various operations."""
    
    name: str
    config: Dict[str, Any]
    
    def process_data(self, data: List[Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        results = {
            "processed_count": len(data),
            "timestamp": datetime.now().isoformat(),
            "processor_name": self.name
        }
        
        if data:
            results["data_summary"] = {
                "first_item": data[0],
                "last_item": data[-1],
                "total_items": len(data)
            }
        
        return results
    
    def validate_config(self) -> bool:
        """Validate the processor configuration."""
        required_keys = ["version", "mode"]
        return all(key in self.config for key in required_keys)


class RoundTripEngine:
    """Main engine for round-trip engineering operations."""
    
    def __init__(self, source_file: str):
        self.source_file = source_file
        self.logger = logging.getLogger(__name__)
        self.analysis_results = {}
    
    def analyze_source(self) -> Dict[str, Any]:
        """Analyze the source file and extract model."""
        try:
            with open(self.source_file, 'r') as f:
                content = f.read()
            
            self.analysis_results = {
                "file_path": self.source_file,
                "file_size": len(content),
                "line_count": len(content.splitlines()),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return self.analysis_results
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return {"error": str(e)}
    
    def generate_model(self) -> Dict[str, Any]:
        """Generate a model from the analysis results."""
        if not self.analysis_results:
            return {"error": "No analysis results available"}
        
        model = {
            "metadata": self.analysis_results,
            "classes": [
                {
                    "name": "DataProcessor",
                    "type": "dataclass",
                    "fields": ["name", "config"],
                    "methods": ["process_data", "validate_config"]
                },
                {
                    "name": "RoundTripEngine", 
                    "type": "class",
                    "fields": ["source_file", "logger", "analysis_results"],
                    "methods": ["analyze_source", "generate_model"]
                }
            ],
            "imports": [
                "logging", "typing", "dataclasses", "datetime"
            ]
        }
        
        return model


def main():
    """Main function to demonstrate the classes."""
    processor = DataProcessor(
        name="test_processor",
        config={"version": "1.0", "mode": "test"}
    )
    
    engine = RoundTripEngine("test_file.py")
    
    # Test data processing
    test_data = [1, 2, 3, 4, 5]
    results = processor.process_data(test_data)
    print(f"Processing results: {results}")
    
    # Test configuration validation
    is_valid = processor.validate_config()
    print(f"Configuration valid: {is_valid}")
    
    # Test source analysis
    analysis = engine.analyze_source()
    print(f"Source analysis: {analysis}")
    
    # Generate model
    model = engine.generate_model()
    print(f"Generated model: {model}")


if __name__ == "__main__":
    main()
