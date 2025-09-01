#!/usr/bin/env python3
"""
Test Enhanced AST Parser Determinism
"""

import hashlib
import json

from enhanced_reverse_engineer import EnhancedReverseEngineer


def test_parser_determinism(file_path: str, num_runs: int = 5) -> None:
    """Test if the parser produces deterministic results"""

    print("🧪 Testing Enhanced AST Parser Determinism")
    print("=" * 60)
    print(f"📁 File: {file_path}")
    print(f"🔄 Number of runs: {num_runs}")
    print()

    results = []
    hashes = []

    # Run the parser multiple times
    for i in range(num_runs):
        print(f"🔄 Run {i + 1}/{num_runs}...")

        # Create a fresh instance each time
        reverse_engineer = EnhancedReverseEngineer()

        # Run reverse engineering
        model = reverse_engineer.reverse_engineer_file(file_path)

        if model:
            # Convert to JSON string for hashing
            model_json = json.dumps(model, sort_keys=True, indent=2)

            # Calculate hash
            model_hash = hashlib.md5(model_json.encode()).hexdigest()

            results.append(model)
            hashes.append(model_hash)

            print(f"   ✅ Run {i + 1} completed - Hash: {model_hash[:8]}...")
        else:
            print(f"   ❌ Run {i + 1} failed")
            return

    print()

    # Check determinism
    print("🔍 Determinism Analysis:")

    # Check if all hashes are identical
    first_hash = hashes[0]
    all_identical = all(hash == first_hash for hash in hashes)

    if all_identical:
        print("   ✅ DETERMINISTIC - All runs produced identical results!")
        print(f"   🔐 Consistent hash: {first_hash[:8]}...")
    else:
        print("   ❌ NON-DETERMINISTIC - Runs produced different results!")
        print("   🔍 Hash variations:")
        for i, hash_val in enumerate(hashes):
            status = "✅" if hash_val == first_hash else "❌"
            print(f"      Run {i + 1}: {hash_val[:8]}... {status}")

    # Detailed comparison of results
    print(f"\n📊 Detailed Result Comparison:")

    # Compare key metrics across runs
    key_metrics = [
        ("system_name", "System Name"),
        ("description", "Description"),
        ("components_count", "Components Count"),
        ("module_functions_count", "Module Functions Count"),
        ("total_lines", "Total Lines"),
    ]

    for i, (metric, label) in enumerate(key_metrics):
        if metric == "components_count":
            values = [len(result.get("components", {})) for result in results]
        elif metric == "module_functions_count":
            values = [len(result.get("module_functions", [])) for result in results]
        elif metric == "total_lines":
            values = [result.get("file_structure", {}).get("total_lines", 0) for result in results]
        else:
            values = [result.get(metric, "N/A") for result in results]

        # Check if all values are identical
        first_value = values[0]
        all_identical = all(val == first_value for val in values)

        status = "✅" if all_identical else "❌"
        print(f"   {status} {label}: {first_value}")

        if not all_identical:
            print(f"      Variations: {values}")

    # Check for any differences in the actual data
    print(f"\n🔍 Deep Content Analysis:")

    # Compare first and last results in detail
    first_result = results[0]
    last_result = results[-1]

    differences_found = []

    # Check system-level fields
    for field in [
        "system_name",
        "description",
        "purpose",
        "graph_api_level",
        "projection_system",
    ]:
        if first_result.get(field) != last_result.get(field):
            differences_found.append(f"System field '{field}' differs")

    # Check components
    first_components = first_result.get("components", {})
    last_components = last_result.get("components", {})

    if len(first_components) != len(last_components):
        differences_found.append("Component count differs")
    else:
        for comp_name in first_components:
            if comp_name not in last_components:
                differences_found.append(f"Component '{comp_name}' missing in later run")
            else:
                first_comp = first_components[comp_name]
                last_comp = last_components[comp_name]

                # Check method count
                first_methods = len(first_comp.get("methods", []))
                last_methods = len(last_comp.get("methods", []))
                if first_methods != last_methods:
                    differences_found.append(f"Component '{comp_name}' method count differs: {first_methods} vs {last_methods}")

    # Check module functions
    first_functions = first_result.get("module_functions", [])
    last_functions = last_result.get("module_functions", [])

    if len(first_functions) != len(last_functions):
        differences_found.append("Module function count differs")

    if differences_found:
        print("   ❌ Content differences detected:")
        for diff in differences_found:
            print(f"      • {diff}")
    else:
        print("   ✅ No content differences detected")

    # Final assessment
    print(f"\n🎯 Determinism Assessment:")

    if all_identical and not differences_found:
        print("   🏆 PERFECT DETERMINISM - Parser is completely deterministic!")
    elif all_identical:
        print("   ✅ HASH DETERMINISTIC - All runs produce identical hashes")
        print("   ⚠️  Minor content variations may exist")
    else:
        print("   ❌ NON-DETERMINISTIC - Parser produces different results")

    print(f"\n" + "=" * 60)
    print("🧪 Determinism Test Complete")


def main() -> None:
    """Main function"""
    test_parser_determinism("scripts/simple_calculator.py", 5)


if __name__ == "__main__":
    main()
