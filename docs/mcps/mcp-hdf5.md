---
id: mcp-hdf5
title: HDF5 MCP
sidebar_label: HDF5
description: HDF5 MCP - Scientific Data Access for LLMs with comprehensive HDF5 file operations
keywords: ['hdf5', 'scientific-data', 'hierarchical-data', 'data-analysis', 'scientific-computing', 'data-structures']
tags: ['hdf5', 'scientific-data', 'hierarchical-data', 'data-analysis', 'scientific-computing', 'data-structures']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# HDF5 MCP

## Overview
HDF5 MCP - Scientific Data Access for LLMs with comprehensive HDF5 file operations

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Hdf5 • Scientific Data • Hierarchical Data • Data Analysis • Scientific Computing • Data Structures
- **Actions**: 4
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
    "hdf5-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "hdf5"]
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
    "hdf5-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "hdf5"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add hdf5-mcp -- uvx iowarp-mcps hdf5
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "hdf5-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "hdf5"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/HDF5 run hdf5-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\HDF5 run hdf5-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\HDF5 run hdf5-mcp --help
```

</details>

## Available Actions

### `list_hdf5`

**Description**: List all HDF5 files in a specified directory with comprehensive file discovery and metadata extraction for scientific data management.

**Parameters**: directory: Path to directory containing HDF5 files (default: "data/")

### `inspect_hdf5`

**Description**: Inspect HDF5 file structure including detailed analysis of groups, datasets, and attributes for comprehensive data understanding.

**Parameters**: filename: Absolute path to HDF5 file

### `preview_hdf5`

**Description**: Preview first N elements of each dataset in an HDF5 file with configurable data sampling for efficient data exploration.

**Parameters**: filename: Absolute path to HDF5 file, count: Number of elements to preview from each dataset (default: 10)

### `read_all_hdf5`

**Description**: Read every element of every dataset in an HDF5 file with complete data extraction and memory-efficient processing.

**Parameters**: filename: Absolute path to HDF5 file



## Examples

### Scientific Data Structure Analysis

```
I have an HDF5 file containing simulation results at /data/climate_simulation.h5. Can you analyze its structure and show me what datasets are available?
```

**Tools used:**
- **inspect_hdf5**: Analyze the HDF5 file structure and organization
- **list_hdf5**: Discover available HDF5 files in the directory

### Multi-File Scientific Data Discovery

```
Explore my research data directory at /research/experiments/ to find all HDF5 files, then inspect the structure of the most recent experimental data file.
```

**Tools used:**
- **list_hdf5**: Discover all HDF5 files in the research directory
- **inspect_hdf5**: Analyze structure of selected experimental data file

### Data Preview and Validation

```
Before processing the large dataset at /data/sensor_measurements.hdf5, I want to preview the first 20 data points from each sensor dataset to validate the data quality.
```

**Tools used:**
- **preview_hdf5**: Preview first 20 elements from each dataset
- **inspect_hdf5**: Get detailed dataset information

### Complete Dataset Analysis

```
I need to perform comprehensive analysis on the experimental results stored in /experiments/trial_001.h5. Extract all data from every dataset for statistical processing.
```

**Tools used:**
- **read_all_hdf5**: Read complete datasets for analysis
- **inspect_hdf5**: Get dataset metadata and structure information

### Scientific Data Exploration Workflow

```
Help me understand the contents of my computational fluid dynamics results directory at /cfd/simulations/. Show me all HDF5 files, inspect their structures, and preview key datasets.
```

**Tools used:**
- **list_hdf5**: Discover all HDF5 files in simulation directory
- **inspect_hdf5**: Analyze structure of simulation files
- **preview_hdf5**: Preview key simulation datasets

### Research Data Management

```
I'm organizing my laboratory data stored in HDF5 format at /lab/measurements/. List all files, inspect their structures, and provide detailed previews of measurement datasets.
```

**Tools used:**
- **list_hdf5**: Inventory all HDF5 files in laboratory directory
- **inspect_hdf5**: Detailed structure analysis of measurement files
- **preview_hdf5**: Preview measurement datasets for quality assessment

