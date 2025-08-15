#!/usr/bin/env python3
"""
Call Ghostbusters for Round-Trip Model System Analysis
"""

import asyncio
import logging

from src.ghostbusters import run_ghostbusters

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def call_ghostbusters():
    """Call Ghostbusters for expert analysis of round-trip model system"""

    print("🎯 GHOSTBUSTERS EMERGENCY CALL!")
    print("=" * 50)
    print("📊 Round-Trip Model System Analysis Requested")
    print("🎯 Current Status: 66% Success Rate (2/3 components working)")
    print("❌ Critical Issues: Dependency management, Import generation")
    print("=" * 50)

    try:
        # Call Ghostbusters
        print("🚨 Calling Ghostbusters for expert analysis...")
        result = await run_ghostbusters(".")

        print("\n✅ GHOSTBUSTERS ANALYSIS COMPLETE!")
        print("=" * 50)
        print(f"📊 Confidence Score: {result.confidence_score}")
        print(f"🚨 Delusions Detected: {len(result.delusions_detected)}")
        print(f"🔧 Recovery Actions: {len(result.recovery_actions)}")
        print(f"⚠️ Errors: {len(result.errors)}")
        print(f"⚠️ Warnings: {len(result.warnings)}")
        print(f"🎯 Current Phase: {result.current_phase}")

        # Display delusions if any
        if result.delusions_detected:
            print("\n🚨 DELUSIONS DETECTED:")
            for i, delusion in enumerate(result.delusions_detected, 1):
                print(
                    f"  {i}. {delusion.get( \
    'type', 'Unknown')}: {delusion.get('description', 'No description')}",
                )

        # Display recovery actions if any
        if result.recovery_actions:
            print("\n🔧 RECOVERY ACTIONS:")
            for i, action in enumerate(result.recovery_actions, 1):
                print(
                    f"  {i}. {action.get( \
    'type', 'Unknown')}: {action.get('description', 'No description')}",
                )

        # Display errors if any
        if result.errors:
            print("\n⚠️ ERRORS:")
            for i, error in enumerate(result.errors, 1):
                print(f"  {i}. {error}")

        # Display warnings if any
        if result.warnings:
            print("\n⚠️ WARNINGS:")
            for i, warning in enumerate(result.warnings, 1):
                print(f"  {i}. {warning}")

        print("\n🎯 GHOSTBUSTERS RECOMMENDATIONS:")
        print("=" * 50)

        # Analyze round-trip model system specifically
        round_trip_issues = []
        for delusion in result.delusions_detected:
            if any(
                keyword in delusion.get("description", "").lower()
                for keyword in ["model", "round-trip", "dependency", "import"]
            ):
                round_trip_issues.append(delusion)

        if round_trip_issues:
            print("🚨 ROUND-TRIP MODEL SYSTEM ISSUES:")
            for i, issue in enumerate(round_trip_issues, 1):
                print(
                    f"  {i}. {issue.get('type', 'Unknown')}: {issue.get('description', 'No description')}",
                )
        else:
            print("✅ No specific round-trip model system issues detected")

        # Check for recovery actions related to round-trip
        round_trip_recoveries = []
        for action in result.recovery_actions:
            if any(
                keyword in action.get("description", "").lower()
                for keyword in ["model", "round-trip", "dependency", "import"]
            ):
                round_trip_recoveries.append(action)

        if round_trip_recoveries:
            print("\n🔧 ROUND-TRIP MODEL SYSTEM RECOVERIES:")
            for i, recovery in enumerate(round_trip_recoveries, 1):
                print(
                    f"  {i}. {recovery.get( \
    'type', 'Unknown')}: {recovery.get('description', 'No description')}",
                )

        print("\n🎯 NEXT STEPS:")
        print("=" * 50)
        print("1. Review Ghostbusters analysis results")
        print("2. Implement recommended recovery actions")
        print("3. Enhance round-trip model system based on findings")
        print("4. Test improvements and validate 100% success rate")
        print("5. Integrate with existing Ghostbusters infrastructure")

        return result

    except Exception as e:
        print(f"❌ Error calling Ghostbusters: {e}")
        logger.error(f"Ghostbusters call failed: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(call_ghostbusters())
