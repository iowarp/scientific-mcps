---
id: mcp-jarvis
title: Jarvis MCP
sidebar_label: Jarvis
description: Jarvis-CD MCP - Pipeline Management for High-Performance Computing with comprehensive workflow operations
keywords: ['jarvis', 'pipeline-management', 'high-performance-computing', 'hpc', 'workflow', 'data-pipelines', 'scientific-computing', 'package-management']
tags: ['jarvis', 'pipeline-management', 'high-performance-computing', 'hpc', 'workflow', 'data-pipelines', 'scientific-computing', 'package-management']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Jarvis MCP

## Overview
Jarvis-CD MCP - Pipeline Management for High-Performance Computing with comprehensive workflow operations

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Jarvis • Pipeline Management • High Performance Computing • Hpc • Workflow • Data Pipelines • Scientific Computing • Package Management
- **Actions**: 29
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)


<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "jarvis-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "jarvis"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

```json
"mcp": {
  "servers": {
    "jarvis-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "jarvis"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add jarvis-mcp -- uvx iowarp-mcps jarvis
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "jarvis-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "jarvis"]
    }
  }
}
```

</details>

<details>
<summary><b>Manual Setup</b></summary>

**Linux/macOS:**
```bash
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Jarvis run jarvis-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Jarvis run jarvis-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Jarvis run jarvis-mcp --help
```

</details>

## Available Actions

### `update_pipeline`

**Description**: Re-apply environment and configuration to every package in a Jarvis pipeline.

**Parameters**: pipeline_id: ID of the pipeline to update

### `build_pipeline_env`

**Description**: Build the pipeline execution environment for a given pipeline.

**Parameters**: pipeline_id: ID of the pipeline to build

### `create_pipeline`

**Description**: Create a new pipeline environment for data-centric workflows.

**Parameters**: pipeline_id: Name/ID for the new pipeline

### `load_pipeline`

**Description**: Load an existing pipeline environment by ID, or the current one if not specified.

**Parameters**: pipeline_id: ID of the pipeline to load

### `get_pkg_config`

**Description**: Retrieve the configuration of a specific package in a pipeline.

**Parameters**: pipeline_id: ID of the pipeline, pkg_id: ID of the package

### `append_pkg`

**Description**: Add a package to a pipeline for execution or analysis.

**Parameters**: pipeline_id: ID of the pipeline, pkg_type: Type of package to add, pkg_id: ID for the new package, do_configure: Whether to configure after adding, extra_args: Additional configuration arguments

### `configure_pkg`

**Description**: Configure a package in a pipeline with new settings.

**Parameters**: pipeline_id: ID of the pipeline, pkg_id: ID of the package, extra_args: Configuration arguments

### `unlink_pkg`

**Description**: Unlink a package from a pipeline without deleting its files.

**Parameters**: pipeline_id: ID of the pipeline, pkg_id: ID of the package to unlink

### `remove_pkg`

**Description**: Remove a package and its files from a pipeline.

**Parameters**: pipeline_id: ID of the pipeline, pkg_id: ID of the package to remove

### `run_pipeline`

**Description**: Execute the pipeline, running all configured steps.

**Parameters**: pipeline_id: ID of the pipeline to run

### `destroy_pipeline`

**Description**: Destroy a pipeline and clean up all associated files and resources.

**Parameters**: pipeline_id: ID of the pipeline to destroy

### `jm_create_config`

**Description**: Initialize manager directories and persist configuration.

**Parameters**: config_dir: Parameter for config_dir, private_dir: Parameter for private_dir, shared_dir: Parameter for shared_dir

### `jm_load_config`

**Description**: Load manager configuration from saved state.

**Parameters**: No parameters

### `jm_save_config`

**Description**: Save current configuration state to disk.

**Parameters**: No parameters

### `jm_set_hostfile`

**Description**: Set and save the path to the hostfile for deployments.

**Parameters**: path: Parameter for path

### `jm_bootstrap_from`

**Description**: Bootstrap configuration based on a predefined machine template.

**Parameters**: machine: Parameter for machine

### `jm_bootstrap_list`

**Description**: List all bootstrap templates available.

**Parameters**: No parameters

### `jm_reset`

**Description**: Reset manager to a clean state by destroying all pipelines and config.

**Parameters**: No parameters

### `jm_list_pipelines`

**Description**: List all current pipelines under management.

**Parameters**: No parameters

### `jm_cd`

**Description**: Set the working pipeline context.

**Parameters**: pipeline_id: Parameter for pipeline_id

### `jm_list_repos`

**Description**: List all registered repositories.

**Parameters**: No parameters

### `jm_add_repo`

**Description**: Add a repository path to the manager.

**Parameters**: path: Parameter for path, force: Parameter for force (default: False)

### `jm_remove_repo`

**Description**: Remove a repository from configuration.

**Parameters**: repo_name: Parameter for repo_name

### `jm_promote_repo`

**Description**: Promote a repository to higher priority.

**Parameters**: repo_name: Parameter for repo_name

### `jm_get_repo`

**Description**: Get detailed information about a repository.

**Parameters**: repo_name: Parameter for repo_name

### `jm_construct_pkg`

**Description**: Generate a new package skeleton by type.

**Parameters**: pkg_type: Parameter for pkg_type

### `jm_graph_show`

**Description**: Print the resource graph to the console.

**Parameters**: No parameters

### `jm_graph_build`

**Description**: Construct or rebuild the graph with a given sleep delay.

**Parameters**: net_sleep: Parameter for net_sleep

### `jm_graph_modify`

**Description**: Modify the current resource graph with a delay between operations.

**Parameters**: net_sleep: Parameter for net_sleep



## Examples

### Pipeline Creation and Basic Management

```
I need to set up a new HPC pipeline called "performance_test" for running performance benchmarks. Initialize the Jarvis configuration, create the pipeline, and add the IOR package to it.
```

**Tools used:**
- **jm_create_config**: Initialize Jarvis configuration directories
- **create_pipeline**: Create new pipeline environment
- **append_pkg**: Add IOR package to the pipeline

### Package Configuration and Environment Setup

```
For the "performance_test" pipeline, configure the IOR package to use 16 processes, then build the pipeline environment and execute it.
```

**Tools used:**
- **get_pkg_config**: Retrieve current IOR package configuration
- **configure_pkg**: Configure IOR package with 16 processes
- **build_pipeline_env**: Build pipeline execution environment
- **run_pipeline**: Execute the configured pipeline

### Repository Management and Package Discovery

```
Show me all available repositories in the system, add a new custom repository at "/path/to/custom/repo", and promote it to higher priority for package resolution.
```

**Tools used:**
- **jm_list_repos**: List all configured repositories
- **jm_add_repo**: Add custom repository to the system
- **jm_promote_repo**: Promote repository to higher priority

### Advanced Pipeline Operations and Package Management

```
Create a comprehensive workflow: list all existing pipelines, load pipeline "data_analysis", show configuration of the "pandas" package, update its memory settings to 32GB, and rebuild the environment.
```

**Tools used:**
- **jm_list_pipelines**: List all existing pipelines
- **load_pipeline**: Load the data_analysis pipeline
- **get_pkg_config**: Show pandas package configuration
- **configure_pkg**: Update memory settings for pandas package
- **update_pipeline**: Re-apply configurations to all packages
- **build_pipeline_env**: Rebuild environment with new settings

### Resource Monitoring and System Management

```
I need to monitor system resources and manage pipeline contexts. Show me the current resource graph, build a new resource graph with 2.0 second intervals, and set "hpc_workflow" as the current working pipeline.
```

**Tools used:**
- **jm_graph_show**: Display current resource graph frames
- **jm_graph_build**: Build resource graph with custom intervals
- **jm_cd**: Change current pipeline context

### Package Lifecycle Management

```
For troubleshooting purposes, I need to unlink the "tensorflow" package from "ml_pipeline" without deleting files, then completely remove the "outdated_tool" package, and finally destroy the "test_pipeline" entirely.
```

**Tools used:**
- **unlink_pkg**: Unlink tensorflow package while preserving files
- **remove_pkg**: Completely remove outdated_tool package
- **destroy_pipeline**: Destroy entire test pipeline and cleanup

### Configuration Management and Bootstrapping

```
Initialize a new Jarvis setup by listing available bootstrap templates, bootstrap from "cluster_template", save the configuration, and create a package skeleton for a "mpi_application" type.
```

**Tools used:**
- **jm_bootstrap_list**: List available bootstrap machine templates
- **jm_bootstrap_from**: Bootstrap configuration from cluster template
- **jm_save_config**: Save current configuration state
- **jm_construct_pkg**: Create MPI application package skeleton

### System Reset and Repository Information

```
I need to perform maintenance on the Jarvis system: get detailed information about the "hpc_tools" repository, then perform a complete system reset to clean state for testing.
```

**Tools used:**
- **jm_get_repo**: Get detailed repository information
- **jm_reset**: Reset entire Jarvis system to clean state

### Advanced Resource Graph Management

```
Set up comprehensive resource monitoring by modifying the resource graph with 1.5 second intervals, then display the updated graph frames for analysis.
```

**Tools used:**
- **jm_graph_modify**: Modify resource graph with custom intervals
- **jm_graph_show**: Display current resource graph frames

### Complete Pipeline Lifecycle with Configuration Management

```
Load my existing configuration, set hostfile to "/etc/hosts.cluster", remove the deprecated "old_repo" repository, and create a comprehensive workflow pipeline.
```

**Tools used:**
- **jm_load_config**: Load existing Jarvis configuration
- **jm_set_hostfile**: Configure hostfile for deployments
- **jm_remove_repo**: Remove deprecated repository
- **create_pipeline**: Create new comprehensive workflow pipeline

