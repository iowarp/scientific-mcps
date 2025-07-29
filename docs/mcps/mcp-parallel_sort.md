---
id: mcp-parallel_sort
title: Parallel_Sort MCP
sidebar_label: Parallel_Sort
description: Parallel Sort MCP - High-Performance Log File Processing for LLMs with advanced sorting and analysis
keywords: ['parallel-sorting', 'log-processing', 'log-analysis', 'high-performance', 'timestamp-sorting', 'pattern-detection', 'log-filtering', 'data-export']
tags: ['parallel-sorting', 'log-processing', 'log-analysis', 'high-performance', 'timestamp-sorting', 'pattern-detection', 'log-filtering', 'data-export']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Parallel_Sort MCP

## Overview
Parallel Sort MCP - High-Performance Log File Processing for LLMs with advanced sorting and analysis

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Parallel Sorting • Log Processing • Log Analysis • High Performance • Timestamp Sorting • Pattern Detection • Log Filtering • Data Export
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
    "parallel-sort-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
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
    "parallel-sort-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
    }
  }
}
```
 
</details>
 
<details>
<summary><b>Install in Claude Code</b></summary>
 
Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.
 
```sh
claude mcp add parallel-sort-mcp -- uvx iowarp-mcps parallel-sort
```
 
</details>
 
<details>
<summary><b>Install in Claude Desktop</b></summary>
 
Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.
 
```json
{
  "mcpServers": {
    "parallel-sort-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Parallel_Sort run parallel-sort-mcp --help
```
 
**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Parallel_Sort run parallel-sort-mcp --help
```
 
**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Parallel_Sort run parallel-sort-mcp --help
```
 
</details>

## Available Actions

### `sort_log_by_timestamp`

**Description**: Sort log files by timestamp in chronological order with support for standard log formats.

**Parameters**: log_file: Path to input log file, output_file: Path for sorted output file, reverse: Sort in descending order (default: False)

### `parallel_sort_large_file`

**Description**: Sort large log files using parallel processing with chunked approach for memory efficiency.

**Parameters**: log_file: Path to large log file, output_file: Path for sorted output file, chunk_size_mb: Chunk size in MB (default: 100), num_workers: Number of worker processes (default: CPU count)

### `analyze_log_statistics`

**Description**: Perform comprehensive statistical analysis of log files including temporal patterns and log levels.

**Parameters**: log_file: Path to log file, include_patterns: Include pattern analysis (default: True)

### `detect_log_patterns`

**Description**: Detect patterns, anomalies, and trends in log files for proactive issue identification.

**Parameters**: log_file: Path to log file, pattern_types: Types of patterns to detect, sensitivity: Detection sensitivity ('low', 'medium', 'high')

### `filter_logs`

**Description**: Apply multiple filter conditions to log files with complex logical operations.

**Parameters**: log_file: Path to log file, filters: List of filter conditions, logical_operator: Logical operator between filters ('AND', 'OR'), output_file: Path for filtered output

### `filter_by_time_range`

**Description**: Filter log entries within a specific time range.

**Parameters**: log_file: Path to log file, start_time: Start timestamp (YYYY-MM-DD HH:MM:SS), end_time: End timestamp (YYYY-MM-DD HH:MM:SS), output_file: Path for filtered output

### `filter_by_log_level`

**Description**: Filter log entries by log level (ERROR, WARN, INFO, DEBUG, etc.).

**Parameters**: log_file: Path to log file, log_levels: List of log levels to include, output_file: Path for filtered output

### `filter_by_keyword`

**Description**: Filter log entries containing specific keywords with advanced matching options.

**Parameters**: log_file: Path to log file, keywords: List of keywords to search for, case_sensitive: Case sensitive matching (default: False), logical_operator: Operator between keywords ('AND', 'OR'), output_file: Path for filtered output

### `apply_filter_preset`

**Description**: Apply predefined filter presets for common log analysis scenarios.

**Parameters**: log_file: Path to log file, preset_name: Preset name ('errors_only', 'warnings_and_errors', 'connection_issues', etc.), output_file: Path for filtered output

### `export_to_json`

**Description**: Export results to JSON format.

**Parameters**: data: Parameter for data, include_metadata: Parameter for include_metadata (default: True)

### `export_to_csv`

**Description**: Export results to CSV format.

**Parameters**: data: Parameter for data, include_headers: Parameter for include_headers (default: True)

### `export_to_text`

**Description**: Export results to text format.

**Parameters**: data: Parameter for data, include_summary: Parameter for include_summary (default: True)

### `generate_summary_report`

**Description**: Generate a summary report.

**Parameters**: data: Parameter for data



## Examples

### Large Log File Sorting and Analysis

```
I have a large application log file at /var/logs/app.log with millions of entries. Sort this log chronologically and analyze the error patterns.
```

**Tools used:**
- **parallel_sort_large_file**: Sort the large log file using parallel processing
- **analyze_log_statistics**: Analyze log statistics and patterns
- **detect_log_patterns**: Detect error patterns and anomalies

### Error Log Filtering and Export

```
Filter all ERROR and WARN level entries from /var/logs/system.log from the last 24 hours and export to CSV for analysis.
```

**Tools used:**
- **filter_by_time_range**: Filter logs by time range
- **filter_by_log_level**: Filter by ERROR and WARN levels
- **export_to_csv**: Export filtered results to CSV

### Connection Issue Pattern Detection

```
Analyze /var/logs/network.log for connection timeout patterns and generate a comprehensive report with trend analysis.
```

**Tools used:**
- **filter_by_keyword**: Filter for connection-related entries
- **detect_log_patterns**: Detect timeout patterns and trends
- **generate_summary_report**: Create comprehensive analysis report

### Multi-Condition Log Analysis

```
Find all database connection errors in /var/logs/db.log that occurred during business hours (9 AM - 5 PM) and contain "timeout" or "refused".
```

**Tools used:**
- **filter_by_time_range**: Filter for business hours
- **filter_by_keyword**: Filter for timeout and connection refused
- **filter_logs**: Apply complex multi-condition filtering
- **analyze_log_statistics**: Analyze filtered results

### Log Quality Assessment and Cleanup

```
Analyze the quality of /var/logs/application.log, identify malformed entries, and generate a clean sorted version with quality metrics.
```

**Tools used:**
- **analyze_log_statistics**: Assess log quality and identify issues
- **sort_log_by_timestamp**: Sort logs chronologically
- **generate_summary_report**: Create quality assessment report

### Historical Log Trend Analysis

```
Analyze error trends in /var/logs/historic.log over the past month, detect anomalies, and export findings to JSON for dashboard integration.
```

**Tools used:**
- **filter_by_time_range**: Filter for past month
- **detect_log_patterns**: Detect trends and anomalies
- **analyze_log_statistics**: Generate temporal analysis
- **export_to_json**: Export results for dashboard

