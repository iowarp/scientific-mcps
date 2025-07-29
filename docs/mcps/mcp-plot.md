---
id: mcp-plot
title: Plot MCP
sidebar_label: Plot
description: MCP server for advanced data visualization and plotting operations
keywords: ['plotting', 'visualization', 'analytics', 'matplotlib', 'seaborn', 'data-science']
tags: ['plotting', 'visualization', 'analytics', 'matplotlib', 'seaborn', 'data-science']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Plot MCP

## Overview
MCP server for advanced data visualization and plotting operations

## Information
- **Version**: 0.1.0
- **Language**: Python
- **Category**: Plotting • Visualization • Analytics • Matplotlib • Seaborn • Data Science
- **Actions**: 6
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
    "plot-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "plot"]
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
    "plot-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "plot"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add plot-mcp -- uvx iowarp-mcps plot
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "plot-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "plot"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Plot run plot-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Plot run plot-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Plot run plot-mcp --help
```

</details>

## Available Actions

### `line_plot`

**Description**: Create a line plot from data file with comprehensive visualization options.

**Parameters**: file_path: Parameter for file_path, x_column: Parameter for x_column, y_column: Parameter for y_column, title: Parameter for title (default: Line Plot), output_path: Parameter for output_path (default: line_plot.png)

### `bar_plot`

**Description**: Create a bar plot from data file with comprehensive customization options.

**Parameters**: file_path: Parameter for file_path, x_column: Parameter for x_column, y_column: Parameter for y_column, title: Parameter for title (default: Bar Plot), output_path: Parameter for output_path (default: bar_plot.png)

### `scatter_plot`

**Description**: Create a scatter plot from data file with advanced correlation analysis.

**Parameters**: file_path: Parameter for file_path, x_column: Parameter for x_column, y_column: Parameter for y_column, title: Parameter for title (default: Scatter Plot), output_path: Parameter for output_path (default: scatter_plot.png)

### `histogram_plot`

**Description**: Create a histogram from data file with advanced statistical analysis.

**Parameters**: file_path: Parameter for file_path, column: Parameter for column, bins: Parameter for bins (default: 30), title: Parameter for title (default: Histogram), output_path: Parameter for output_path (default: histogram.png)

### `heatmap_plot`

**Description**: Create a heatmap from data file with advanced correlation visualization.

**Parameters**: file_path: Parameter for file_path, title: Parameter for title (default: Heatmap), output_path: Parameter for output_path (default: heatmap.png)

### `data_info`

**Description**: Get comprehensive data file information with detailed analysis.

**Parameters**: file_path: Parameter for file_path



## Examples

### Data Exploration and Analysis

```
I have a CSV file at /data/sales_data.csv with sales information. Can you first analyze the data structure and then create appropriate visualizations to show sales trends over time?
```

**Tools used:**
- **data_info**: Analyze the dataset structure
- **line_plot**: Create time-series plots showing sales trends

### Comparative Analysis with Multiple Charts

```
Using the file /data/survey_results.csv, create a comprehensive analysis showing:
1. Age distribution of respondents (histogram)
2. Correlation between satisfaction scores (heatmap)  
3. Department vs average salary comparison (bar chart)
```

**Tools used:**
- **histogram_plot**: Age distribution of respondents
- **heatmap_plot**: Correlation between satisfaction scores
- **bar_plot**: Department vs average salary comparison

### Scientific Data Visualization

```
I have temperature measurement data in /data/temperature.csv. Create a scatter plot showing the relationship between ambient temperature and device performance, and add a trend analysis.
```

**Tools used:**
- **scatter_plot**: Relationship between ambient temperature and device performance

### Business Intelligence Dashboard

```
From /data/quarterly_metrics.xlsx, create visualizations showing:
- Revenue trends by quarter (line plot)
- Performance metrics distribution (histogram)
- Regional comparison (bar chart)
```

**Tools used:**
- **line_plot**: Revenue trends by quarter
- **histogram_plot**: Performance metrics distribution
- **bar_plot**: Regional comparison

### Research Data Publication

```
Using /data/experiment_results.csv, create publication-quality figures showing experimental conditions vs outcomes with proper error handling and statistical annotations.
```

**Tools used:**
- **data_info**: Analyze experimental data structure and quality
- **scatter_plot**: Show relationship between experimental conditions and outcomes
- **heatmap_plot**: Display correlation matrix of experimental variables

### Quick Data Quality Check

```
I need to quickly assess the quality of my dataset at /data/customer_data.csv - show me data completeness, distributions, and suggest the best visualization approaches.
```

**Tools used:**
- **data_info**: Comprehensive data quality assessment

