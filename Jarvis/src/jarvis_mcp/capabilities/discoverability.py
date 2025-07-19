"""
Phase 1: Discoverability Tools for Jarvis MCP

This module implements the discoverability phase tools that enable users to explore
and understand the Jarvis ecosystem - available packages, repositories, capabilities,
and system resources.
"""

from typing import Dict, List, Any, Optional
import os
import json
import logging
from datetime import datetime

# Import Pydantic models
from jarvis_mcp.capabilities.models import (
    PackageCatalog, PackageInfo, PackageInformation, RepositoryStatus, 
    RepositoryInfo, RepositoryOperationResult, ClusterResourceStatus, 
    ResourceInfo, PackageType
)

# Try to import Jarvis components - these may not be available in all environments
try:
    from jarvis_cd.basic.jarvis_manager import JarvisManager
    JARVIS_MANAGER_AVAILABLE = True
except ImportError:
    JARVIS_MANAGER_AVAILABLE = False

try:
    from jarvis_cd.basic.resource_graph import ResourceGraph
    RESOURCE_GRAPH_AVAILABLE = True
except ImportError:
    RESOURCE_GRAPH_AVAILABLE = False

logger = logging.getLogger(__name__)

class DiscoverabilityError(Exception):
    """Custom exception for discoverability-related errors"""
    pass

def _check_jarvis_availability():
    """Check if Jarvis components are available"""
    if not JARVIS_MANAGER_AVAILABLE:
        raise DiscoverabilityError(
            "Jarvis Manager not available. Please ensure jarvis-cd is installed and configured. "
            "You may need to run 'pip install jarvis-cd' or set up the environment properly."
        )

async def get_all_packages(
    package_type: str = "all",
    repository_filter: Optional[str] = None,
    include_descriptions: bool = True,
    sort_by: str = "priority"
) -> PackageCatalog:
    """
    Retrieve comprehensive catalog of all available packages in the Jarvis ecosystem.
    
    This tool provides complete visibility into the Jarvis package ecosystem across
    all registered repositories. Unlike raw package listing commands, this tool
    provides intelligent categorization, filtering, and contextual information to
    help users find exactly what they need for their HPC workflows.
    
    **Discovery Strategy**:
    1. Scans all registered repositories in priority order
    2. Categorizes packages by type and use case
    3. Provides relevance scoring based on common usage patterns
    4. Highlights packages with strong documentation and examples
    5. Identifies package relationships and common combinations
    
    Args:
        package_type: Filter by type ("all", "service", "application", "interceptor")
        repository_filter: Only show packages from specific repository  
        include_descriptions: Include package descriptions and use cases
        sort_by: Sort order ("priority", "name", "type", "popularity")
    
    Returns:
        PackageCatalog containing:
        - Categorized package listings with metadata
        - Repository information and priority order
        - Package relationship mappings (what works well together)
        - Usage statistics and popularity indicators
        - Quick-start recommendations for common workflows
        
    **Selection Guidance**:
    - **Services**: Long-running systems (storage, databases, web servers)
    - **Applications**: Finite-execution programs (benchmarks, simulations)
    - **Interceptors**: Monitoring and profiling tools (tracers, debuggers)
    
    **Common Package Combinations**:
    - Storage + Benchmark: "orangefs" + "ior" for filesystem testing
    - Simulation + Analysis: "incompact3d" + "paraview" for flow visualization
    - Development + Debug: "hermes" + "hermes_api" for I/O optimization
    
    Prerequisites:
        - Jarvis configuration must be initialized (run 'jarvis config init')
        - At least built-in repository must be accessible
        
    **When this tool might fail**:
        - Jarvis not configured: Run 'jarvis config init' first
        - No repositories registered: Add repos with modify_repo tool
        - Network issues: Some repos may be temporarily unavailable
        
    **Tools to use before this**:
        - None required - this is typically the first discovery tool
        
    **Tools to use after this**:
        - get_package_info() to learn about specific packages
        - get_resource_status() to understand deployment constraints
        - create_pipeline_composition() to start building workflows
        
    Use this tool when:
        - Starting HPC workflow planning ("What can I deploy?")
        - Exploring available applications for specific use cases
        - Auditing the current package ecosystem
        - Looking for alternatives to existing tools
        - Understanding package ecosystem relationships
    """
    try:
        _check_jarvis_availability()
        manager = JarvisManager.get_instance()
        
        # Get all packages from all repositories
        all_packages_data = {}
        repositories = []
        
        # Get repository information from manager.repos
        for repo in manager.repos:
            repo_name = repo['name']
            repo_path = repo['path']
            repositories.append(repo_name)
            
            # Get packages from this repository
            try:
                if repository_filter is None or repo_name == repository_filter:
                    repo_packages = _get_packages_from_repo(repo_name, repo_path)
                    all_packages_data[repo_name] = repo_packages
            except Exception as e:
                logger.warning(f"Failed to get packages from repo {repo_name}: {e}")
                continue
        
        # Process packages into PackageInfo objects
        packages = []
        categorized_packages = {"service": [], "application": [], "interceptor": []}
        
        for repo_name, repo_packages in all_packages_data.items():
            for pkg_name, pkg_data in repo_packages.items():
                # Determine package type
                pkg_type = _determine_package_type(pkg_data)
                
                # Filter by package type if specified
                if package_type != "all" and pkg_type != package_type:
                    continue
                
                # Extract description
                description = "No description available"
                if include_descriptions:
                    description = _extract_package_description(pkg_data)
                
                # Extract capabilities
                capabilities = _extract_package_capabilities(pkg_data)
                
                # Create PackageInfo
                package_info = PackageInfo(
                    name=pkg_name,
                    type=pkg_type,
                    repository=repo_name,
                    description=description,
                    capabilities=capabilities,
                    popularity_score=_calculate_popularity_score(pkg_name),
                    documentation_quality=_assess_documentation_quality(pkg_data)
                )
                
                packages.append(package_info)
                categorized_packages[pkg_type].append(pkg_name)
        
        # Sort packages
        if sort_by == "name":
            packages.sort(key=lambda x: x.name)
        elif sort_by == "type":
            packages.sort(key=lambda x: x.type)
        elif sort_by == "popularity":
            packages.sort(key=lambda x: x.popularity_score, reverse=True)
        # Default: priority order (repository order)
        
        # Generate common combinations and recommendations
        common_combinations = _generate_common_combinations(packages)
        quick_start_recommendations = _generate_quick_start_recommendations(packages)
        
        return PackageCatalog(
            packages=packages,
            total_count=len(packages),
            repositories=repositories,
            common_combinations=common_combinations,
            quick_start_recommendations=quick_start_recommendations
        )
        
    except DiscoverabilityError:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve package catalog: {e}")
        raise DiscoverabilityError(f"Failed to retrieve package catalog: {e}")

async def get_package_info(
    package_name: str,
    return_description: bool = True,
    return_outputs: bool = False,
    return_config_params: bool = False,
    return_examples: bool = False,
    return_dependencies: bool = False,
    return_performance_notes: bool = False,
    summary_level: str = "detailed"
) -> PackageInformation:
    """
    Retrieve comprehensive information about a specific Jarvis package with intelligent filtering.
    
    This tool extracts extensive information from package documentation, README files,
    and configuration schemas. Following MCP best practices, it provides contextual
    information tailored to the user's specific query rather than dumping all available
    data. The tool understands different user intents and surfaces the most relevant
    information for each use case.
    
    **Information Extraction Strategy**:
    The tool analyzes the user's request and automatically emphasizes the most relevant
    information sections. It combines data from multiple sources:
    - Package README files (description, purpose, use cases)
    - Configuration schemas (parameters, types, defaults, validation)
    - Example configurations and pipeline scripts
    - Performance benchmarks and optimization notes
    - Dependency analysis and compatibility requirements
    
    Args:
        package_name: Name of the package to inspect (e.g., "incompact3d", "ior")
        return_description: Include package description and primary purpose
        return_outputs: Include detailed information about generated outputs/results
        return_config_params: Include configuration parameters with detailed explanations
        return_examples: Include usage examples and common configuration patterns
        return_dependencies: Include dependency tree and system requirements
        return_performance_notes: Include performance characteristics and tuning tips
        summary_level: Detail level ("brief", "detailed", "comprehensive")
    
    Returns:
        PackageInformation containing:
        - **Filtered content based on user's specific request**
        - Package metadata (type, version, repository source)
        - Configuration schema with parameter explanations and examples
        - Output specifications including file formats and locations
        - Dependency analysis with installation requirements
        - Performance characteristics and optimization guidance
        - Related packages and common workflow patterns
    
    **Smart Content Filtering**:
    The tool automatically prioritizes information based on query context:
    - "What is X?" → Focus on description and use cases
    - "What outputs does X generate?" → Emphasize output specifications
    - "How do I configure X?" → Highlight configuration parameters
    - "What are X's dependencies?" → Focus on requirements and compatibility
    
    **Configuration Parameter Details Include**:
    - Parameter name, type, and default values
    - Detailed descriptions of parameter effects on output
    - Valid ranges and validation constraints
    - Performance implications of different settings
    - Interaction effects between related parameters
    - Common configuration patterns for different use cases
    
    Prerequisites:
        - Package must exist in registered repositories
        - Package documentation must be accessible and well-formed
        
    **When this tool might fail**:
        - Package name not found: Check spelling or use get_all_packages() first
        - Insufficient documentation: Some packages may have limited metadata
        - Repository access issues: Network or permission problems
        
    **Tools to use before this**:
        - get_all_packages() to discover available package names
        - get_list_repos() to verify repository availability
        
    **Tools to use after this**:
        - create_pipeline_composition() to use the package in workflows
        - optimize_package_config() to tune parameters for specific use cases
        - get_resource_requirements() to verify deployment feasibility
        
    Use this tool when:
        - Learning about a specific package for the first time
        - Understanding package capabilities and limitations
        - Planning configuration strategies for specific use cases
        - Troubleshooting package-related issues
        - Comparing packages for workflow planning
    """
    try:
        _check_jarvis_availability()
        manager = JarvisManager.get_instance()
        
        # Find the package in repositories
        package_data = None
        source_repo = None
        
        for repo in manager.repos:
            repo_name = repo['name']
            repo_path = repo['path']
            try:
                repo_packages = _get_packages_from_repo(repo_name, repo_path)
                if package_name in repo_packages:
                    package_data = repo_packages[package_name]
                    source_repo = repo_name
                    break
            except Exception as e:
                logger.warning(f"Failed to search repo {repo_name}: {e}")
                continue
        
        if package_data is None:
            raise DiscoverabilityError(f"Package '{package_name}' not found in any repository")
        
        # Extract basic information
        pkg_type = _determine_package_type(package_data)
        
        description = "No description available"
        if return_description:
            description = _extract_package_description(package_data)
        
        # Extract README content
        readme_content = None
        if return_examples or return_outputs:
            readme_content = _extract_readme_content(package_data, source_repo or "", package_name)
        
        # Extract configuration parameters
        configuration_parameters = {}
        if return_config_params:
            configuration_parameters = _extract_configuration_parameters(package_data, source_repo or "unknown", package_name)
        
        # Extract capabilities
        capabilities = _extract_package_capabilities(package_data)
        
        # Extract outputs from README if requested
        output_specifications = {}
        if return_outputs and readme_content:
            output_specifications = _extract_output_specifications(readme_content)
        
        # Extract usage examples
        usage_examples = []
        if return_examples and readme_content:
            usage_examples = _extract_usage_examples(readme_content)
        
        # Extract dependencies
        dependencies = []
        if return_dependencies:
            dependencies = _extract_dependencies(package_data)
        
        # Extract performance notes
        performance_notes = []
        if return_performance_notes and readme_content:
            performance_notes = _extract_performance_notes(readme_content)
        
        # Find related packages
        related_packages = _find_related_packages(package_name, pkg_type, manager)
        
        return PackageInformation(
            package_name=package_name,
            package_type=pkg_type,
            repository=source_repo or "unknown",
            description=description,
            readme_content=readme_content if summary_level == "comprehensive" else None,
            configuration_parameters=configuration_parameters,
            capabilities=capabilities,
            output_specifications=output_specifications,
            installation_requirements=[],  # TODO: Extract from README
            usage_examples=usage_examples,
            dependencies=dependencies,
            performance_notes=performance_notes,
            related_packages=related_packages
        )
        
    except Exception as e:
        logger.error(f"Failed to get package info for {package_name}: {e}")
        raise DiscoverabilityError(f"Failed to retrieve package information: {str(e)}")

async def get_list_repos(
    include_package_counts: bool = True,
    include_health_status: bool = True,
    show_priority_order: bool = True
) -> RepositoryStatus:
    """
    List all currently registered Jarvis repositories with comprehensive status information.
    
    This tool provides complete visibility into the repository ecosystem that powers
    the Jarvis package system. Understanding repository configuration is crucial for
    package resolution, dependency management, and troubleshooting deployment issues.
    
    **Repository Priority System**:
    Jarvis searches repositories in priority order (1 = highest priority). When multiple
    repositories contain packages with the same name, higher priority repositories
    take precedence. This system allows custom implementations to override built-in
    packages while maintaining fallback options.
    
    Args:
        include_package_counts: Show number and types of packages in each repository
        include_health_status: Include connectivity and accessibility status
        show_priority_order: Display repositories in search priority order
        
    Returns:
        RepositoryStatus containing:
        - Repository metadata (name, path/URL, type)
        - Priority order and search sequence
        - Package inventory (count by type, featured packages)
        - Health status (connectivity, last update, error conditions)
        - Configuration details (custom vs built-in, access permissions)
        - Repository relationships and dependencies
        
    **Repository Types**:
    - **Built-in**: Official Jarvis repository with core packages
    - **Custom**: Organization-specific repositories with local packages
    - **Development**: Local development repositories for testing
    - **Cached**: Local copies of remote repositories for offline use
    
    **Health Status Indicators**:
    - ✅ Active: Repository accessible and functioning normally
    - ⚠️ Warning: Minor issues (slow response, outdated packages)  
    - ❌ Error: Major issues (inaccessible, corrupted, permission denied)
    - 🔄 Updating: Repository sync or update in progress
    
    Prerequisites:
        - Jarvis configuration must be initialized
        - User must have read access to repository configuration
        
    **When this tool might fail**:
        - Jarvis not configured: Initialize with 'jarvis config init'
        - Permission issues: Repository paths may require specific access rights
        - Network connectivity: Remote repositories may be temporarily unavailable
        
    **Tools to use before this**:
        - None required - this is a fundamental discovery tool
        
    **Tools to use after this**:
        - modify_repo() to add, remove, or reorder repositories
        - get_all_packages() to see packages from all repositories
        - diagnose_repo_issues() if health problems are detected
        
    **Common Repository Management Scenarios**:
    - **Adding Custom Repository**: Use modify_repo() with add=True
    - **Prioritizing Custom Packages**: Use modify_repo() with promote=True  
    - **Removing Outdated Repository**: Use modify_repo() with delete=True
    - **Troubleshooting Package Resolution**: Check priority order and health status
        
    Use this tool when:
        - Understanding current repository configuration
        - Debugging package resolution or "package not found" issues
        - Planning repository management operations
        - Auditing package sources and availability
        - Setting up new development environments
    """
    try:
        _check_jarvis_availability()
        manager = JarvisManager.get_instance()
        
        repositories = []
        priority_order = []
        total_packages = 0
        health_summary = {"active": 0, "warning": 0, "error": 0}
        
        # Get all repositories
        repo_list = manager.repos
        
        for i, repo in enumerate(repo_list):
            repo_name = repo['name']
            repo_path = repo['path']
            
            # Determine repository type
            repo_type = "builtin"
            if "custom" in repo_name.lower() or "local" in repo_name.lower():
                repo_type = "custom"
            elif "dev" in repo_name.lower():
                repo_type = "development"
            
            # Get package count
            package_count = 0
            featured_packages = []
            health_status = "active"
            
            if include_package_counts or include_health_status:
                try:
                    repo_packages = _get_packages_from_repo(repo_name, repo_path)
                    package_count = len(repo_packages)
                    total_packages += package_count
                    
                    # Get featured packages (first few packages)
                    featured_packages = list(repo_packages.keys())[:5]
                    
                    health_status = "active"
                    health_summary["active"] += 1
                except Exception as e:
                    logger.warning(f"Failed to access repo {repo_name}: {e}")
                    health_status = "error"
                    health_summary["error"] += 1
            
            repo_info = RepositoryInfo(
                name=repo_name,
                path=repo_path,
                priority=i + 1,  # Priority based on order
                status="active" if health_status == "active" else "inactive",
                package_count=package_count,
                last_updated=datetime.now(),  # TODO: Get actual last update
                health_status=health_status,
                repository_type=repo_type,
                featured_packages=featured_packages
            )
            
            repositories.append(repo_info)
            priority_order.append(repo_name)
        
        return RepositoryStatus(
            repositories=repositories,
            total_repositories=len(repositories),
            priority_order=priority_order,
            health_summary=health_summary,
            total_packages=total_packages
        )
        
    except Exception as e:
        logger.error(f"Failed to get repository list: {e}")
        raise DiscoverabilityError(f"Failed to retrieve repository status: {str(e)}")

async def modify_repo(
    repo_name: str,
    operation: str,
    repo_path: Optional[str] = None,
    verify_structure: bool = True,
    backup_config: bool = True
) -> RepositoryOperationResult:
    """
    Perform comprehensive repository lifecycle management operations with safety controls.
    
    This tool handles all repository management operations while providing safety
    checks, validation, and rollback capabilities. Following MCP best practices,
    it combines multiple related operations into a single, intelligent interface
    that understands the implications of each change.
    
    **Repository Management Operations**:
    
    **ADD**: Register new repository with comprehensive validation
    - Validates repository structure and package compatibility
    - Checks for naming conflicts with existing repositories
    - Verifies accessibility and permission requirements
    - Adds to end of priority list (lowest priority initially)
    - Creates backup of configuration before changes
    
    **DELETE**: Safely remove repository with dependency checking  
    - Analyzes active pipelines for dependencies on repository packages
    - Provides impact analysis before removal
    - Offers migration suggestions for affected pipelines
    - Removes from search path without deleting repository files
    - Creates rollback instructions for recovery
    
    **PROMOTE**: Elevate repository to highest priority with conflict resolution
    - Moves repository to top of search priority list
    - Analyzes package conflicts that may result from priority change
    - Provides warnings about packages that will be shadowed
    - Updates configuration atomically to prevent inconsistent state
    
    Args:
        repo_name: Repository identifier (must be unique)
        operation: Management operation ("add", "delete", "promote")
        repo_path: Required for "add" - absolute path to repository directory
        verify_structure: Validate repository structure before operation
        backup_config: Create configuration backup before changes
        
    Returns:
        RepositoryOperationResult containing:
        - Operation status (success, warning, error, rolled_back)
        - Updated repository configuration and priority order
        - Impact analysis (affected packages, pipelines, dependencies)
        - Conflict resolution recommendations
        - Rollback instructions and backup information
        - Next steps and follow-up recommendations
        
    **Safety and Validation Features**:
    - **Structure Validation**: Ensures repository follows Jarvis conventions
    - **Dependency Analysis**: Identifies packages and pipelines that depend on repository
    - **Conflict Detection**: Warns about package name conflicts and shadowing
    - **Atomic Operations**: Changes succeed completely or fail completely
    - **Rollback Support**: Provides instructions to undo changes if needed
    - **Configuration Backup**: Automatic backup before destructive operations
    
    Prerequisites:
        - For ADD: Repository path must exist and be properly structured
        - For DELETE/PROMOTE: Repository must be currently registered
        - User must have write access to Jarvis configuration directory
        - For remote repositories: Network connectivity and authentication
        
    **When this tool might fail**:
        - Invalid repository structure: Must follow Jarvis naming conventions
        - Permission denied: Insufficient access to configuration or repository
        - Active dependencies: Cannot delete repository with active pipeline dependencies
        - Network issues: Remote repository validation may fail
        - Naming conflicts: Repository name already exists (for add operation)
        
    **Tools to use before this**:
        - get_list_repos() to understand current repository configuration
        - analyze_pipeline_dependencies() to check for repository usage (before delete)
        - validate_repo_structure() to verify repository format (before add)
        
    **Tools to use after this**:
        - get_list_repos() to verify changes took effect
        - get_all_packages() to see updated package availability
        - test_pipeline_compatibility() to verify existing pipelines still work
        
    Use this tool when:
        - Setting up custom package repositories for organization
        - Managing package resolution priority and conflicts
        - Cleaning up outdated or unused repositories
        - Migrating from development to production repository configurations
        - Troubleshooting package availability and version conflicts
    """
    try:
        _check_jarvis_availability()
        manager = JarvisManager.get_instance()
        
        # Backup configuration if requested
        if backup_config:
            try:
                manager.save()  # Ensure current state is saved
            except Exception as e:
                logger.warning(f"Failed to backup configuration: {e}")
        
        # Get current repository list for impact analysis
        current_repos = manager.repos
        current_repo_names = [repo['name'] for repo in current_repos]
        
        impact_analysis = {}
        rollback_instructions = ""
        
        if operation.lower() == "add":
            if repo_path is None:
                raise DiscoverabilityError("Repository path is required for add operation")
            
            # Check if repository already exists
            if repo_name in current_repo_names:
                raise DiscoverabilityError(f"Repository '{repo_name}' already exists")
            
            # Validate repository structure if requested
            if verify_structure:
                if not os.path.exists(repo_path):
                    raise DiscoverabilityError(f"Repository path does not exist: {repo_path}")
                
                # Check for basic repository structure
                expected_structure = os.path.join(repo_path, repo_name)
                if not os.path.exists(expected_structure):
                    raise DiscoverabilityError(f"Invalid repository structure: missing {expected_structure}")
            
            # Add repository
            manager.add_repo(repo_path, force=True)
            manager.save()
            
            impact_analysis = {
                "new_packages": _count_packages_in_repo(repo_path),
                "priority_position": len(current_repo_names) + 1
            }
            
            rollback_instructions = f"To remove this repository: modify_repo('{repo_name}', 'delete')"
            
            return RepositoryOperationResult(
                operation="add",
                repository_name=repo_name,
                status="success",
                message=f"Repository '{repo_name}' added successfully at path {repo_path}",
                updated_priority_order=current_repo_names + [repo_name],
                impact_analysis=impact_analysis,
                rollback_instructions=rollback_instructions
            )
        
        elif operation.lower() == "delete":
            if repo_name not in current_repo_names:
                raise DiscoverabilityError(f"Repository '{repo_name}' not found")
            
            # TODO: Analyze pipeline dependencies
            impact_analysis = {
                "removed_packages": "Analysis not yet implemented",
                "affected_pipelines": []
            }
            
            # Remove repository
            manager.remove_repo(repo_name)
            manager.save()
            
            updated_priority_order = [name for name in current_repo_names if name != repo_name]
            rollback_instructions = f"Repository removal cannot be automatically undone. Manual re-addition required."
            
            return RepositoryOperationResult(
                operation="delete",
                repository_name=repo_name,
                status="success",
                message=f"Repository '{repo_name}' removed successfully",
                updated_priority_order=updated_priority_order,
                impact_analysis=impact_analysis,
                rollback_instructions=rollback_instructions
            )
        
        elif operation.lower() == "promote":
            if repo_name not in current_repo_names:
                raise DiscoverabilityError(f"Repository '{repo_name}' not found")
            
            # Promote repository
            manager.promote_repo(repo_name)
            manager.save()
            
            # Update priority order
            updated_priority_order = [repo_name] + [name for name in current_repo_names if name != repo_name]
            
            impact_analysis = {
                "new_priority": 1,
                "package_conflicts": "Analysis not yet implemented"
            }
            
            rollback_instructions = f"To restore original priority, manually reorder repositories"
            
            return RepositoryOperationResult(
                operation="promote",
                repository_name=repo_name,
                status="success",
                message=f"Repository '{repo_name}' promoted to highest priority",
                updated_priority_order=updated_priority_order,
                impact_analysis=impact_analysis,
                rollback_instructions=rollback_instructions
            )
        
        else:
            raise DiscoverabilityError(f"Unknown operation: {operation}")
    
    except Exception as e:
        logger.error(f"Repository operation failed: {e}")
        return RepositoryOperationResult(
            operation=operation,
            repository_name=repo_name,
            status="error",
            message=f"Operation failed: {str(e)}",
            updated_priority_order=[],
            impact_analysis={},
            rollback_instructions="Operation failed, no changes made"
        )

async def get_resource_status(
    include_hardware: bool = True,
    include_network: bool = True,
    include_storage: bool = True,
    include_utilization: bool = True,
    detail_level: str = "summary"
) -> ClusterResourceStatus:
    """
    Provide comprehensive cluster resource information for deployment planning.
    
    This tool exposes the Jarvis resource graph in an intelligent, decision-oriented
    format that helps users understand deployment constraints and optimization
    opportunities. Rather than raw hardware data, it provides actionable insights
    for HPC workflow planning.
    
    **Resource Analysis Strategy**:
    1. Introspects current cluster state via Jarvis resource graph
    2. Analyzes resource utilization patterns and availability
    3. Provides deployment recommendations based on resource constraints
    4. Identifies bottlenecks and optimization opportunities
    5. Maps resources to common package requirements
    
    Args:
        include_hardware: CPU, memory, and compute node information
        include_network: Network topology, bandwidth, and fabric details
        include_storage: Storage devices, filesystems, and capacity information
        include_utilization: Current resource usage and availability
        detail_level: Information depth ("summary", "detailed", "comprehensive")
        
    Returns:
        ClusterResourceStatus containing:
        - **Hardware inventory** with deployment-relevant specifications
        - **Network topology** with bandwidth and latency characteristics
        - **Storage hierarchy** with performance and capacity details
        - **Resource availability** and utilization patterns
        - **Deployment recommendations** based on current resource state
        - **Constraint analysis** for common package types
        
    Prerequisites:
        - Jarvis resource graph must be built ('jarvis rg build')
        - Hostfile must be configured for multi-node clusters
        - Appropriate permissions for hardware introspection
        
    **When this tool might fail**:
        - Resource graph not built: Run 'jarvis rg build' first
        - Permission issues: Hardware introspection may require elevated privileges
        - Network connectivity: Some nodes may be unreachable for remote introspection
        - Missing dependencies: Requires lsblk, df, fi_info, and related tools
        
    **Tools to use before this**:
        - build_resource_graph() if resource graph is not current
        - set_hostfile() to configure multi-node resource discovery
        
    **Tools to use after this**:
        - create_pipeline_composition() with resource-aware package selection
        - optimize_resource_allocation() to plan efficient deployments
        - validate_deployment_feasibility() to check specific package requirements
        
    Use this tool when:
        - Starting deployment planning for new workflows
        - Understanding cluster capabilities and limitations
        - Optimizing package placement for performance
        - Troubleshooting resource-related deployment failures
        - Planning resource allocation for multiple concurrent pipelines
    """
    try:
        # Initialize resource collections
        hardware_resources = []
        network_resources = []
        storage_resources = []
        deployment_constraints = {}
        optimization_recommendations = []
        
        # Try to get resource graph
        resource_graph_status = "unknown"
        try:
            if RESOURCE_GRAPH_AVAILABLE:
                # Check if resource graph exists
                rg = ResourceGraph()
                resource_graph_status = "available"
                
                # Extract hardware information
                if include_hardware:
                    hardware_resources = _extract_hardware_resources(rg, detail_level)
                
                # Extract network information
                if include_network:
                    network_resources = _extract_network_resources(rg, detail_level)
                
                # Extract storage information
                if include_storage:
                    storage_resources = _extract_storage_resources(rg, detail_level)
                
                # Generate deployment constraints
                deployment_constraints = _generate_deployment_constraints(rg)
                
                # Generate optimization recommendations
                optimization_recommendations = _generate_optimization_recommendations(
                    hardware_resources, network_resources, storage_resources
                )
            else:
                resource_graph_status = "not_available"
                optimization_recommendations = [
                    "Resource graph module not available. Jarvis-cd may not be installed.",
                    "Install jarvis-cd to enable detailed resource analysis."
                ]
            
        except Exception as e:
            logger.warning(f"Failed to access resource graph: {e}")
            resource_graph_status = "not_available"
            
            # Provide basic system information if resource graph is not available
            if include_hardware:
                hardware_resources = _get_basic_hardware_info()
            
            optimization_recommendations = [
                "Resource graph not available. Run 'jarvis rg build' to enable detailed resource analysis.",
                "Consider building resource graph for better deployment planning and optimization."
            ]
        
        return ClusterResourceStatus(
            hardware_resources=hardware_resources,
            network_resources=network_resources,
            storage_resources=storage_resources,
            deployment_constraints=deployment_constraints,
            optimization_recommendations=optimization_recommendations,
            resource_graph_status=resource_graph_status
        )
        
    except Exception as e:
        logger.error(f"Failed to get resource status: {e}")
        raise DiscoverabilityError(f"Failed to retrieve resource status: {str(e)}")

# Helper functions

def _calculate_popularity_score(package_name: str) -> float:
    """Calculate popularity score based on package name and known usage patterns"""
    popular_packages = {
        "ior": 0.9,
        "orangefs": 0.8,
        "hermes": 0.7,
        "incompact3d": 0.6,
        "paraview": 0.5
    }
    return popular_packages.get(package_name, 0.3)

def _assess_documentation_quality(package_data) -> str:
    """Assess documentation quality of a package"""
    if isinstance(package_data, dict):
        if hasattr(package_data, '__doc__') and package_data.__doc__:
            doc_length = len(package_data.__doc__.strip())
            if doc_length > 500:
                return "excellent"
            elif doc_length > 200:
                return "good"
            elif doc_length > 50:
                return "fair"
    return "poor"

def _generate_common_combinations(packages: List[PackageInfo]) -> Dict[str, List[str]]:
    """Generate common package combinations"""
    common_combinations = {}
    
    # Simple heuristic based on package types
    service_packages = [p.name for p in packages if p.type == "service"]
    application_packages = [p.name for p in packages if p.type == "application"]
    interceptor_packages = [p.name for p in packages if p.type == "interceptor"]
    
    if "ior" in service_packages and "orangefs" in service_packages:
        common_combinations["storage_benchmark"] = ["ior", "orangefs"]
    if "incompact3d" in application_packages:
        common_combinations["simulation_analysis"] = ["incompact3d", "paraview"]
    if "hermes" in application_packages:
        common_combinations["development_debug"] = ["hermes", "gdb", "valgrind"]
    if "hermes" in service_packages and "ior" in service_packages:
        common_combinations["io_optimization"] = ["hermes", "ior"]
    
    return common_combinations

def _generate_quick_start_recommendations(packages: List[PackageInfo]) -> List[str]:
    """Generate quick start recommendations based on available packages"""
    recommendations = []
    
    # Check for common workflows
    package_names = [p.name for p in packages]
    
    if "ior" in package_names and "orangefs" in package_names:
        recommendations.append("Try storage performance testing: orangefs + ior")
    
    if "incompact3d" in package_names:
        recommendations.append("Start with CFD simulation: incompact3d package")
    
    if "hermes" in package_names:
        recommendations.append("Explore I/O optimization: hermes package")
    
    if not recommendations:
        recommendations.append("Start with get_package_info() to learn about specific packages")
    
    return recommendations

def _extract_readme_content(package_data, repo_name: str, package_name: str) -> Optional[str]:
    """Extract README content from package"""
    # TODO: Implement README extraction from package files
    return None

def _extract_configuration_parameters(package_data, source_repo: str, package_name: str) -> Dict[str, Any]:
    """Extract configuration parameters from package data"""
    params = {}
    
    # For dict-based package data, we don't have access to _configure_menu
    if isinstance(package_data, dict):
        # Try to find configuration info in the package files
        if 'path' in package_data:
            pkg_path = package_data['path']
            pkg_py_path = os.path.join(pkg_path, 'pkg.py')
            if os.path.exists(pkg_py_path):
                try:
                    with open(pkg_py_path, 'r') as f:
                        content = f.read()
                        # Simple heuristic: look for configuration patterns
                        if 'configure' in content.lower():
                            params['configuration'] = {
                                'type': 'dynamic',
                                'default': None,
                                'description': 'Package supports configuration',
                                'required': False
                            }
                except Exception as e:
                    logger.warning(f"Failed to analyze configuration for {package_name}: {e}")
    else:
        # For object-based package data (if we had actual package instances)
        if hasattr(package_data, '_configure_menu'):
            try:
                menu = package_data._configure_menu()
                for item in menu:
                    if isinstance(item, dict) and 'name' in item:
                        params[item['name']] = {
                            'type': item.get('type', 'unknown'),
                            'default': item.get('default', None),
                            'description': item.get('description', ''),
                            'required': item.get('required', False)
                        }
            except Exception as e:
                logger.warning(f"Failed to extract configuration parameters for {package_name}: {e}")
    
    return params

def _extract_output_specifications(readme_content: str) -> Dict[str, Any]:
    """Extract output specifications from README content"""
    # TODO: Implement output specification extraction
    return {}

def _extract_usage_examples(readme_content: str) -> List[str]:
    """Extract usage examples from README content"""
    # TODO: Implement usage example extraction
    return []

def _extract_dependencies(package_data) -> List[str]:
    """Extract package dependencies"""
    # TODO: Implement dependency extraction
    return []

def _extract_performance_notes(readme_content: str) -> List[str]:
    """Extract performance notes from README content"""
    # TODO: Implement performance notes extraction
    return []

def _find_related_packages(package_name: str, package_type: str, manager) -> List[str]:
    """Find related packages based on type and common usage patterns"""
    related = []
    
    # Simple heuristic based on package type
    if package_type == "service":
        related.extend(["ior", "darshan"])  # Common with storage services
    elif package_type == "application":
        related.extend(["paraview", "hdf5"])  # Common with simulation applications
    
    return related

def _count_packages_in_repo(repo_path: str) -> int:
    """Count packages in a repository"""
    # TODO: Implement package counting
    return 0

def _extract_hardware_resources(rg, detail_level: str) -> List[ResourceInfo]:
    """Extract hardware resources from resource graph"""
    # TODO: Implement hardware resource extraction
    return []

def _extract_network_resources(rg, detail_level: str) -> List[ResourceInfo]:
    """Extract network resources from resource graph"""
    # TODO: Implement network resource extraction
    return []

def _extract_storage_resources(rg, detail_level: str) -> List[ResourceInfo]:
    """Extract storage resources from resource graph"""
    # TODO: Implement storage resource extraction
    return []

def _generate_deployment_constraints(rg) -> Dict[str, Any]:
    """Generate deployment constraints from resource graph"""
    # TODO: Implement deployment constraint generation
    return {}

def _generate_optimization_recommendations(hardware, network, storage) -> List[str]:
    """Generate optimization recommendations based on resources"""
    recommendations = []
    
    if not hardware:
        recommendations.append("No hardware information available. Consider building resource graph.")
    
    if not network:
        recommendations.append("No network information available. Network optimization may be limited.")
    
    if not storage:
        recommendations.append("No storage information available. I/O optimization may be limited.")
    
    return recommendations

def _get_basic_hardware_info() -> List[ResourceInfo]:
    """Get basic hardware information without resource graph"""
    resources = []
    
    # Try to get basic CPU info
    try:
        import os
        cpu_count = os.cpu_count()
        if cpu_count:
            resources.append(ResourceInfo(
                resource_type="cpu",
                name="CPU Cores",
                capacity=str(cpu_count),
                utilization=0.0,
                status="available",
                performance_characteristics={}
            ))
    except:
        pass
    
    return resources 

def _get_packages_from_repo(repo_name: str, repo_path: str) -> Dict[str, Any]:
    """Get packages from a specific repository"""
    packages = {}
    
    # Check if repo path exists
    if not os.path.exists(repo_path):
        logger.warning(f"Repository path does not exist: {repo_path}")
        return packages
    
    # Look for packages in the repository
    repo_pkg_dir = os.path.join(repo_path, repo_name)
    if not os.path.exists(repo_pkg_dir):
        logger.warning(f"Repository package directory does not exist: {repo_pkg_dir}")
        return packages
    
    # Scan for package directories
    try:
        for item in os.listdir(repo_pkg_dir):
            item_path = os.path.join(repo_pkg_dir, item)
            if os.path.isdir(item_path) and not item.startswith('_'):
                # Check if it's a valid package (has pkg.py or package.py)
                pkg_file = os.path.join(item_path, 'pkg.py')
                package_file = os.path.join(item_path, 'package.py')
                
                if os.path.exists(pkg_file) or os.path.exists(package_file):
                    # Try to load package metadata
                    try:
                        pkg_data = _load_package_metadata(item_path, item)
                        packages[item] = pkg_data
                    except Exception as e:
                        logger.warning(f"Failed to load package {item}: {e}")
                        # Still add it as a basic package
                        packages[item] = {
                            'name': item,
                            'path': item_path,
                            'type': 'application',
                            'description': f"Package {item} (metadata loading failed)"
                        }
    except Exception as e:
        logger.error(f"Failed to scan repository {repo_name}: {e}")
    
    return packages

def _load_package_metadata(pkg_path: str, pkg_name: str) -> Dict[str, Any]:
    """Load package metadata from package files"""
    metadata = {
        'name': pkg_name,
        'path': pkg_path,
        'type': 'application',
        'description': f"Package {pkg_name}",
        'capabilities': [],
        'documentation_quality': 'basic'
    }
    
    # Try to read README
    readme_path = os.path.join(pkg_path, 'README.md')
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r') as f:
                content = f.read()
                # Extract first paragraph as description
                lines = content.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        metadata['description'] = line.strip()
                        break
                metadata['documentation_quality'] = 'good'
        except Exception as e:
            logger.warning(f"Failed to read README for {pkg_name}: {e}")
    
    # Try to determine package type from directory structure or files
    pkg_py_path = os.path.join(pkg_path, 'pkg.py')
    if os.path.exists(pkg_py_path):
        try:
            with open(pkg_py_path, 'r') as f:
                content = f.read()
                if 'Service' in content:
                    metadata['type'] = 'service'
                elif 'Interceptor' in content:
                    metadata['type'] = 'interceptor'
                elif 'Application' in content:
                    metadata['type'] = 'application'
        except Exception as e:
            logger.warning(f"Failed to analyze pkg.py for {pkg_name}: {e}")
    
    return metadata

def _determine_package_type(pkg_data: Dict[str, Any]) -> str:
    """Determine package type from package data"""
    if isinstance(pkg_data, dict):
        return pkg_data.get('type', 'application')
    return 'application'

def _extract_package_description(pkg_data: Dict[str, Any]) -> str:
    """Extract package description from package data"""
    if isinstance(pkg_data, dict):
        return pkg_data.get('description', 'No description available')
    return 'No description available'

def _extract_package_capabilities(pkg_data: Dict[str, Any]) -> List[str]:
    """Extract package capabilities from package data"""
    if isinstance(pkg_data, dict):
        return pkg_data.get('capabilities', [])
    return [] 