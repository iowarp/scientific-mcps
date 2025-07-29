---
id: mcp-slurm
title: Slurm MCP
sidebar_label: Slurm
description: MCP server for Slurm workload management and HPC job scheduling
keywords: ['Slurm', 'HPC', 'job-management', 'cluster-monitoring', 'workload-management', 'scientific-computing', 'high-performance-computing']
tags: ['Slurm', 'HPC', 'job-management', 'cluster-monitoring', 'workload-management', 'scientific-computing', 'high-performance-computing']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Slurm MCP

## Overview
MCP server for Slurm workload management and HPC job scheduling

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Slurm • Hpc • Job Management • Cluster Monitoring • Workload Management • Scientific Computing • High Performance Computing
- **Actions**: 13
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
    "slurm-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
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
    "slurm-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add slurm-mcp -- uvx iowarp-mcps slurm
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "slurm-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Slurm run slurm-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Slurm run slurm-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Slurm run slurm-mcp --help
```

</details>

## Available Actions

### `submit_slurm_job`

**Description**: Submit a job script to Slurm scheduler with advanced resource specification and intelligent optimization.

**Parameters**: script_path: Parameter for script_path, cores: Parameter for cores (default: 1), memory: Parameter for memory (default: 1GB), time_limit: Parameter for time_limit (default: 01:00:00), job_name: Parameter for job_name, partition: Parameter for partition

### `check_job_status`

**Description**: Check comprehensive status of a Slurm job with advanced monitoring and intelligent analysis.

**Parameters**: job_id: Parameter for job_id

### `cancel_slurm_job`

**Description**: Cancel a Slurm job.

**Parameters**: job_id: Parameter for job_id

### `list_slurm_jobs`

**Description**: List Slurm jobs with optional filtering.

**Parameters**: user: Parameter for user, state: Parameter for state

### `get_slurm_info`

**Description**: Get information about the Slurm cluster.

**Parameters**: No parameters

### `get_job_details`

**Description**: Get detailed information about a Slurm job.

**Parameters**: job_id: Parameter for job_id

### `get_job_output`

**Description**: Get job output content.

**Parameters**: job_id: Parameter for job_id, output_type: Parameter for output_type (default: stdout)

### `get_queue_info`

**Description**: Get job queue information.

**Parameters**: partition: Parameter for partition

### `submit_array_job`

**Description**: Submit an array job to Slurm scheduler.

**Parameters**: script_path: Parameter for script_path, array_range: Parameter for array_range, cores: Parameter for cores (default: 1), memory: Parameter for memory (default: 1GB), time_limit: Parameter for time_limit (default: 01:00:00), job_name: Parameter for job_name, partition: Parameter for partition

### `get_node_info`

**Description**: Get cluster node information.

**Parameters**: No parameters

### `allocate_slurm_nodes`

**Description**: Allocate Slurm nodes using salloc command.

**Parameters**: nodes: Parameter for nodes (default: 1), cores: Parameter for cores (default: 1), memory: Parameter for memory, time_limit: Parameter for time_limit (default: 01:00:00), partition: Parameter for partition, job_name: Parameter for job_name, immediate: Parameter for immediate (default: False)

### `deallocate_slurm_nodes`

**Description**: Deallocate Slurm nodes by canceling the allocation.

**Parameters**: allocation_id: Parameter for allocation_id

### `get_allocation_status`

**Description**: Get status of a node allocation.

**Parameters**: allocation_id: Parameter for allocation_id



## Examples

### Job Submission and Monitoring

```
I need to submit a Python simulation script to Slurm with 16 cores and 32GB memory, then monitor its progress until completion.
```

**Tools used:**
- **submit_slurm_job**: Submit job with resource specification
- **check_job_status**: Monitor job progress and performance

### Array Job Management

```
Submit an array job for parameter sweep analysis with 100 tasks, each requiring 4 cores and 8GB memory, then check the overall progress.
```

**Tools used:**
- **submit_array_job**: Submit parallel array job
- **list_slurm_jobs**: Monitor array job progress
- **get_job_details**: Get detailed array job information

### Interactive Session Management

```
Allocate 2 compute nodes with 8 cores each for an interactive analysis session, then deallocate when finished.
```

**Tools used:**
- **allocate_slurm_nodes**: Allocate interactive nodes
- **get_node_info**: Check node status and resources
- **get_allocation_status**: Monitor allocation efficiency
- **deallocate_slurm_nodes**: Clean up allocated resources

### Job Management and Cleanup

```
I have a long-running job that needs to be cancelled, and I want to retrieve the output from a completed job before cleaning up.
```

**Tools used:**
- **cancel_slurm_job**: Cancel running job with cleanup
- **get_job_output**: Retrieve completed job outputs
- **get_job_details**: Get final job performance metrics

### Comprehensive Cluster Analysis

```
Analyze the current cluster queue status, identify bottlenecks, and suggest optimal resource allocation for my pending jobs.
```

**Tools used:**
- **get_slurm_info**: Get cluster status and capacity
- **get_queue_info**: Analyze queue performance and bottlenecks
- **list_slurm_jobs**: Review pending job queue and priorities

### HPC Workflow Optimization

```
I need to optimize my computational workflow by analyzing my recent job performance, understanding cluster utilization patterns, and planning future submissions with better resource allocation.
```

**Tools used:**
- **list_slurm_jobs**: Review recent job history and performance patterns
- **get_job_details**: Analyze specific job performance metrics
- **get_slurm_info**: Understand cluster capacity and optimization opportunities
- **get_queue_info**: Analyze queue performance for optimal timing

