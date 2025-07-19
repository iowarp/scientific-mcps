from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# Phase 1: Discoverability Models

class PackageType(str, Enum):
    SERVICE = "service"
    APPLICATION = "application"
    INTERCEPTOR = "interceptor"
    ALL = "all"

class PackageInfo(BaseModel):
    name: str = Field(..., description="Package name")
    type: str = Field(..., description="Package type (service, application, interceptor)")
    repository: str = Field(..., description="Repository name where package is located")
    description: str = Field(..., description="Package description")
    version: Optional[str] = Field(None, description="Package version if available")
    dependencies: List[str] = Field(default_factory=list, description="List of package dependencies")
    popularity_score: float = Field(default=0.0, description="Usage popularity score")
    documentation_quality: str = Field(default="unknown", description="Documentation quality assessment")
    capabilities: List[str] = Field(default_factory=list, description="Package capabilities")
    configuration_params: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters")

class PackageRelationship(BaseModel):
    package_a: str = Field(..., description="First package in relationship")
    package_b: str = Field(..., description="Second package in relationship")
    relationship_type: str = Field(..., description="Type of relationship (complement, conflict, dependency)")
    strength: float = Field(..., description="Relationship strength (0.0 to 1.0)")
    description: str = Field(..., description="Human-readable description of relationship")

class PackageCatalog(BaseModel):
    packages: List[PackageInfo] = Field(..., description="List of available packages")
    total_count: int = Field(..., description="Total number of packages")
    repositories: List[str] = Field(..., description="List of repository names")
    common_combinations: Dict[str, List[str]] = Field(default_factory=dict, description="Common package combinations")
    quick_start_recommendations: List[str] = Field(default_factory=list, description="Quick start recommendations")
    categorized_packages: Dict[str, List[str]] = Field(default_factory=dict, description="Packages organized by category")

class RepositoryInfo(BaseModel):
    name: str = Field(..., description="Repository name")
    path: str = Field(..., description="Repository filesystem path")
    priority: int = Field(..., description="Search priority (1 = highest)")
    status: str = Field(..., description="Repository status (active, inactive, error)")
    package_count: int = Field(..., description="Number of packages in repository")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    health_status: str = Field(..., description="Health status indicator")
    repository_type: str = Field(..., description="Repository type (builtin, custom, development)")
    featured_packages: List[str] = Field(default_factory=list, description="Notable packages in repository")

class RepositoryStatus(BaseModel):
    repositories: List[RepositoryInfo] = Field(..., description="List of repository information")
    total_repositories: int = Field(..., description="Total number of repositories")
    priority_order: List[str] = Field(..., description="Repository names in priority order")
    health_summary: Dict[str, int] = Field(default_factory=dict, description="Health status counts")
    total_packages: int = Field(..., description="Total packages across all repositories")

class RepositoryOperationResult(BaseModel):
    operation: str = Field(..., description="Operation performed (add, delete, promote)")
    repository_name: str = Field(..., description="Repository name")
    status: str = Field(..., description="Operation status (success, warning, error)")
    message: str = Field(..., description="Human-readable result message")
    updated_priority_order: List[str] = Field(default_factory=list, description="New repository priority order")
    impact_analysis: Dict[str, Any] = Field(default_factory=dict, description="Impact analysis of the operation")
    rollback_instructions: Optional[str] = Field(None, description="Instructions to undo the operation")

class ResourceInfo(BaseModel):
    resource_type: str = Field(..., description="Type of resource (cpu, memory, storage, network)")
    name: str = Field(..., description="Resource name or identifier")
    capacity: str = Field(..., description="Resource capacity")
    utilization: float = Field(..., description="Current utilization percentage")
    status: str = Field(..., description="Resource status")
    performance_characteristics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")

class ClusterResourceStatus(BaseModel):
    hardware_resources: List[ResourceInfo] = Field(default_factory=list, description="Hardware resource information")
    network_resources: List[ResourceInfo] = Field(default_factory=list, description="Network resource information")
    storage_resources: List[ResourceInfo] = Field(default_factory=list, description="Storage resource information")
    deployment_constraints: Dict[str, Any] = Field(default_factory=dict, description="Deployment constraints")
    optimization_recommendations: List[str] = Field(default_factory=list, description="Resource optimization suggestions")
    resource_graph_status: str = Field(..., description="Resource graph build status")

class PackageInformation(BaseModel):
    package_name: str = Field(..., description="Package name")
    package_type: str = Field(..., description="Package type")
    repository: str = Field(..., description="Source repository")
    description: str = Field(..., description="Package description")
    readme_content: Optional[str] = Field(None, description="README content")
    configuration_parameters: Dict[str, Any] = Field(default_factory=dict, description="Configuration parameters with details")
    capabilities: List[str] = Field(default_factory=list, description="Package capabilities")
    output_specifications: Dict[str, Any] = Field(default_factory=dict, description="Output specifications")
    installation_requirements: List[str] = Field(default_factory=list, description="Installation requirements")
    usage_examples: List[str] = Field(default_factory=list, description="Usage examples")
    dependencies: List[str] = Field(default_factory=list, description="Package dependencies")
    performance_notes: List[str] = Field(default_factory=list, description="Performance characteristics")
    related_packages: List[str] = Field(default_factory=list, description="Related or complementary packages") 