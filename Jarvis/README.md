
# Jarvis-MCP - Phase 1: Discoverability

*A MCP server for exploring and understanding the Jarvis ecosystem*

---

## Overview

**Jarvis-MCP** is a Python package that implements **Phase 1: Discoverability** tools for the Jarvis Model Context Protocol (MCP) server. This phase focuses on enabling users to explore and understand the Jarvis ecosystem - available packages, repositories, capabilities, and system resources.

With **Jarvis-MCP Phase 1**, you can:

* **Discover Packages**: Get comprehensive catalog of all available packages across repositories
* **Explore Package Details**: Retrieve detailed information about specific packages including configuration, capabilities, and usage examples
* **Manage Repositories**: List, add, remove, and prioritize package repositories
* **Analyze Resources**: Get comprehensive cluster resource information for deployment planning
* **Configure System**: Initialize Jarvis configuration, set hostfiles, and build resource graphs

---

## Prerequisites

- Python 3.10.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)
- Jarvis-CD (optional, for full functionality)

## Phase 1 Tools Implemented

The following discoverability tools are available:

| Tool | Type | Description |
|---|---|---|
| `get_all_packages` | Discovery | Retrieve comprehensive catalog of all available packages from all repositories |
| `get_package_info` | Discovery | Get detailed information about specific packages including README, configuration, and capabilities |
| `get_all_repos` | Repository Management | List all registered repositories with status, package counts, and metadata |
| `modify_repo` | Repository Management | Add, remove, or promote repositories with safety controls |
| `get_resource_status` | Resource Planning | Provide cluster resource information for deployment planning |
| `jm_create_config` | Configuration | Initialize JarvisManager configuration directories |
| `jm_load_config` | Configuration | Load existing JarvisManager configuration |
| `jm_set_hostfile` | Configuration | Set hostfile path for multi-node deployments |
| `jm_graph_build` | Configuration | Build or rebuild the resource graph |

## Setup

### Method 1: Direct UV Run (Recommended for Development)
```bash
# From the Jarvis directory
uv run jarvis-mcp
```
This will create a `.venv/` folder, install all required packages, and run the server directly.

### Method 2: Installation and CLI
```bash
# Install in development mode
uv pip install -e .

# Run the server
jarvis-mcp
```

### Method 3: Python Module Execution
```bash
# Run with stdio transport (default)
python -m jarvis_mcp.server

# Run with SSE transport
MCP_TRANSPORT=sse python -m jarvis_mcp.server
```

--- 

## Running the Server with different types of Clients:

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
    For quick setup with Gemini, see our [Quick Start Guide](docs/basic_install.md).
    
    
    For detailed setup with local LLMs and other providers, see the [Complete Installation Guide](../bin/docs/Installation.md).

### Running the Server on Claude Command Line Interface Tool

1. Install the Claude Code using NPM:
```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp jarvis -- uv --directory ~/scientific-mcps/Jarvis run jarvis-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"jarvis-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/scientific-mcps/Jarvis",
        "run",
        "jarvis-mcp"
    ]
}
```

---

## Phase 1 Operations and Usage Examples

##### 1. **Initialize Jarvis Configuration**

The first step is to initialize Jarvis configuration directories. This prepares the system for interaction.

```bash
# Query to initialize Jarvis
Query: Initialize Jarvis configuration with config dir './config', private dir './private', and shared dir './shared'
```

**Example Usage:**
```python
# Initialize configuration
await jm_create_config(
    config_dir="./config",
    private_dir="./private", 
    shared_dir="./shared"
)
```

---

##### 2. **Discover Available Packages**

Explore the complete catalog of available packages across all repositories.

```bash
# Query to get all packages
Query: What packages are available in the Jarvis ecosystem?
```

**Example Usage:**
```python
# Get all packages
catalog = await get_all_packages()

# Filter by package type
applications = await get_all_packages(package_type="application")

# Sort by popularity
popular = await get_all_packages(sort_by="popularity")
```

---

##### 3. **Get Detailed Package Information**

Learn about specific packages including their configuration parameters and capabilities.

```bash
# Query to get package details
Query: What is the Incompact3D package and how do I configure it?
```

**Example Usage:**
```python
# Get basic package info
info = await get_package_info("incompact3d")

# Get configuration parameters
config_info = await get_package_info(
    "incompact3d",
    return_config_params=True,
    return_examples=True
)
```

---

##### 4. **Manage Package Repositories**

List, add, or manage package repositories in the system.

```bash
# Query to list repositories
Query: What repositories are currently configured?
```

**Example Usage:**
```python
# List all repositories
repos = await get_all_repos()

# Add a new repository
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
```

---

##### 5. **Analyze Cluster Resources**

Get comprehensive information about available cluster resources for deployment planning.

```bash
# Query to get resource status
Query: What resources are available on this cluster?
```

**Example Usage:**
```python
# Get complete resource status
resources = await get_resource_status()

# Focus on hardware information
hardware = await get_resource_status(
    include_network=False,
    include_storage=False,
    detail_level="comprehensive"
)
```

---

##### 6. **Build Resource Graph**

Build the resource graph for resource-aware deployment planning.

```bash
# Query to build resource graph
Query: Build the resource graph for the cluster
```

**Example Usage:**
```python
# Build resource graph
await jm_graph_build(net_sleep=1.0)
```

---

## Testing

Run the comprehensive Phase 1 test suite:

```bash
# From the Jarvis directory
python test_phase1.py
```

The test suite verifies:
- ✅ Model imports and functionality
- ✅ Discoverability function availability
- ✅ Server structure and tool registration
- ✅ Pydantic model serialization

## Implementation Status

**Current Phase**: ✅ **Phase 1 (Discoverability)** - Complete and Tested

**Implemented Tools**:
- ✅ Package Discovery (`get_all_packages`)
- ✅ Package Information (`get_package_info`)
- ✅ Repository Management (`get_all_repos`, `modify_repo`)
- ✅ Resource Planning (`get_resource_status`)
- ✅ Configuration Management (`jm_*` tools)

**Next Phases**:
- **Phase 2: Composition** - Intelligent workflow design and package combination
- **Phase 3: Configuration** - Parameter optimization and performance tuning
- **Phase 4: Deployment** - Execution management and monitoring

## Documentation

For detailed documentation about the Phase 1 implementation:
- [PHASE1_README.md](./PHASE1_README.md) - Complete Phase 1 documentation


## Notes

* Ensure your environment is set up with Python 3.12+
* Jarvis-CD is optional but recommended for full functionality
* Use `uv pip install -e .` to enable development mode
* The server supports both stdio and SSE transports
* Phase 1 focuses on discoverability - pipeline creation and execution will be available in future phases
