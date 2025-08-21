#!/usr/bin/env python3
"""
1Password Integration Utility

Provides secure access to credentials stored in 1Password
using item IDs from environment configuration.
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class OnePasswordIntegration:
    """Secure integration with 1Password CLI"""

    def __init__(self):
        self.op_available = self._check_op_availability()
        if not self.op_available:
            logger.warning(
                "1Password CLI (op) not available. Credential lookup will fail."
            )

    def _check_op_availability(self) -> bool:
        """Check if 1Password CLI is available"""
        try:
            result = subprocess.run(
                ["op", "--version"], capture_output=True, text=True, check=False
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.SubprocessError):
            return False

    def get_credential(
        self, item_id: str, field_name: str = "password"
    ) -> Optional[str]:
        """Get a credential from 1Password by item ID and field name"""
        if not self.op_available:
            logger.error("1Password CLI not available")
            return None

        try:
            # Use op read to get the field value
            cmd = ["op", "read", f"op://Private/{item_id}/{field_name}"]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            credential = result.stdout.strip()
            if credential:
                logger.debug(
                    f"Retrieved credential for item {item_id}, field {field_name}"
                )
                return credential
            logger.warning(
                f"No credential found for item {item_id}, field {field_name}"
            )
            return None

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve credential from 1Password: {e}")
            logger.error(f"Command output: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving credential: {e}")
            return None

    def get_item_details(self, item_id: str) -> Optional[dict[str, Any]]:
        """Get full item details from 1Password"""
        if not self.op_available:
            logger.error("1Password CLI not available")
            return None

        try:
            cmd = ["op", "item", "get", item_id, "--format", "json"]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            import json

            item_data = json.loads(result.stdout)
            logger.debug(f"Retrieved item details for {item_id}")
            return item_data

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve item details from 1Password: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving item details: {e}")
            return None

    def list_available_fields(self, item_id: str) -> Optional[list[str]]:
        """List available fields for a 1Password item"""
        item_data = self.get_item_details(item_id)
        if not item_data:
            return None

        try:
            fields = []
            for field in item_data.get("fields", []):
                field_name = field.get("label", "unknown")
                field_type = field.get("type", "unknown")
                fields.append(f"{field_name} ({field_type})")

            return fields
        except Exception as e:
            logger.error(f"Failed to parse item fields: {e}")
            return None


class CredentialManager:
    """Manages credential retrieval from environment and 1Password"""

    def __init__(self):
        self.op_integration = OnePasswordIntegration()
        self.env_file = Path.home() / ".env"
        self._load_env_vars()

    def _load_env_vars(self):
        """Load environment variables from .env file"""
        if self.env_file.exists():
            try:
                with open(self.env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            os.environ[key] = value
                logger.info(f"Loaded environment variables from {self.env_file}")
            except Exception as e:
                logger.error(f"Failed to load .env file: {e}")

    def get_gitguardian_api_token(self) -> Optional[str]:
        """Get GitGuardian API token from 1Password"""
        item_id = os.getenv("GITGUARDIAN_API_ITEM_ID")
        if not item_id:
            logger.error("GITGUARDIAN_API_ITEM_ID not set in environment")
            return None

        # Try to get the API token from 1Password
        token = self.op_integration.get_credential(item_id, "API Key")
        if not token:
            # Fallback to password field if API Key doesn't exist
            token = self.op_integration.get_credential(item_id, "password")

        if token:
            logger.info("Successfully retrieved GitGuardian API token from 1Password")
            return token
        logger.error("Failed to retrieve GitGuardian API token from 1Password")
        return None

    def get_neo4j_credentials(self) -> Optional[dict[str, str]]:
        """Get Neo4j credentials from 1Password"""
        item_id = os.getenv("NEO4J_CREDENTIALS_ITEM_ID")
        if not item_id:
            logger.warning(
                "NEO4J_CREDENTIALS_ITEM_ID not set, using environment defaults"
            )
            return {
                "username": os.getenv("NEO4J_USERNAME", "neo4j"),
                "password": os.getenv("NEO4J_PASSWORD", ""),
            }

        # Get credentials from 1Password
        username = self.op_integration.get_credential(item_id, "username")
        password = self.op_integration.get_credential(item_id, "password")

        if username and password:
            logger.info("Successfully retrieved Neo4j credentials from 1Password")
            return {"username": username, "password": password}
        logger.warning(
            "Failed to retrieve Neo4j credentials from 1Password, using environment defaults"
        )
        return {
            "username": os.getenv("NEO4J_USERNAME", "neo4j"),
            "password": os.getenv("NEO4J_PASSWORD", ""),
        }

    def get_security_config(self) -> dict[str, Any]:
        """Get security configuration from environment"""
        return {
            "security_scan_enabled": os.getenv("SECURITY_SCAN_ENABLED", "true").lower()
            == "true",
            "security_scan_days_back": int(os.getenv("SECURITY_SCAN_DAYS_BACK", "30")),
            "minimum_security_score": float(
                os.getenv("MINIMUM_SECURITY_SCORE", "70.0")
            ),
            "max_high_severity_issues": int(os.getenv("MAX_HIGH_SEVERITY_ISSUES", "0")),
            "max_total_security_issues": int(
                os.getenv("MAX_TOTAL_SECURITY_ISSUES", "10")
            ),
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
        }

    def test_1password_connection(self) -> bool:
        """Test 1Password CLI connection and authentication"""
        if not self.op_integration.op_available:
            logger.error("1Password CLI not available")
            return False

        try:
            # Test basic op command
            result = subprocess.run(
                ["op", "whoami"], capture_output=True, text=True, check=False
            )

            if result.returncode == 0:
                logger.info(f"1Password CLI authenticated as: {result.stdout.strip()}")
                return True
            logger.error(f"1Password CLI not authenticated: {result.stderr}")
            return False

        except Exception as e:
            logger.error(f"Failed to test 1Password connection: {e}")
            return False


def main():
    """Test the credential manager"""
    import argparse

    parser = argparse.ArgumentParser(description="1Password Credential Manager Test")
    parser.add_argument(
        "--test-op", action="store_true", help="Test 1Password connection"
    )
    parser.add_argument(
        "--get-gitguardian", action="store_true", help="Get GitGuardian API token"
    )
    parser.add_argument(
        "--get-neo4j", action="store_true", help="Get Neo4j credentials"
    )
    parser.add_argument(
        "--config", action="store_true", help="Show security configuration"
    )

    args = parser.parse_args()

    credential_manager = CredentialManager()

    if args.test_op:
        print("🔐 Testing 1Password Connection...")
        if credential_manager.test_1password_connection():
            print("✅ 1Password connection successful")
        else:
            print("❌ 1Password connection failed")

    if args.get_gitguardian:
        print("🔑 Getting GitGuardian API Token...")
        token = credential_manager.get_gitguardian_api_token()
        if token:
            print(f"✅ Token retrieved: {token[:10]}...{token[-10:]}")
        else:
            print("❌ Failed to retrieve token")

    if args.get_neo4j:
        print("🗄️ Getting Neo4j Credentials...")
        creds = credential_manager.get_neo4j_credentials()
        if creds:
            print(f"✅ Username: {creds['username']}")
            print(
                f"✅ Password: {'*' * len(creds['password']) if creds['password'] else 'Not set'}"
            )
        else:
            print("❌ Failed to retrieve credentials")

    if args.config:
        print("⚙️ Security Configuration:")
        config = credential_manager.get_security_config()
        for key, value in config.items():
            print(f"  {key}: {value}")

    if not any([args.test_op, args.get_gitguardian, args.get_neo4j, args.config]):
        print("🔐 1Password Credential Manager")
        print("Use --help to see available options")


if __name__ == "__main__":
    main()
