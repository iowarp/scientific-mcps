# Jarvis MCP - Phase 1: Discoverability Implementation

## Overview

This document describes the first phase implementation of the Jarvis Model Context Protocol (MCP) server, focusing on **Discoverability** tools that enable users to explore and understand the Jarvis ecosystem.

## Design Philosophy

Following MCP best practices from the comprehensive design document, this implementation uses a **workflow-first approach** rather than direct API mapping. The tools are designed to solve complete user problems and provide intelligent, contextual assistance for HPC workflow planning.

## Phase 1: Discoverability Tools

The discoverability phase provides five core tools that enable users to explore and understand the Jarvis ecosystem:

### 🔍 Core Tools

#### 1. `get_all_packages`
**Purpose**: Retrieve comprehensive catalog of all available packages in the Jarvis ecosystem.

**Key Features**:
- Scans all registered repositories in priority order
- Categorizes packages by type (service, application, interceptor)
- Provides relevance scoring based on usage patterns
- Identifies package relationships and common combinations
- Generates quick-start recommendations

**Usage Example**:
```python
# Get all packages
catalog = await get_all_packages()

# Filter by type
applications = await get_all_packages(package_type="application")

# Sort by popularity
popular = await get_all_packages(sort_by="popularity")
```

#### 2. `get_package_info`
**Purpose**: Retrieve detailed information about specific packages with intelligent filtering.

**Key Features**:
- Smart content filtering based on user intent
- Configuration parameter extraction with detailed explanations
- Output specifications and usage examples
- Performance characteristics and optimization guidance
- Related package suggestions

**Usage Example**:
```python
# Basic package info
info = await get_package_info("incompact3d")

# Configuration-focused query
config_info = await get_package_info(
    "incompact3d", 
    return_config_params=True,
    return_examples=True
)

# Output-focused query
output_info = await get_package_info(
    "incompact3d",
    return_outputs=True,
    return_performance_notes=True
)
```

#### 3. `get_all_repos`
**Purpose**: List all registered repositories with comprehensive status information.

**Key Features**:
- Repository priority system explanation
- Health status indicators (active, warning, error)
- Package inventory with counts and featured packages
- Repository types (builtin, custom, development)

**Usage Example**:
```python
# Full repository status
repos = await get_all_repos()

# Basic repository list
simple_repos = await get_all_repos(
    include_package_counts=False,
    include_health_status=False
)
```

#### 4. `modify_repo`
**Purpose**: Comprehensive repository lifecycle management with safety controls.

**Key Features**:
- ADD: Register new repositories with validation
- DELETE: Safely remove repositories with impact analysis
- PROMOTE: Elevate repository priority with conflict resolution
- Safety features: structure validation, dependency analysis, rollback support

**Usage Example**:
```python
# Add new repository
result = await modify_repo(
    repo_name="myorg_tools",
    operation="add",
    repo_path="/path/to/myorg_tools"
)

# Promote repository to highest priority
result = await modify_repo(
    repo_name="myorg_tools",
    operation="promote"
)

# Remove repository
result = await modify_repo(
    repo_name="old_repo",
    operation="delete"
)
```

#### 5. `get_resource_status`
**Purpose**: Provide comprehensive cluster resource information for deployment planning.

**Key Features**:
- Hardware inventory with deployment-relevant specifications
- Network topology with bandwidth and latency characteristics
- Storage hierarchy with performance and capacity details
- Deployment recommendations based on resource constraints
- Optimization opportunities identification

**Usage Example**:
```python
# Complete resource status
resources = await get_resource_status()

# Hardware-focused analysis
hardware = await get_resource_status(
    include_network=False,
    include_storage=False,
    detail_level="comprehensive"
)
```

### 🛠️ Configuration Tools

Essential Jarvis Manager configuration tools for Phase 1:

#### `jm_create_config`
Initialize Jarvis configuration directories.

#### `jm_load_config`
Load existing Jarvis configuration.

#### `jm_set_hostfile`
Configure hostfile for multi-node deployments.

#### `jm_graph_build`
Build resource graph for deployment planning.

## Architecture

### Data Models

All tools use Pydantic models for type-safe, structured responses:

- **PackageCatalog**: Comprehensive package listings with metadata
- **PackageInformation**: Detailed package information with filtering
- **RepositoryStatus**: Repository health and configuration data
- **RepositoryOperationResult**: Repository management operation results
- **ClusterResourceStatus**: Resource information for deployment planning

### Error Handling

Comprehensive error handling with specific guidance:

```python
class DiscoverabilityError(Exception):
    """Custom exception for discoverability-related errors"""
    pass

def handle_mcp_errors(func):
    """Decorator to handle errors and convert to appropriate MCP responses"""
    # Provides specific guidance based on error type
    # Converts Jarvis errors to MCP-compatible responses
```

### Optional Dependencies

The implementation gracefully handles missing Jarvis components:

```python
# Jarvis components are optional dependencies
try:
    from jarvis_cd.basic.jarvis_manager import JarvisManager
    JARVIS_MANAGER_AVAILABLE = True
except ImportError:
    JARVIS_MANAGER_AVAILABLE = False
```

## Installation and Setup

### Prerequisites

1. **Python 3.8+** with pip
2. **Pydantic 2.0+** for data models
3. **FastMCP** for MCP server implementation
4. **Jarvis-CD** (optional, for full functionality)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Jarvis-CD (optional):
```bash
pip install jarvis-cd
```

### Running the Server

```bash
# Run with stdio transport (default)
python -m jarvis_mcp.server

# Run with SSE transport
MCP_TRANSPORT=sse python -m jarvis_mcp.server

# Run with custom host/port
MCP_TRANSPORT=sse MCP_SSE_HOST=localhost MCP_SSE_PORT=8080 python -m jarvis_mcp.server
```

## Testing

Run the comprehensive test suite:

```bash
python test_phase1.py
```

The test suite verifies:
- ✅ Model imports and functionality
- ✅ Discoverability function availability
- ✅ Server structure and tool registration
- ✅ Pydantic model serialization

## User Query Patterns

Phase 1 tools are designed to handle these common user queries:

### Discovery Queries
- "What packages are available?"
- "What can I deploy with Jarvis?"
- "Show me all storage-related packages"
- "What are the most popular packages?"

### Package Information Queries
- "What is the Incompact3D package?"
- "What outputs does Incompact3D generate?"
- "How do I configure Incompact3D?"
- "What are Incompact3D's dependencies?"

### Repository Management Queries
- "What repositories are currently configured?"
- "Add my organization's package repository"
- "Which repository has the highest priority?"
- "Remove the outdated experimental repository"

### Resource Planning Queries
- "What resources are available on this cluster?"
- "What are the hardware specifications?"
- "Is the resource graph built?"
- "What are the deployment constraints?"

## MCP Best Practices Implemented

### 1. Workflow-First Design
Tools solve complete user problems rather than exposing individual CLI commands.

### 2. Comprehensive Documentation
Each tool includes extensive docstrings with:
- Prerequisites and failure scenarios
- Related tools and workflow guidance
- Usage examples and common patterns
- Decision-making logic and recommendations

### 3. Intelligent Decision Support
Tools provide guidance and recommendations:
- Package selection guidance by type
- Common package combinations
- Quick-start recommendations
- Resource optimization suggestions

### 4. Structured Output
Type-safe Pydantic models ensure consistent, actionable responses.

### 5. Context Awareness
Tools understand their role in larger workflows and provide appropriate guidance.

### 6. Error Handling Excellence
Comprehensive error handling with specific resolution guidance.

## Future Phases

This Phase 1 implementation provides the foundation for:

- **Phase 2: Composition** - Intelligent workflow design and package combination
- **Phase 3: Configuration** - Parameter optimization and performance tuning
- **Phase 4: Deployment** - Execution management and monitoring

## Contributing

When extending or modifying Phase 1 tools:

1. Follow the workflow-first design philosophy
2. Provide comprehensive docstrings with all guidance sections
3. Use Pydantic models for structured responses
4. Handle errors gracefully with specific guidance
5. Add appropriate tests to the test suite

## License

This implementation follows the same license as the Jarvis-CD project.

---

**Phase 1 Status**: ✅ Complete and Tested
**Next Phase**: Phase 2 (Composition) - Intelligent workflow design tools 