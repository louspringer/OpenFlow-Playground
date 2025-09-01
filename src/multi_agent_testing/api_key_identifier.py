#!/usr/bin/env python3
"""
API Key Identifier

This script tests an API key against different providers to identify which service it belongs to.
"""

import os
from typing import Any, Optional

import requests


def test_openai_api(api_key: str) -> Optional[dict[str, Any]]:
    """Test if API key works with OpenAI"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
        if response.status_code == 200:
            return {
                "provider": "openai",
                "status": "working",
                "models": response.json(),
            }
        return {"provider": "openai", "status": "failed", "error": response.status_code}
    except Exception as e:
        return {"provider": "openai", "status": "error", "error": str(e)}


def test_anthropic_api(api_key: str) -> Optional[dict[str, Any]]:
    """Test if API key works with Anthropic"""
    try:
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers, timeout=10)
        if response.status_code == 200:
            return {
                "provider": "anthropic",
                "status": "working",
                "models": response.json(),
            }
        return {
            "provider": "anthropic",
            "status": "failed",
            "error": response.status_code,
        }
    except Exception as e:
        return {"provider": "anthropic", "status": "error", "error": str(e)}


def test_google_api(api_key: str) -> Optional[dict[str, Any]]:
    """Test if API key works with Google AI"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            "https://generativelanguage.googleapis.com/v1beta/models",
            headers=headers,
            timeout=10,
        )
        if response.status_code == 200:
            return {
                "provider": "google",
                "status": "working",
                "models": response.json(),
            }
        return {"provider": "google", "status": "failed", "error": response.status_code}
    except Exception as e:
        return {"provider": "google", "status": "error", "error": str(e)}


def test_openrouter_api(api_key: str) -> Optional[dict[str, Any]]:
    """Test if API key works with OpenRouter"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
        if response.status_code == 200:
            return {
                "provider": "openrouter",
                "status": "working",
                "models": response.json(),
            }
        return {
            "provider": "openrouter",
            "status": "failed",
            "error": response.status_code,
        }
    except Exception as e:
        return {"provider": "openrouter", "status": "error", "error": str(e)}


def identify_api_key(api_key: str) -> dict[str, Any]:
    """Test API key against all providers to identify which one it belongs to"""
    print(f"🔍 Testing API key: {api_key[:8]}...")
    print()

    results = {}

    # Test OpenAI
    print("🧪 Testing OpenAI...")
    results["openai"] = test_openai_api(api_key)
    print(f"   Result: {results['openai']['status']}")

    # Test Anthropic
    print("🧪 Testing Anthropic...")
    results["anthropic"] = test_anthropic_api(api_key)
    print(f"   Result: {results['anthropic']['status']}")

    # Test Google
    print("🧪 Testing Google AI...")
    results["google"] = test_google_api(api_key)
    print(f"   Result: {results['google']['status']}")

    # Test OpenRouter
    print("🧪 Testing OpenRouter...")
    results["openrouter"] = test_openrouter_api(api_key)
    print(f"   Result: {results['openrouter']['status']}")

    print()

    # Find working providers
    working_providers = [k for k, v in results.items() if v["status"] == "working"]

    if working_providers:
        print(f"✅ API key works with: {', '.join(working_providers)}")
        for provider in working_providers:
            print(f"   📊 {provider.upper()}: {results[provider]}")
    else:
        print("❌ API key doesn't work with any tested providers")
        print("   This might be:")
        print("   - An expired key")
        print("   - A key for a different service")
        print("   - A malformed key")

    return results


def main():
    """Main function"""
    # Get API key from environment or command line
    api_key = os.getenv("UNKNOWN_API_KEY")

    if not api_key:
        print("❌ No UNKNOWN_API_KEY found in environment")
        print("   Set it with: export UNKNOWN_API_KEY='your_key_here'")
        return

    print("🔑 API Key Identifier")
    print("=" * 50)
    print()

    results = identify_api_key(api_key)

    print()
    print("📋 Summary:")
    for provider, result in results.items():
        status_emoji = "✅" if result["status"] == "working" else "❌"
        print(f"   {status_emoji} {provider.upper()}: {result['status']}")


if __name__ == "__main__":
    main()
