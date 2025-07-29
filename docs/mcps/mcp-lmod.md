---
id: mcp-lmod
title: lmod MCP
sidebar_label: lmod
description: Lmod MCP - Environment Module Management for LLMs with comprehensive module operations
keywords: ['lmod', 'environment-modules', 'module-management', 'hpc', 'scientific-computing', 'supercomputing', 'cluster-computing', 'module-system']
tags: ['lmod', 'environment-modules', 'module-management', 'hpc', 'scientific-computing', 'supercomputing', 'cluster-computing', 'module-system']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# lmod MCP

## Overview
Lmod MCP - Environment Module Management for LLMs with comprehensive module operations

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Lmod • Environment Modules • Module Management • Hpc • Scientific Computing • Supercomputing • Cluster Computing • Module System
- **Actions**: 10
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Lmod system installed and available in PATH
- HPC environment with module system access

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "lmod-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "lmod"]
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
    "lmod-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "lmod"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add lmod-mcp -- uvx iowarp-mcps lmod
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "lmod-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "lmod"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/lmod run lmod-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\lmod run lmod-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\lmod run lmod-mcp --help
```

</details>

## Available Actions

### `module_list`

**Description**: List all currently loaded environment modules with their versions and status information.

**Parameters**: No parameters

### `module_avail`

**Description**: Search for available modules that can be loaded with optional pattern matching and filtering.

**Parameters**: pattern: Search pattern with wildcards (e.g., 'python*', 'gcc/*')

### `module_show`

**Description**: Display comprehensive information about a specific module including dependencies and environment changes.

**Parameters**: module_name: Name of the module (e.g., 'python/3.9.0')

### `module_load`

**Description**: Load one or more environment modules with automatic dependency resolution and conflict detection.

**Parameters**: modules: List of module names to load

### `module_unload`

**Description**: Unload one or more currently loaded modules with dependency checking and cleanup.

**Parameters**: modules: List of module names to unload

### `module_swap`

**Description**: Atomically swap one module for another, handling dependencies and version conflicts automatically.

**Parameters**: old_module: Module to unload, new_module: Module to load in its place

### `module_spider`

**Description**: Search the entire module tree comprehensively with deep hierarchy exploration and metadata extraction.

**Parameters**: pattern: Search pattern for comprehensive module discovery

### `module_save`

**Description**: Save the current set of loaded modules as a named collection for reproducible environments.

**Parameters**: collection_name: Name for the saved collection

### `module_restore`

**Description**: Restore a previously saved module collection with automatic environment configuration.

**Parameters**: collection_name: Name of the collection to restore

### `module_savelist`

**Description**: List all saved module collections with creation dates and module counts.

**Parameters**: No parameters



## Examples

### HPC Development Environment Setup

```
Set up my development environment by loading the latest GCC compiler, Python 3.9, and OpenMPI. Save this configuration as 'dev_env' for future use.
```

**Tools used:**
- **module_avail**: Search for available versions
- **module_load**: Load development tools
- **module_save**: Save configuration as collection

### Scientific Computing Environment

```
I need to switch from Intel compilers to GNU compilers for my simulation. Show me what's currently loaded, find GNU alternatives, and make the switch safely.
```

**Tools used:**
- **module_list**: Show current environment
- **module_avail**: Find GNU compiler alternatives
- **module_swap**: Switch compiler toolchains
- **module_show**: Verify new configuration

### Reproducible Research Environment

```
Create a reproducible environment for my research project by restoring my 'research_v2' module collection and verifying all dependencies are properly loaded.
```

**Tools used:**
- **module_savelist**: List available collections
- **module_restore**: Restore research environment
- **module_list**: Verify loaded modules

### Module Discovery and Analysis

```
I'm looking for machine learning libraries and frameworks. Search the module system comprehensively and show me detailed information about the most relevant options.
```

**Tools used:**
- **module_spider**: Comprehensive module search
- **module_avail**: Search for ML-related modules
- **module_show**: Get detailed module information

### Environment Cleanup and Optimization

```
Clean up my current module environment by unloading unnecessary modules and optimizing for performance computing workflows.
```

**Tools used:**
- **module_list**: Assess current environment
- **module_show**: Analyze module dependencies
- **module_unload**: Remove unnecessary modules

