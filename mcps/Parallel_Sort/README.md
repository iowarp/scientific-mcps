# Parallel Sort MCP - Log Processing and Analysis for LLMs


## Description

Parallel Sort MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to perform advanced log file processing, analysis, and sorting operations with high-performance parallel computing capabilities. This server provides sophisticated log analysis tools, pattern detection, statistical analysis, and flexible export options with seamless integration with AI coding assistants.

The system automatically handles large-scale log processing with parallel sorting algorithms, provides comprehensive statistical analysis and pattern detection, and supports enterprise-level log management workflows with professional reporting capabilities. It offers high-performance data processing with memory-efficient streaming and configurable parallelization for production environments.

**Key Features:**
- **High-Performance Parallel Processing**: True parallel sorting and analysis using multiprocessing with configurable chunk sizes
- **Advanced Log Analytics**: Comprehensive statistics, pattern detection, temporal analysis, and anomaly detection
- **Intelligent Filtering**: Multi-condition filtering with logical operations, time ranges, and predefined presets
- **Multiple Export Formats**: JSON, CSV, plain text export with metadata and comprehensive summary reports
- **Memory Efficient Processing**: Streaming file processing with configurable memory limits and temporary file management
- **MCP Integration**: Full Model Context Protocol compliance for seamless LLM integration



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
    "parallel-sort-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/Parallel_Sort", "run", "parallel-sort-mcp"]
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
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/Parallel_Sort", "run", "parallel-sort-mcp"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp) for more info.

```sh
claude mcp add parallel-sort-mcp -- uv --directory /absolute/path/to/Parallel_Sort run parallel-sort-mcp
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "parallel-sort-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/Parallel_Sort", "run", "parallel-sort-mcp"],
      "env": {
        "UV_PROJECT_ENVIRONMENT": "/absolute/path/to/Parallel_Sort/.venv"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Manual Setup</b></summary>

1. Clone or download the Parallel Sort MCP server
2. Install dependencies:
   ```bash
   cd /path/to/Parallel_Sort
   uv sync
   ```
3. Test the installation:
   ```bash
   uv run python -m pytest tests/ -v
   ```

</details>

## Available Actions

### `sort_log_by_timestamp`
**Description**: Sort log file lines by timestamps in YYYY-MM-DD HH:MM:SS format with comprehensive error handling for malformed entries.

**Parameters**:
- `file_path` (str): Path to the log file to sort

**Returns**: Dictionary with sorted log entries and processing statistics including timestamp validation metrics.

### `parallel_sort_large_file`
**Description**: Sort large log files using parallel processing with chunked approach for improved performance and memory efficiency.

**Parameters**:
- `file_path` (str): Path to the log file to sort
- `chunk_size_mb` (int, optional): Size of each chunk in MB (default: 100)
- `max_workers` (int, optional): Maximum number of worker processes (default: CPU count)

**Returns**: Dictionary with sorted log entries and comprehensive processing statistics including parallelization metrics.

### `analyze_log_statistics`
**Description**: Generate comprehensive statistics and analysis for log files including temporal patterns, log levels, and quality metrics.

**Parameters**:
- `file_path` (str): Path to the log file to analyze

**Returns**: Dictionary with comprehensive log analysis including temporal patterns, level distribution, and data quality metrics.

### `detect_log_patterns`
**Description**: Detect patterns in log files including anomalies, error clusters, trending issues, and repeated patterns with configurable detection algorithms.

**Parameters**:
- `file_path` (str): Path to the log file to analyze
- `detection_config` (dict, optional): Configuration for pattern detection algorithms

**Returns**: Dictionary with detected patterns, anomaly analysis, and trend identification results.

### `filter_logs`
**Description**: Filter log entries based on multiple conditions with support for complex logical operations and advanced matching criteria.

**Parameters**:
- `file_path` (str): Path to the log file to filter
- `filter_conditions` (list): List of filter condition dictionaries
- `logical_operator` (str, optional): How to combine conditions ("and", "or") (default: "and")

**Returns**: Dictionary with filtered log entries and filtering statistics.

### `filter_by_time_range`
**Description**: Filter log entries by time range using start and end timestamps with flexible time format support.

**Parameters**:
- `file_path` (str): Path to the log file
- `start_time` (str): Start time in ISO format or 'YYYY-MM-DD HH:MM:SS'
- `end_time` (str): End time in ISO format or 'YYYY-MM-DD HH:MM:SS'

**Returns**: Dictionary with time-filtered log entries and temporal analysis statistics.

### `filter_by_log_level`
**Description**: Filter log entries by log level (ERROR, WARN, INFO, DEBUG, etc.) with inclusion and exclusion modes.

**Parameters**:
- `file_path` (str): Path to the log file
- `levels` (str): Comma-separated list of levels to filter
- `exclude` (bool, optional): If True, exclude these levels instead of including (default: False)

**Returns**: Dictionary with level-filtered log entries and log level distribution analysis.

### `filter_by_keyword`
**Description**: Filter log entries by keywords in message content with support for multiple keywords and logical operations.

**Parameters**:
- `file_path` (str): Path to the log file
- `keywords` (str): Comma-separated list of keywords
- `case_sensitive` (bool, optional): Whether to perform case-sensitive matching (default: False)
- `match_all` (bool, optional): If True, all keywords must be present (AND), else any (OR) (default: False)

**Returns**: Dictionary with keyword-filtered log entries and keyword matching statistics.

### `apply_filter_preset`
**Description**: Apply predefined filter presets like 'errors_only', 'warnings_and_errors', 'connection_issues' for common log analysis scenarios.

**Parameters**:
- `file_path` (str): Path to the log file
- `preset_name` (str): Name of the preset to apply

**Returns**: Dictionary with preset-filtered log entries and preset application results.

### `export_to_json`
**Description**: Export log processing results to JSON format with optional metadata and structured data organization.

**Parameters**:
- `data` (dict): Processing results to export
- `include_metadata` (bool, optional): Whether to include processing metadata (default: True)

**Returns**: Dictionary with JSON export results and export metadata.

### `export_to_csv`
**Description**: Export log entries to CSV format with structured columns for timestamp, level, and message with configurable headers.

**Parameters**:
- `data` (dict): Processing results to export
- `include_headers` (bool, optional): Whether to include CSV headers (default: True)

**Returns**: Dictionary with CSV export results and column structure information.

### `export_to_text`
**Description**: Export log entries to plain text format with optional processing summary and formatted output.

**Parameters**:
- `data` (dict): Processing results to export
- `include_summary` (bool, optional): Whether to include processing summary (default: True)

**Returns**: Dictionary with text export results and formatting information.

### `generate_summary_report`
**Description**: Generate a comprehensive summary report of log processing results with statistics, analysis, and actionable insights.

**Parameters**:
- `data` (dict): Processing results to summarize

**Returns**: Dictionary with comprehensive summary report including statistics, patterns, and recommendations.

## Examples

### 1. Enterprise Log Processing and Analysis
```
I have large application log files that need to be processed and analyzed. Sort the logs at /var/log/application.log by timestamp, analyze patterns, and generate a comprehensive report.
```

**Tools called:**
- `sort_log_by_timestamp` - Sort logs chronologically for temporal analysis
- `analyze_log_statistics` - Generate comprehensive statistics and metrics
- `detect_log_patterns` - Identify anomalies and trending issues
- `generate_summary_report` - Create executive summary report

This prompt will:
- Use `sort_log_by_timestamp` to organize logs chronologically
- Apply `analyze_log_statistics` to extract comprehensive metrics and trends
- Utilize `detect_log_patterns` to identify anomalies and critical issues
- Generate professional report using `generate_summary_report`

### 2. High-Performance Parallel Log Processing
```
Process a massive log file at /data/system_logs.txt (>5GB) using parallel processing. Use 4 workers with 200MB chunks, then filter for errors and export results.
```

**Tools called:**
- `parallel_sort_large_file` - High-performance parallel sorting
- `filter_by_log_level` - Filter for error-level entries
- `export_to_json` - Export results with metadata

This prompt will:
- Use `parallel_sort_large_file` with optimized parallel processing settings
- Apply `filter_by_log_level` to focus on error-level entries
- Export comprehensive results using `export_to_json` with full metadata

### 3. Security Incident Investigation
```
Investigate potential security incidents in /security/auth.log. Filter for authentication failures between 2024-01-15 09:00:00 and 2024-01-15 18:00:00, detect patterns, and export findings.
```

**Tools called:**
- `filter_by_time_range` - Focus on incident time window
- `filter_by_keyword` - Search for authentication-related keywords
- `detect_log_patterns` - Identify suspicious patterns and anomalies
- `export_to_csv` - Export findings for security team analysis

This prompt will:
- Use `filter_by_time_range` to focus on the incident time window
- Apply `filter_by_keyword` to identify authentication-related entries
- Utilize `detect_log_patterns` to find suspicious activity patterns
- Export structured data using `export_to_csv` for security analysis

### 4. DevOps Monitoring and Alerting
```
Monitor application health by analyzing recent logs at /apps/microservice.log. Apply the 'errors_only' preset, analyze statistics, and generate an operational summary.
```

**Tools called:**
- `apply_filter_preset` - Apply predefined error filtering
- `analyze_log_statistics` - Generate operational metrics
- `generate_summary_report` - Create monitoring summary

This prompt will:
- Use `apply_filter_preset` with 'errors_only' for focused error analysis
- Apply `analyze_log_statistics` to extract operational health metrics
- Generate actionable insights using `generate_summary_report`

### 5. Performance Analysis and Optimization
```
Analyze performance issues in /performance/api_logs.txt. Filter for response time keywords, detect performance patterns, and export detailed analysis for optimization planning.
```

**Tools called:**
- `filter_by_keyword` - Search for performance-related keywords
- `detect_log_patterns` - Identify performance degradation patterns
- `analyze_log_statistics` - Generate performance metrics
- `export_to_text` - Export human-readable analysis

This prompt will:
- Use `filter_by_keyword` to focus on performance-related log entries
- Apply `detect_log_patterns` to identify performance degradation trends
- Generate comprehensive metrics using `analyze_log_statistics`
- Create readable analysis report using `export_to_text`

### 6. Comprehensive Log Management Workflow
```
Implement complete log management for /system/combined.log. Sort chronologically, apply multiple filters (exclude debug, focus on warnings and errors), analyze patterns, and create multiple export formats.
```

**Tools called:**
- `sort_log_by_timestamp` - Chronological organization
- `filter_logs` - Complex multi-condition filtering
- `detect_log_patterns` - Pattern and anomaly detection
- `export_to_json` - Structured data export
- `export_to_csv` - Spreadsheet-compatible export
- `generate_summary_report` - Executive summary

This prompt will:
- Use `sort_log_by_timestamp` for chronological organization
- Apply `filter_logs` with complex multi-condition logic
- Utilize `detect_log_patterns` for comprehensive pattern analysis
- Generate multiple export formats for different stakeholder needs
- Create comprehensive management summary with actionable insights