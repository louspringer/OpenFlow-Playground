"""
Pydantic schemas for model validation and type safety.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class DomainInfo(BaseModel):
    """Schema for domain information."""

    patterns: List[str] = Field(default_factory=list, description="File patterns for domain")
    content_indicators: List[str] = Field(default_factory=list, description="Content indicators")
    linter: Optional[str] = Field(None, description="Linter tool")
    formatter: Optional[str] = Field(None, description="Formatter tool")
    validator: Optional[str] = Field(None, description="Validator tool")
    exclusions: List[str] = Field(default_factory=list, description="Exclusion patterns")
    requirements: List[str] = Field(default_factory=list, description="Domain requirements")
    demo_role: Optional[str] = Field(None, description="Demo role")
    extraction_candidate: bool = Field(False, description="Extraction candidate flag")
    reason: Optional[str] = Field(None, description="Reason for domain")
    completion_status: Optional[str] = Field(None, description="Completion status")
    refactoring_status: Optional[str] = Field(None, description="Refactoring status")
    current_phase: Optional[str] = Field(None, description="Current phase")
    refactored_modules: List[str] = Field(default_factory=list, description="Refactored modules")
    new_modules: List[str] = Field(default_factory=list, description="New modules")
    tools: List[str] = Field(default_factory=list, description="Tools")
    capabilities: List[str] = Field(default_factory=list, description="Capabilities")
    description: Optional[str] = Field(None, description="Domain description")
    package_potential: Optional[Dict[str, Any]] = Field(None, description="Package potential info")


class CategoryInfo(BaseModel):
    """Schema for category information."""

    description: Optional[str] = Field(None, description="Category description")
    domains: List[str] = Field(default_factory=list, description="Domains in category")
    purpose: Optional[str] = Field(None, description="Category purpose")


class ProjectModel(BaseModel):
    """Schema for project model registry."""

    description: str = Field(..., description="Project description")
    author: str = Field(..., description="Project author")
    project_purpose: str = Field(..., description="Project purpose")
    domain_architecture: Dict[str, CategoryInfo] = Field(default_factory=dict, description="Domain architecture")
    domains: Dict[str, DomainInfo] = Field(default_factory=dict, description="Domain definitions")
    dependency_relationships: Dict[str, Any] = Field(default_factory=dict, description="Dependency relationships")
    requirements_traceability: List[Dict[str, Any]] = Field(default_factory=list, description="Requirements traceability")
    use_cases: List[Dict[str, Any]] = Field(default_factory=list, description="Use cases")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Meta information")

    @field_validator("domain_architecture")
    @classmethod
    def validate_domain_architecture(cls, v):
        """Validate domain architecture structure."""
        for category_name, category_info in v.items():
            if category_info is None:
                raise ValueError(f"Category info for '{category_name}' cannot be None")
        return v

    @field_validator("domains")
    @classmethod
    def validate_domains(cls, v):
        """Validate domains structure."""
        for domain_name, domain_info in v.items():
            if domain_info is None:
                raise ValueError(f"Domain info for '{domain_name}' cannot be None")
        return v


class ModelRegistryEntry(BaseModel):
    """Schema for model registry entry."""

    implementation: str = Field(..., description="Implementation type")
    config: Dict[str, Any] = Field(default_factory=dict, description="Model configuration")
    instance: Optional[Any] = Field(None, description="Model instance")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    last_accessed: Optional[datetime] = Field(None, description="Last access timestamp")
    access_count: int = Field(0, description="Access count")


class ModelRegistry(BaseModel):
    """Schema for model registry."""

    models: Dict[str, ModelRegistryEntry] = Field(default_factory=dict, description="Registered models")
    registry_file: str = Field(..., description="Registry file path")
    created_at: datetime = Field(default_factory=datetime.now, description="Registry creation timestamp")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")


class ValidationResult(BaseModel):
    """Schema for validation results."""

    is_valid: bool = Field(..., description="Validation result")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    timestamp: datetime = Field(default_factory=datetime.now, description="Validation timestamp")


class PerformanceMetrics(BaseModel):
    """Schema for performance metrics."""

    operation: str = Field(..., description="Operation name")
    duration_ms: float = Field(..., description="Operation duration in milliseconds")
    memory_usage_mb: Optional[float] = Field(None, description="Memory usage in MB")
    cpu_usage_percent: Optional[float] = Field(None, description="CPU usage percentage")
    timestamp: datetime = Field(default_factory=datetime.now, description="Metrics timestamp")
    success: bool = Field(..., description="Operation success")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class LogEntry(BaseModel):
    """Schema for log entries."""

    level: str = Field(..., description="Log level")
    message: str = Field(..., description="Log message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Log timestamp")
    operation: Optional[str] = Field(None, description="Operation name")
    target_model: Optional[str] = Field(None, description="Target model name")  # Fixed: was model_name
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")

    model_config = ConfigDict(protected_namespaces=())  # Disable protected namespace warnings
