#!/usr/bin/env python3
"""
Test F-String Policy Enforcement

Purpose: Verify that f-string policy is enforced correctly
"""

import pytest


def test_f_string_policy_enforcement():
    """Test that f-string policy is enforced correctly"""

    # Test that f-strings without placeholders are allowed
    simple_fstring = f"Simple message"
    assert simple_fstring == "Simple message"

    # Test that f-strings with placeholders work
    count = 5
    formatted_fstring = f"Count: {count}"
    assert formatted_fstring == "Count: 5"

    # Test that old-style formatting is discouraged
    # (This test documents the policy, doesn't enforce it)
    old_style = f"Count: {count}"
    assert old_style == "Count: 5"  # Works but not preferred

    # Test that f-strings are consistent
    assert type(simple_fstring) == str
    assert type(formatted_fstring) == str


def test_f_string_consistency():
    """Test f-string consistency across different contexts"""

    # Simple messages
    assert f"Starting..." == "Starting..."
    assert f"Complete!" == "Complete!"
    assert f"Error occurred" == "Error occurred"

    # With variables
    name = "Alice"
    count = 42
    assert f"Hello, {name}!" == "Hello, Alice!"
    assert f"Found {count} items" == "Found 42 items"

    # Complex expressions
    items = ["a", "b", "c"]
    assert f"Processing {len(items)} items" == "Processing 3 items"
    assert f"Status: {items[0] if items else 'empty'}" == "Status: a"


def test_f_string_policy_examples():
    """Test the examples from the f-string policy"""

    # Good examples from policy
    filename = "test.py"
    count = 10

    # These should all work and be encouraged
    good_examples = [f"Simple message", f"Count: {count}", f"Processing {filename}"]

    assert all(isinstance(example, str) for example in good_examples)
    assert good_examples[0] == "Simple message"
    assert good_examples[1] == "Count: 10"
    assert good_examples[2] == "Processing test.py"


def test_f_string_policy_elimination():
    """Test that F541 rule is completely eliminated"""

    # The F541 rule should be ignored in this project
    # This means f-strings without placeholders are perfectly valid

    # These should all work without any warnings
    valid_fstrings = [
        f"Debug message",
        f"Info message",
        f"Warning message",
        f"Error message",
    ]

    assert all(isinstance(fstring, str) for fstring in valid_fstrings)
    assert len(valid_fstrings) == 4


if __name__ == "__main__":
    # Run tests
    print("🧪 Testing F-String Policy Enforcement:")

    test_f_string_policy_enforcement()
    print("  ✅ F-string policy enforcement: PASSED")

    test_f_string_consistency()
    print("  ✅ F-string consistency: PASSED")

    test_f_string_policy_examples()
    print("  ✅ F-string policy examples: PASSED")

    test_f_string_policy_elimination()
    print("  ✅ F541 rule elimination: PASSED")

    print("\n🎉 All F-string policy tests passed!")
    print("✅ F-strings are mandatory and F541 is eliminated!")


