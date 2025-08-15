#!/usr/bin/env python3
"""
Cloud Build Webhook Trigger Setup
Alternative to GitHub integration using webhook triggers
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


def create_webhook_trigger(token: str) -> None:
    """Create webhook-based build trigger."""
    print("🎯 Creating webhook-based trigger...")

    url = "https://cloudbuild.googleapis.com/v1/projects/aardvark-linkedin-grepper/triggers"

    data = {
        "name": "ghostbusters-api-webhook-trigger",
        "description": "Webhook-based trigger for Ghostbusters API",
        "webhookConfig": {"secret": "webhook-secret-123"},
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
        print("✅ Webhook trigger created successfully!")
        print("🔗 Webhook URL will be provided in the response")
    else:
        print("❌ Webhook trigger creation failed")


def main() -> None:
    """Main setup function using webhook trigger."""
    print("🚀 Creating Cloud Build webhook trigger...")
    print("📋 Project: aardvark-linkedin-grepper")
    print("🌍 Region: us-central1")
    print("🔧 Method: Webhook-based trigger")
    print()

    try:
        # Get access token
        token = run_gcloud_auth()
        print("🔑 Authentication successful")

        # Create webhook trigger
        create_webhook_trigger(token)

        print()
        print("📊 Summary:")
        print("   Trigger: ghostbusters-api-webhook-trigger")
        print("   Type: Webhook-based")
        print("   Secret: webhook-secret-123")
        print()
        print(
            "🔗 View triggers: https://console.cloud.google.com/cloud-build/triggers?project = \
    aardvark-linkedin-grepper",
        )
        print("🧪 Test with: curl -X POST <webhook-url>")

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
