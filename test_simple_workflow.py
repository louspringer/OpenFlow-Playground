#!/usr/bin/env python3
"""
Simple workflow test file for enhanced activity diagram generation.
"""

def validate_input(data):
    """Validate input data."""
    if not data:
        return False
    return len(data) > 0

def process_data(data):
    """Process the data."""
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
        else:
            result.append(0)
    return result

def save_results(results):
    """Save the results."""
    if results:
        print(f"Saved {len(results)} results")
        return True
    return False

def main():
    """Main workflow function."""
    # Input data
    data = [1, -2, 3, 0, 5]
    
    # Validate input
    if not validate_input(data):
        print("Invalid input")
        return False
    
    # Process data
    results = process_data(data)
    
    # Save results
    if save_results(results):
        print("Workflow completed successfully")
        return True
    else:
        print("Failed to save results")
        return False

if __name__ == "__main__":
    main()
