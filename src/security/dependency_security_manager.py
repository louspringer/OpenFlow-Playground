#!/usr/bin/env python3
"""
Dependency Security Manager - RM Compliant
Manages security vulnerabilities in dependencies
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SecurityVulnerability:
    """Security vulnerability information."""

    cve_id: str
    package: str
    ecosystem: str
    severity: str
    description: str
    fixed_version: Optional[str] = None
    current_version: Optional[str] = None
    published_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class DependencyUpdate:
    """Dependency update information."""

    package: str
    ecosystem: str
    current_version: str
    target_version: str
    security_fix: bool
    cve_ids: List[str]


class DependencySecurityManager:
    """Dependency Security Manager - RM Compliant."""

    def __init__(self, project_root: str = "."):
        """Initialize the security manager."""
        self.project_root = Path(project_root)
        self.vulnerabilities: List[SecurityVulnerability] = []
        self.updates: List[DependencyUpdate] = []
        self.health_status = {"status": "healthy", "last_check": datetime.now(), "total_vulnerabilities": 0, "high_severity": 0, "medium_severity": 0, "low_severity": 0, "total_updates": 0}
        logger.info("Dependency Security Manager initialized")

    def scan_vulnerabilities(self) -> List[SecurityVulnerability]:
        """Scan for security vulnerabilities."""
        logger.info("Scanning for security vulnerabilities...")

        # Check GitHub Dependabot alerts
        try:
            result = subprocess.run(["gh", "api", "repos/louspringer/OpenFlow-Playground/dependabot/alerts"], capture_output=True, text=True, check=True)

            alerts = json.loads(result.stdout)

            for alert in alerts:
                vulnerability = SecurityVulnerability(
                    cve_id=alert.get("security_advisory", {}).get("cve_id", ""),
                    package=alert.get("dependency", {}).get("package", {}).get("name", ""),
                    ecosystem=alert.get("dependency", {}).get("package", {}).get("ecosystem", ""),
                    severity=alert.get("security_advisory", {}).get("severity", ""),
                    description=alert.get("security_advisory", {}).get("description", ""),
                    published_at=alert.get("security_advisory", {}).get("published_at", ""),
                    updated_at=alert.get("security_advisory", {}).get("updated_at", ""),
                )

                # Get fixed version if available
                if "vulnerabilities" in alert.get("security_advisory", {}):
                    for vuln in alert["security_advisory"]["vulnerabilities"]:
                        if vuln.get("package", {}).get("name") == vulnerability.package:
                            vulnerability.fixed_version = vuln.get("first_patched_version", {}).get("identifier")
                            break

                self.vulnerabilities.append(vulnerability)

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to fetch GitHub alerts: {e}")
        except Exception as e:
            logger.error(f"Error scanning vulnerabilities: {e}")

        self._update_health_status()
        logger.info(f"Found {len(self.vulnerabilities)} vulnerabilities")
        return self.vulnerabilities

    def check_go_dependencies(self) -> List[DependencyUpdate]:
        """Check Go dependencies for updates."""
        logger.info("Checking Go dependencies...")

        go_mod_path = self.project_root / "src" / "secure_shell_service" / "go.mod"
        if not go_mod_path.exists():
            logger.warning("go.mod not found")
            return []

        try:
            # Run go list -u -m all to get outdated dependencies
            result = subprocess.run(["go", "list", "-u", "-m", "all"], cwd=go_mod_path.parent, capture_output=True, text=True, check=True)

            lines = result.stdout.strip().split("\n")

            for line in lines[1:]:  # Skip the first line (module name)
                if "[" in line and "]" in line:
                    # Parse line like: golang.org/x/net v0.17.0 [v0.41.0]
                    parts = line.split()
                    if len(parts) >= 3:
                        package = parts[0]
                        current_version = parts[1]
                        target_version = parts[2].strip("[]")

                        # Check if this is a security-related update
                        security_fix = self._is_security_update(package, current_version, target_version)
                        cve_ids = self._get_cve_ids_for_package(package)

                        update = DependencyUpdate(package=package, ecosystem="go", current_version=current_version, target_version=target_version, security_fix=security_fix, cve_ids=cve_ids)

                        self.updates.append(update)

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to check Go dependencies: {e}")
        except Exception as e:
            logger.error(f"Error checking Go dependencies: {e}")

        logger.info(f"Found {len(self.updates)} dependency updates")
        return self.updates

    def update_dependency(self, package: str, version: str) -> bool:
        """Update a specific dependency."""
        logger.info(f"Updating {package} to {version}")

        go_mod_path = self.project_root / "src" / "secure_shell_service"
        if not go_mod_path.exists():
            logger.error("Go module directory not found")
            return False

        try:
            # Update the dependency
            result = subprocess.run(["go", "get", f"{package}@{version}"], cwd=go_mod_path, capture_output=True, text=True, check=True)

            logger.info(f"Successfully updated {package} to {version}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update {package}: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error updating {package}: {e}")
            return False

    def update_all_dependencies(self) -> Dict[str, bool]:
        """Update all outdated dependencies."""
        logger.info("Updating all dependencies...")

        results = {}
        for update in self.updates:
            if update.security_fix:
                logger.info(f"Updating security fix: {update.package}")
                success = self.update_dependency(update.package, update.target_version)
                results[update.package] = success

        return results

    def _is_security_update(self, package: str, current_version: str, target_version: str) -> bool:
        """Check if an update is security-related."""
        # Check if this package has known vulnerabilities
        for vuln in self.vulnerabilities:
            if vuln.package == package and vuln.fixed_version:
                # Check if target version is >= fixed version
                if self._version_compare(target_version, vuln.fixed_version) >= 0:
                    return True
        return False

    def _get_cve_ids_for_package(self, package: str) -> List[str]:
        """Get CVE IDs for a specific package."""
        cve_ids = []
        for vuln in self.vulnerabilities:
            if vuln.package == package and vuln.cve_id:
                cve_ids.append(vuln.cve_id)
        return cve_ids

    def _version_compare(self, version1: str, version2: str) -> int:
        """Compare two version strings."""
        # Simple version comparison (can be enhanced)
        try:
            v1_parts = [int(x) for x in version1.replace("v", "").split(".")]
            v2_parts = [int(x) for x in version2.replace("v", "").split(".")]

            # Pad with zeros if needed
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))

            for v1, v2 in zip(v1_parts, v2_parts):
                if v1 < v2:
                    return -1
                elif v1 > v2:
                    return 1
            return 0
        except:
            return 0

    def _update_health_status(self):
        """Update health status."""
        self.health_status.update(
            {
                "last_check": datetime.now(),
                "total_vulnerabilities": len(self.vulnerabilities),
                "high_severity": len([v for v in self.vulnerabilities if v.severity == "high"]),
                "medium_severity": len([v for v in self.vulnerabilities if v.severity == "medium"]),
                "low_severity": len([v for v in self.vulnerabilities if v.severity == "low"]),
                "total_updates": len(self.updates),
            }
        )

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status."""
        return self.health_status

    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        return self.health_status["high_severity"] == 0

    def generate_security_report(self) -> Dict[str, Any]:
        """Generate security report."""
        return {
            "timestamp": datetime.now().isoformat(),
            "health_status": self.health_status,
            "vulnerabilities": [asdict(v) for v in self.vulnerabilities],
            "updates": [asdict(u) for u in self.updates],
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations."""
        recommendations = []

        if self.health_status["high_severity"] > 0:
            recommendations.append("CRITICAL: Address high-severity vulnerabilities immediately")

        if self.health_status["medium_severity"] > 0:
            recommendations.append("HIGH: Address medium-severity vulnerabilities within 7 days")

        if self.health_status["low_severity"] > 0:
            recommendations.append("MEDIUM: Address low-severity vulnerabilities within 30 days")

        security_updates = [u for u in self.updates if u.security_fix]
        if security_updates:
            recommendations.append(f"Update {len(security_updates)} security-related dependencies")

        return recommendations


def main():
    """Main function for testing."""
    # Create security manager
    manager = DependencySecurityManager()

    # Scan for vulnerabilities
    vulnerabilities = manager.scan_vulnerabilities()

    # Check Go dependencies
    updates = manager.check_go_dependencies()

    # Display results
    print("🔒 Dependency Security Manager - RM Compliant")
    print("=" * 50)
    print(f"Health Status: {manager.health_status['status']}")
    print(f"Total Vulnerabilities: {manager.health_status['total_vulnerabilities']}")
    print(f"High Severity: {manager.health_status['high_severity']}")
    print(f"Medium Severity: {manager.health_status['medium_severity']}")
    print(f"Low Severity: {manager.health_status['low_severity']}")
    print(f"Total Updates: {manager.health_status['total_updates']}")

    # Show vulnerabilities
    if vulnerabilities:
        print("\n🚨 Security Vulnerabilities:")
        for vuln in vulnerabilities:
            print(f"  - {vuln.cve_id}: {vuln.package} ({vuln.severity})")
            if vuln.fixed_version:
                print(f"    Fixed in: {vuln.fixed_version}")

    # Show updates
    if updates:
        print("\n📦 Dependency Updates:")
        for update in updates:
            security_marker = "🔒" if update.security_fix else "📦"
            print(f"  {security_marker} {update.package}: {update.current_version} → {update.target_version}")
            if update.cve_ids:
                print(f"    CVEs: {', '.join(update.cve_ids)}")

    # Generate report
    report = manager.generate_security_report()

    # Save report
    with open("security_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n✅ Security report saved to: security_report.json")
    print(f"System Healthy: {manager.is_healthy()}")


if __name__ == "__main__":
    main()
