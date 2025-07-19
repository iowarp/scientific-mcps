"""
Jarvis MCP Server - Phase 1: Discoverability Implementation

This server implements the first phase of the Jarvis MCP according to the design document,
focusing on discoverability tools that enable users to explore and understand the Jarvis
ecosystem - available packages, repositories, capabilities, and system resources.

Following MCP best practices, these tools are designed with a workflow-first approach
rather than direct API mapping, providing intelligent, contextual assistance for
HPC workflow planning and deployment.
"""

from fastmcp import FastMCP
import os
import sys
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Import Phase 1 discoverability tools
from src.implementation.discoverability import (
    get_all_packages,
    get_package_info,
    get_list_repos,
    modify_repo,
    get_resource_status,
    DiscoverabilityError
)

# Import data models
from src.implementation.models import (
    PackageCatalog,
    PackageInformation,
    RepositoryStatus,
    RepositoryOperationResult,
    ClusterResourceStatus
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server instance
mcp = FastMCP("Jarvis-MCP-Phase1-Discoverability")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: DISCOVERABILITY TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="get_all_packages",
    description="""Get all available packages from all repositories with their descriptions and capabilities. 

This tool scans through all registered Jarvis repositories and returns a comprehensive catalog 
of available packages including their types, descriptions, configuration parameters, capabilities, 
and installation requirements. 

Use this to explore what packages are available before creating pipelines or to understand the 
full ecosystem of tools at your disposal.

**Discovery Strategy**:
1. Scans all registered repositories in priority order
2. Categorizes packages by type and use case  
3. Provides relevance scoring based on common usage patterns
4. Highlights packages with strong documentation and examples
5. Identifies package relationships and common combinations

**Selection Guidance**:
- **Services**: Long-running systems (storage, databases, web servers)
- **Applications**: Finite-execution programs (benchmarks, simulations)  
- **Interceptors**: Monitoring and profiling tools (tracers, debuggers)

**Common Package Combinations**:
- Storage + Benchmark: "orangefs" + "ior" for filesystem testing
- Simulation + Analysis: "incompact3d" + "paraview" for flow visualization
- Development + Debug: "hermes" + "hermes_api" for I/O optimization

**Prerequisites**: Jarvis configuration must be initialized
**Tools to use after this**: get_package_info() to learn about specific packages

Use this tool when:
- Starting HPC workflow planning ("What can I deploy?")
- Exploring available applications for specific use cases
- Auditing the current package ecosystem
- Looking for alternatives to existing tools"""
)
async def get_all_packages_tool(
    package_type: str = "all",
    repository_filter: Optional[str] = None,
    include_descriptions: bool = True,
    sort_by: str = "priority"
) -> dict:
    """
    Get comprehensive catalog of all available packages in the Jarvis ecosystem.
    
    Args:
        package_type: Filter by type ("all", "service", "application", "interceptor")
        repository_filter: Only show packages from specific repository
        include_descriptions: Include package descriptions and use cases
        sort_by: Sort order ("priority", "name", "type", "popularity")
    
    Returns:
        Comprehensive package catalog with metadata and recommendations
    """
    try:
        result = await get_all_packages(
            package_type=package_type,
            repository_filter=repository_filter,
            include_descriptions=include_descriptions,
            sort_by=sort_by
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_all_packages: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_all_packages: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_package_info",
    description="""Get detailed information about a specific package including README, configuration, capabilities, and more.

This comprehensive tool retrieves extensive details about any package in the Jarvis ecosystem 
including its full description, README documentation, configuration parameters with their types 
and default values, package capabilities and features, output specifications, installation 
instructions, and usage examples.

Use flexible boolean flags to control which information sections are returned. This is essential 
for understanding how to properly configure and use packages in your pipelines, troubleshooting 
package issues, or learning about package functionality before integration.

**Information Extraction Strategy**:
The tool analyzes the user's request and automatically emphasizes the most relevant information 
sections. It combines data from multiple sources:
- Package README files (description, purpose, use cases)
- Configuration schemas (parameters, types, defaults, validation)
- Example configurations and pipeline scripts
- Performance benchmarks and optimization notes
- Dependency analysis and compatibility requirements

**Smart Content Filtering**:
- "What is X?" → Focus on description and use cases
- "What outputs does X generate?" → Emphasize output specifications
- "How do I configure X?" → Highlight configuration parameters
- "What are X's dependencies?" → Focus on requirements and compatibility

**Prerequisites**: Package must exist in registered repositories
**Tools to use before this**: get_all_packages() to discover available package names

Use this tool when:
- Learning about a specific package for the first time
- Understanding package capabilities and limitations
- Planning configuration strategies for specific use cases
- Troubleshooting package-related issues"""
)
async def get_package_info_tool(
    package_name: str,
    return_description: bool = True,
    return_outputs: bool = False,
    return_config_params: bool = False,
    return_examples: bool = False,
    return_dependencies: bool = False,
    return_performance_notes: bool = False,
    summary_level: str = "detailed"
) -> dict:
    """
    Get detailed information about a specific package.
    
    Args:
        package_name: Name of the package to get information about
        return_description: Include package description
        return_outputs: Include information about outputs
        return_config_params: Include configuration parameters
        return_examples: Include usage examples
        return_dependencies: Include dependency information
        return_performance_notes: Include performance characteristics
        summary_level: Detail level ("brief", "detailed", "comprehensive")
    
    Returns:
        Detailed package information based on requested components
    """
    try:
        result = await get_package_info(
            package_name=package_name,
            return_description=return_description,
            return_outputs=return_outputs,
            return_config_params=return_config_params,
            return_examples=return_examples,
            return_dependencies=return_dependencies,
            return_performance_notes=return_performance_notes,
            summary_level=summary_level
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_package_info: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_package_info: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_all_repos",
    description="""Get all currently registered repositories with their status, package counts, and metadata.

This tool provides detailed information about each repository including the repository name, 
file system path, current status (active/inactive), total number of packages available, 
metadata such as maintainer information, and repository health status.

Use this to understand your repository configuration, troubleshoot repository issues, or get 
an overview of your package ecosystem before managing repositories or debugging package availability.

**Repository Priority System**:
Jarvis searches repositories in priority order (1 = highest priority). When multiple repositories 
contain packages with the same name, higher priority repositories take precedence. This system 
allows custom implementations to override built-in packages while maintaining fallback options.

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

**Prerequisites**: Jarvis configuration must be initialized
**Tools to use after this**: modify_repo() to add, remove, or reorder repositories

Use this tool when:
- Understanding current repository configuration
- Debugging package resolution or "package not found" issues
- Planning repository management operations
- Auditing package sources and availability"""
)
async def get_all_repos_tool(
    include_package_counts: bool = True,
    include_health_status: bool = True,
    show_priority_order: bool = True
) -> dict:
    """
    Get comprehensive list of all registered repositories.
    
    Args:
        include_package_counts: Show number and types of packages in each repository
        include_health_status: Include connectivity and accessibility status
        show_priority_order: Display repositories in search priority order
    
    Returns:
        Repository status information with health and package details
    """
    try:
        result = await get_list_repos(
            include_package_counts=include_package_counts,
            include_health_status=include_health_status,
            show_priority_order=show_priority_order
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_all_repos: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_all_repos: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="modify_repo",
    description="""Perform comprehensive repository lifecycle management operations with safety controls.

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

**Repository Structure Requirements** (for add operation):
```
repository_name/
├── repository_name/        # Package namespace directory
│   ├── package1/          # Individual package directories
│   │   └── pkg.py         # Package implementation
│   └── package2/
│       └── pkg.py
└── pipelines/             # Optional: pipeline examples
    ├── example1.yaml
    └── example2.yaml
```

Prerequisites:
- For ADD: Repository path must exist and be properly structured
- For DELETE/PROMOTE: Repository must be currently registered
- User must have write access to Jarvis configuration directory

**Tools to use before this**: get_all_repos() to understand current repository configuration
**Tools to use after this**: get_all_repos() to verify changes took effect

Use this tool when:
- Setting up custom package repositories for organization
- Managing package resolution priority and conflicts
- Cleaning up outdated or unused repositories
- Troubleshooting package availability and version conflicts"""
)
async def modify_repo_tool(
    repo_name: str,
    operation: str,
    repo_path: str = "",
    verify_structure: bool = True,
    backup_config: bool = True
) -> dict:
    """
    Perform comprehensive repository lifecycle management operations.
    
    Args:
        repo_name: Repository identifier (must be unique)
        operation: Management operation ("add", "delete", "promote")
        repo_path: Required for "add" - absolute path to repository directory
        verify_structure: Validate repository structure before operation
        backup_config: Create configuration backup before changes
    
    Returns:
        Operation result with status, impact analysis, and rollback instructions
    """
    try:
        # Convert empty string to None for repo_path
        actual_repo_path = repo_path if repo_path else None
        
        result = await modify_repo(
            repo_name=repo_name,
            operation=operation,
            repo_path=actual_repo_path,
            verify_structure=verify_structure,
            backup_config=backup_config
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in modify_repo: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in modify_repo: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

@mcp.tool(
    name="get_resource_status",
    description="""Provide comprehensive cluster resource information for deployment planning.

This tool exposes the Jarvis resource graph in an intelligent, decision-oriented format that 
helps users understand deployment constraints and optimization opportunities. Rather than raw 
hardware data, it provides actionable insights for HPC workflow planning.

**Resource Analysis Strategy**:
1. Introspects current cluster state via Jarvis resource graph
2. Analyzes resource utilization patterns and availability
3. Provides deployment recommendations based on resource constraints
4. Identifies bottlenecks and optimization opportunities
5. Maps resources to common package requirements

**Resource Information Includes**:
- **Hardware inventory** with deployment-relevant specifications
- **Network topology** with bandwidth and latency characteristics
- **Storage hierarchy** with performance and capacity details
- **Resource availability** and utilization patterns
- **Deployment recommendations** based on current resource state
- **Constraint analysis** for common package types

**Prerequisites**: 
- Jarvis resource graph must be built ('jarvis rg build')
- Hostfile must be configured for multi-node clusters
- Appropriate permissions for hardware introspection

**Tools to use before this**: build_resource_graph() if resource graph is not current
**Tools to use after this**: create_pipeline_composition() with resource-aware package selection

Use this tool when:
- Starting deployment planning for new workflows
- Understanding cluster capabilities and limitations
- Optimizing package placement for performance
- Troubleshooting resource-related deployment failures
- Planning resource allocation for multiple concurrent pipelines"""
)
async def get_resource_status_tool(
    include_hardware: bool = True,
    include_network: bool = True,
    include_storage: bool = True,
    include_utilization: bool = True,
    detail_level: str = "summary"
) -> dict:
    """
    Get comprehensive cluster resource information.
    
    Args:
        include_hardware: CPU, memory, and compute node information
        include_network: Network topology, bandwidth, and fabric details
        include_storage: Storage devices, filesystems, and capacity information
        include_utilization: Current resource usage and availability
        detail_level: Information depth ("summary", "detailed", "comprehensive")
    
    Returns:
        Cluster resource status with hardware, network, and storage details
    """
    try:
        result = await get_resource_status(
            include_hardware=include_hardware,
            include_network=include_network,
            include_storage=include_storage,
            include_utilization=include_utilization,
            detail_level=detail_level
        )
        return result.model_dump()
    except DiscoverabilityError as e:
        logger.error(f"Discoverability error in get_resource_status: {e}")
        return {"error": str(e), "type": "discoverability_error"}
    except Exception as e:
        logger.error(f"Unexpected error in get_resource_status: {e}")
        return {"error": f"Unexpected error: {str(e)}", "type": "internal_error"}

# ═══════════════════════════════════════════════════════════════════════════════
# JARVIS MANAGER CONFIGURATION TOOLS (Essential for Phase 1)
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="jm_create_config",
    description="""Initialize JarvisManager config directories.

This tool sets up the basic Jarvis configuration directories and initializes the manager.
This is typically the first step when setting up Jarvis in a new environment.

Args:
    config_dir: Directory where pipeline metadata is stored
    private_dir: Directory for private files (SSH keys, etc.)
    shared_dir: Directory accessible by all nodes in cluster (optional)

Use this tool when:
- Setting up Jarvis for the first time
- Initializing Jarvis in a new environment
- Resetting Jarvis configuration"""
)
def jm_create_config_tool(config_dir: str, private_dir: str, shared_dir: Optional[str] = None) -> dict:
    """Initialize manager directories and persist configuration."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.create(config_dir, private_dir, shared_dir)
        manager.save()
        return {"status": "success", "message": "Jarvis configuration initialized successfully"}
    except Exception as e:
        logger.error(f"Failed to create Jarvis config: {e}")
        return {"status": "error", "message": f"Failed to initialize configuration: {str(e)}"}

@mcp.tool(
    name="jm_load_config",
    description="""Load existing JarvisManager configuration.

This tool loads the Jarvis configuration from saved state. Use this to restore
a previously configured Jarvis environment.

Use this tool when:
- Loading an existing Jarvis configuration
- Restoring Jarvis state after restart
- Switching between different Jarvis configurations"""
)
def jm_load_config_tool() -> dict:
    """Load manager configuration from saved state."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.load()
        return {"status": "success", "message": "Configuration loaded successfully"}
    except Exception as e:
        logger.error(f"Failed to load Jarvis config: {e}")
        return {"status": "error", "message": f"Failed to load configuration: {str(e)}"}

@mcp.tool(
    name="jm_set_hostfile",
    description="""Set hostfile path for JarvisManager.

This tool configures the hostfile that defines which machines are available
for multi-node deployments. The hostfile is essential for distributed HPC workflows.

Args:
    path: Absolute path to the hostfile

Use this tool when:
- Setting up multi-node deployments
- Configuring cluster resources
- Changing available compute nodes"""
)
def jm_set_hostfile_tool(path: str) -> dict:
    """Set and save the path to the hostfile for deployments."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.set_hostfile(path)
        manager.save()
        return {"status": "success", "message": f"Hostfile set to '{path}'"}
    except Exception as e:
        logger.error(f"Failed to set hostfile: {e}")
        return {"status": "error", "message": f"Failed to set hostfile: {str(e)}"}

@mcp.tool(
    name="jm_graph_build",
    description="""Build or rebuild the resource graph with a net sleep interval.

This tool constructs the Jarvis resource graph by introspecting the cluster hardware,
network, and storage resources. The resource graph is essential for resource-aware
deployment planning and optimization.

Args:
    net_sleep: Sleep interval between network operations (seconds)

Use this tool when:
- Setting up Jarvis for the first time
- Hardware configuration has changed
- Resource graph is outdated or corrupted
- Need updated resource information for deployment planning"""
)
def jm_graph_build_tool(net_sleep: float) -> dict:
    """Construct or rebuild the resource graph with a given sleep delay."""
    try:
        from jarvis_cd.basic.jarvis_manager import JarvisManager
        manager = JarvisManager.get_instance()
        manager.resource_graph_build(net_sleep)
        return {"status": "success", "message": "Resource graph built successfully"}
    except Exception as e:
        logger.error(f"Failed to build resource graph: {e}")
        return {"status": "error", "message": f"Failed to build resource graph: {str(e)}"}

def main():
    """
    Main entry point to start the FastMCP server using the specified transport.
    Chooses between stdio and SSE based on MCP_TRANSPORT environment variable.
    """
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport == "sse":
        host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SSE_PORT", "8000"))
        print(f"Starting Jarvis MCP Phase 1 (Discoverability) on {host}:{port}", file=sys.stderr)
        mcp.run(transport="sse", host=host, port=port)
    else:
        print("Starting Jarvis MCP Phase 1 (Discoverability) with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()