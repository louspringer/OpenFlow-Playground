#!/usr/bin/env python3
"""
Test script for the Quality System

This script tests the basic functionality of the quality system components.
"""


import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_quality_metrics():
    """Test quality metrics calculation"""
    print("Testing Quality Metrics...")
    
    try:
        from code_quality_system.quality_metrics import QualityMetrics, QualityScore, QualityMetricsCalculator
        
        # Test basic score creation
        score = QualityScore("test_metric", 85.0, weight=2.0)
        print(f"✅ Created quality score: {score.metric_name} = {score.score}")
        
        # Test metrics collection
        metrics = QualityMetrics(Path("."))
        metrics.add_score(score)
        print(f"✅ Added score to metrics, overall: {metrics.overall_score:.1f}")
        
        # Test calculator
        QualityMetricsCalculator(Path("."))
        print("✅ Created metrics calculator")
        
        return True
        
    except Exception as e:
        print(f"❌ Quality metrics test failed: {e}")
        return False


def test_quality_gates():
    """Test quality gates system"""
    print("Testing Quality Gates...")
    
    try:
        from code_quality_system.quality_gates import QualityGateManager, QualityGate, GateSeverity
        
        # Test gate manager
        manager = QualityGateManager(Path("."))
        print(f"✅ Created gate manager with {len(manager.gates)} gates")
        
        # Test gate creation
        custom_gate = QualityGate(
            name="custom_test",
            description="Custom test gate",
            severity=GateSeverity.MEDIUM,
            threshold=75.0,
            metric_name="test_metric"
        )
        manager.add_gate(custom_gate)
        print(f"✅ Added custom gate: {custom_gate.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quality gates test failed: {e}")
        return False


def test_quality_enforcer():
    """Test quality enforcer"""
    print("Testing Quality Enforcer...")
    
    try:
        from code_quality_system.quality_enforcer import QualityEnforcer
        
        # Test enforcer creation
        enforcer = QualityEnforcer(Path("."))
        print("✅ Created quality enforcer")
        
        # Test configuration
        enforcer.configure_enforcement(enforcement_level="moderate")
        print(f"✅ Configured enforcement level: {enforcer.enforcement_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quality enforcer test failed: {e}")
        return False


def test_pre_commit_integration():
    """Test pre-commit integration"""
    print("Testing Pre-commit Integration...")
    
    try:
        from code_quality_system.integrations.pre_commit_integration import PreCommitIntegration
        
        # Test integration creation
        integration = PreCommitIntegration(Path("."))
        print("✅ Created pre-commit integration")
        
        # Test git repository detection
        is_git = integration._is_git_repository()
        print(f"✅ Git repository detection: {is_git}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pre-commit integration test failed: {e}")
        return False


def test_ci_cd_integration():
    """Test CI/CD integration"""
    print("Testing CI/CD Integration...")
    
    try:
        from code_quality_system.integrations.ci_cd_integration import CICDIntegration
        
        # Test integration creation
        integration = CICDIntegration(Path("."))
        print("✅ Created CI/CD integration")
        print(f"✅ Detected CI environment: {integration.ci_environment}")
        
        return True
        
    except Exception as e:
        print(f"❌ CI/CD integration test failed: {e}")
        return False


def test_end_to_end():
    """Test end-to-end quality enforcement"""
    print("Testing End-to-End Quality Enforcement...")
    
    try:
        from code_quality_system.quality_enforcer import QualityEnforcer
        
        enforcer = QualityEnforcer(Path("."))
        
        # Create mock analysis results
        mock_results = {
            "flake8_issues": [
                {
                    "file": "test_file.py",
                    "type": "code_quality_issue",
                    "priority": "medium",
                    "description": "Line too long"
                }
            ],
            "security_issues": [],
            "coverage_percentage": 85.0,
            "performance_metrics": {}
        }
        
        # Run quality enforcement
        result = enforcer.enforce_quality(mock_results)
        
        print("✅ End-to-end test completed")
        print(f"   Overall score: {result.get('overall_score', 'N/A')}")
        print(f"   Can proceed: {result.get('can_proceed', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 Testing Quality System Components")
    print("=" * 50)
    
    tests = [
        test_quality_metrics,
        test_quality_gates,
        test_quality_enforcer,
        test_pre_commit_integration,
        test_ci_cd_integration,
        test_end_to_end,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Quality System Test Results")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! Quality system is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
