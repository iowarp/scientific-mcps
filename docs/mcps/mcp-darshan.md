---
id: mcp-darshan
title: Darshan MCP
sidebar_label: Darshan
description: Darshan I/O profiler MCP server for analyzing I/O trace files
keywords: []
tags: []
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Darshan MCP

## Overview
Darshan I/O profiler MCP server for analyzing I/O trace files

## Information
- **Version**: 0.1.0
- **Language**: Python
- **Category**: Other
- **Actions**: 10
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Darshan tools (`darshan-parser` in PATH)
- Python libraries: numpy, pandas, matplotlib

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "darshan-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "darshan"]
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
    "darshan-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "darshan"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add darshan-mcp -- uvx iowarp-mcps darshan
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "darshan-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "darshan"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Darshan run darshan-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Darshan run darshan-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Darshan run darshan-mcp --help
```

</details>

## Available Actions

### `load_darshan_log`

**Description**: Load and parse a Darshan log file to extract metadata and basic I/O information.

**Parameters**: log_file_path: Absolute path to the .darshan log file

### `get_job_summary`

**Description**: Get comprehensive job-level summary including runtime statistics and I/O performance overview.

**Parameters**: log_file_path: Path to the Darshan log file

### `analyze_file_access_patterns`

**Description**: Analyze file access patterns to understand application I/O behavior and optimization opportunities.

**Parameters**: log_file_path: Path to the Darshan log file, file_pattern: Filter files by pattern (e.g., '*.dat', '/scratch/*')

### `get_io_performance_metrics`

**Description**: Extract detailed I/O performance metrics including bandwidth, IOPS, and request size analysis.

**Parameters**: log_file_path: Path to the Darshan log file

### `analyze_posix_operations`

**Description**: Analyze POSIX system call patterns including open, read, write, and seek operations.

**Parameters**: log_file_path: Path to the Darshan log file

### `analyze_mpiio_operations`

**Description**: Analyze MPI-IO operations including collective vs independent I/O patterns and performance.

**Parameters**: log_file_path: Path to the Darshan log file

### `identify_io_bottlenecks`

**Description**: Automatically identify potential I/O performance bottlenecks and optimization opportunities.

**Parameters**: log_file_path: Path to the Darshan log file

### `get_timeline_analysis`

**Description**: Generate temporal analysis of I/O activity to understand performance patterns over time.

**Parameters**: log_file_path: Path to the Darshan log file, time_resolution: Time resolution for analysis (e.g., '1s', '100ms')

### `compare_darshan_logs`

**Description**: Compare two Darshan log files to identify performance differences and optimization results.

**Parameters**: log_file_1: Path to the first log file, log_file_2: Path to the second log file, comparison_metrics: List of metrics to compare ['bandwidth', 'iops', 'file_count']

### `generate_io_summary_report`

**Description**: Generate comprehensive I/O analysis report with detailed metrics and recommendations.

**Parameters**: log_file_path: Path to the Darshan log file, include_visualizations: Whether to include visualization data in the report



## Examples

### HPC Application Performance Analysis

```
Analyze the I/O performance of my application using the Darshan log at /data/app_trace.darshan. Identify bottlenecks and provide optimization recommendations.
```

**Tools used:**
- **load_darshan_log**: Parse the Darshan trace file
- **get_job_summary**: Extract job-level statistics
- **identify_io_bottlenecks**: Find performance issues
- **get_io_performance_metrics**: Calculate detailed metrics

### I/O Pattern Optimization Study

```
Compare the I/O patterns between /data/before_opt.darshan and /data/after_opt.darshan to validate our optimization efforts and measure performance improvements.
```

**Tools used:**
- **analyze_file_access_patterns**: Analyze access patterns for both files
- **compare_darshan_logs**: Compare performance metrics
- **get_io_performance_metrics**: Extract detailed performance data

### MPI-IO Collective Performance Analysis

```
Examine the MPI-IO operations in /data/parallel_app.darshan, focusing on collective vs independent I/O patterns and their impact on overall performance.
```

**Tools used:**
- **analyze_mpiio_operations**: Analyze MPI-IO patterns
- **get_timeline_analysis**: Understand temporal patterns
- **generate_io_summary_report**: Create comprehensive report

### POSIX System Call Analysis

```
Investigate the POSIX I/O operations in /data/serial_app.darshan to understand file access patterns and identify potential optimizations for system call efficiency.
```

**Tools used:**
- **analyze_posix_operations**: Examine POSIX system calls
- **analyze_file_access_patterns**: Study file access behavior
- **identify_io_bottlenecks**: Find system-level bottlenecks

### Comprehensive I/O Performance Report

```
Generate a complete I/O performance analysis report for /data/production_app.darshan including all metrics, visualizations, and recommendations for our production environment.
```

**Tools used:**
- **load_darshan_log**: Load and validate trace file
- **generate_io_summary_report**: Create comprehensive analysis
- **get_timeline_analysis**: Add temporal performance data

