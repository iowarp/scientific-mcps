---
id: mcp-node_hardware
title: Node_Hardware MCP
sidebar_label: Node_Hardware
description: Node Hardware MCP - Comprehensive Hardware Monitoring and System Analysis for LLMs with real-time performance metrics
keywords: ['hardware-monitoring', 'system-analysis', 'performance-metrics', 'node-information', 'ssh-monitoring', 'remote-hardware', 'infrastructure-monitoring', 'distributed-systems']
tags: ['hardware-monitoring', 'system-analysis', 'performance-metrics', 'node-information', 'ssh-monitoring', 'remote-hardware', 'infrastructure-monitoring', 'distributed-systems']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Node_Hardware MCP

## Overview
Node Hardware MCP - Comprehensive Hardware Monitoring and System Analysis for LLMs with real-time performance metrics

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Hardware Monitoring • System Analysis • Performance Metrics • Node Information • Ssh Monitoring • Remote Hardware • Infrastructure Monitoring • Distributed Systems
- **Actions**: 11
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- SSH client (for remote node capabilities)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "node-hardware-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
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
    "node-hardware-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add node-hardware-mcp -- uvx iowarp-mcps node-hardware
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "node-hardware-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Node_Hardware run node-hardware-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Node_Hardware run node-hardware-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Node_Hardware run node-hardware-mcp --help
```

</details>

## Available Actions

### `get_cpu_info`

**Description**: Get comprehensive CPU information including specifications, core configuration, frequency analysis, and performance metrics.

**Parameters**: No parameters

### `get_memory_info`

**Description**: Get comprehensive memory information including capacity, usage patterns, and performance characteristics.

**Parameters**: No parameters

### `get_system_info`

**Description**: Get comprehensive system information including operating system details, platform configuration, and system status.

**Parameters**: No parameters

### `get_disk_info`

**Description**: Get comprehensive disk information including storage devices, partitions, and I/O performance metrics.

**Parameters**: No parameters

### `get_network_info`

**Description**: Get comprehensive network information including interfaces, connections, and bandwidth analysis.

**Parameters**: No parameters

### `get_gpu_info`

**Description**: Get comprehensive GPU information including specifications, memory, and compute capabilities.

**Parameters**: No parameters

### `get_sensor_info`

**Description**: Get sensor information including temperature, fan speeds, and thermal data.

**Parameters**: No parameters

### `get_process_info`

**Description**: Get process information including running processes and resource usage.

**Parameters**: No parameters

### `get_performance_info`

**Description**: Get real-time performance metrics including CPU, memory, and disk usage.

**Parameters**: No parameters

### `get_remote_node_info`

**Description**: Get comprehensive remote node hardware and system information via SSH with advanced filtering and intelligent analysis.

**Parameters**: hostname: Target hostname or IP address for remote collection., username: SSH username for remote authentication., port: SSH port number for remote connection., ssh_key: Path to SSH private key file for authentication., timeout: SSH connection timeout in seconds., components: List of specific components to include in collection., exclude_components: List of specific components to exclude from collection., include_performance: Whether to include real-time performance analysis., include_health: Whether to include health assessment and predictive maintenance insights.

### `health_check`

**Description**: Perform comprehensive health check and system diagnostics with advanced capability verification.

**Parameters**: No parameters



## Examples

### Local Hardware Overview

```
I need a comprehensive overview of my local system's hardware including CPU, memory, disk, and network components.
```

**Tools used:**
- **get_cpu_info**: Get detailed CPU specifications and performance metrics
- **get_memory_info**: Get memory capacity and usage analysis
- **get_disk_info**: Get storage device information and health status
- **get_network_info**: Get network interface and connection details
- **get_system_info**: Get operating system and platform information

### Remote Server Monitoring

```
Monitor the hardware status of a remote server via SSH, focusing on CPU and memory utilization for performance analysis.
```

**Tools used:**
- **get_remote_node_info**: Connect to remote host with SSH authentication and collect CPU/memory data

### GPU and Thermal Monitoring

```
Check GPU specifications and thermal sensors on both local and remote systems for machine learning workloads.
```

**Tools used:**
- **get_gpu_info**: Local GPU specifications and performance metrics
- **get_sensor_info**: Local thermal monitoring and hardware health
- **get_remote_node_info**: Remote GPU and thermal analysis via SSH

### System Health Assessment

```
Perform a comprehensive health check of system capabilities and verify all monitoring tools are working correctly.
```

**Tools used:**
- **health_check**: System health verification and diagnostic assessment
- **get_performance_info**: Performance monitoring and bottleneck analysis

### Performance Bottleneck Analysis

```
Identify performance bottlenecks on a production server by analyzing CPU, memory, disk I/O, and running processes.
```

**Tools used:**
- **get_remote_node_info**: Remote performance analysis via SSH with comprehensive component collection
- **get_performance_info**: Real-time performance monitoring and bottleneck identification

### Storage and Network Analysis

```
Analyze storage health and network interface performance on multiple systems for infrastructure monitoring.
```

**Tools used:**
- **get_disk_info**: Local storage analysis and health monitoring
- **get_network_info**: Local network interface performance analysis
- **get_remote_node_info**: Remote storage and network monitoring via SSH

