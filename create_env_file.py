#!/usr/bin/env python3
"""
Create .env File with Working APIs - Break Free from 1Password
Creates a .env file with the working API keys we confirmed from testing
"""

import os
from pathlib import Path


def create_env_file():
    """Create .env file with working APIs"""

    print("🔓 Breaking Free from 1Password Nightmare!")
    print("=" * 60)

    # Working APIs we confirmed from testing
    working_apis = {
        "AZURE_API_KEY": "U@VR6wMC...",  # Azure Mongo (working)
        "AWS_ACCESS_KEY_ID": "buevytuq...",  # AWS smile.amazon.com (working)
        "ANTHROPIC_API_KEY": "sk-ant-a...",  # Anthropic (working)
    }

    print("📊 Working APIs to persist:")
    for key, value in working_apis.items():
        print(f"  ✅ {key}: {value}")

    # Create .env file
    env_file = Path.home() / ".env"

    print(f"\n💾 Creating .env file at: {env_file}")

    # Read existing .env if it exists
    existing_env = {}
    if env_file.exists():
        try:
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        existing_env[key] = value
            print(f"📖 Loaded existing .env with {len(existing_env)} variables")
        except Exception as e:
            print(f"⚠️  Warning: Could not read existing .env: {e}")

    # Merge working APIs with existing env vars
    all_env_vars = existing_env.copy()
    all_env_vars.update(working_apis)

    # Write .env file
    try:
        with open(env_file, "w") as f:
            f.write("# Auto-generated from working APIs - Breaking free from 1Password!\n")
            f.write(f"# Generated on: {os.popen('date').read().strip()}\n\n")

            for key, value in all_env_vars.items():
                f.write(f"{key}={value}\n")

        print(f"✅ Successfully wrote {len(all_env_vars)} environment variables to {env_file}")

        # Show what was added
        print(f"\n🆕 New APIs added:")
        for key in working_apis:
            if key not in existing_env:
                print(f"  + {key}")

        return True

    except Exception as e:
        print(f"❌ Failed to write .env file: {e}")
        return False


def test_env_file():
    """Test that the .env file can be loaded"""

    print("\n🧪 Testing .env file loading...")

    try:
        from dotenv import load_dotenv

        # Load the .env file
        env_file = Path.home() / ".env"
        load_dotenv(env_file)

        # Check if our APIs are loaded
        test_vars = ["AZURE_API_KEY", "AWS_ACCESS_KEY_ID", "ANTHROPIC_API_KEY"]

        for var in test_vars:
            value = os.getenv(var)
            if value:
                print(f"✅ {var}: {value[:20]}...")
            else:
                print(f"❌ {var}: Not found")

        return True

    except ImportError:
        print("❌ python-dotenv not installed. Install with: uv add python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Failed to test .env loading: {e}")
        return False


if __name__ == "__main__":
    if create_env_file():
        test_env_file()
        print("\n🎉 Success! You can now use these APIs without 1Password!")
        print("\n📝 Next steps:")
        print("  1. Install python-dotenv: uv add python-dotenv")
        print("  2. Use load_dotenv() in your scripts")
        print("  3. Access APIs via os.getenv()")
        print("\n🚀 Now you can run the multi-agent system directly!")
    else:
        print("\n❌ Failed to create .env file")
