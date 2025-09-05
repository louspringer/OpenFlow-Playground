#!/usr/bin/env python3
"""
Comprehensive Test Suite for Meta-Cognitive Orchestrator

This test suite implements the missing test meta-cases identified in Phase 3 analysis:
1. Recursive testing meta-cases
2. Multi-dimensional test orchestration validation
3. Blind spot detection meta-testing
4. Quality system meta-validation
5. Self-referential testing capabilities
"""

import unittest

from meta_cognitive_orchestrator import MetaCognitiveOrchestrator


class TestMetaCognitiveOrchestrator(unittest.TestCase):
    """Test suite for meta-cognitive orchestrator"""

    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = MetaCognitiveOrchestrator(confidence_threshold=0.7)

    def test_assumption_detection(self):
        """Test assumption detection capabilities"""
        context = "I think this should work, probably, I assume it's correct"
        assumptions = self.orchestrator.detect_assumptions(context)

        self.assertIn("Using assumption indicator: 'I think'", assumptions)
        self.assertIn("Using assumption indicator: 'probably'", assumptions)
        self.assertIn("Using assumption indicator: 'I assume'", assumptions)
        self.assertEqual(len(assumptions), 3)

    def test_jeopardy_question_generation(self):
        """Test Jeopardy-style question generation"""
        # Test PR context
        pr_context = "I need to create a pull request"
        question = self.orchestrator.generate_jeopardy_question(pr_context)
        self.assertIn("GitHub PR workflow", question)

        # Test git context
        git_context = "I did a git merge"
        question = self.orchestrator.generate_jeopardy_question(git_context)
        self.assertIn("git workflow", question)

        # Test unknown context
        unknown_context = "I'm doing something else"
        question = self.orchestrator.generate_jeopardy_question(unknown_context)
        self.assertIn("Question me about this", question)

    def test_partner_investigation_simulation(self):
        """Test partner LLM investigation simulation"""
        context = "I created a PR and did git merge"
        questions = self.orchestrator.simulate_partner_investigation(context)

        # Should have questions from both PR and git contexts
        self.assertGreater(len(questions), 5)
        self.assertIn("What workflow were you following?", questions)
        self.assertIn("What's the difference between git merge and GitHub PR?", questions)

    def test_blind_spot_identification(self):
        """Test blind spot identification from partner questions"""
        questions = [
            "What workflow were you following?",
            "What tools did you use?",
            "What would a human expect?",
            "What process did you follow?",
        ]

        blind_spots = self.orchestrator.identify_blind_spots(questions)

        self.assertIn("Missing proper workflow understanding", blind_spots)
        self.assertIn("Using wrong tools for the job", blind_spots)
        self.assertIn("Not considering human expectations", blind_spots)
        self.assertIn("Bypassing standard processes", blind_spots)

    def test_confidence_calculation(self):
        """Test confidence calculation based on issues"""
        # No issues should give high confidence
        confidence = self.orchestrator.calculate_confidence([], [])
        self.assertEqual(confidence, 1.0)

        # Assumptions should reduce confidence
        confidence = self.orchestrator.calculate_confidence(["assumption1", "assumption2"], [])
        self.assertEqual(confidence, 0.6)

        # Blind spots should reduce confidence more
        confidence = self.orchestrator.calculate_confidence([], ["blind_spot1", "blind_spot2"])
        self.assertEqual(confidence, 0.4)

        # Combined issues should reduce confidence significantly
        confidence = self.orchestrator.calculate_confidence(["assumption"], ["blind_spot"])
        self.assertEqual(confidence, 0.5)

    def test_decision_making(self):
        """Test decision making based on confidence and blind spots"""
        # High confidence, no blind spots
        decision = self.orchestrator.make_decision(0.8, [])
        self.assertEqual(decision, "PROCEED_WITH_CAUTION")

        # Low confidence
        decision = self.orchestrator.make_decision(0.5, [])
        self.assertEqual(decision, "ASK_HUMAN")

        # Has blind spots
        decision = self.orchestrator.make_decision(0.8, ["blind_spot"])
        self.assertEqual(decision, "INVESTIGATE_BLIND_SPOTS")

    def test_full_orchestration(self):
        """Test complete orchestration workflow"""
        context = "I think git merge is the same as creating a PR, I assume it's correct"
        result = self.orchestrator.orchestrate(context)

        # Check all required keys
        required_keys = [
            "assumptions_detected",
            "jeopardy_question",
            "blind_spots_identified",
            "partner_questions",
            "confidence",
            "final_decision",
            "human_feedback",
        ]
        for key in required_keys:
            self.assertIn(key, result)

        # Should detect assumptions
        self.assertGreater(len(result["assumptions_detected"]), 0)

        # Should have partner questions
        self.assertGreater(len(result["partner_questions"]), 0)

        # Should identify blind spots
        self.assertGreater(len(result["blind_spots_identified"]), 0)

        # Confidence should be reduced due to issues
        self.assertLess(result["confidence"], 1.0)


class TestMetaTestingCapabilities(unittest.TestCase):
    """Test meta-testing capabilities - the missing test meta-cases"""

    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = MetaCognitiveOrchestrator()

    def test_recursive_testing_meta_case(self):
        """Test recursive testing meta-case: orchestrator testing itself"""
        # Create a context about testing the orchestrator with PR workflow
        test_context = "I'm testing the meta-cognitive orchestrator by creating a PR workflow, I think it should work well"

        # The orchestrator should be able to analyze its own testing context
        result = self.orchestrator.orchestrate(test_context)

        # Should generate appropriate questions about testing
        self.assertIn("Question me about my approach", result["jeopardy_question"])

        # Should identify potential blind spots in testing approach
        self.assertGreater(len(result["blind_spots_identified"]), 0)

    def test_multi_dimensional_orchestration_validation(self):
        """Test multi-dimensional test orchestration validation"""
        # Test orchestrator with multiple contexts
        contexts = [
            "I'm doing code quality testing",
            "I'm doing security testing",
            "I'm doing performance testing",
        ]

        results = []
        for context in contexts:
            result = self.orchestrator.orchestrate(context)
            results.append(result)

        # Should handle multiple contexts without errors
        self.assertEqual(len(results), 3)

        # Each result should have complete structure
        for result in results:
            self.assertIn("confidence", result)
            self.assertIn("final_decision", result)

    def test_blind_spot_detection_meta_testing(self):
        """Test blind spot detection meta-testing capabilities"""
        # Test the orchestrator's ability to detect its own blind spots
        # by giving it a context that should trigger multiple blind spots

        complex_context = """
        I'm doing something I think will work, probably, I assume it's correct,
        I believe this approach is obvious, I guess it should be fine
        """

        result = self.orchestrator.orchestrate(complex_context)

        # Should detect multiple assumptions
        self.assertGreater(len(result["assumptions_detected"]), 3)

        # Should have low confidence due to many assumptions
        self.assertLess(result["confidence"], 0.5)

        # Should recommend asking human
        self.assertEqual(result["final_decision"], "ASK_HUMAN")

    def test_quality_system_meta_validation(self):
        """Test quality system meta-validation capabilities"""
        # Test that the orchestrator can validate quality-related decisions

        quality_context = "I'm implementing a quality system with PR workflow, I think it's comprehensive, I assume it covers everything"

        result = self.orchestrator.orchestrate(quality_context)

        # Should detect assumption about comprehensiveness
        self.assertIn("assumption", str(result["assumptions_detected"]).lower())

        # Should generate questions about quality approach
        self.assertGreater(len(result["partner_questions"]), 0)

        # Should provide actionable feedback
        self.assertIn("human_feedback", result)

    def test_self_referential_testing_capabilities(self):
        """Test self-referential testing capabilities"""
        # Test the orchestrator's ability to test its own testing approach

        # Create a meta-context about testing
        meta_test_context = "I'm testing how well I can test things"

        result = self.orchestrator.orchestrate(meta_test_context)

        # Should be able to analyze its own testing approach
        self.assertIsInstance(result, dict)

        # Should generate appropriate questions about testing methodology
        self.assertIn("Question me about this", result["jeopardy_question"])

        # Should identify potential blind spots in testing approach
        self.assertGreaterEqual(len(result["blind_spots_identified"]), 0)


class TestMetaCognitiveOrchestratorIntegration(unittest.TestCase):
    """Test integration with other systems"""

    def test_confidence_threshold_configuration(self):
        """Test confidence threshold configuration"""
        # Test with different confidence thresholds
        low_threshold_orchestrator = MetaCognitiveOrchestrator(confidence_threshold=0.3)
        high_threshold_orchestrator = MetaCognitiveOrchestrator(confidence_threshold=0.9)

        # Same context should give different decisions based on threshold
        context = "I think this might work"
        result_low = low_threshold_orchestrator.orchestrate(context)
        result_high = high_threshold_orchestrator.orchestrate(context)

        # Low threshold should be more permissive
        self.assertNotEqual(result_low["final_decision"], result_high["final_decision"])

    def test_error_handling(self):
        """Test error handling capabilities"""
        # Test with edge cases
        orchestrator = MetaCognitiveOrchestrator()

        # Empty context
        result = orchestrator.orchestrate("")
        self.assertIsInstance(result, dict)

        # Very long context
        long_context = "test " * 1000
        result = orchestrator.orchestrate(long_context)
        self.assertIsInstance(result, dict)

        # Special characters
        special_context = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = orchestrator.orchestrate(special_context)
        self.assertIsInstance(result, dict)


def run_meta_testing_suite():
    """Run the complete meta-testing suite"""
    print("🧠 Running Meta-Cognitive Orchestrator Test Suite")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMetaCognitiveOrchestrator)
    suite.addTests(loader.loadTestsFromTestCase(TestMetaTestingCapabilities))
    suite.addTests(loader.loadTestsFromTestCase(TestMetaCognitiveOrchestratorIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("🧪 Test Results Summary:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_meta_testing_suite()
    exit(0 if success else 1)
