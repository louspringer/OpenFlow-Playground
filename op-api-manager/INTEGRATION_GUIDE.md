# 🔗 OP API Manager Integration Guide

## Overview

This guide explains how to integrate the OP API Manager with the main multi-agent system and other projects. The OP API Manager provides a clean, focused interface for 1Password API key discovery and management.

## 🚀 Quick Start

### 1. Install the Package

```bash
# From the op-api-manager directory
make install

# Or manually
pip install -e .
```

### 2. Verify Installation

```bash
# Check if CLI is available
make check-cli

# Check if 1Password CLI is available
make check-op

# Test basic functionality
make op-discover
```

### 3. Run Integration Test

```bash
# Test integration with main project
python integrate_with_main.py
```

## 🔧 Integration Methods

### Method 1: Direct Import (Recommended)

```python
from op_api_manager import OnePasswordAPIKeyManager, CacheConfig

# Initialize with custom cache
cache_config = CacheConfig(
    cache_file="my_cache.json",
    max_age_hours=12
)

manager = OnePasswordAPIKeyManager(cache_config)

# Discover API keys
result = manager.discover_api_keys()

# Get working keys
working_keys = manager.get_working_api_keys()

# Get keys by provider
openai_keys = manager.get_api_keys_by_provider("openai")
```

### Method 2: Integration Bridge

```python
from integrate_with_main import OPManagerIntegration

# Initialize integration
integration = OPManagerIntegration()

# Get working API keys
working_keys = integration.get_working_api_keys()

# Get discovery summary
summary = integration.get_discovery_summary()

# Get credential pairs
pairs = integration.get_credential_pairs()
```

### Method 3: CLI Integration

```bash
# Discover and save results
make op-discover-save

# Get provider-specific summary
make op-summary-provider PROVIDER=openai

# Get status-specific summary
make op-summary-status STATUS=working

# Check overall status
make op-status
```

## 🎯 Use Cases

### 1. Multi-Agent System Integration

Replace the old `op_api_key_manager.py` import with:

```python
# OLD (remove this)
# from scripts.op_api_key_manager import OnePasswordAPIKeyManager

# NEW (use this)
from op_api_manager import OnePasswordAPIKeyManager

# Initialize manager
manager = OnePasswordAPIKeyManager()

# Get working API keys for LLM analysis
working_keys = manager.get_working_api_keys()

# Use keys in multi-agent system
for key in working_keys:
    if key.provider.value == "openai":
        # Use OpenAI key
        pass
    elif key.provider.value == "anthropic":
        # Use Anthropic key
        pass
```

### 2. Standalone Scripts

```python
#!/usr/bin/env python3
"""Script to check API key status."""

from op_api_manager import OnePasswordAPIKeyManager

def check_api_status():
    manager = OnePasswordAPIKeyManager()
    
    # Get summary
    result = manager.discover_api_keys()
    
    print(f"Total API keys: {len(result.api_keys)}")
    print(f"Working keys: {len([k for k in result.api_keys if k.status.value == 'working'])}")
    
    # Check specific providers
    for provider in ["openai", "anthropic", "google", "aws"]:
        keys = manager.get_api_keys_by_provider(provider)
        print(f"{provider}: {len(keys)} keys")

if __name__ == "__main__":
    check_api_status()
```

### 3. CI/CD Integration

```yaml
# .github/workflows/check-api-keys.yml
name: Check API Keys

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM

jobs:
  check-keys:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install OP API Manager
        run: |
          cd op-api-manager
          pip install -e .
      
      - name: Check API Keys
        run: |
          cd op-api-manager
          op-api-manager discover --output api_keys_report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: api-keys-report
          path: op-api-manager/api_keys_report.json
```

## 🔄 Migration from Old System

### Step 1: Update Imports

```python
# OLD
from scripts.op_api_key_manager import OnePasswordAPIKeyManager

# NEW
from op_api_manager import OnePasswordAPIKeyManager
```

### Step 2: Update Configuration

```python
# OLD
manager = OnePasswordAPIKeyManager()

# NEW (with optional custom config)
from op_api_manager import CacheConfig

cache_config = CacheConfig(
    cache_file="api_keys_cache.json",
    max_age_hours=24
)
manager = OnePasswordAPIKeyManager(cache_config)
```

### Step 3: Update Method Calls

```python
# OLD
keys = manager.get_api_keys()

# NEW
result = manager.discover_api_keys()
keys = result.api_keys

# Or use convenience methods
working_keys = manager.get_working_api_keys()
openai_keys = manager.get_api_keys_by_provider("openai")
```

## 🛠️ Development Workflow

### 1. Setup Development Environment

```bash
cd op-api-manager
make dev-setup
```

### 2. Run Development Checks

```bash
# Format and lint
make format
make lint

# Run tests
make test
make test-cov

# Test OP Manager
make op-discover
make op-summary
```

### 3. Test Integration

```bash
# Test with main project
make link-main
python integrate_with_main.py
make unlink-main
```

## 📊 Monitoring and Maintenance

### 1. Regular Status Checks

```bash
# Daily status check
make status

# Weekly detailed check
make op-discover-fresh
make op-summary
make op-providers
```

### 2. Cache Management

```bash
# Check cache status
make op-cache

# Force refresh when needed
make op-refresh

# Clean old cache files
make clean
```

### 3. Performance Monitoring

```bash
# Test discovery performance
time make op-discover

# Check cache hit rates
make op-cache
```

## 🚨 Troubleshooting

### Common Issues

#### 1. CLI Not Available

```bash
# Check if package is installed
make check-cli

# Reinstall if needed
make install
```

#### 2. 1Password CLI Issues

```bash
# Check 1Password CLI
make check-op

# Authenticate if needed
op signin --account <your-account>
```

#### 3. Cache Issues

```bash
# Force refresh
make op-refresh

# Clean cache
make clean
make op-discover
```

#### 4. Import Errors

```python
# Check if package is in path
import sys
print(sys.path)

# Add to path if needed
sys.path.insert(0, '/path/to/op-api-manager/src')
```

### Debug Mode

```bash
# Enable debug output
export OP_DEBUG=1
make op-discover

# Check logs
tail -f api_discovery_cache.json
```

## 🔮 Advanced Integration

### 1. Custom Cache Backends

```python
from op_api_manager import OnePasswordAPIKeyManager
from op_api_manager.models import CacheConfig

# Custom cache configuration
cache_config = CacheConfig(
    enabled=True,
    cache_file="/var/cache/op_manager/api_keys.json",
    max_age_hours=6,
    auto_refresh=True
)

manager = OnePasswordAPIKeyManager(cache_config)
```

### 2. Event-Driven Updates

```python
import time
from op_api_manager import OnePasswordAPIKeyManager

manager = OnePasswordAPIKeyManager()

def monitor_api_keys():
    """Monitor API keys for changes."""
    last_count = 0
    
    while True:
        result = manager.discover_api_keys()
        current_count = len(result.api_keys)
        
        if current_count != last_count:
            print(f"API key count changed: {last_count} -> {current_count}")
            last_count = current_count
        
        time.sleep(300)  # Check every 5 minutes

# Run in background
import threading
monitor_thread = threading.Thread(target=monitor_api_keys, daemon=True)
monitor_thread.start()
```

### 3. Multi-Project Integration

```python
# Shared configuration
OP_MANAGER_CONFIG = {
    "cache_file": "/shared/cache/op_api_keys.json",
    "max_age_hours": 12
}

# Project A
from op_api_manager import OnePasswordAPIKeyManager, CacheConfig
config_a = CacheConfig(**OP_MANAGER_CONFIG)
manager_a = OnePasswordAPIKeyManager(config_a)

# Project B (same cache)
config_b = CacheConfig(**OP_MANAGER_CONFIG)
manager_b = OnePasswordAPIKeyManager(config_b)
```

## 📚 Additional Resources

### Documentation

- [README.md](README.md) - Package overview and usage
- [PACKAGE_SUMMARY.md](PACKAGE_SUMMARY.md) - Technical details
- [examples/basic_usage.py](examples/basic_usage.py) - Basic usage examples

### Commands Reference

```bash
# Package management
make install          # Install package
make install-dev      # Install with dev dependencies
make build            # Build distribution
make clean            # Clean artifacts

# Testing
make test             # Run tests
make test-cov         # Run with coverage
make lint             # Check code quality
make format           # Format code

# OP Manager operations
make op-discover      # Discover API keys
make op-summary       # Show summary
make op-cache         # Check cache
make op-providers     # Show providers
make op-refresh       # Force refresh
make op-status        # Overall status

# Development
make dev-setup        # Setup dev environment
make dev-test         # Run all dev checks
make examples         # Run examples
make docs             # Generate docs

# Integration
make link-main        # Link to main project
make unlink-main      # Unlink from main project
```

### Support

- **Issues**: Create GitHub issues for bugs or feature requests
- **Documentation**: Check the README and examples
- **Integration**: Use the integration bridge for complex use cases

---

**Happy integrating! 🚀**

The OP API Manager provides a clean, professional interface for 1Password API key management that can be easily integrated into any Python project.

