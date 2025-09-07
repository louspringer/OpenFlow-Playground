#!/usr/bin/env python3
"""
Beast Mode Spore Extractor

This script extracts and sets up the complete Beast Mode Agent Collaboration Network
from the JSON spore. Any LLM can run this to immediately get a working system.
"""

import json
import os
import sys
import asyncio
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def extract_spore(spore_file: str = "complete_beast_mode_spore.json"):
    """Extract the spore and create all necessary files."""

    print("🚀 BEAST MODE SPORE EXTRACTOR")
    print("=" * 50)

    # Load the spore
    try:
        with open(spore_file, "r") as f:
            spore = json.load(f)
        print(f"✅ Loaded spore: {spore['spore_metadata']['name']} v{spore['spore_metadata']['version']}")
    except FileNotFoundError:
        print(f"❌ Spore file not found: {spore_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in spore file: {e}")
        return False

    # Extract core system files
    print("\n📁 Extracting core system files...")
    core_system = spore["core_system"]

    for module_name, module_data in core_system.items():
        filename = module_data["file"]
        content = module_data["content"]

        with open(filename, "w") as f:
            f.write(content)
        print(f"   ✅ Created {filename}")

    # Extract auto setup script
    print("\n🔧 Extracting auto setup script...")
    auto_setup = spore["auto_setup_script"]
    with open(auto_setup["file"], "w") as f:
        f.write(auto_setup["content"])
    print(f"   ✅ Created {auto_setup['file']}")

    # Make auto setup executable
    os.chmod(auto_setup["file"], 0o755)

    # Create usage examples
    print("\n📚 Creating usage examples...")
    examples = spore["usage_examples"]

    for example_name, example_data in examples.items():
        filename = f"example_{example_name}.py"
        with open(filename, "w") as f:
            f.write(example_data["code"])
        print(f"   ✅ Created {filename}")

    # Create README
    print("\n📖 Creating README...")
    readme_content = f"""# {spore['spore_metadata']['name']}

{spore['spore_metadata']['description']}

## Quick Start

1. **Start Redis server:**
   - macOS: `brew install redis && redis-server`
   - Ubuntu: `sudo apt-get install redis-server && sudo systemctl start redis`
   - Docker: `docker run -d -p 6379:6379 redis:alpine`

2. **Run the auto setup:**
   ```bash
   python auto_setup.py
   ```

3. **Your agent is ready!**

## Features

{chr(10).join([f"- {feature}" for feature in spore['features'].values()])}

## Message Types

{chr(10).join([f"- **{msg_type}**: {description}" for msg_type, description in spore['message_types'].items()])}

## Examples

- `example_basic_agent.py` - Basic agent usage
- `example_custom_agent.py` - Custom agent with handlers

## Troubleshooting

{chr(10).join([f"- **{issue}**: {solution}" for issue, solution in spore['troubleshooting'].items()])}

## Advanced Usage

{chr(10).join([f"- **{topic}**: {description}" for topic, description in spore['advanced_usage'].items()])}

---
*This spore was created by {spore['spore_metadata']['author']} on {spore['spore_metadata']['created']}*
"""

    with open("README.md", "w") as f:
        f.write(readme_content)
    print("   ✅ Created README.md")

    print("\n🎉 SPORE EXTRACTION COMPLETE!")
    print("=" * 50)
    print("✅ All files extracted successfully")
    print("✅ System is ready to use")
    print("\nNext steps:")
    print("1. Start Redis server")
    print("2. Run: python auto_setup.py")
    print("3. Your agent is ready to collaborate!")

    return True


def check_redis():
    """Check if Redis is available."""
    try:
        import redis

        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()
        return True
    except:
        return False


def install_dependencies():
    """Install required Python dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "redis"])
        print("   ✅ Redis package installed")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Failed to install Redis package")
        return False


async def test_system():
    """Test the extracted system."""
    print("\n🧪 Testing the system...")

    # Check Redis
    if not check_redis():
        print("   ❌ Redis not available. Please start Redis server.")
        return False

    print("   ✅ Redis connection verified")

    # Test imports
    try:
        from message_models import BeastModeMessage, MessageType
        from redis_foundation import RedisConnectionManager
        from agent_discovery import AgentDiscoveryManager
        from help_system import HelpSystemManager
        from bus_client import BeastModeBusClient

        print("   ✅ All modules imported successfully")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

    # Test basic functionality
    try:
        # Create a test message
        message = BeastModeMessage(type=MessageType.SIMPLE_MESSAGE, source="test_agent", payload={"message": "Hello world"})
        print("   ✅ Message creation works")

        # Test Redis connection
        redis_manager = RedisConnectionManager()
        if await redis_manager.connect():
            print("   ✅ Redis connection works")
            await redis_manager.disconnect()
        else:
            print("   ❌ Redis connection failed")
            return False

    except Exception as e:
        print(f"   ❌ System test failed: {e}")
        return False

    print("   ✅ System test passed!")
    return True


async def main():
    """Main function."""
    print("🚀 BEAST MODE SPORE EXTRACTOR")
    print("=" * 50)

    # Extract the spore
    if not extract_spore():
        return

    # Install dependencies
    if not install_dependencies():
        print("⚠️  Dependencies installation failed, but continuing...")

    # Test the system
    if await test_system():
        print("\n🎉 EXTRACTION AND SETUP COMPLETE!")
        print("=" * 50)
        print("✅ The Beast Mode Agent Collaboration Network is ready!")
        print("✅ All files extracted and tested")
        print("✅ System is fully functional")
        print("\n🚀 Ready to collaborate!")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Please check the error messages above")


if __name__ == "__main__":
    asyncio.run(main())
