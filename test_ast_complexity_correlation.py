#!/usr/bin/env python3
"""Test correlation between AST complexity and code length"""

import ast
import random
import string


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


def generate_simple_function(length: int) -> str:
    """Generate function with target length"""
    base = '''def simple_function():
    """Simple function"""
    result = 0
    for i in range(10):
        result += i
    return result'''

    if length <= len(base):
        return base[:length]

    # Add comments to reach target length
    extra = length - len(base)
    if extra > 4:
        comments = "\n    # " + "".join(
            random.choices(string.ascii_letters, k=extra - 4)
        )
        return base + comments
    return base


def generate_complex_function(length: int) -> str:
    """Generate complex function with target length"""
    base = '''def complex_function(data: List[Dict[str, Any]], config: Optional[Config] = None) -> Dict[str, Union[int, float, str]]:
    """Complex function with types and logic"""
    if not data or not isinstance(data, list):
        raise ValueError("Data must be non-empty list")

    result: Dict[str, Union[int, float, str]] = {}
    processed_count: int = 0
    error_count: int = 0

    try:
        for item in data:
            if isinstance(item, dict):
                key = item.get("key", str(processed_count))
                value = item.get("value", 0)
                if isinstance(value, (int, float)):
                    result[str(key)] = value
                    processed_count += 1
                else:
                    result[str(key)] = str(value)
                    processed_count += 1
            else:
                error_count += 1
    except Exception as e:
        print(f"Error processing data: {e}")
        error_count += 1

    return {"result": result, "processed": processed_count, "errors": error_count}'''

    if length <= len(base):
        return base[:length]

    # Add more complexity to reach target length
    extra = length - len(base)
    additional_logic = f"""
    # Additional processing
    if config and hasattr(config, 'validate'):
        validation_result = config.validate(result)
        if not validation_result:
            print("Validation failed")
            return {{"error": "validation_failed"}}

    # Final processing
    final_result = {{}}
    for key, value in result.items():
        if isinstance(value, (int, float)):
            final_result[key] = value * 2
        else:
            final_result[key] = value

    return final_result"""

    return base + additional_logic[:extra]


def test_correlation():
    """Test correlation between code length and AST complexity"""
    print("🧪 Testing AST Complexity vs Code Length Correlation:")

    # Test simple functions
    print("\n📊 Simple Functions (No Types):")
    simple_results = []
    for length in [100, 200, 300, 400, 500]:
        code = generate_simple_function(length)
        actual_length = len(code)
        ast_nodes = count_ast_nodes(code)
        simple_results.append((actual_length, ast_nodes))
        print(f"  Length: {actual_length:3d} chars → AST: {ast_nodes:3d} nodes")

    # Test complex functions
    print("\n📊 Complex Functions (With Types):")
    complex_results = []
    for length in [200, 400, 600, 800, 1000]:
        code = generate_complex_function(length)
        actual_length = len(code)
        ast_nodes = count_ast_nodes(code)
        complex_results.append((actual_length, ast_nodes))
        print(f"  Length: {actual_length:3d} chars → AST: {ast_nodes:3d} nodes")

    # Calculate correlations
    print("\n🔍 Correlation Analysis:")

    # Simple functions correlation
    simple_lengths = [r[0] for r in simple_results]
    simple_asts = [r[1] for r in simple_results]
    simple_correlation = calculate_correlation(simple_lengths, simple_asts)
    print(f"Simple functions correlation: {simple_correlation:.3f}")

    # Complex functions correlation
    complex_lengths = [r[0] for r in complex_results]
    complex_asts = [r[1] for r in complex_results]
    complex_correlation = calculate_correlation(complex_lengths, complex_asts)
    print(f"Complex functions correlation: {complex_correlation:.3f}")

    # Overall correlation
    all_lengths = simple_lengths + complex_lengths
    all_asts = simple_asts + complex_asts
    overall_correlation = calculate_correlation(all_lengths, all_asts)
    print(f"Overall correlation: {overall_correlation:.3f}")

    # Interpret results
    print("\n🎯 Interpretation:")
    if overall_correlation > 0.8:
        print(
            "✅ STRONG correlation: AST complexity is directly proportional to code length"
        )
    elif overall_correlation > 0.6:
        print("⚠️ MODERATE correlation: Some relationship exists")
    else:
        print("❌ WEAK correlation: Little relationship between length and complexity")

    # Check if types affect correlation
    type_impact = abs(simple_correlation - complex_correlation)
    print(f"Type annotation impact on correlation: {type_impact:.3f}")

    return overall_correlation > 0.8


def calculate_correlation(x_values: list, y_values: list) -> float:
    """Calculate Pearson correlation coefficient"""
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return 0.0

    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x * x for x in x_values)
    sum_y2 = sum(y * y for y in y_values)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def main():
    """Main test function"""
    strong_correlation = test_correlation()

    print(f"\n🏆 Hypothesis 2 Result:")
    if strong_correlation:
        print("✅ CONFIRMED: AST complexity is directly proportional to code length")
        print("   This supports the idea that longer code = more complex ASTs")
    else:
        print("❌ REJECTED: AST complexity is NOT directly proportional to code length")
        print("   This suggests other factors affect complexity more than length")


if __name__ == "__main__":
    main()


import ast
import random
import string


def count_ast_nodes(code: str) -> int:
    """Count AST nodes in code string"""
    try:
        tree = ast.parse(code)
        return len(list(ast.walk(tree)))
    except Exception as e:
        print(f"AST parsing error: {e}")
        return 0


def generate_simple_function(length: int) -> str:
    """Generate function with target length"""
    base = '''def simple_function():
    """Simple function"""
    result = 0
    for i in range(10):
        result += i
    return result'''

    if length <= len(base):
        return base[:length]

    # Add comments to reach target length
    extra = length - len(base)
    if extra > 4:
        comments = "\n    # " + "".join(
            random.choices(string.ascii_letters, k=extra - 4)
        )
        return base + comments
    return base


def generate_complex_function(length: int) -> str:
    """Generate complex function with target length"""
    base = '''def complex_function(data: List[Dict[str, Any]], config: Optional[Config] = None) -> Dict[str, Union[int, float, str]]:
    """Complex function with types and logic"""
    if not data or not isinstance(data, list):
        raise ValueError("Data must be non-empty list")

    result: Dict[str, Union[int, float, str]] = {}
    processed_count: int = 0
    error_count: int = 0

    try:
        for item in data:
            if isinstance(item, dict):
                key = item.get("key", str(processed_count))
                value = item.get("value", 0)
                if isinstance(value, (int, float)):
                    result[str(key)] = value
                    processed_count += 1
                else:
                    result[str(key)] = str(value)
                    processed_count += 1
            else:
                error_count += 1
    except Exception as e:
        print(f"Error processing data: {e}")
        error_count += 1

    return {"result": result, "processed": processed_count, "errors": error_count}'''

    if length <= len(base):
        return base[:length]

    # Add more complexity to reach target length
    extra = length - len(base)
    additional_logic = f"""
    # Additional processing
    if config and hasattr(config, 'validate'):
        validation_result = config.validate(result)
        if not validation_result:
            print("Validation failed")
            return {{"error": "validation_failed"}}

    # Final processing
    final_result = {{}}
    for key, value in result.items():
        if isinstance(value, (int, float)):
            final_result[key] = value * 2
        else:
            final_result[key] = value

    return final_result"""

    return base + additional_logic[:extra]


def test_correlation():
    """Test correlation between code length and AST complexity"""
    print("🧪 Testing AST Complexity vs Code Length Correlation:")

    # Test simple functions
    print("\n📊 Simple Functions (No Types):")
    simple_results = []
    for length in [100, 200, 300, 400, 500]:
        code = generate_simple_function(length)
        actual_length = len(code)
        ast_nodes = count_ast_nodes(code)
        simple_results.append((actual_length, ast_nodes))
        print(f"  Length: {actual_length:3d} chars → AST: {ast_nodes:3d} nodes")

    # Test complex functions
    print("\n📊 Complex Functions (With Types):")
    complex_results = []
    for length in [200, 400, 600, 800, 1000]:
        code = generate_complex_function(length)
        actual_length = len(code)
        ast_nodes = count_ast_nodes(code)
        complex_results.append((actual_length, ast_nodes))
        print(f"  Length: {actual_length:3d} chars → AST: {ast_nodes:3d} nodes")

    # Calculate correlations
    print("\n🔍 Correlation Analysis:")

    # Simple functions correlation
    simple_lengths = [r[0] for r in simple_results]
    simple_asts = [r[1] for r in simple_results]
    simple_correlation = calculate_correlation(simple_lengths, simple_asts)
    print(f"Simple functions correlation: {simple_correlation:.3f}")

    # Complex functions correlation
    complex_lengths = [r[0] for r in complex_results]
    complex_asts = [r[1] for r in complex_results]
    complex_correlation = calculate_correlation(complex_lengths, complex_asts)
    print(f"Complex functions correlation: {complex_correlation:.3f}")

    # Overall correlation
    all_lengths = simple_lengths + complex_lengths
    all_asts = simple_asts + complex_asts
    overall_correlation = calculate_correlation(all_lengths, all_asts)
    print(f"Overall correlation: {overall_correlation:.3f}")

    # Interpret results
    print("\n🎯 Interpretation:")
    if overall_correlation > 0.8:
        print(
            "✅ STRONG correlation: AST complexity is directly proportional to code length"
        )
    elif overall_correlation > 0.6:
        print("⚠️ MODERATE correlation: Some relationship exists")
    else:
        print("❌ WEAK correlation: Little relationship between length and complexity")

    # Check if types affect correlation
    type_impact = abs(simple_correlation - complex_correlation)
    print(f"Type annotation impact on correlation: {type_impact:.3f}")

    return overall_correlation > 0.8


def calculate_correlation(x_values: list, y_values: list) -> float:
    """Calculate Pearson correlation coefficient"""
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return 0.0

    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x * x for x in x_values)
    sum_y2 = sum(y * y for y in y_values)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def main():
    """Main test function"""
    strong_correlation = test_correlation()

    print(f"\n🏆 Hypothesis 2 Result:")
    if strong_correlation:
        print("✅ CONFIRMED: AST complexity is directly proportional to code length")
        print("   This supports the idea that longer code = more complex ASTs")
    else:
        print("❌ REJECTED: AST complexity is NOT directly proportional to code length")
        print("   This suggests other factors affect complexity more than length")


if __name__ == "__main__":
    main()
