#!/usr/bin/env python3
"""
SSH Key Management Domain

This domain provides comprehensive SSH key management functionality for secure remote connections.
Implements ReflectiveModule interface for self-monitoring and architectural boundaries.
"""

import os
import sys
import subprocess
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

# Import ReflectiveModule interface
try:
    from src.reflective_modules.base import ReflectiveModule
    from src.reflective_modules.health import ModuleHealth, ModuleCapability, ModuleStatus
    from src.reflective_modules.registry import ReflectiveModuleRegistry

    REFLECTIVE_MODULE_AVAILABLE = True
except ImportError:
    # Fallback if ReflectiveModule not available
    from abc import ABC

    ReflectiveModule = ABC
    ModuleHealth = Dict[str, Any]
    ModuleCapability = Dict[str, Any]
    ModuleStatus = type("ModuleStatus", (), {"AVAILABLE": "AVAILABLE", "PARTIALLY_AVAILABLE": "PARTIALLY_AVAILABLE", "NOT_AVAILABLE": "NOT_AVAILABLE"})()
    ReflectiveModuleRegistry = type("ReflectiveModuleRegistry", (), {"register": lambda self, module: None})()
    REFLECTIVE_MODULE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SSHKeyManager(ReflectiveModule):
    """Manages SSH keys and configuration for remote hosts with RM compliance"""

    def __init__(self, ssh_dir: str = "~/.ssh"):
        """Initialize SSH key manager with RM compliance"""
        if REFLECTIVE_MODULE_AVAILABLE:
            super().__init__()
            # Register with RM registry
            ReflectiveModuleRegistry().register_module(self)

        self.ssh_dir = Path(ssh_dir).expanduser()
        self.ssh_dir.mkdir(mode=0o700, exist_ok=True)
        self.config_file = self.ssh_dir / "config"
        self.known_hosts_file = self.ssh_dir / "known_hosts"

        # Get current user
        self.current_user = os.getenv("USER", "lou")

        # RM health tracking
        self._operation_count = 0
        self._error_count = 0
        self._success_count = 0
        self._last_operation_time = time.time()
        self._start_time = time.time()

        # Ensure proper permissions
        self._ensure_ssh_permissions()

        logger.info(f"✅ SSH Key Manager initialized with RM compliance")

    def _track_operation(self, success: bool = True) -> None:
        """Track operation for RM health monitoring"""
        self._operation_count += 1
        self._last_operation_time = time.time()

        if success:
            self._success_count += 1
        else:
            self._error_count += 1

    def _ensure_ssh_permissions(self):
        """Ensure SSH directory and files have correct permissions"""
        try:
            # Set SSH directory permissions
            self.ssh_dir.chmod(0o700)

            # Set config file permissions if it exists
            if self.config_file.exists():
                self.config_file.chmod(0o600)

            # Set known_hosts permissions if it exists
            if self.known_hosts_file.exists():
                self.known_hosts_file.chmod(0o600)

            logger.info("✅ SSH permissions verified")
            self._track_operation(True)
        except Exception as e:
            logger.error(f"❌ Failed to set SSH permissions: {e}")
            self._track_operation(False)
            raise

    def generate_ssh_key(self, key_name: str = "id_rsa", key_type: str = "rsa", bits: int = 4096, comment: str = None) -> Tuple[bool, str]:
        """Generate SSH key pair"""
        try:
            key_path = self.ssh_dir / key_name
            private_key = key_path
            public_key = key_path.with_suffix(".pub")

            # Check if key already exists
            if private_key.exists() and public_key.exists():
                logger.info(f"✅ SSH key {key_name} already exists")
                self._track_operation(True)
                return True, str(private_key)

            # Generate key comment
            if comment is None:
                comment = f"OpenFlow-Playground-{os.getenv('USER', 'user')}-{int(time.time())}"

            # Generate SSH key
            cmd = ["ssh-keygen", "-t", key_type, "-b", str(bits), "-f", str(private_key), "-N", "", "-C", comment]  # No passphrase for automation

            logger.info(f"🔑 Generating SSH key: {key_name}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Set proper permissions
            private_key.chmod(0o600)
            public_key.chmod(0o644)

            logger.info(f"✅ SSH key generated successfully: {private_key}")
            self._track_operation(True)
            return True, str(private_key)

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to generate SSH key: {e.stderr}")
            self._track_operation(False)
            return False, e.stderr
        except Exception as e:
            logger.error(f"❌ Error generating SSH key: {e}")
            self._track_operation(False)
            return False, str(e)

    def get_public_key(self, key_name: str = "id_rsa") -> Optional[str]:
        """Get public key content"""
        try:
            public_key_path = self.ssh_dir / f"{key_name}.pub"
            if public_key_path.exists():
                with open(public_key_path, "r") as f:
                    content = f.read().strip()
                self._track_operation(True)
                return content
            else:
                logger.warning(f"⚠️ Public key not found: {public_key_path}")
                self._track_operation(False)
                return None
        except Exception as e:
            logger.error(f"❌ Error reading public key: {e}")
            self._track_operation(False)
            return None

    def install_key_on_host(self, host: str, user: str, key_name: str = "id_rsa", password: str = None) -> bool:
        """Install SSH public key on remote host"""
        try:
            public_key = self.get_public_key(key_name)
            if not public_key:
                logger.error("❌ No public key available to install")
                self._track_operation(False)
                return False

            # Create temporary file with public key
            temp_key_file = self.ssh_dir / f"temp_key_{int(time.time())}"
            with open(temp_key_file, "w") as f:
                f.write(public_key)

            try:
                # Use ssh-copy-id if available
                cmd = ["ssh-copy-id", "-i", str(temp_key_file), f"{user}@{host}"]

                logger.info(f"🔑 Installing SSH key on {user}@{host}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    logger.info(f"✅ SSH key installed successfully on {host}")
                    self._track_operation(True)
                    return True
                else:
                    logger.warning(f"⚠️ ssh-copy-id failed, trying manual installation")

                    # Manual installation via SSH
                    success = self._manual_key_install(host, user, public_key, password)
                    self._track_operation(success)
                    return success

            finally:
                # Clean up temporary file
                if temp_key_file.exists():
                    temp_key_file.unlink()

        except Exception as e:
            logger.error(f"❌ Error installing SSH key on {host}: {e}")
            self._track_operation(False)
            return False

    def _manual_key_install(self, host: str, user: str, public_key: str, password: str = None) -> bool:
        """Manually install SSH key using SSH command"""
        try:
            # Create the command to add key to authorized_keys
            install_cmd = f"mkdir -p ~/.ssh && echo '{public_key}' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"

            if password:
                # Use sshpass for password authentication
                cmd = ["sshpass", "-p", password, "ssh", f"{user}@{host}", install_cmd]
            else:
                # Try without password (if key-based auth is already set up)
                cmd = ["ssh", f"{user}@{host}", install_cmd]

            logger.info(f"🔑 Installing SSH key manually on {user}@{host}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                logger.info(f"✅ SSH key installed manually on {host}")
                return True
            else:
                logger.error(f"❌ Manual key installation failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Error in manual key installation: {e}")
            return False

    def add_host_to_known_hosts(self, host: str, port: int = 22) -> bool:
        """Add host to known_hosts file"""
        try:
            logger.info(f"🔍 Adding {host} to known_hosts")

            # Use ssh-keyscan to get host key
            cmd = ["ssh-keyscan", "-p", str(port), host]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0 and result.stdout.strip():
                # Append to known_hosts
                with open(self.known_hosts_file, "a") as f:
                    f.write(result.stdout)

                logger.info(f"✅ Added {host} to known_hosts")
                self._track_operation(True)
                return True
            else:
                logger.error(f"❌ Failed to get host key for {host}")
                self._track_operation(False)
                return False

        except Exception as e:
            logger.error(f"❌ Error adding host to known_hosts: {e}")
            self._track_operation(False)
            return False

    def update_ssh_config(self, host_configs: Dict[str, Dict]) -> bool:
        """Update SSH config file with host configurations"""
        try:
            logger.info("📝 Updating SSH config file")

            # Read existing config
            config_content = ""
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    config_content = f.read()

            # Add new host configurations
            for host_name, config in host_configs.items():
                host_section = f"""
Host {host_name}
    HostName {config.get("hostname", host_name)}
    User {config.get("user", self.current_user)}
    Port {config.get("port", 22)}
    IdentityFile {config.get("identity_file", "~/.ssh/id_rsa")}
    StrictHostKeyChecking no
    UserKnownHostsFile ~/.ssh/known_hosts
    ServerAliveInterval 60
    ServerAliveCountMax 3
"""

                # Check if host already exists in config
                if f"Host {host_name}" not in config_content:
                    config_content += host_section
                    logger.info(f"✅ Added {host_name} to SSH config")
                else:
                    logger.info(f"ℹ️ Host {host_name} already in SSH config")

            # Write updated config
            with open(self.config_file, "w") as f:
                f.write(config_content)

            # Set proper permissions
            self.config_file.chmod(0o600)

            logger.info("✅ SSH config updated successfully")
            self._track_operation(True)
            return True

        except Exception as e:
            logger.error(f"❌ Error updating SSH config: {e}")
            self._track_operation(False)
            return False

    def test_connection(self, host: str, timeout: int = 10) -> bool:
        """Test SSH connection to host"""
        try:
            logger.info(f"🔍 Testing SSH connection to {host}")

            cmd = ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes", host, "echo 'SSH connection successful'"]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            if result.returncode == 0:
                logger.info(f"✅ SSH connection to {host} successful")
                self._track_operation(True)
                return True
            else:
                logger.error(f"❌ SSH connection to {host} failed: {result.stderr}")
                self._track_operation(False)
                return False

        except Exception as e:
            logger.error(f"❌ Error testing SSH connection: {e}")
            self._track_operation(False)
            return False

    def setup_host_connection(self, host: str, host_user: str = None, key_name: str = "id_rsa") -> bool:
        """Complete setup for any host connection"""
        try:
            # Use current user if not specified
            if host_user is None:
                host_user = self.current_user

            logger.info(f"🚀 Setting up SSH connection to {host} as {host_user}")

            # Step 1: Generate SSH key if needed
            success, message = self.generate_ssh_key(key_name)
            if not success:
                logger.error(f"❌ Failed to generate SSH key: {message}")
                return False

            # Step 2: Add host to known_hosts
            if not self.add_host_to_known_hosts(host):
                logger.error(f"❌ Failed to add {host} to known_hosts")
                return False

            # Step 3: Update SSH config
            host_config = {host: {"hostname": host, "user": host_user, "port": 22, "identity_file": f"~/.ssh/{key_name}"}}

            if not self.update_ssh_config(host_config):
                logger.error("❌ Failed to update SSH config")
                return False

            # Step 4: Install key on host
            logger.info(f"🔑 Installing SSH key on {host}...")
            logger.info("⚠️ You may need to provide password for initial setup")

            if not self.install_key_on_host(host, host_user, key_name):
                logger.warning("⚠️ Automatic key installation failed")
                logger.info("📋 Manual installation required:")
                logger.info(f"   Run: ssh-copy-id -i ~/.ssh/{key_name}.pub {host_user}@{host}")
                return False

            # Step 5: Test connection
            if not self.test_connection(host):
                logger.error("❌ SSH connection test failed")
                return False

            logger.info(f"✅ SSH setup for {host} completed successfully!")
            return True

        except Exception as e:
            logger.error(f"❌ Error in {host} setup: {e}")
            return False

    # RM Interface Implementation
    async def get_module_status(self) -> ModuleHealth:
        """Get current module status for RM compliance"""
        if not REFLECTIVE_MODULE_AVAILABLE:
            return {"status": "AVAILABLE", "message": "SSH Key Manager operational (RM not available)", "capabilities": [], "health_indicators": {}, "module_version": "1.0.0"}

        return ModuleHealth(
            status=ModuleStatus.AVAILABLE if await self.is_healthy() else ModuleStatus.PARTIALLY_AVAILABLE,
            message="SSH Key Manager operational",
            capabilities=await self.get_module_capabilities(),
            health_indicators=await self.get_health_indicators(),
            module_version="1.0.0",
        )

    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get module capabilities for RM compliance"""
        if not REFLECTIVE_MODULE_AVAILABLE:
            return []

        return [
            ModuleCapability(name="key_generation", description="Generate SSH key pairs", available=True, version="1.0.0", dependencies=[]),
            ModuleCapability(name="key_installation", description="Install SSH keys on remote hosts", available=True, version="1.0.0", dependencies=["ssh-copy-id"]),
            ModuleCapability(name="connection_testing", description="Test SSH connections to hosts", available=True, version="1.0.0", dependencies=["ssh"]),
            ModuleCapability(name="config_management", description="Manage SSH configuration files", available=True, version="1.0.0", dependencies=[]),
            ModuleCapability(name="host_management", description="Add hosts to known_hosts", available=True, version="1.0.0", dependencies=["ssh-keyscan"]),
        ]

    async def is_healthy(self) -> bool:
        """Check if module is healthy for RM compliance"""
        try:
            # Check basic health indicators
            health_indicators = await self.get_health_indicators()

            # Must have SSH directory with correct permissions
            if not health_indicators.get("ssh_dir_exists", False):
                return False

            # Must have correct permissions
            if health_indicators.get("ssh_dir_permissions") != "700":
                return False

            # Must be operational (not too many errors)
            success_rate = health_indicators.get("success_rate", 0.0)
            if success_rate < 0.5:  # At least 50% success rate
                return False

            return True
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return False

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get detailed health indicators for RM compliance"""
        try:
            # Calculate success rate
            total_operations = self._success_count + self._error_count
            success_rate = self._success_count / total_operations if total_operations > 0 else 1.0

            # Calculate uptime
            uptime = time.time() - self._start_time

            # Check SSH directory and files
            ssh_dir_exists = self.ssh_dir.exists()
            ssh_dir_permissions = oct(self.ssh_dir.stat().st_mode)[-3:] if ssh_dir_exists else "000"

            # Count keys
            public_keys = list(self.ssh_dir.glob("*.pub"))
            private_keys = list(self.ssh_dir.glob("id_*"))
            private_keys = [k for k in private_keys if not k.suffix == ".pub"]

            return {
                "uptime": uptime,
                "operation_count": self._operation_count,
                "success_count": self._success_count,
                "error_count": self._error_count,
                "success_rate": success_rate,
                "last_operation_time": self._last_operation_time,
                "ssh_dir_exists": ssh_dir_exists,
                "ssh_dir_permissions": ssh_dir_permissions,
                "config_file_exists": self.config_file.exists(),
                "known_hosts_exists": self.known_hosts_file.exists(),
                "public_keys_count": len(public_keys),
                "private_keys_count": len(private_keys),
                "current_user": self.current_user,
                "rm_compliance": True,
            }
        except Exception as e:
            logger.error(f"❌ Error getting health indicators: {e}")
            return {"error": str(e), "rm_compliance": False}


class SSHKeyManagementDomain:
    """Domain for SSH key management operations with RM compliance"""

    def __init__(self):
        """Initialize SSH key management domain"""
        self.ssh_manager = SSHKeyManager()

    def setup_host(self, host: str, user: str = None, key_name: str = "id_rsa") -> bool:
        """Setup SSH connection for a host"""
        return self.ssh_manager.setup_host_connection(host, user, key_name)

    def generate_key(self, key_name: str = "id_rsa", key_type: str = "rsa", bits: int = 4096) -> Tuple[bool, str]:
        """Generate SSH key pair"""
        return self.ssh_manager.generate_ssh_key(key_name, key_type, bits)

    def install_key(self, host: str, user: str, key_name: str = "id_rsa") -> bool:
        """Install SSH key on remote host"""
        return self.ssh_manager.install_key_on_host(host, user, key_name)

    def test_connection(self, host: str) -> bool:
        """Test SSH connection to host"""
        return self.ssh_manager.test_connection(host)

    def get_public_key(self, key_name: str = "id_rsa") -> Optional[str]:
        """Get public key content"""
        return self.ssh_manager.get_public_key(key_name)

    def get_current_user(self) -> str:
        """Get current user"""
        return self.ssh_manager.current_user

    # RM Interface delegation
    async def get_module_status(self) -> ModuleHealth:
        """Get domain status"""
        return await self.ssh_manager.get_module_status()

    async def get_module_capabilities(self) -> List[ModuleCapability]:
        """Get domain capabilities"""
        return await self.ssh_manager.get_module_capabilities()

    async def is_healthy(self) -> bool:
        """Check if domain is healthy"""
        return await self.ssh_manager.is_healthy()

    async def get_health_indicators(self) -> Dict[str, Any]:
        """Get domain health indicators"""
        return await self.ssh_manager.get_health_indicators()


def main():
    """Main function for SSH key management"""
    import argparse

    parser = argparse.ArgumentParser(description="SSH Key Manager for OpenFlow Playground")
    parser.add_argument("--host", default="vonnegut", help="Host name to configure")
    parser.add_argument("--user", help="Username for SSH connection (defaults to current user)")
    parser.add_argument("--key-name", default="id_rsa", help="SSH key name")
    parser.add_argument("--generate-key", action="store_true", help="Generate new SSH key")
    parser.add_argument("--install-key", action="store_true", help="Install key on remote host")
    parser.add_argument("--test-connection", action="store_true", help="Test SSH connection")
    parser.add_argument("--setup-host", action="store_true", help="Complete host setup")
    parser.add_argument("--setup-vonnegut", action="store_true", help="Complete vonnegut setup (legacy)")
    parser.add_argument("--rm-status", action="store_true", help="Show RM status")

    args = parser.parse_args()

    # Initialize SSH key manager
    ssh_manager = SSHKeyManager()

    # RM status check
    if args.rm_status:

        async def show_rm_status():
            status = await ssh_manager.get_module_status()
            capabilities = await ssh_manager.get_module_capabilities()
            health = await ssh_manager.is_healthy()
            indicators = await ssh_manager.get_health_indicators()

            print("🔍 SSH Key Manager RM Status:")
            print(f"  Health: {'✅ Healthy' if health else '❌ Unhealthy'}")
            print(f"  Status: {status.status if hasattr(status, 'status') else status.get('status')}")
            print(f"  Capabilities: {len(capabilities)}")
            print(f"  Success Rate: {indicators.get('success_rate', 0):.2%}")
            print(f"  Operations: {indicators.get('operation_count', 0)}")
            print(f"  Uptime: {indicators.get('uptime', 0):.1f}s")

        asyncio.run(show_rm_status())
        return

    if args.generate_key:
        success, message = ssh_manager.generate_ssh_key(args.key_name)
        if success:
            print(f"✅ SSH key generated: {message}")
        else:
            print(f"❌ Failed to generate SSH key: {message}")
            sys.exit(1)

    if args.install_key:
        success = ssh_manager.install_key_on_host(args.host, args.user or ssh_manager.current_user, args.key_name)
        if success:
            print(f"✅ SSH key installed on {args.host}")
        else:
            print(f"❌ Failed to install SSH key on {args.host}")
            sys.exit(1)

    if args.test_connection:
        success = ssh_manager.test_connection(args.host)
        if success:
            print(f"✅ SSH connection to {args.host} successful")
        else:
            print(f"❌ SSH connection to {args.host} failed")
            sys.exit(1)

    if args.setup_host:
        success = ssh_manager.setup_host_connection(args.host, args.user, args.key_name)
        if success:
            print(f"✅ SSH setup for {args.host} completed successfully!")
        else:
            print(f"❌ SSH setup for {args.host} failed")
            sys.exit(1)

    if args.setup_vonnegut:
        # Legacy support for vonnegut
        success = ssh_manager.setup_host_connection("vonnegut", args.user or "lou", args.key_name)
        if success:
            print("✅ vonnegut SSH setup completed successfully!")
        else:
            print("❌ vonnegut SSH setup failed")
            sys.exit(1)

    # Default: complete setup for specified host
    if not any([args.generate_key, args.install_key, args.test_connection, args.setup_host, args.setup_vonnegut]):
        success = ssh_manager.setup_host_connection(args.host, args.user, args.key_name)
        if success:
            print(f"✅ SSH setup for {args.host} completed successfully!")
        else:
            print(f"❌ SSH setup for {args.host} failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
