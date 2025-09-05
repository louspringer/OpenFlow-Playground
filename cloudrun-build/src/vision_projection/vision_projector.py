#!/usr/bin/env python3
"""
Vision Projector - Reflective Module Compliant

A systematic approach to transforming complex technical innovations into 
audience-specific content formats with full RM compliance.
"""

import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

# Add src to path for absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


class ContentFormat(Enum):
    """Content format types for vision projection."""

    EXECUTIVE_SUMMARY = "executive_summary"
    TECHNICAL_DEEP_DIVE = "technical_deep_dive"
    IMPLEMENTATION_GUIDE = "implementation_guide"
    MARKETING_CONTENT = "marketing_content"
    EDUCATIONAL_CONTENT = "educational_content"
    LINKEDIN_ARTICLE = "linkedin_article"
    CONFERENCE_PRESENTATION = "conference_presentation"
    TECHNICAL_BLOG = "technical_blog"
    DOCUMENTATION = "documentation"


class AudienceType(Enum):
    """Audience types for vision projection."""

    CXO = "cxo"
    CTO = "cto"
    VP_ENGINEERING = "vp_engineering"
    DEVELOPERS = "developers"
    PARTNERS = "partners"
    INVESTORS = "investors"
    CUSTOMERS = "customers"
    STUDENTS = "students"


@dataclass
class VisionProjectionConfig:
    """Configuration for vision projection."""

    core_innovation: str
    target_audiences: List[AudienceType]
    content_formats: List[ContentFormat]
    platforms: List[str]
    engagement_metrics: Dict[str, Any]
    success_criteria: Dict[str, Any]


@dataclass
class ContentAsset:
    """Content asset for vision projection."""

    id: str
    title: str
    content: str
    format: ContentFormat
    audience: AudienceType
    platform: str
    created_at: datetime
    updated_at: datetime
    engagement_metrics: Dict[str, Any]
    health_status: str = "unknown"


class VisionProjector:
    """
    Reflective Module Compliant Vision Projector

    Transforms technical innovations into audience-specific content formats
    with full RM compliance including health monitoring, self-reporting,
    and operational visibility.
    """

    def __init__(self, config: VisionProjectionConfig):
        """Initialize the vision projector with RM compliance."""
        self.config = config
        self.assets_dir = Path("content_assets")
        self.metrics_file = Path("vision_projection_metrics.json")
        self.health_status = "unknown"
        self.last_health_check = None
        self.error_count = 0
        self.success_count = 0
        self.performance_history = []
        self.avg_execution_time = 0

        # RM Compliance: Initialize health monitoring
        self._initialize_health_monitoring()

        # RM Compliance: Ensure operational visibility
        self._ensure_operational_visibility()

    def _initialize_health_monitoring(self):
        """Initialize health monitoring (RM Self-Monitoring)."""
        self.health_status = "initializing"
        self.last_health_check = time.time()

        # Create assets directory if it doesn't exist
        self.assets_dir.mkdir(exist_ok=True)

        # Load existing metrics
        self._load_metrics()

        self.health_status = "healthy"
        self.success_count += 1

    def _ensure_operational_visibility(self):
        """Ensure operational visibility (RM Operational Visibility)."""
        # Create health status file
        health_file = Path("vision_projector_health.json")
        health_data = {
            "status": self.health_status,
            "last_check": self.last_health_check,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "avg_execution_time": self.avg_execution_time,
        }

        with open(health_file, "w") as f:
            json.dump(health_data, f, indent=2, default=str)

    def _load_metrics(self):
        """Load existing metrics (RM Self-Reporting)."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r") as f:
                    metrics = json.load(f)
                    self.performance_history = metrics.get("performance_history", [])
                    if self.performance_history:
                        self.avg_execution_time = sum(self.performance_history) / len(self.performance_history)
            except Exception as e:
                self._log_error(f"Failed to load metrics: {e}")

    def _save_metrics(self):
        """Save metrics (RM Self-Reporting)."""
        try:
            metrics = {
                "performance_history": self.performance_history,
                "avg_execution_time": self.avg_execution_time,
                "total_assets": len(self._list_assets()),
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.metrics_file, "w") as f:
                json.dump(metrics, f, indent=2, default=str)
        except Exception as e:
            self._log_error(f"Failed to save metrics: {e}")

    def _log_error(self, message: str):
        """Log error (RM Self-Monitoring)."""
        self.error_count += 1
        self.health_status = "degraded"
        print(f"❌ Vision Projector Error: {message}")

    def _log_success(self, message: str):
        """Log success (RM Self-Monitoring)."""
        self.success_count += 1
        self.health_status = "healthy"
        print(f"✅ Vision Projector Success: {message}")

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status (RM Self-Reporting)."""
        return {
            "status": self.health_status,
            "last_check": self.last_health_check,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "avg_execution_time": self.avg_execution_time,
            "total_assets": len(self._list_assets()),
        }

    def is_healthy(self) -> bool:
        """Check if system is healthy (RM Self-Monitoring)."""
        return self.health_status == "healthy" and self.error_count < 5

    def project_vision(self) -> Dict[str, ContentAsset]:
        """
        Project vision into multiple content formats (RM Single Responsibility).

        Returns:
            Dict of content assets keyed by format_audience
        """
        start_time = time.time()

        try:
            if not self.is_healthy():
                raise Exception("System not healthy - cannot project vision")

            assets = {}

            # Generate content for each audience and format combination
            for audience in self.config.target_audiences:
                for format_type in self.config.content_formats:
                    asset = self._create_content_asset(audience, format_type)
                    key = f"{format_type.value}_{audience.value}"
                    assets[key] = asset

            execution_time = time.time() - start_time
            self.performance_history.append(execution_time)
            self.avg_execution_time = sum(self.performance_history) / len(self.performance_history)

            self._log_success(f"Vision projected into {len(assets)} content assets")
            self._save_metrics()

            return assets

        except Exception as e:
            execution_time = time.time() - start_time
            self.performance_history.append(execution_time)
            self._log_error(f"Vision projection failed: {e}")
            raise

    def _create_content_asset(self, audience: AudienceType, format_type: ContentFormat) -> ContentAsset:
        """Create content asset for specific audience and format."""
        asset_id = f"{format_type.value}_{audience.value}_{int(time.time())}"

        # Generate content based on format and audience
        content = self._generate_content(audience, format_type)

        asset = ContentAsset(
            id=asset_id,
            title=self._generate_title(audience, format_type),
            content=content,
            format=format_type,
            audience=audience,
            platform=self._get_platform_for_format(format_type),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            engagement_metrics={},
            health_status="created",
        )

        # Save asset to file
        self._save_asset(asset)

        return asset

    def _generate_content(self, audience: AudienceType, format_type: ContentFormat) -> str:
        """Generate content for specific audience and format."""
        templates = {
            (AudienceType.CXO, ContentFormat.EXECUTIVE_SUMMARY): self._generate_cxo_executive_summary,
            (AudienceType.CTO, ContentFormat.TECHNICAL_DEEP_DIVE): self._generate_cto_technical_deep_dive,
            (AudienceType.VP_ENGINEERING, ContentFormat.IMPLEMENTATION_GUIDE): self._generate_vp_implementation_guide,
            (AudienceType.DEVELOPERS, ContentFormat.DOCUMENTATION): self._generate_developer_documentation,
            (AudienceType.PARTNERS, ContentFormat.MARKETING_CONTENT): self._generate_partner_marketing_content,
        }

        # Default to generic content generation
        generator = templates.get((audience, format_type), self._generate_generic_content)
        return generator()

    def _generate_cxo_executive_summary(self) -> str:
        """Generate CXO executive summary."""
        return f"""
# Executive Summary: {self.config.core_innovation}

## Business Impact
- **Competitive Advantage**: Revolutionary approach to quality requirements
- **Risk Mitigation**: Strong convergence guardrails prevent system divergence
- **Innovation Enablement**: Quality systems that support rather than hinder innovation
- **Scalable Growth**: Quality requirements that evolve with business expansion

## Key Benefits
✅ Faster Development: Essential quality requirements prevent analysis paralysis
✅ Better Quality: Adaptive quality requirements ensure quality evolves with the system
✅ Reduced Technical Debt: Incident-driven improvement prevents quality debt accumulation
✅ Continuous Learning: Knowledge capture ensures quality improvement over time

## Implementation Strategy
- **Phase 1**: Essential quality requirements (5 critical guardrails)
- **Phase 2**: Quality monitoring framework
- **Phase 3**: Incident-driven improvement processes

## ROI Projection
- **Development Velocity**: 30% improvement
- **Quality Improvement**: 50% reduction in production issues
- **Technical Debt**: 40% reduction in accumulated debt
- **Team Productivity**: 25% improvement in delivery speed
"""

    def _generate_cto_technical_deep_dive(self) -> str:
        """Generate CTO technical deep dive."""
        return f"""
# Technical Deep Dive: {self.config.core_innovation}

## Architecture Overview
The system implements a recursive, self-reinforcing architecture with multiple levels:

### Level 1: Essential Quality Requirements
- Health Monitoring
- Graceful Degradation
- Performance Monitoring
- Security Monitoring
- Operational Visibility

### Level 2: Adaptive Quality Monitoring
- Thresholds that adapt based on real usage patterns
- Quality requirements that evolve with system growth
- Incident-driven improvement based on real problems

### Level 3: Continuous Learning
- Knowledge capture from every quality incident
- Requirements that improve through operational experience
- Systems that get smarter over time

## Technical Implementation
- **Recursive Architecture**: Turtles all the way down
- **Wheels Within Wheels**: Four interconnected loops
- **Convergence Guardrails**: Strong boundaries prevent divergence
- **Adaptive Thresholds**: Dynamic adjustment based on usage patterns

## Performance Metrics
- **100% Quality Requirements Coverage**: All critical components monitored
- **95% Adaptive Threshold Accuracy**: Thresholds adapt correctly
- **90% Incident Resolution Rate**: Issues resolved within 24 hours
- **100% Knowledge Capture Rate**: Every incident results in learning
"""

    def _generate_vp_implementation_guide(self) -> str:
        """Generate VP Engineering implementation guide."""
        return f"""
# Implementation Guide: {self.config.core_innovation}

## Phase 1: Foundation (Immediate)
1. **Implement Essential Quality Requirements**
   - Health Monitoring for all critical components
   - Graceful Degradation for failure scenarios
   - Performance Monitoring with adaptive thresholds
   - Security Monitoring with threat detection
   - Operational Visibility for system state

2. **Deploy Quality Monitoring Framework**
   - Set up continuous monitoring
   - Configure adaptive thresholds
   - Implement incident detection
   - Create knowledge capture systems

## Phase 2: Scaling (6 Months)
1. **Expand Multi-System Monitoring**
   - Cross-system quality monitoring
   - Integrated incident response
   - Centralized knowledge management

2. **Implement Team Collaboration**
   - Cross-team quality knowledge sharing
   - Collaborative incident resolution
   - Shared quality improvement processes

## Phase 3: Intelligence (12 Months)
1. **AI-Driven Quality Enhancement**
   - Predictive quality issue detection
   - Autonomous quality system optimization
   - Industry quality benchmarking

## Success Metrics
- **Development Velocity**: Measure team productivity improvement
- **Quality Metrics**: Track production issue reduction
- **Technical Debt**: Monitor debt accumulation trends
- **Team Satisfaction**: Survey team experience with quality systems
"""

    def _generate_developer_documentation(self) -> str:
        """Generate developer documentation."""
        innovation = self.config.core_innovation
        return f"""
# Developer Documentation: {innovation}

## Getting Started
1. **Installation**
   ```bash
   pip install vision-projection-framework
   ```

2. **Basic Usage**
   ```python
   from vision_projection import VisionProjector, VisionProjectionConfig
   
   config = VisionProjectionConfig(
       core_innovation="Your Innovation",
       target_audiences=[AudienceType.CXO, AudienceType.CTO],
       content_formats=[ContentFormat.EXECUTIVE_SUMMARY],
       platforms=["linkedin", "blog"],
       engagement_metrics={{}},
       success_criteria={{}}
   )
   
   projector = VisionProjector(config)
   assets = projector.project_vision()
   ```

## API Reference
### VisionProjector Class
- `project_vision()`: Generate content assets
- `get_health_status()`: Get system health
- `is_healthy()`: Check system health

### ContentAsset Class
- `id`: Unique asset identifier
- `title`: Asset title
- `content`: Generated content
- `format`: Content format type
- `audience`: Target audience
- `platform`: Target platform

## Examples
See the examples directory for complete usage examples.
"""

    def _generate_partner_marketing_content(self) -> str:
        """Generate partner marketing content."""
        innovation = self.config.core_innovation
        return f"""
# Marketing Content: {innovation}

## Value Proposition
Revolutionary approach to quality requirements that provides:
- **Competitive Advantage**: Adaptive quality systems that scale with business growth
- **Market Differentiation**: First-to-market recursive quality architecture
- **Partnership Opportunity**: Joint go-to-market for quality transformation
- **Revenue Growth**: New revenue streams through quality consulting

## Market Opportunity
- **Total Addressable Market**: $50B+ quality assurance market
- **Target Market**: Enterprise software companies
- **Competitive Advantage**: 2-3 year technology lead
- **Partnership Value**: Joint solution development and market expansion

## Partnership Benefits
- **Technical Excellence**: Access to cutting-edge quality technology
- **Market Leadership**: Position as quality innovation leader
- **Revenue Sharing**: Joint revenue opportunities
- **Customer Success**: Improved customer satisfaction and retention

## Next Steps
1. **Technical Integration**: Integrate quality framework
2. **Joint Marketing**: Co-marketing opportunities
3. **Customer Success**: Joint customer implementations
4. **Revenue Growth**: Expand market reach together
"""

    def _generate_generic_content(self) -> str:
        """Generate generic content."""
        innovation = self.config.core_innovation
        return f"""
# Content: {innovation}

## Overview
{innovation} represents a revolutionary approach to quality requirements.

## Key Features
- Adaptive quality requirements
- Incident-driven improvement
- Continuous learning
- Strong convergence guardrails

## Benefits
- Improved development velocity
- Better quality outcomes
- Reduced technical debt
- Continuous improvement

## Implementation
Contact us to learn more about implementing this innovation in your organization.
"""

    def _generate_title(self, audience: AudienceType, format_type: ContentFormat) -> str:
        """Generate title for content asset."""
        titles = {
            (AudienceType.CXO, ContentFormat.EXECUTIVE_SUMMARY): f"Executive Summary: {self.config.core_innovation}",
            (AudienceType.CTO, ContentFormat.TECHNICAL_DEEP_DIVE): f"Technical Deep Dive: {self.config.core_innovation}",
            (AudienceType.VP_ENGINEERING, ContentFormat.IMPLEMENTATION_GUIDE): f"Implementation Guide: {self.config.core_innovation}",
            (AudienceType.DEVELOPERS, ContentFormat.DOCUMENTATION): f"Developer Documentation: {self.config.core_innovation}",
            (AudienceType.PARTNERS, ContentFormat.MARKETING_CONTENT): f"Marketing Content: {self.config.core_innovation}",
        }

        return titles.get((audience, format_type), f"{format_type.value.title()}: {self.config.core_innovation}")

    def _get_platform_for_format(self, format_type: ContentFormat) -> str:
        """Get platform for content format."""
        platform_mapping = {
            ContentFormat.EXECUTIVE_SUMMARY: "linkedin",
            ContentFormat.TECHNICAL_DEEP_DIVE: "conference",
            ContentFormat.IMPLEMENTATION_GUIDE: "blog",
            ContentFormat.MARKETING_CONTENT: "website",
            ContentFormat.EDUCATIONAL_CONTENT: "learning_platform",
            ContentFormat.LINKEDIN_ARTICLE: "linkedin",
            ContentFormat.CONFERENCE_PRESENTATION: "conference",
            ContentFormat.TECHNICAL_BLOG: "blog",
            ContentFormat.DOCUMENTATION: "documentation_site",
        }

        return platform_mapping.get(format_type, "general")

    def _save_asset(self, asset: ContentAsset):
        """Save content asset to file (RM Self-Documentation)."""
        asset_file = self.assets_dir / f"{asset.id}.json"

        asset_data = asdict(asset)
        asset_data["created_at"] = asset.created_at.isoformat()
        asset_data["updated_at"] = asset.updated_at.isoformat()
        asset_data["format"] = asset.format.value
        asset_data["audience"] = asset.audience.value

        with open(asset_file, "w") as f:
            json.dump(asset_data, f, indent=2)

    def _list_assets(self) -> List[Path]:
        """List all content assets (RM Operational Visibility)."""
        if not self.assets_dir.exists():
            return []

        return list(self.assets_dir.glob("*.json"))

    def get_assets(self) -> List[ContentAsset]:
        """Get all content assets."""
        assets = []

        for asset_file in self._list_assets():
            try:
                with open(asset_file, "r") as f:
                    asset_data = json.load(f)

                asset = ContentAsset(
                    id=asset_data["id"],
                    title=asset_data["title"],
                    content=asset_data["content"],
                    format=ContentFormat(asset_data["format"]),
                    audience=AudienceType(asset_data["audience"]),
                    platform=asset_data["platform"],
                    created_at=datetime.fromisoformat(asset_data["created_at"]),
                    updated_at=datetime.fromisoformat(asset_data["updated_at"]),
                    engagement_metrics=asset_data.get("engagement_metrics", {}),
                    health_status=asset_data.get("health_status", "unknown"),
                )

                assets.append(asset)

            except Exception as e:
                self._log_error(f"Failed to load asset {asset_file}: {e}")

        return assets

    def update_asset_engagement(self, asset_id: str, metrics: Dict[str, Any]):
        """Update asset engagement metrics (RM Self-Monitoring)."""
        asset_file = self.assets_dir / f"{asset_id}.json"

        if not asset_file.exists():
            self._log_error(f"Asset {asset_id} not found")
            return

        try:
            with open(asset_file, "r") as f:
                asset_data = json.load(f)

            asset_data["engagement_metrics"] = metrics
            asset_data["updated_at"] = datetime.now().isoformat()

            with open(asset_file, "w") as f:
                json.dump(asset_data, f, indent=2)

            self._log_success(f"Updated engagement metrics for asset {asset_id}")

        except Exception as e:
            self._log_error(f"Failed to update asset {asset_id}: {e}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics (RM Self-Reporting)."""
        assets = self.get_assets()

        return {
            "total_assets": len(assets),
            "avg_execution_time": self.avg_execution_time,
            "performance_history": self.performance_history,
            "health_status": self.health_status,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "assets_by_format": self._get_assets_by_format(assets),
            "assets_by_audience": self._get_assets_by_audience(assets),
        }

    def _get_assets_by_format(self, assets: List[ContentAsset]) -> Dict[str, int]:
        """Get asset count by format."""
        format_counts = {}
        for asset in assets:
            format_name = asset.format.value
            format_counts[format_name] = format_counts.get(format_name, 0) + 1
        return format_counts

    def _get_assets_by_audience(self, assets: List[ContentAsset]) -> Dict[str, int]:
        """Get asset count by audience."""
        audience_counts = {}
        for asset in assets:
            audience_name = asset.audience.value
            audience_counts[audience_name] = audience_counts.get(audience_name, 0) + 1
        return audience_counts


def main():
    """Main function for testing the vision projector."""
    config = VisionProjectionConfig(
        core_innovation="Recursive Turtle Architecture",
        target_audiences=[AudienceType.CXO, AudienceType.CTO, AudienceType.VP_ENGINEERING],
        content_formats=[ContentFormat.EXECUTIVE_SUMMARY, ContentFormat.TECHNICAL_DEEP_DIVE],
        platforms=["linkedin", "conference"],
        engagement_metrics={},
        success_criteria={},
    )

    projector = VisionProjector(config)

    print("🎯 Vision Projector - RM Compliant")
    print("==================================")

    # Check health
    health = projector.get_health_status()
    print(f"Health Status: {health['status']}")
    print(f"Total Assets: {health['total_assets']}")

    # Project vision
    assets = projector.project_vision()
    print(f"Generated {len(assets)} content assets")

    # Show performance metrics
    metrics = projector.get_performance_metrics()
    print(f"Average Execution Time: {metrics['avg_execution_time']:.2f}s")
    print(f"Assets by Format: {metrics['assets_by_format']}")
    print(f"Assets by Audience: {metrics['assets_by_audience']}")


if __name__ == "__main__":
    main()
