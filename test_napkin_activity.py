#!/usr/bin/env python3
"""
Test Napkin Activity Diagram Generation
"""

import napkin


@napkin.generate('plantuml_svg')
def test_activity_diagram():
    """Generate a simple activity diagram using napkin"""
    
    with napkin.act():
        start = napkin.start()
        process = napkin.activity("Process Data")
        decision = napkin.decision("Valid?")
        success = napkin.activity("Success")
        error = napkin.activity("Error")
        end = napkin.end()
        
        start >> process >> decision
        decision >> success >> end
        decision >> error >> end


if __name__ == "__main__":
    print("Testing napkin activity diagram generation...")
    test_activity_diagram()
    print("Check for generated files...")


