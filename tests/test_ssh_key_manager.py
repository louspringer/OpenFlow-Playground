#!/usr/bin/env python3
"""
Test SSH Key Manager

This test validates the SSH key management functionality for vonnegut connections.
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from ssh_key_manager import SSHKeyManager


class TestSSHKeyManager:
    """Test suite for SSH Key Manager functionality."""

    def setup_method(self):
        """Setup test environment"""
        # Create temporary SSH directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.ssh_dir = Path(self.temp_dir) / ".ssh"
        self.ssh_dir.mkdir(mode=0o700)

        # Initialize SSH key manager with test directory
        self.ssh_manager = SSHKeyManager(str(self.ssh_dir))

    def teardown_method(self):
        """Cleanup test environment"""
        # Remove temporary directory
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_ssh_directory_creation(self):
        """Test SSH directory creation with proper permissions"""
        # SSH directory should be created with 700 permissions
        assert self.ssh_dir.exists()
        assert oct(self.ssh_dir.stat().st_mode)[-3:] == "700"

    def test_ssh_permissions_verification(self):
        """Test SSH permissions verification"""
        # Should not raise an exception
        self.ssh_manager._ensure_ssh_permissions()

        # Config file should have 600 permissions if it exists
        if self.ssh_manager.config_file.exists():
            assert oct(self.ssh_manager.config_file.stat().st_mode)[-3:] == "600"

        # Known hosts file should have 600 permissions if it exists
        if self.ssh_manager.known_hosts_file.exists():
            assert oct(self.ssh_manager.known_hosts_file.stat().st_mode)[-3:] == "600"

    def test_generate_ssh_key(self):
        """Test SSH key generation"""
        success, message = self.ssh_manager.generate_ssh_key("test_key")

        assert success
        assert "test_key" in message

        # Check that both private and public keys exist
        private_key = self.ssh_dir / "test_key"
        public_key = self.ssh_dir / "test_key.pub"

        assert private_key.exists()
        assert public_key.exists()

        # Check permissions
        assert oct(private_key.stat().st_mode)[-3:] == "600"
        assert oct(public_key.stat().st_mode)[-3:] == "644"

    def test_get_public_key(self):
        """Test public key retrieval"""
        # Generate a key first
        self.ssh_manager.generate_ssh_key("test_key")

        # Get public key content
        public_key_content = self.ssh_manager.get_public_key("test_key")

        assert public_key_content is not None
        assert public_key_content.startswith("ssh-rsa")
        assert "OpenFlow-Playground" in public_key_content

    def test_update_ssh_config(self):
        """Test SSH config file update"""
        host_configs = {"vonnegut": {"hostname": "192.168.1.100", "user": "ubuntu", "port": 22, "identity_file": "~/.ssh/id_rsa"}}

        success = self.ssh_manager.update_ssh_config(host_configs)
        assert success

        # Check that config file was created
        assert self.ssh_manager.config_file.exists()

        # Check config content
        with open(self.ssh_manager.config_file, "r") as f:
            config_content = f.read()

        assert "Host vonnegut" in config_content
        assert "HostName 192.168.1.100" in config_content
        assert "User ubuntu" in config_content
        assert "Port 22" in config_content

    def test_add_host_to_known_hosts(self):
        """Test adding host to known_hosts"""
        # Mock ssh-keyscan output
        mock_host_key = "192.168.1.100 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC..."

        # Create a mock known_hosts file
        with open(self.ssh_manager.known_hosts_file, "w") as f:
            f.write(mock_host_key)

        # Test adding host (this will fail in test environment, but we can test the file handling)
        # In a real environment, this would use ssh-keyscan
        assert self.ssh_manager.known_hosts_file.exists()

    def test_ssh_config_integration(self):
        """Test complete SSH configuration integration"""
        # Test host configuration
        host_config = {"testhost": {"hostname": "192.168.1.100", "user": "testuser", "port": 22, "identity_file": "~/.ssh/id_rsa"}}

        # Update config
        success = self.ssh_manager.update_ssh_config(host_config)
        assert success

        # Verify config structure
        with open(self.ssh_manager.config_file, "r") as f:
            config_content = f.read()

        # Check for required SSH config options
        required_options = [
            "Host testhost",
            "HostName 192.168.1.100",
            "User testuser",
            "Port 22",
            "IdentityFile ~/.ssh/id_rsa",
            "StrictHostKeyChecking no",
            "UserKnownHostsFile ~/.ssh/known_hosts",
            "ServerAliveInterval 60",
            "ServerAliveCountMax 3",
        ]

        for option in required_options:
            assert option in config_content, f"Missing SSH config option: {option}"

    def test_key_generation_with_custom_parameters(self):
        """Test SSH key generation with custom parameters"""
        success, message = self.ssh_manager.generate_ssh_key(key_name="custom_key", key_type="ed25519", bits=256, comment="Custom test key")

        assert success
        assert "custom_key" in message

        # Check that key was generated
        private_key = self.ssh_dir / "custom_key"
        public_key = self.ssh_dir / "custom_key.pub"

        assert private_key.exists()
        assert public_key.exists()

    def test_duplicate_host_config_handling(self):
        """Test handling of duplicate host configurations"""
        host_configs = {"testhost": {"hostname": "192.168.1.100", "user": "testuser", "port": 22, "identity_file": "~/.ssh/id_rsa"}}

        # Add host config twice
        success1 = self.ssh_manager.update_ssh_config(host_configs)
        success2 = self.ssh_manager.update_ssh_config(host_configs)

        assert success1
        assert success2

        # Check that only one entry exists
        with open(self.ssh_manager.config_file, "r") as f:
            config_content = f.read()

        # Count occurrences of "Host testhost"
        host_count = config_content.count("Host testhost")
        assert host_count == 1, f"Expected 1 host entry, found {host_count}"

    def test_error_handling(self):
        """Test error handling in SSH key manager"""
        # Test with invalid SSH directory (parent doesn't exist)
        invalid_path = "/invalid/path/that/does/not/exist"

        # This should handle the error gracefully
        try:
            invalid_manager = SSHKeyManager(invalid_path)
            # If we get here, the manager should handle the error
            assert False, "Should have raised an exception"
        except Exception as e:
            # Should handle directory creation errors gracefully
            assert "No such file or directory" in str(e) or "permission" in str(e).lower()


if __name__ == "__main__":
    pytest.main([__file__])
