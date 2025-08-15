#!/usr/bin/env python3
"""
GitHub Cloud Build Setup Script using 1st-gen GitHub integration
Uses GitHub App installation approach
"""

import json
import subprocess
import sys
from typing import Any, Optional


def run_gcloud_auth() -> str:
    """Get access token for REST API calls."""
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def make_rest_call(
    method: str,
    url: str,
    data: Optional[dict[str, Any]] = None,
    token: Optional[str] = None,
) -> dict[str, Any]:
    """Make REST API call to Google Cloud."""
    if token is None:
        token = run_gcloud_auth()

    cmd = [
        "curl",
        "-X",
        method,
        "-H",
        f"Authorization: Bearer {token}",
        "-H",
        "Content-Type: application/json",
    ]

    if data:
        cmd.extend(["-d", json.dumps(data)])

    cmd.append(url)

    print(f"🔧 Making {method} request to: {url}")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"⚠️  Non-JSON response: {result.stdout}")
            return {}
    else:
        print("⚠️  Empty response")
        return {}


def create_1stgen_trigger(token: str) -> None:
    """Create build trigger using 1st-gen GitHub integration."""
    print("🎯 Creating 1st-gen GitHub trigger...")

    url = "https://cloudbuild.googleapis.com/v1/projects/aardvark-linkedin-grepper/triggers"

    data = {
        "name": "ghostbusters-api-develop-trigger",
        "description": "Automatic build and deploy Ghostbusters API on push to develop branch",
        "github": {
            "name": "OpenFlow-Playground",
            "owner": "louspringer",
            "push": {"branch": "^develop$"},
        },
        "build": {
            "steps": [
                {
                    "name": "gcr.io/cloud-builders/docker",
                    "args": [
                        "build",
                        "-t",
                        "gcr.io/aardvark-linkedin-grepper/ghostbusters-api:latest",
                        ".",
                    ],
                    "dir": "src/ghostbusters_api",
                },
            ],
            "images": ["gcr.io/aardvark-linkedin-grepper/ghostbusters-api:latest"],
        },
    }

    response = make_rest_call("POST", url, data, token)
    print(f"📋 Trigger creation response: {response}")

    if "error" not in response:
        print("✅ Build trigger created successfully!")
    else:
        print("❌ Trigger creation failed")


def main() -> None:
    """Main setup function using 1st-gen GitHub integration."""
    print("🚀 Setting up GitHub Cloud Build integration using 1st-gen approach...")
    print("📋 Project: aardvark-linkedin-grepper")
    print("🌍 Region: us-central1")
    print("📦 Repository: louspringer/OpenFlow-Playground")
    print("🔧 Method: 1st-gen GitHub App integration")
    print()

    try:
        # Get access token
        token = run_gcloud_auth()
        print("🔑 Authentication successful")

        # Create 1st-gen trigger
        create_1stgen_trigger(token)

        print()
        print("📊 Summary:")
        print("   Method: 1st-gen GitHub integration")
        print("   Trigger: ghostbusters-api-develop-trigger")
        print("   Branch: develop")
        print()
        print(
            "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project = \
    aardvark-linkedin-grepper",
        )
        print("🧪 Test with: git push origin develop")

    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
