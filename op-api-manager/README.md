# OP API Manager

[![PyPI version](https://badge.fury.io/py/op-api-manager.svg)](https://badge.fury.io/py/op-api-manager)
[![Python versions](https://img.shields.io/pypi/pyversions/op-api-manager.svg)](https://pypi.python.org/pypi/op-api-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent API key discovery and management for 1Password**

OP API Manager is a Python package that provides intelligent discovery, organization, and management of API keys stored in 1Password. It automatically detects potential API keys, organizes them into logical groups, assigns unique GUIDs, and provides comprehensive CLI tools for management.

## 🚀 Features

### ✨ **Intelligent Discovery**

- **Automatic Detection**: Scans 1Password vault for items that appear to be API keys
- **Smart Filtering**: Uses multiple indicators (title, category, tags) to identify API keys
- **Provider Recognition**: Automatically detects and categorizes API keys by provider (OpenAI, Anthropic, Google, AWS, etc.)

### 🔐 **Credential Organization**

- **Automatic Pairing**: Pairs related credentials (e.g., AWS Access Key + Secret Access Key)
- **Logical Grouping**: Organizes credentials into logical groups based on provider and type
- **GUID Assignment**: Assigns unique identifiers to each discovered API key

### 💾 **Caching & Performance**

- **Intelligent Caching**: Caches discovery results to avoid repeated 1Password API calls
- **Configurable Expiry**: Set custom cache expiration times
- **Force Refresh**: Option to bypass cache when needed

### 🖥️ **Rich CLI Interface**

- **Beautiful Output**: Rich terminal output with tables, panels, and color coding
- **Multiple Commands**: Discover, summary, cache management, provider breakdown
- **Filtering Options**: Filter results by provider, status, and other criteria

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- 1Password CLI (`op`) installed and authenticated
- Access to 1Password vault

### Install from PyPI

```bash
pip install op-api-manager
```

### Install from Source

```bash
git clone https://github.com/openflow-dev/op-api-manager.git
cd op-api-manager
pip install -e .
```

## 🔧 Setup

### 1. Install 1Password CLI

```bash
# macOS
brew install --cask 1password-cli

# Linux
curl -sS https://downloads.1password.com/linux/keys/1password.asc | sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --codename) stable main" | sudo tee /etc/apt/sources.list.d/1password.list
sudo apt update && sudo apt install 1password-cli

# Windows
# Download from https://app-updates.agilebits.com/product_history/CLI2
```

### 2. Authenticate with 1Password

```bash
# Sign in to your account
op account add

# Get your account details
op account list

# Sign in to your account
op signin --account <account-name>
```

### 3. Verify Installation

```bash
# Check if op-api-manager is available
op-api-manager --help

# Check 1Password CLI connection
op item list --limit 1
```

## 🎯 Usage

### Basic Discovery

```bash
# Discover all API keys
op-api-manager discover

# Force refresh (ignore cache)
op-api-manager discover --force-refresh

# Save results to file
op-api-manager discover --output results.json
```

### View Summary

```bash
# Show all discovered API keys
op-api-manager summary

# Filter by provider
op-api-manager summary --provider openai

# Filter by status
op-api-manager summary --status working
```

### Cache Management

```bash
# Check cache status
op-api-manager cache

# Force refresh cache
op-api-manager refresh

# Use custom cache file
op-api-manager cache --cache-file /path/to/cache.json
```

### Provider Information

```bash
# Show provider breakdown
op-api-manager providers

# Show specific provider details
op-api-manager summary --provider aws
```

## 🔍 Supported Providers

OP API Manager automatically detects and categorizes API keys from these providers:

- **OpenAI**: GPT models, API keys
- **Anthropic**: Claude models, API keys
- **Google**: Gemini models, API keys, service accounts
- **AWS**: Access keys, secret keys, Bedrock
- **HuggingFace**: API tokens, model access
- **Cohere**: API keys
- **AI21**: API keys
- **Azure**: OpenAI, Cognitive Services
- **Custom**: Other API keys and credentials

## 📊 Output Examples

### Discovery Results

```
================================================================================
API Key Discovery Results
================================================================================
┌──────────────────────────────────────────────────────────────────────────────┐
│ Summary                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ Total Items: 150                                                            │
│ API Keys Found: 23                                                          │
│ Credential Pairs: 8                                                         │
│ Discovery Time: 2025-01-20T10:30:00                                        │
└──────────────────────────────────────────────────────────────────────────────┘

┌───────────┬───────┐
│ Provider  │ Count │
├───────────┼───────┤
│ openai    │ 5     │
│ anthropic │ 3     │
│ google    │ 4     │
│ aws       │ 6     │
│ huggingface│ 3    │
│ cohere    │ 2     │
└───────────┴───────┘
```

### Credential Pairs

```
┌─────────────────┬──────────────────────────────┬──────────────────────────────┬─────────────────────────────────────┐
│ Type            │ Primary                       │ Secondary                    │ Description                          │
├─────────────────┼──────────────────────────────┼──────────────────────────────┼─────────────────────────────────────┤
│ aws_access_secret│ AWS Access Key ID           │ AWS Secret Access Key       │ Auto-paired credentials for aws     │
│ single          │ OpenAI API Key               │ None                         │ Single credential for openai        │
│ google_credentials│ Google Service Account     │ Google API Key               │ Auto-paired credentials for google  │
└─────────────────┴──────────────────────────────┴──────────────────────────────┴─────────────────────────────────────┘
```

## ⚙️ Configuration

### Cache Configuration

```python
from op_api_manager import OnePasswordAPIKeyManager, CacheConfig

# Custom cache configuration
cache_config = CacheConfig(
    enabled=True,
    cache_file="my_cache.json",
    max_age_hours=12,
    auto_refresh=False
)

manager = OnePasswordAPIKeyManager(cache_config)
```

### Environment Variables

```bash
# Custom cache file location
export OP_API_CACHE_FILE="/path/to/cache.json"

# Cache expiration time (hours)
export OP_API_CACHE_MAX_AGE=24

# Disable caching
export OP_API_CACHE_ENABLED=false
```

## 🧪 Testing

### Run Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=op_api_manager

# Run specific test categories
pytest -m "unit"
pytest -m "integration"
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **CLI Tests**: Command-line interface testing

## 🔧 Development

### Project Structure

```
op-api-manager/
├── src/op_api_manager/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Data models
│   ├── core.py              # Core functionality
│   └── cli.py               # Command-line interface
├── tests/                   # Test suite
├── docs/                    # Documentation
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

### Adding New Providers

```python
# In models.py, add new provider type
class ProviderType(str, Enum):
    # ... existing providers ...
    NEW_PROVIDER = "new_provider"

# In core.py, update provider detection
def _is_api_key_item(self, item: Dict[str, Any]) -> bool:
    # ... existing logic ...
    if any(indicator in title for indicator in ["new_provider", "api_key"]):
        return True
```

### Contributing

1. Fork the repository
1. Create a feature branch
1. Make your changes
1. Add tests for new functionality
1. Ensure all tests pass
1. Submit a pull request

## 📚 API Reference

### OnePasswordAPIKeyManager

The main class for managing API key discovery and organization.

#### Methods

- `discover_api_keys(force_refresh=False)`: Discover all API keys
- `get_api_keys_by_provider(provider)`: Get keys for specific provider
- `get_working_api_keys()`: Get all working API keys
- `refresh_cache()`: Force refresh cache
- `get_cache_status()`: Get cache status information

### Models

#### APIKeyItem

Represents a discovered API key with metadata.

#### CredentialPair

Represents a pair of related credentials.

#### DiscoveryResult

Contains the complete result of a discovery operation.

#### CacheConfig

Configuration for caching operations.

## 🚨 Security Considerations

### Credential Safety

- **No Credential Storage**: OP API Manager never stores actual credential values
- **Metadata Only**: Only stores metadata (titles, IDs, categories) from 1Password
- **Secure Caching**: Cache files contain no sensitive information
- **1Password Integration**: Leverages 1Password's security for credential storage

### Best Practices

- **Regular Rotation**: Regularly rotate API keys and credentials
- **Access Control**: Limit access to 1Password vault
- **Audit Logging**: Monitor access to sensitive credentials
- **Secure Environment**: Run in secure, controlled environments

## 🤝 Support

### Getting Help

- **Documentation**: [https://op-api-manager.readthedocs.io](https://op-api-manager.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/openflow-dev/op-api-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/openflow-dev/op-api-manager/discussions)

### Common Issues

- **Authentication Errors**: Ensure 1Password CLI is properly authenticated
- **Permission Denied**: Check 1Password vault access permissions
- **Cache Issues**: Use `--force-refresh` to bypass cache problems

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **1Password Team**: For the excellent CLI tool
- **Rich Library**: For beautiful terminal output
- **Click Library**: For robust CLI framework
- **Pydantic**: For data validation and serialization

## 🚀 Roadmap

### Upcoming Features

- **Credential Testing**: Test API keys for validity
- **Cost Tracking**: Track API usage and costs
- **Integration APIs**: Python library for programmatic use
- **Web Interface**: Web-based management dashboard
- **Multi-Vault Support**: Support for multiple 1Password vaults

### Version History

- **v0.1.0**: Initial release with basic discovery and CLI
- **v0.2.0**: Enhanced credential pairing and caching
- **v0.3.0**: Provider-specific optimizations and testing

______________________________________________________________________

**Made with ❤️ by the OpenFlow Team**

For more information, visit [https://github.com/openflow-dev/op-api-manager](https://github.com/openflow-dev/op-api-manager)
