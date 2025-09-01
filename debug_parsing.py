#!/usr/bin/env python3
"""
Debug script to test method signature parsing
"""

from typing import Any


def _parse_method_signature(method_signature: str) -> dict[str, Any]:
    """Parse method signature string into components"""
    # Example: "add(self, a: float, b: float) -> float"
    print(f"Parsing: {method_signature}")

    try:
        # Split on -> to separate parameters from return type
        if "->" in method_signature:
            params_part, return_type = method_signature.split("->", 1)
            return_type = return_type.strip()
            print(f"  Params part: '{params_part}'")
            print(f"  Return type: '{return_type}'")
        else:
            params_part = method_signature
            return_type = "None"
            print(f"  Params part: '{params_part}'")
            print(f"  Return type: '{return_type}'")

        # Extract method name and parameters
        # Remove trailing ) and split on first (
        if "(" in params_part and params_part.endswith(")"):
            method_name = params_part[: params_part.find("(")]
            params_str = params_part[params_part.find("(") + 1 : -1]

            print(f"  Method name: '{method_name}'")
            print(f"  Params string: '{params_str}'")

            # Parse parameters
            params = []
            if params_str.strip():
                for param in params_str.split(","):
                    param = param.strip()
                    print(f"    Processing param: '{param}'")
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        params.append({"name": param_name.strip(), "type": param_type.strip()})
                        print(f"      -> name: '{param_name.strip()}', type: '{param_type.strip()}'")
                    else:
                        params.append({"name": param.strip(), "type": "Any"})
                        print(f"      -> name: '{param.strip()}', type: 'Any'")

            result = {
                "name": method_name.strip(),
                "params": params,
                "return_type": return_type,
            }
            print(f"  Result: {result}")
            return result
        # Fallback for malformed signatures
        print(f"  Malformed signature, using fallback")
        return {
            "name": method_signature.strip(),
            "params": [],
            "return_type": "Any",
        }
    except Exception as e:
        # Fallback for any parsing errors
        print(f"  Exception: {e}, using fallback")
        return {"name": method_signature.strip(), "params": [], "return_type": "Any"}


def main() -> None:
    """Test parsing with the actual method signatures"""

    test_signatures = [
        "add(self, a: float, b: float) -> float",
        "subtract(self, a: float, b: float) -> float",
        "multiply(self, a: float, b: float) -> float",
        "divide(self, a: float, b: float) -> float",
        "display_result(self, result: float) -> None",
        "get_user_input(self) -> str",
        "run_calculator(self) -> None",
    ]

    print("🧪 Testing method signature parsing\n")

    for sig in test_signatures:
        print(f"🔍 Testing: {sig}")
        result = _parse_method_signature(sig)
        print(f"✅ Result: {result}")
        print()


if __name__ == "__main__":
    main()
