---
id: mcp-adios
title: Adios MCP
sidebar_label: Adios
description: Fetch and analyze BP5 data files using ADIOS2. Access scientific data, metadata, and attributes for research and analysis purposes.
keywords: ['adios2', 'bp5', 'scientific data', 'data access', 'variable inspection', 'attribute extraction']
tags: ['adios2', 'bp5', 'scientific data', 'data access', 'variable inspection', 'attribute extraction']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Adios MCP

## Overview
Fetch and analyze BP5 data files using ADIOS2. Access scientific data, metadata, and attributes for research and analysis purposes.

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Adios2 • Bp5 • Scientific Data • Data Access • Variable Inspection • Attribute Extraction
- **Actions**: 5
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Linux/macOS environment (Windows supported)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "adios-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "adios"]
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
    "adios-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "adios"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add adios-mcp -- uvx iowarp-mcps adios
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "adios-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "adios"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Adios run adios-mcp --help
```
 
**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Adios run adios-mcp --help
```
 
**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Adios run adios-mcp --help
```

</details>

## Available Actions

### `list_bp5`

**Description**: List all BP5 files in a specified directory with comprehensive file information including metadata and structure details.

**Parameters**: directory: Absolute path to directory containing BP5 files

### `inspect_variables`

**Description**: Inspect all variables in a BP5 file including type information, shape dimensions, and available time steps for comprehensive data structure analysis. If variable_name is provided, returns data for that specific variable.

**Parameters**: filename: Absolute path to BP5 file, variable_name: Specific variable name for targeted inspection

### `inspect_variables_at_step`

**Description**: Inspect a specific variable at a given step in a BP5 file. Shows variable type, shape, and metadata at the specified time step.

**Parameters**: filename: Absolute path to BP5 file, variable_name: Name of the variable to inspect, step: Step number to inspect

### `inspect_attributes`

**Description**: Read global or variable-specific attributes from a BP5 file with detailed metadata extraction and attribute value analysis.

**Parameters**: filename: Absolute path to BP5 file, variable_name: Specific variable name for targeted attribute inspection

### `read_variable_at_step`

**Description**: Read a named variable at a specific time step from a BP5 file with full data extraction and conversion to Python native types.

**Parameters**: filename: Absolute path to BP5 file, variable_name: Name of variable to read, target_step: Time step number to read from



## Examples

### Scientific Data Structure Analysis

```
I have a BP5 simulation file at /data/simulation_results.bp. Can you first analyze the data structure and then show me the temperature variable evolution over time?
```

**Tools used:**
- **inspect_variables**: Analyze the dataset structure and available variables
- **read_variable_at_step**: Read temperature data at specific time steps

### Multi-Variable Scientific Analysis

```
Using the file /data/fluid_dynamics.bp, perform a comprehensive analysis showing:
1. All available variables and their properties
2. Pressure field at step 50
3. Variable metadata and attributes for the pressure field
```

**Tools used:**
- **inspect_variables**: List all available variables and properties
- **read_variable_at_step**: Extract pressure field at step 50
- **inspect_attributes**: Get pressure variable metadata

### Time-Series Variable Inspection

```
From /data/climate_model.bp, I want to understand the temperature variable structure across different time steps and inspect its properties at step 25.
```

**Tools used:**
- **inspect_variables**: Get temperature variable structure and available steps
- **inspect_variables_at_step**: Detailed inspection at step 25

### High-Performance Computing Data Analysis

```
Analyze the simulation output at /data/parallel_computation.bp - show me the variable structure, read specific computational domain data, and extract metadata attributes.
```

**Tools used:**
- **inspect_variables**: Analyze computational variables and structure
- **inspect_attributes**: Extract simulation metadata and parameters
- **read_variable_at_step**: Read domain-specific data

### Scientific Data Validation and Exploration

```
I need to validate the integrity of my ADIOS dataset at /data/experimental_results.bp - check all variables, their step-wise properties, and ensure metadata completeness.
```

**Tools used:**
- **inspect_variables**: Comprehensive variable structure validation
- **inspect_variables_at_step**: Step-specific variable validation
- **inspect_attributes**: Metadata integrity check

### Quick BP5 File Discovery

```
Show me all BP5 files in my simulation directory at /data/simulations/ and provide a quick overview of their contents and structure.
```

**Tools used:**
- **list_bp5**: Directory-wide BP5 file discovery
- **inspect_variables**: Quick structure overview for each file

