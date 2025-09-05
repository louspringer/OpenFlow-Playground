#!/usr/bin/env python3
"""
Security Monitoring Dashboard - RM Compliant
Comprehensive security monitoring and reporting system
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SecurityMetric:
    """Security metric data."""
    name: str
    value: float
    unit: str
    status: str
    trend: str
    last_updated: datetime
    target: Optional[float] = None
    threshold: Optional[float] = None


@dataclass
class SecurityAlert:
    """Security alert data."""
    id: str
    type: str
    severity: str
    message: str
    timestamp: datetime
    status: str
    resolved_at: Optional[datetime] = None


class SecurityMonitoringDashboard:
    """Security Monitoring Dashboard - RM Compliant."""
    
    def __init__(self, project_root: str = "."):
        """Initialize the security dashboard."""
        self.project_root = Path(project_root)
        self.metrics: List[SecurityMetric] = []
        self.alerts: List[SecurityAlert] = []
        self.health_status = {
            "status": "healthy",
            "last_check": datetime.now(),
            "total_metrics": 0,
            "total_alerts": 0,
            "critical_alerts": 0,
            "high_alerts": 0,
            "medium_alerts": 0,
            "low_alerts": 0
        }
        logger.info("Security Monitoring Dashboard initialized")
    
    def collect_security_metrics(self) -> List[SecurityMetric]:
        """Collect security metrics."""
        logger.info("Collecting security metrics...")
        
        # Load security report if available
        security_report_path = self.project_root / "security_report.json"
        if security_report_path.exists():
            with open(security_report_path, 'r') as f:
                security_data = json.load(f)
            
            # Extract metrics from security data
            vulnerabilities = security_data.get("vulnerabilities", [])
            health_status = security_data.get("health_status", {})
            
            # Vulnerability metrics
            total_vulns = health_status.get("total_vulnerabilities", 0)
            high_severity = health_status.get("high_severity", 0)
            medium_severity = health_status.get("medium_severity", 0)
            low_severity = health_status.get("low_severity", 0)
            
            # Create security metrics
            self.metrics = [
                SecurityMetric(
                    name="Total Vulnerabilities",
                    value=total_vulns,
                    unit="count",
                    status="critical" if total_vulns > 0 else "healthy",
                    trend="stable",
                    last_updated=datetime.now(),
                    target=0.0,
                    threshold=0.0
                ),
                SecurityMetric(
                    name="High Severity Vulnerabilities",
                    value=high_severity,
                    unit="count",
                    status="critical" if high_severity > 0 else "healthy",
                    trend="stable",
                    last_updated=datetime.now(),
                    target=0.0,
                    threshold=0.0
                ),
                SecurityMetric(
                    name="Medium Severity Vulnerabilities",
                    value=medium_severity,
                    unit="count",
                    status="warning" if medium_severity > 0 else "healthy",
                    trend="stable",
                    last_updated=datetime.now(),
                    target=0.0,
                    threshold=5.0
                ),
                SecurityMetric(
                    name="Low Severity Vulnerabilities",
                    value=low_severity,
                    unit="count",
                    status="warning" if low_severity > 5 else "healthy",
                    trend="stable",
                    last_updated=datetime.now(),
                    target=0.0,
                    threshold=10.0
                ),
                SecurityMetric(
                    name="Security Compliance",
                    value=100.0 if total_vulns == 0 else max(0, 100 - (total_vulns * 10)),
                    unit="percentage",
                    status="healthy" if total_vulns == 0 else "warning",
                    trend="stable",
                    last_updated=datetime.now(),
                    target=100.0,
                    threshold=90.0
                )
            ]
        
        self._update_health_status()
        logger.info(f"Collected {len(self.metrics)} security metrics")
        return self.metrics
    
    def generate_security_alerts(self) -> List[SecurityAlert]:
        """Generate security alerts based on metrics."""
        logger.info("Generating security alerts...")
        
        self.alerts = []
        
        for metric in self.metrics:
            if metric.status == "critical":
                alert = SecurityAlert(
                    id=f"SEC-ALERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    type="Vulnerability",
                    severity="Critical",
                    message=f"Critical security issue: {metric.name} = {metric.value} {metric.unit}",
                    timestamp=datetime.now(),
                    status="Active"
                )
                self.alerts.append(alert)
            
            elif metric.status == "warning":
                alert = SecurityAlert(
                    id=f"SEC-ALERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    type="Vulnerability",
                    severity="High",
                    message=f"Security warning: {metric.name} = {metric.value} {metric.unit}",
                    timestamp=datetime.now(),
                    status="Active"
                )
                self.alerts.append(alert)
        
        self._update_health_status()
        logger.info(f"Generated {len(self.alerts)} security alerts")
        return self.alerts
    
    def generate_dashboard_report(self) -> Dict[str, Any]:
        """Generate comprehensive dashboard report."""
        logger.info("Generating dashboard report...")
        
        # Calculate summary statistics
        total_metrics = len(self.metrics)
        healthy_metrics = len([m for m in self.metrics if m.status == "healthy"])
        warning_metrics = len([m for m in self.metrics if m.status == "warning"])
        critical_metrics = len([m for m in self.metrics if m.status == "critical"])
        
        total_alerts = len(self.alerts)
        critical_alerts = len([a for a in self.alerts if a.severity == "Critical"])
        high_alerts = len([a for a in self.alerts if a.severity == "High"])
        medium_alerts = len([a for a in self.alerts if a.severity == "Medium"])
        low_alerts = len([a for a in self.alerts if a.severity == "Low"])
        
        # Calculate overall security score
        security_score = (healthy_metrics / total_metrics * 100) if total_metrics > 0 else 100
        
        report = {
            "dashboard_info": {
                "generated_at": datetime.now().isoformat(),
                "project_root": str(self.project_root),
                "report_version": "1.0"
            },
            "summary": {
                "overall_security_score": security_score,
                "security_status": "healthy" if security_score >= 90 else "warning" if security_score >= 70 else "critical",
                "total_metrics": total_metrics,
                "healthy_metrics": healthy_metrics,
                "warning_metrics": warning_metrics,
                "critical_metrics": critical_metrics,
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
                "high_alerts": high_alerts,
                "medium_alerts": medium_alerts,
                "low_alerts": low_alerts
            },
            "metrics": [asdict(metric) for metric in self.metrics],
            "alerts": [asdict(alert) for alert in self.alerts],
            "health_status": self.health_status,
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        # Check for critical issues
        critical_metrics = [m for m in self.metrics if m.status == "critical"]
        if critical_metrics:
            recommendations.append("CRITICAL: Address critical security issues immediately")
        
        # Check for warning issues
        warning_metrics = [m for m in self.metrics if m.status == "warning"]
        if warning_metrics:
            recommendations.append("HIGH: Address security warnings within 7 days")
        
        # Check for high-severity vulnerabilities
        high_vuln_metric = next((m for m in self.metrics if m.name == "High Severity Vulnerabilities"), None)
        if high_vuln_metric and high_vuln_metric.value > 0:
            recommendations.append("CRITICAL: Address high-severity vulnerabilities immediately")
        
        # Check for medium-severity vulnerabilities
        medium_vuln_metric = next((m for m in self.metrics if m.name == "Medium Severity Vulnerabilities"), None)
        if medium_vuln_metric and medium_vuln_metric.value > 0:
            recommendations.append("HIGH: Address medium-severity vulnerabilities within 7 days")
        
        # Check for low-severity vulnerabilities
        low_vuln_metric = next((m for m in self.metrics if m.name == "Low Severity Vulnerabilities"), None)
        if low_vuln_metric and low_vuln_metric.value > 5:
            recommendations.append("MEDIUM: Address low-severity vulnerabilities within 30 days")
        
        # Check security compliance
        compliance_metric = next((m for m in self.metrics if m.name == "Security Compliance"), None)
        if compliance_metric and compliance_metric.value < 90:
            recommendations.append("HIGH: Improve security compliance to meet target of 90%")
        
        if not recommendations:
            recommendations.append("EXCELLENT: All security metrics are within acceptable ranges")
        
        return recommendations
    
    def _update_health_status(self):
        """Update health status."""
        self.health_status.update({
            "last_check": datetime.now(),
            "total_metrics": len(self.metrics),
            "total_alerts": len(self.alerts),
            "critical_alerts": len([a for a in self.alerts if a.severity == "Critical"]),
            "high_alerts": len([a for a in self.alerts if a.severity == "High"]),
            "medium_alerts": len([a for a in self.alerts if a.severity == "Medium"]),
            "low_alerts": len([a for a in self.alerts if a.severity == "Low"])
        })
        
        # Update overall status
        if self.health_status["critical_alerts"] > 0:
            self.health_status["status"] = "critical"
        elif self.health_status["high_alerts"] > 0:
            self.health_status["status"] = "warning"
        else:
            self.health_status["status"] = "healthy"
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status."""
        return self.health_status
    
    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        return self.health_status["status"] == "healthy"
    
    def export_dashboard_data(self, filename: str) -> None:
        """Export dashboard data to file."""
        report = self.generate_dashboard_report()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Dashboard data exported to: {filename}")


def main():
    """Main function for testing."""
    # Create security dashboard
    dashboard = SecurityMonitoringDashboard()
    
    # Collect security metrics
    metrics = dashboard.collect_security_metrics()
    
    # Generate security alerts
    alerts = dashboard.generate_security_alerts()
    
    # Generate dashboard report
    report = dashboard.generate_dashboard_report()
    
    # Display results
    print("🔒 Security Monitoring Dashboard - RM Compliant")
    print("=" * 60)
    print(f"Health Status: {dashboard.health_status['status']}")
    print(f"Overall Security Score: {report['summary']['overall_security_score']:.1f}%")
    print(f"Total Metrics: {dashboard.health_status['total_metrics']}")
    print(f"Total Alerts: {dashboard.health_status['total_alerts']}")
    print(f"Critical Alerts: {dashboard.health_status['critical_alerts']}")
    print(f"High Alerts: {dashboard.health_status['high_alerts']}")
    
    # Show metrics
    if metrics:
        print("\n📊 Security Metrics:")
        for metric in metrics:
            status_icon = "🔴" if metric.status == "critical" else "🟡" if metric.status == "warning" else "🟢"
            print(f"  {status_icon} {metric.name}: {metric.value} {metric.unit} ({metric.status})")
    
    # Show alerts
    if alerts:
        print("\n🚨 Security Alerts:")
        for alert in alerts:
            severity_icon = "🔴" if alert.severity == "Critical" else "🟡" if alert.severity == "High" else "🟠" if alert.severity == "Medium" else "🔵"
            print(f"  {severity_icon} {alert.severity}: {alert.message}")
    
    # Show recommendations
    if report['recommendations']:
        print("\n💡 Recommendations:")
        for recommendation in report['recommendations']:
            print(f"  • {recommendation}")
    
    # Export dashboard data
    dashboard.export_dashboard_data("security_dashboard_report.json")
    
    print(f"\n✅ Dashboard report saved to: security_dashboard_report.json")
    print(f"System Healthy: {dashboard.is_healthy()}")


if __name__ == "__main__":
    main()
