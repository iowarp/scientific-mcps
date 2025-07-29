---
id: mcp-pandas
title: Pandas MCP
sidebar_label: Pandas
description: Pandas MCP - Advanced Data Analysis for LLMs with comprehensive pandas operations
keywords: ['pandas', 'data-analysis', 'statistical-analysis', 'data-science', 'data-manipulation', 'time-series', 'data-cleaning', 'data-transformation']
tags: ['pandas', 'data-analysis', 'statistical-analysis', 'data-science', 'data-manipulation', 'time-series', 'data-cleaning', 'data-transformation']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Pandas MCP

## Overview
Pandas MCP - Advanced Data Analysis for LLMs with comprehensive pandas operations

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Pandas • Data Analysis • Statistical Analysis • Data Science • Data Manipulation • Time Series • Data Cleaning • Data Transformation
- **Actions**: 15
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
    "pandas-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
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
    "pandas-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add pandas-mcp -- uvx iowarp-mcps pandas
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "pandas-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Pandas run pandas-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Pandas run pandas-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Pandas run pandas-mcp --help
```

</details>

## Available Actions

### `load_data`

**Description**: Load data from various file formats with comprehensive parsing options.

**Parameters**: file_path: Parameter for file_path, file_format: Parameter for file_format, sheet_name: Parameter for sheet_name, encoding: Parameter for encoding, columns: Parameter for columns, nrows: Parameter for nrows

### `save_data`

**Description**: Save data to various file formats with comprehensive export options.

**Parameters**: data: Parameter for data, file_path: Parameter for file_path, file_format: Parameter for file_format, index: Parameter for index (default: True)

### `statistical_summary`

**Description**: Generate comprehensive statistical summary with advanced analytics.

**Parameters**: file_path: Parameter for file_path, columns: Parameter for columns, include_distributions: Parameter for include_distributions (default: False)

### `correlation_analysis`

**Description**: Perform comprehensive correlation analysis with statistical significance testing.

**Parameters**: file_path: Parameter for file_path, method: Parameter for method (default: pearson), columns: Parameter for columns

### `hypothesis_testing`

**Description**: Perform comprehensive statistical hypothesis testing with multiple test types and advanced analysis.

**Parameters**: file_path: Parameter for file_path, test_type: Parameter for test_type, column1: Parameter for column1, column2: Parameter for column2, alpha: Parameter for alpha (default: 0.05)

### `handle_missing_data`

**Description**: Handle missing data with comprehensive strategies and statistical methods.

**Parameters**: file_path: Parameter for file_path, strategy: Parameter for strategy (default: detect), method: Parameter for method, columns: Parameter for columns

### `clean_data`

**Description**: Perform comprehensive data cleaning with advanced quality improvement techniques.

**Parameters**: file_path: Parameter for file_path, remove_duplicates: Parameter for remove_duplicates (default: False), detect_outliers: Parameter for detect_outliers (default: False), convert_types: Parameter for convert_types (default: False)

### `groupby_operations`

**Description**: Perform sophisticated groupby operations with comprehensive aggregation options.

**Parameters**: file_path: Parameter for file_path, group_by: Parameter for group_by, operations: Parameter for operations, filter_condition: Parameter for filter_condition

### `merge_datasets`

**Description**: Merge and join datasets with comprehensive integration capabilities.

**Parameters**: left_file: Parameter for left_file, right_file: Parameter for right_file, join_type: Parameter for join_type (default: inner), left_on: Parameter for left_on, right_on: Parameter for right_on, on: Parameter for on

### `pivot_table`

**Description**: Create sophisticated pivot tables with comprehensive aggregation options.

**Parameters**: file_path: Parameter for file_path, index: Parameter for index, columns: Parameter for columns, values: Parameter for values, aggfunc: Parameter for aggfunc (default: mean)

### `time_series_operations`

**Description**: Perform comprehensive time series operations with advanced temporal analysis.

**Parameters**: file_path: Parameter for file_path, date_column: Parameter for date_column, operation: Parameter for operation, window_size: Parameter for window_size, frequency: Parameter for frequency

### `validate_data`

**Description**: Perform comprehensive data validation with advanced constraint checking and quality assessment.

**Parameters**: file_path: Parameter for file_path, validation_rules: Parameter for validation_rules

### `filter_data`

**Description**: Perform advanced data filtering with sophisticated boolean indexing and conditional expressions.

**Parameters**: file_path: Parameter for file_path, filter_conditions: Parameter for filter_conditions, output_file: Parameter for output_file

### `optimize_memory`

**Description**: Perform advanced memory optimization for large datasets with intelligent strategies.

**Parameters**: file_path: Parameter for file_path, optimize_dtypes: Parameter for optimize_dtypes (default: True), chunk_size: Parameter for chunk_size

### `profile_data`

**Description**: Perform comprehensive data profiling with detailed statistical analysis and quality assessment.

**Parameters**: file_path: Parameter for file_path, include_correlations: Parameter for include_correlations (default: False), sample_size: Parameter for sample_size



## Examples

### Data Loading and Profiling

```
I have a large CSV file with sales data that I need to load and get a comprehensive profile including data types, missing values, and basic statistics.
```

**Tools used:**
- **load_data**: Load CSV file with intelligent format detection
- **profile_data**: Get comprehensive data profile and quality metrics
- **statistical_summary**: Generate descriptive statistics and distributions

### Data Cleaning and Quality Assessment

```
My dataset has missing values and outliers that need to be handled. I also want to remove duplicates and validate the data quality.
```

**Tools used:**
- **handle_missing_data**: Impute missing values with appropriate strategies
- **clean_data**: Remove outliers, duplicates, and optimize data types
- **validate_data**: Apply business rules and data quality checks

### Statistical Analysis and Correlation

```
Analyze the relationships between different variables in my dataset and perform hypothesis testing to validate my assumptions.
```

**Tools used:**
- **correlation_analysis**: Calculate correlation matrices with different methods
- **hypothesis_testing**: Perform t-tests, ANOVA, and normality tests
- **statistical_summary**: Generate comprehensive statistical insights

### Data Transformation and Aggregation

```
I need to group my sales data by region and product category, then create pivot tables for cross-analysis and merge with customer data.
```

**Tools used:**
- **groupby_operations**: Group data and perform multiple aggregations
- **pivot_table**: Create pivot tables with multi-level indexing
- **merge_datasets**: Join datasets using different merge strategies

### Time Series Analysis and Filtering

```
Analyze my time series data by resampling to different frequencies, calculating rolling averages, and filtering specific date ranges.
```

**Tools used:**
- **time_series_operations**: Resample, rolling windows, and lag features
- **filter_data**: Apply complex time-based filtering conditions
- **statistical_summary**: Analyze time series patterns and trends

### Data Export and Memory Optimization

```
Optimize memory usage of my large dataset and export the cleaned data to multiple formats for different teams.
```

**Tools used:**
- **optimize_memory**: Reduce memory usage with dtype optimization
- **save_data**: Export to CSV, Excel, Parquet, and JSON formats
- **profile_data**: Verify optimization results and final data quality

