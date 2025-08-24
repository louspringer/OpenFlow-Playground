#!/usr/bin/env python3
"""
Cache Manager Integration for OP-API-Manager

This script integrates the cache-manager to fix the op-manager's cache loading issues.
"""

import sys
import json
from pathlib import Path

# Add cache-manager to path
sys.path.append('../cache-manager/src')

try:
    from cache_manager.core import CacheManager
    from cache_manager.models import CacheConfig
    CACHE_MANAGER_AVAILABLE = True
except ImportError:
    CACHE_MANAGER_AVAILABLE = False
    print("⚠️  Cache manager not available")


def load_cache_with_cache_manager(cache_file: str = "api_discovery_cache.json") -> dict:
    """Load cache using the cache-manager."""
    if not CACHE_MANAGER_AVAILABLE:
        print("❌ Cache manager not available")
        return {}
    
    try:
        # Create cache manager
        config = CacheConfig(cache_dir=Path("."))
        manager = CacheManager(config)
        
        # Load cache
        cache_key = "api_discovery_cache"
        data = manager.load_cache(cache_key, Path(cache_file))
        
        if data:
            print("✅ Cache loaded successfully using cache-manager")
            print("📊 Found {} API keys".format(len(data.get('api_keys', []))))
            return data
        else:
            print("❌ No cache data found")
            return {}
            
    except Exception as e:
        print(f"❌ Error loading cache with cache-manager: {e}")
        return {}


def validate_cache_data(data: dict) -> bool:
    """Validate that cache data has the expected structure."""
    if not data:
        return False
    
    required_fields = ["api_keys", "total_items"]
    for field in required_fields:
        if field not in data:
            print(f"❌ Missing required field: {field}")
            return False
    
    api_keys = data.get("api_keys", [])
    if not isinstance(api_keys, list):
        print("❌ api_keys field is not a list")
        return False
    
    print("✅ Cache data structure is valid")
    print("📊 Total items: {}".format(data.get('total_items', 0)))
    print("📊 API keys count: {}".format(len(api_keys)))
    
    # Show API key details
    for i, key in enumerate(api_keys):
        print(f"   🔑 Key {i+1}: {key.get('title', 'Unknown')} ({key.get('provider', 'unknown')})")
    
    return True


def fix_cache_file(cache_file: str = "api_discovery_cache.json"):
    """Fix common cache file issues."""
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        # Fix total_items if it doesn't match actual count
        actual_count = len(data.get("api_keys", []))
        if data.get("total_items", 0) != actual_count:
            print(f"🔧 Fixing total_items: {data.get('total_items', 0)} → {actual_count}")
            data["total_items"] = actual_count
        
        # Ensure all API keys have required fields
        for key in data.get("api_keys", []):
            if "provider" not in key and "detected_provider" in key:
                key["provider"] = key["detected_provider"]
                print(f"🔧 Fixed provider field for: {key.get('title', 'Unknown')}")
        
        # Save fixed cache
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Cache file fixed and saved")
        return data
        
    except Exception as e:
        print(f"❌ Error fixing cache file: {e}")
        return {}


def main():
    """Main integration function."""
    print("🔧 Cache Manager Integration for OP-API-Manager")
    print("=" * 50)
    
    # Check if cache file exists
    cache_file = "api_discovery_cache.json"
    if not Path(cache_file).exists():
        print(f"❌ Cache file not found: {cache_file}")
        return
    
    print(f"📁 Found cache file: {cache_file}")
    
    # Try to load with cache-manager first
    print("\n🔍 Attempting to load cache with cache-manager...")
    data = load_cache_with_cache_manager(cache_file)
    
    if data:
        # Validate the data
        print("\n🔍 Validating cache data...")
        if validate_cache_data(data):
            print("\n✅ Cache integration successful!")
            return
        else:
            print("\n⚠️  Cache data validation failed")
    
    # Fallback: try to fix the cache file
    print("\n🔧 Attempting to fix cache file...")
    fixed_data = fix_cache_file(cache_file)
    
    if fixed_data:
        # Try loading again with cache-manager
        print("\n🔍 Retrying cache load with cache-manager...")
        data = load_cache_with_cache_manager(cache_file)
        
        if data and validate_cache_data(data):
            print("\n✅ Cache integration successful after fixing!")
        else:
            print("\n❌ Cache integration still failed")
    else:
        print("\n❌ Failed to fix cache file")


if __name__ == "__main__":
    main()
