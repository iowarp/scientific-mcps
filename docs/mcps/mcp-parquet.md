---
id: mcp-parquet
title: parquet MCP
sidebar_label: parquet
description: MCP server with Parquet file operations and data analytics
keywords: ['Parquet', 'columnar', 'data', 'analytics', 'pandas']
tags: ['Parquet', 'columnar', 'data', 'analytics', 'pandas']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# parquet MCP

## Overview
MCP server with Parquet file operations and data analytics

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Parquet • Columnar • Data • Analytics • Pandas
- **Actions**: 4
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- PyArrow library for Parquet file processing

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "parquet-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parquet"]
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
    "parquet-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "parquet"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add parquet-mcp -- uvx iowarp-mcps parquet
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "parquet-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parquet"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/parquet run parquet-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\parquet run parquet-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\parquet run parquet-mcp --help
```

</details>

## Available Actions

### `list_parquet_resources`

**Description**: Discover and list all available Parquet files and datasets with comprehensive metadata extraction and schema information.

**Parameters**: No parameters

### `read_parquet_column`

**Description**: Read specific columns from Parquet files with efficient columnar access and memory optimization.

**Parameters**: file_path: Path to the Parquet file, column_name: Name of the column to read

### `get_parquet_schema`

**Description**: Extract comprehensive schema information from Parquet files including column types and metadata.

**Parameters**: file_path: Path to the Parquet file

### `preview_parquet_data`

**Description**: Preview sample data from Parquet files with configurable row limits and column selection.

**Parameters**: file_path: Path to the Parquet file, num_rows: Number of rows to preview (default: 10), columns: Specific columns to preview



## Examples

### Data Discovery and Schema Analysis

```
I have Parquet files in my data directory. Can you discover all available files and show me their schemas to understand the data structure?
```

**Tools used:**
- **list_parquet_resources**: Discover available Parquet files
- **get_parquet_schema**: Analyze file schemas and structure

### Selective Column Analysis

```
From the weather data file at /data/weather_measurements.parquet, read the temperature column and show me the data distribution and statistics.
```

**Tools used:**
- **read_parquet_column**: Read temperature column data
- **get_parquet_schema**: Get column metadata and types

### Data Quality Assessment

```
Before processing the large dataset at /analytics/customer_data.parquet, preview the first 50 rows to validate data quality and structure.
```

**Tools used:**
- **preview_parquet_data**: Preview dataset sample
- **get_parquet_schema**: Get comprehensive schema information

### Multi-Column Data Exploration

```
Explore the sales dataset at /business/quarterly_sales.parquet by reading the revenue, region, and date columns for trend analysis.
```

**Tools used:**
- **read_parquet_column**: Read multiple columns (revenue, region, date)
- **preview_parquet_data**: Preview multi-column data sample

### Large Dataset Processing Preparation

```
I need to process a large Parquet dataset at /warehouse/transaction_logs.parquet. Show me the schema, preview sample data, and help me understand the optimal columns for analysis.
```

**Tools used:**
- **get_parquet_schema**: Analyze dataset structure
- **preview_parquet_data**: Sample data for understanding
- **list_parquet_resources**: Verify resource availability

### Business Intelligence Data Pipeline

```
Set up analysis of our customer behavior data stored in /bi/customer_analytics.parquet by examining schema, previewing key metrics columns, and reading engagement data.
```

**Tools used:**
- **get_parquet_schema**: Understand data structure
- **preview_parquet_data**: Preview key metrics
- **read_parquet_column**: Read engagement data columns

