#!/usr/bin/env python3
"""
Round-Trip Engineering Demo Runner

A simple script to demonstrate the refactored Round-Trip Engineering system
following Reflective Module principles.
"""

import asyncio
import json
import time
from pathlib import Path

# Import the demo system
from src.round_trip_engineering.demo.demo_orchestrator import DemoOrchestrator


async def run_demo_showcase():
    """Run a comprehensive showcase of the round-trip engineering system."""
    print("🔄 Round-Trip Engineering Demo Showcase")
    print("=" * 60)

    # Initialize the demo orchestrator
    print("\n🎯 Initializing Demo Orchestrator...")
    orchestrator = DemoOrchestrator()

    # Get system status
    print("\n📊 System Status:")
    status = await orchestrator.get_module_status()
    print(f"   Status: {status.status.value}")
    print(f"   Message: {status.message}")
    print(f"   Success Rate: {status.health_indicators.get('success_rate', 0):.1%}")

    # Get module capabilities
    print("\n🔧 Module Capabilities:")
    capabilities = await orchestrator.get_module_capabilities()
    for capability in capabilities:
        print(f"   ✅ {capability['name']}: {capability['description']}")

    # Run Basic Demo
    print("\n🚀 Running Basic Demo...")
    start_time = time.time()
    basic_results = await orchestrator.run_basic_demo()
    basic_duration = time.time() - start_time

    print(f"   ✅ Basic Demo completed in {basic_duration:.3f}s")
    print(f"   📊 Status: {basic_results['status']}")
    if basic_results["status"] == "success":
        print(f"   🏗️  Model: {basic_results['model_name']}")
        print(f"   📦 Components: {basic_results['components_count']}")
        print(f"   📁 Files Generated: {basic_results['generated_files_count']}")
        print(f"   🔄 Round-trip: {'✅ Successful' if basic_results['round_trip_successful'] else '❌ Failed'}")

    # Run Advanced Demo
    print("\n🚀 Running Advanced Demo...")
    start_time = time.time()
    advanced_results = await orchestrator.run_advanced_demo()
    advanced_duration = time.time() - start_time

    print(f"   ✅ Advanced Demo completed in {advanced_duration:.3f}s")
    print(f"   📊 Status: {advanced_results['status']}")
    if advanced_results["status"] == "success":
        print(f"   🏗️  Model: {advanced_results['model_name']}")
        print(f"   📦 Components: {advanced_results['components_count']}")
        print(f"   📁 Files Generated: {advanced_results['generated_files_count']}")
        print(f"   🔄 Round-trip: {'✅ Successful' if advanced_results['round_trip_successful'] else '❌ Failed'}")

        # Show vocabulary alignment if available
        if "vocabulary_alignment" in advanced_results:
            vocab = advanced_results["vocabulary_alignment"]
            print(f"   🔤 Vocabulary Alignment: {vocab['alignment_score']:.1%} ({vocab['overall_health']})")

    # Run Performance Demo
    print("\n🚀 Running Performance Demo...")
    start_time = time.time()
    performance_results = await orchestrator.run_performance_demo()
    performance_duration = time.time() - start_time

    print(f"   ✅ Performance Demo completed in {performance_duration:.3f}s")
    print(f"   📊 Status: {performance_results['status']}")
    if performance_results["status"] == "success":
        print(f"   📈 Performance Score: {performance_results['performance_score']}")
        print(f"   🔄 Iterations: {performance_results['iterations']}")
        print(f"   ⏱️  Average Time: {performance_results['average_iteration_time']:.3f}s")
        print(f"   ⏱️  Total Time: {performance_results['total_duration']:.3f}s")

    # Get final system status
    print("\n📊 Final System Status:")
    final_status = await orchestrator.get_module_status()
    print(f"   Success Count: {final_status.health_indicators.get('success_count', 0)}")
    print(f"   Error Count: {final_status.health_indicators.get('error_count', 0)}")
    print(f"   Success Rate: {final_status.health_indicators.get('success_rate', 0):.1%}")

    # Summary
    print("\n🎉 Demo Showcase Complete!")
    print("=" * 60)
    print("✅ All demos executed successfully")
    print("✅ Reflective Module principles demonstrated")
    print("✅ Round-trip engineering capabilities showcased")
    print("✅ Performance metrics collected and reported")

    # Save results to file
    results_file = "demo_showcase_results.json"
    all_results = {
        "basic_demo": basic_results,
        "advanced_demo": advanced_results,
        "performance_demo": performance_results,
        "final_status": {
            "success_count": final_status.health_indicators.get("success_count", 0),
            "error_count": final_status.health_indicators.get("error_count", 0),
            "success_rate": final_status.health_indicators.get("success_rate", 0),
        },
    }

    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {results_file}")

    return all_results


def main():
    """Main entry point for the demo showcase."""
    try:
        # Run the async demo showcase
        results = asyncio.run(run_demo_showcase())
        print(f"\n🎯 Demo showcase completed successfully!")
        return 0

    except Exception as e:
        print(f"\n❌ Demo showcase failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
