#!/usr/bin/env python3
"""
Simple test script for Ghostbusters API
"""

import time

import requests

BASE_URL = "https://us-central1-aardvark-linkedin-grepper.cloudfunctions.net"


def test_ghostbusters_api():
    """Test the Ghostbusters API endpoints"""

    print("🎯 Testing Ghostbusters API")
    print("=" * 40)

    # Test analysis
    print("\n📊 Testing analysis endpoint...")
    analysis_payload = {"project_path": ".", "agents": ["security", "code_quality"]}

    response = requests.post(f"{BASE_URL}/ghostbusters-analyze", json=analysis_payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        job_id = result["job_id"]
        print(f"✅ Analysis queued: {job_id}")

        # Wait and check status
        print("\n⏳ Waiting for analysis to complete...")
        for i in range(6):  # Wait up to 30 seconds
            time.sleep(5)
            status_response = requests.get(
                f"{BASE_URL}/ghostbusters-status?job_id={job_id}",
            )

            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"Status: {status_data['status']}")

                if status_data["status"] == "completed":
                    print("✅ Analysis completed!")
                    if status_data.get("result"):
                        result = status_data["result"]
                        print(f"  Delusions found: {result.get('delusions_found', 0)}")
                        print(f"  Analysis time: {result.get('analysis_time', 'N/A')}")
                    break
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                break
    else:
        print(f"❌ Analysis failed: {response.status_code}")
        print(response.text)

    # Test recovery
    print("\n🔧 Testing recovery endpoint...")
    recovery_payload = {"recovery_type": "syntax", "target_files": ["src/main.py"]}

    response = requests.post(f"{BASE_URL}/ghostbusters-recover", json=recovery_payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        job_id = result["job_id"]
        print(f"✅ Recovery queued: {job_id}")

        # Wait and check status
        print("\n⏳ Waiting for recovery to complete...")
        for i in range(6):  # Wait up to 30 seconds
            time.sleep(5)
            status_response = requests.get(
                f"{BASE_URL}/ghostbusters-status?job_id={job_id}",
            )

            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"Status: {status_data['status']}")

                if status_data["status"] == "completed":
                    print("✅ Recovery completed!")
                    if status_data.get("result"):
                        result = status_data["result"]
                        print(f"  Files processed: {result.get('files_processed', 0)}")
                        print(f"  Files fixed: {result.get('files_fixed', 0)}")
                        print(f"  Recovery time: {result.get('recovery_time', 'N/A')}")
                    break
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                break
    else:
        print(f"❌ Recovery failed: {response.status_code}")
        print(response.text)

    print("\n🎉 API test completed!")


if __name__ == "__main__":
    test_ghostbusters_api()
