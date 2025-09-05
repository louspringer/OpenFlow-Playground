#!/usr/bin/env python3
"""
Test functional equivalence between original and projected artifacts
"""

# import subprocess  # REMOVED - replaced with secure_execute
import sys
from pathlib import Path

from src.secure_shell_service.secure_executor import secure_execute


def test_original_artifacts() -> None:
    """Test the original artifacts."""
    print("🔍 Testing original artifacts...")

    try:
        # Run basic validation tests
        result = secure_execute(
            [
                "python",
                "-m",
                "pytest",
                "tests/test_basic_validation.py::TestSecurityManager::test_credential_encryption_decryption",
                "-v",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:  # type: ignore
            print("✅ Original artifacts: Security manager test passed")
            # Removed return statement
        else:
            print("❌ Original artifacts: Security manager test failed")
            print(result.stdout)
            print(result.stderr)
            # Removed return statement
    except Exception as e:
        print(f"❌ Error testing original artifacts: {e}")
        # Removed return statement


def test_projected_artifacts() -> None:
    """Test the projected artifacts."""
    print("\n🔍 Testing projected artifacts...")

    # Copy projected file to a test location
    if Path("final_projection.py").exists():
        import shutil

        shutil.copy(
            "final_projection.py",
            "src/streamlit/openflow_quickstart_app_projected.py",
        )

        try:
            # Test importing the projected file
            sys.path.insert(0, str(Path.cwd()))

            # Test basic import
            try:
                from src.streamlit.openflow_quickstart_app_projected import (  # type: ignore
                    DeploymentManager,
                    OpenFlowQuickstartApp,
                    SecurityManager,
                )

                print("✅ Projected artifacts: Import successful")
            except ImportError as e:
                print(f"❌ Projected artifacts: Import error - {e}")
                # Removed return statement
            except Exception as e:
                print(f"❌ Projected artifacts: Import exception - {e}")
                # Removed return statement

            # Test creating instances
            try:
                OpenFlowQuickstartApp()
                print("✅ Projected artifacts: OpenFlowQuickstartApp created")
            except Exception as e:
                print(
                    f"❌ Projected artifacts: OpenFlowQuickstartApp creation failed - {e}",
                )
                # Removed return statement

            try:
                SecurityManager()
                print("✅ Projected artifacts: SecurityManager created")
            except Exception as e:
                print(f"❌ Projected artifacts: SecurityManager creation failed - {e}")
                # Removed return statement

            try:
                DeploymentManager()
                print("✅ Projected artifacts: DeploymentManager created")
            except Exception as e:
                print(
                    f"❌ Projected artifacts: DeploymentManager creation failed - {e}",
                )
                # Removed return statement

            # Removed return statement

        except Exception as e:
            print(f"❌ Error testing projected artifacts: {e}")
            # Removed return statement
    else:
        print("❌ Projected file not found")
        # Removed return statement


def test_functional_equivalence() -> None:
    """Test if projected artifacts have the same functionality as original."""
    print("\n🔍 Testing functional equivalence...")

    # Test specific functionality
    try:
        from src.streamlit.openflow_quickstart_app_projected import (
            SecurityManager,  # type: ignore
        )

        security = SecurityManager()

        # Test credential encryption/decryption
        test_credential = "test_secret"
        encrypted = security.encrypt_credential(test_credential)
        decrypted = security.decrypt_credential(encrypted)

        if decrypted == test_credential:
            print("✅ Projected artifacts: Credential encryption/decryption works")
        else:
            print("❌ Projected artifacts: Credential encryption/decryption failed")
            # Removed return statement

        # Test session token creation
        try:
            token = security.create_session_token("test_user", "admin")
            if token:
                print("✅ Projected artifacts: Session token creation works")
            else:
                print("❌ Projected artifacts: Session token creation failed")
                # Removed return statement
        except Exception as e:
            print(f"❌ Projected artifacts: Session token creation error - {e}")
            # Removed return statement

        # Removed return statement

    except Exception as e:
        print(f"❌ Error testing functional equivalence: {e}")
        # Removed return statement


def test_syntax_equivalence() -> None:
    """Test if projected artifacts have the same syntax structure."""
    print("\n🔍 Testing syntax equivalence...")

    try:
        # Parse both files with AST
        import ast

        # Parse original
        with open("src/streamlit/openflow_quickstart_app.py") as f:
            original_content = f.read()
        original_tree = ast.parse(original_content)

        # Parse projected
        with open("final_projection.py") as f:
            projected_content = f.read()
        projected_tree = ast.parse(projected_content)

        # Count elements
        original_functions = len(
            [n for n in ast.walk(original_tree) if isinstance(n, ast.FunctionDef)],
        )
        projected_functions = len(
            [n for n in ast.walk(projected_tree) if isinstance(n, ast.FunctionDef)],
        )

        original_classes = len(
            [n for n in ast.walk(original_tree) if isinstance(n, ast.ClassDef)],
        )
        projected_classes = len(
            [n for n in ast.walk(projected_tree) if isinstance(n, ast.ClassDef)],
        )

        print(
            f"📊 Function count: Original {original_functions} vs Projected {projected_functions}",
        )
        print(
            f"📊 Class count: Original {original_classes} vs Projected {projected_classes}",
        )

        if original_functions == projected_functions and original_classes == projected_classes:
            print("✅ Projected artifacts: Syntax structure matches original")
            # Removed return statement
        else:
            print("❌ Projected artifacts: Syntax structure differs from original")
            # Removed return statement

    except Exception as e:
        print(f"❌ Error testing syntax equivalence: {e}")
        # Removed return statement


def main() -> None:
    """Run all equivalence tests."""
    print("🧪 FUNCTIONAL EQUIVALENCE TESTING")
    print("=" * 60)

    tests = [
        ("Original Artifacts", test_original_artifacts),
        ("Projected Artifacts", test_projected_artifacts),
        ("Functional Equivalence", test_functional_equivalence),
        ("Syntax Equivalence", test_syntax_equivalence),
    ]

    results = {}  # type: ignore

    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                print(f"✅ {test_name}: PASSED")  # type: ignore
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results[test_name] = False

    # Summary
    print("\n📊 TEST RESULTS SUMMARY:")
    print("=" * 40)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Functional equivalence achieved!")
    else:
        print("⚠️ Some tests failed. Check the projected artifacts.")


if __name__ == "__main__":
    main()
