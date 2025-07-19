# Jarvis MCP Server

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive Model Context Protocol (MCP) server for the Jarvis HPC ecosystem. This server provides intelligent package discovery, repository management, and resource analysis capabilities through the Model Context Protocol, enabling users to explore the Jarvis ecosystem, manage HPC packages, and plan deployments with **intelligent analysis**, **beautiful output formatting**, and **workflow-first approach**.

## Key Features

### 🔧 **Five Specialized Tools**
Following MCP best practices, this server provides intelligent, contextual assistance for HPC package management and cluster resource planning:

- **`get_all_packages`**: Comprehensive package discovery across all repositories with intelligent categorization
- **`get_package_info`**: Detailed package information including configuration parameters and capabilities  
- **`get_all_repos`**: Repository management with health status and priority ordering
- **`modify_repo`**: Safe repository lifecycle management with validation and rollback
- **`get_resource_status`**: Cluster resource analysis for deployment planning

### 🚀 **Workflow-First Design**
- **Intelligent Package Discovery**: AI-powered package recommendations and common workflow combinations
- **Advanced Repository Management**: Sophisticated repository prioritization with conflict resolution
- **Resource-Aware Planning**: Comprehensive cluster analysis with deployment constraints and optimization
- **Configuration Management**: Jarvis Manager integration for seamless system configuration

### 🎨 **Beautiful Output Formatting**
- **Structured Layout**: Rich formatting with comprehensive summaries and visual indicators
- **Comprehensive Insights**: Actionable recommendations for package selection and deployment
- **Metadata Tracking**: Detailed operation metadata and performance metrics
- **Error Handling**: Helpful error messages with troubleshooting suggestions

### 🌐 **Complete HPC Ecosystem Coverage**
- **Package Discovery**: Comprehensive package catalog with type classification and popularity scoring
- **Repository Management**: Health monitoring, priority management, and conflict resolution
- **Resource Analysis**: Hardware inventory, network topology, and deployment constraint analysis
- **Configuration Management**: Jarvis Manager integration with configuration validation
- **Workflow Planning**: Intelligent package combinations and deployment optimization

### 🔒 **Enterprise Security**
- **Configuration Validation**: Safe repository management with rollback capabilities
- **Permission Management**: Minimal privilege access with comprehensive audit trails
- **Dependency Analysis**: Package dependency tracking and conflict detection
- **Version Management**: Package versioning and compatibility analysis

## Capabilities

### Primary Tools

#### **1. `get_all_packages` - Package Discovery**

**Comprehensive package discovery across all Jarvis repositories with intelligent categorization.**

This powerful tool provides complete package ecosystem visibility by scanning all registered repositories and providing intelligent categorization, filtering, and recommendations.

**Key Features:**
- **Repository Scanning**: Automatically discovers packages across all registered repositories
- **Intelligent Categorization**: Classifies packages by type (service, application, interceptor)
- **Smart Filtering**: Apply sophisticated filtering by type, repository, or popularity
- **Package Relationships**: Identifies common package combinations and workflows
- **Usage Analytics**: Popularity scoring based on common usage patterns

#### **2. `get_package_info` - Package Details**

**Detailed package information including configuration parameters, capabilities, and usage examples.**

This comprehensive tool retrieves extensive package details by analyzing README files, configuration schemas, and dependency information.

**Key Features:**
- **Configuration Analysis**: Detailed parameter information with types and defaults
- **Capability Discovery**: Package features and supported operations
- **Documentation Extraction**: README content and usage examples
- **Dependency Mapping**: Package dependencies and compatibility requirements
- **Performance Insights**: Performance characteristics and optimization notes

#### **3. `get_all_repos` - Repository Management**

**Repository management with health status, priority ordering, and package inventory.**

This tool provides comprehensive repository management capabilities with health monitoring and priority configuration.

**Key Features:**
- **Health Monitoring**: Repository accessibility and status verification
- **Priority Management**: Repository search order and conflict resolution
- **Package Inventory**: Package counts and featured package listings
- **Status Tracking**: Last update times and error condition monitoring
- **Type Classification**: Built-in vs custom repository identification

#### **4. `modify_repo` - Repository Lifecycle**

**Safe repository lifecycle management with validation, backup, and rollback capabilities.**

This enterprise-grade tool handles repository add/remove/promote operations with comprehensive safety controls.

**Key Features:**
- **Structure Validation**: Repository format and compatibility verification
- **Conflict Detection**: Package name conflicts and shadowing analysis
- **Backup Management**: Configuration backup before destructive operations
- **Impact Analysis**: Dependency analysis and affected pipeline identification
- **Rollback Support**: Complete rollback instructions for failed operations

#### **5. `get_resource_status` - Resource Analysis**

**Cluster resource analysis for deployment planning and optimization.**

This intelligent tool provides comprehensive cluster resource information through Jarvis resource graph integration.

**Key Features:**
- **Hardware Inventory**: CPU, memory, storage, and network analysis
- **Resource Utilization**: Current usage patterns and availability
- **Deployment Constraints**: Resource requirements and compatibility analysis
- **Optimization Recommendations**: Performance tuning and resource allocation guidance
- **Bottleneck Identification**: Resource limitations and scaling recommendations

### Configuration Tools

- **`jm_create_config`**: Initialize Jarvis Manager configuration directories
- **`jm_load_config`**: Load existing Jarvis Manager configuration
- **`jm_set_hostfile`**: Configure hostfile for multi-node deployments
- **`jm_graph_build`**: Build or rebuild the resource graph

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)
- Jarvis-CD (optional, for full functionality)

## Installation and Setup

### Quick Start
```bash
# Navigate to Jarvis directory
cd /path/to/scientific-mcps/Jarvis

# Install and run with UV (recommended)
uv sync && uv run jarvis-mcp
```

### Installation Methods

#### Method 1: UV Package Manager (Recommended)
```bash
# Install dependencies
uv sync

# Run the server
uv run jarvis-mcp
```

#### Method 2: Traditional pip
```bash
# Install in development mode
pip install -e .

# Run the server directly
cd src && python server.py
```

#### Method 3: Direct Execution
```bash
# Run without installation (creates .venv automatically)
uv run jarvis-mcp

# Or run server directly from source
cd src && python server.py
```

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Jarvis MCP server, use the main `wrp.py` client. You will need to configure it to point to the Jarvis server.

1.  **Configure:** Ensure that `Jarvis` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Jarvis
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```

### Running the Server with Claude Desktop
Add to your Claude Desktop `settings.json`:
```json
{
  "mcpServers": {
    "jarvis-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/scientific-mcps/Jarvis",
        "run", 
        "jarvis-mcp"
      ]
    }
  }
}
```

### **Claude CLI Integration**
```bash
claude add mcp jarvis -- uv --directory ~/path/to/scientific-mcps/Jarvis run jarvis-mcp
```

### Example Output Structure

```json
{
  "🤖 Operation": "Get All Packages",
  "✅ Status": "Success",
  "⏰ Timestamp": "2024-01-01 12:00:00",
  "📦 Jarvis Data": {
    "📦 Packages": [
      {
        "📦 Package Name": "incompact3d",
        "🏷️ Package Type": "application",
        "🗂️ Repository": "builtin",
        "📝 Description": "High-performance CFD solver for incompressible flows",
        "⭐ Capabilities": ["simulation", "parallel", "mpi"],
        "📊 Popularity Score": 0.8
      },
      {
        "📦 Package Name": "ior",
        "🏷️ Package Type": "application", 
        "🗂️ Repository": "builtin",
        "📝 Description": "Parallel I/O benchmark for HPC storage systems",
        "⭐ Capabilities": ["benchmark", "io", "parallel"],
        "📊 Popularity Score": 0.9
      }
    ],
    "🔗 Common Combinations": {
      "🔗 Storage Benchmark": ["ior", "orangefs"],
      "🔗 Simulation Analysis": ["incompact3d", "paraview"]
    },
    "🎯 Quick Start Recommendations": [
      "Try storage performance testing: orangefs + ior",
      "Start with CFD simulation: incompact3d package"
    ]
  },
  "📊 Summary": {
    "📈 Total Packages": 25,
    "🗂️ Repositories": 3,
    "🏷️ Package Type Filter": "all",
    "📊 Sort By": "priority"
  },
  "🔍 Metadata": {
    "🔍 Filters Applied": false,
    "✅ Has Recommendations": true
  },
  "💡 Insights": [
    "✅ Found 25 packages across 3 repositories",
    "🎯 Try storage performance testing: orangefs + ior",
    "🚀 Start with CFD simulation: incompact3d package"
  ]
}
```

### Package Information Example Output

```json
{
  "🤖 Operation": "Get Package Info",
  "✅ Status": "Success", 
  "⏰ Timestamp": "2024-01-01 12:00:00",
  "📦 Jarvis Data": {
    "📦 Package Name": "incompact3d",
    "🏷️ Package Type": "application",
    "🗂️ Repository": "builtin",
    "📝 Description": "High-performance CFD solver for incompressible flows using finite differences",
    "⚙️ Configuration Parameters": {
      "⚙️ Mesh Resolution": {
        "🏷️ Type": "integer",
        "📋 Default": 256,
        "📝 Description": "Grid resolution for simulation domain"
      },
      "⚙️ Time Steps": {
        "🏷️ Type": "integer", 
        "📋 Default": 1000,
        "📝 Description": "Number of simulation time steps"
      }
    },
    "⭐ Capabilities": ["mpi", "openmp", "gpu", "checkpoint"],
    "🔗 Related Packages": ["paraview", "hdf5", "mpi"]
  },
  "📊 Summary": {
    "📦 Package Name": "incompact3d",
    "🏷️ Package Type": "application",
    "🗂️ Repository": "builtin",
    "✅ Has Config Params": true,
    "💡 Has Examples": false,
    "🔗 Dependencies Count": 3
  },
  "💡 Insights": [
    "🚀 Package 'incompact3d' is a application from builtin repository",
    "⚙️ Has 2 configuration parameters",
    "🔗 Related packages: paraview, hdf5, mpi"
  ]
}
```

## Usage Examples

### Package Discovery (`get_all_packages`)

```python
# Get all packages with comprehensive analysis
get_all_packages()

# Get only application packages
get_all_packages(package_type="application")

# Filter by specific repository
get_all_packages(repository_filter="custom_repo")

# Sort by popularity
get_all_packages(sort_by="popularity")

# Get packages with descriptions
get_all_packages(include_descriptions=True, sort_by="name")
```

### Package Information (`get_package_info`)

```python
# Get basic package information
get_package_info("incompact3d")

# Get detailed configuration information
get_package_info(
    "incompact3d",
    return_config_params=True,
    return_examples=True,
    return_dependencies=True
)

# Get comprehensive package analysis
get_package_info(
    "ior",
    return_description=True,
    return_outputs=True,
    return_performance_notes=True,
    summary_level="comprehensive"
)

# Focus on specific aspects
get_package_info(
    "paraview",
    return_config_params=True,
    return_examples=True
)
```

### Repository Management (`get_all_repos`, `modify_repo`)

```python
# List all repositories with health status
get_all_repos(include_health_status=True, include_package_counts=True)

# Get repository priority order
get_all_repos(show_priority_order=True)

# Add a new repository
modify_repo(
    repo_name="custom_tools",
    operation="add",
    repo_path="/path/to/custom_tools"
)

# Promote repository to highest priority
modify_repo(
    repo_name="custom_tools", 
    operation="promote"
)

# Remove repository with safety checks
modify_repo(
    repo_name="old_repo",
    operation="delete",
    backup_config=True
)
```

### Resource Analysis (`get_resource_status`)

```python
# Get comprehensive resource status
get_resource_status()

# Focus on specific resource types
get_resource_status(
    include_hardware=True,
    include_network=False,
    include_storage=True
)

# Detailed resource analysis
get_resource_status(
    detail_level="comprehensive",
    include_utilization=True
)

# Quick resource overview
get_resource_status(detail_level="summary")
```

### Configuration Management

```python
# Initialize Jarvis configuration
jm_create_config(
    config_dir="./config",
    private_dir="./private",
    shared_dir="./shared"
)

# Load existing configuration
jm_load_config()

# Set hostfile for multi-node deployments
jm_set_hostfile("/path/to/hostfile")

# Build resource graph
jm_graph_build(net_sleep=1.0)
```

### Jarvis Configuration

For Jarvis functionality, ensure:

1. **Jarvis-CD Installation**: Install jarvis-cd for full functionality
2. **Configuration**: Initialize Jarvis configuration with `jm_create_config`
3. **Resource Graph**: Build resource graph with `jm_graph_build` for resource analysis
4. **Hostfile**: Configure hostfile for multi-node deployments


### Development Guidelines

```bash
# Format code
uv run black src tests

# Sort imports
uv run isort src tests

# Type checking
uv run mypy src

# Linting
uv run ruff check src tests
```

### Running the Server Standalone
For testing and development:

```bash
# Start the server (recommended)
uv run jarvis-mcp

# Alternative method - run server directly
cd src && python server.py
```

## Error Handling and Troubleshooting

The server provides comprehensive error handling with:

- **Detailed Error Messages**: Clear descriptions of what went wrong
- **Error Classifications**: Categorized error types for better understanding
- **Suggestions**: Actionable recommendations for resolving issues
- **Graceful Degradation**: Partial results when some components fail
- **Intelligent Troubleshooting**: Context-aware troubleshooting guidance

### Common Issues and Solutions:

1. **Jarvis-CD Not Available**:
   - Install jarvis-cd: `pip install jarvis-cd`
   - Initialize configuration with `jm_create_config`
   - Verify installation with available tools

2. **Repository Access Errors**:
   - Check repository paths are accessible
   - Verify file system permissions
   - Use `get_all_repos` to check repository health

3. **Configuration Issues**:
   - Initialize Jarvis with `jm_create_config`
   - Load existing config with `jm_load_config`
   - Check configuration file permissions

4. **Resource Graph Errors**:
   - Build resource graph with `jm_graph_build`
   - Ensure system permissions for hardware access
   - Check hostfile configuration for multi-node setups

## Testing

```bash
# Run all tests
pytest tests/ -v
uv run pytest tests/ -v

# Run quick test
python tests/quick_test.py
```

## Performance Considerations

- **Package Operations**: Typically complete in under 2 seconds with intelligent caching
- **Repository Management**: Depend on repository size and network access
- **Resource Analysis**: Requires resource graph build for optimal performance
- **Intelligent Filtering**: Significantly reduces response time for focused queries
- **Configuration Caching**: Smart caching for frequently accessed configuration

## Security Notes

- **Repository Management**: Use validation and backup features for safe operations
- **Configuration**: Store sensitive configuration in secure directories
- **Permissions**: Run with minimal required privileges
- **Audit Trails**: Built-in logging for repository and configuration changes

## Architecture

### Project Structure
```
Jarvis/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── server.py                # Main MCP server with tools and entry point
│   └── implementation/          # Core implementation modules
│       ├── __init__.py
│       ├── output_formatter.py  # Beautiful response formatting
│       ├── discoverability.py   # Package and repository discovery
│       └── models.py            # Pydantic data models
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Test configuration
│   ├── quick_test.py            # Quick integration test
│   ├── run_all_tests.py         # Test runner
│   ├── test_discoverability.py  # Discovery tests
│   ├── test_imports.py          # Import validation tests
│   ├── test_integration.py      # Integration tests
│   └── test_server.py           # Server tests
├── docs/                        # Documentation and guides
│   ├── GUIDE.md                 # Usage guide
│   ├── PHASE1_README.md         # Phase 1 documentation
│   ├── basic_install.md         # Installation guide
│   └── assets/                  # Screenshots and assets
├── pyproject.toml               # Project configuration
├── pytest.ini                  # Test configuration
└── README.md                    # This file
```

### Architecture Design

This implementation follows a **clean, direct architecture** that eliminates unnecessary complexity:

- **Direct FastMCP Integration**: Tools are defined directly in `server.py` using FastMCP decorators, eliminating the need for wrapper handlers
- **Standard Python Entry Point**: Uses the standard `if __name__ == "__main__"` pattern in `server.py` instead of a separate `__main__.py` file
- **Streamlined Dependencies**: Removed intermediate handler layers for better performance and maintainability
- **Single Responsibility**: Each module has a clear, focused purpose without redundant abstraction layers

**Benefits of This Design:**
- **Simpler Maintenance**: Fewer files and layers to manage
- **Better Performance**: Direct function calls without handler indirection
- **Standard Practices**: Follows Python packaging conventions
- **Easier Testing**: Direct access to tool functions for comprehensive testing
- **Cleaner Imports**: Straightforward import structure without complex path manipulation

### Design Philosophy

Following MCP best practices, this server implements:

1. **Workflow-First Approach**: Tools designed for real-world HPC package management workflows
2. **Intelligent Analysis**: AI-powered insights and package recommendations  
3. **Beautiful Formatting**: Structured, readable output with comprehensive metadata
4. **Enterprise Security**: Safe repository management with validation and rollback
5. **Performance Optimization**: Efficient discovery with intelligent caching and filtering

### Available Tools

The server provides 9 specialized tools:

**Discovery Tools:**
- `get_all_packages` - Comprehensive package discovery
- `get_package_info` - Detailed package information
- `get_all_repos` - Repository management and health
- `modify_repo` - Safe repository lifecycle operations
- `get_resource_status` - Cluster resource analysis

**Configuration Tools:**
- `jm_create_config` - Initialize Jarvis configuration
- `jm_load_config` - Load existing configuration
- `jm_set_hostfile` - Configure multi-node hostfile
- `jm_graph_build` - Build resource graph

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`uv sync --dev`)
4. Make your changes following the existing patterns
5. Add tests for new functionality
6. Run tests and ensure they pass (`uv run pytest`)
7. Run formatting and linting (`uv run black . && uv run ruff check .`)
8. Commit your changes (`git commit -m 'Add amazing feature'`)
9. Push to the branch (`git push origin feature/amazing-feature`)
10. Submit a pull request

### Development Guidelines

- Follow the existing code style and patterns
- Add comprehensive tests for new features
- Update documentation for any API changes
- Use type hints for better code clarity
- Follow the workflow-first design philosophy

## License

MIT License - This project is part of the Scientific MCPs collection.

---

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Follow the contributing guidelines
- Ensure all tests pass before submitting PRs

**Part of the IoWarp Scientific MCPs Collection** 🔬
