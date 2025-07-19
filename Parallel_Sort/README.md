# Parallel Sort MCP Server

A comprehensive Model Context Protocol (MCP) server for advanced log file processing and analysis. Provides parallel sorting capabilities, statistical analysis, pattern detection, and flexible export options for large-scale log data processing.

## Implemented MCP Capabilities 

| Capability | Type | Description |
|------------|------|-------------|
| `sort_log_by_timestamp` | Tool | Sort log file lines by timestamps in YYYY-MM-DD HH:MM:SS format |
| `parallel_sort_large_file` | Tool | Sort large log files using parallel processing with chunked approach |
| `analyze_log_statistics` | Tool | Generate comprehensive statistics and analysis for log files |
| `detect_log_patterns` | Tool | Detect patterns including anomalies, error clusters, and trending issues |
| `filter_logs` | Tool | Filter log entries based on multiple conditions with complex logical operations |
| `filter_by_time_range` | Tool | Filter log entries by time range using start and end timestamps |
| `filter_by_log_level` | Tool | Filter log entries by log level (ERROR, WARN, INFO, DEBUG, etc.) |
| `filter_by_keyword` | Tool | Filter log entries by keywords in the message content |
| `apply_filter_preset` | Tool | Apply predefined filter presets for common use cases |
| `export_to_json` | Tool | Export log processing results to JSON format |
| `export_to_csv` | Tool | Export log entries to CSV format with structured columns |
| `export_to_text` | Tool | Export log entries to plain text format |
| `generate_summary_report` | Tool | Generate comprehensive summary report with statistics and analysis |

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iowarp/scientific-mcps.git
   cd scientific-mcps/Parallel_Sort
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Test the installation:**
   ```bash
   uv run python -m pytest tests/ -v
   ```

### Running the Server

```bash
# Using the script
uv run parallel-sort-mcp

# Direct execution
uv run python src/parallel_sort/server.py
```

## Usage Examples

### Basic Log Sorting
```python
# Sort a log file by timestamp
sort_log_by_timestamp("application.log")
```

### Parallel Processing for Large Files
```python
# Sort large files with parallel processing
parallel_sort_large_file("huge_log.txt", chunk_size_mb=100, max_workers=4)
```

### Log Analysis
```python
# Generate comprehensive statistics
analyze_log_statistics("application.log")

# Detect patterns and anomalies
detect_log_patterns("application.log")
```

### Advanced Filtering
```python
# Filter by time range
filter_by_time_range("app.log", "2024-01-01 08:00:00", "2024-01-01 18:00:00")

# Filter by log level
filter_by_log_level("app.log", "ERROR,FATAL", exclude=False)

# Apply preset filters
apply_filter_preset("app.log", "errors_only")
```

### Export Options
```python
# Export to different formats
export_to_json(data, include_metadata=True)
export_to_csv(data, include_headers=True)
generate_summary_report(data)
```

## Core Features

- **Parallel Processing**: True parallel sorting for large files using multiprocessing
- **Advanced Analytics**: Comprehensive statistics, pattern detection, and temporal analysis
- **Flexible Filtering**: Multi-condition filtering with logical operations and presets
- **Multiple Export Formats**: JSON, CSV, plain text, and summary reports
- **Memory Efficient**: Streaming processing and configurable chunk sizes
- **Error Handling**: Robust handling of invalid timestamps and malformed entries

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run specific test files
uv run pytest tests/test_sort_handler.py
uv run pytest tests/test_export_handler.py

# Run with verbose output
uv run pytest -v
```

## Configuration

The server supports environment variables:

- `MCP_TRANSPORT`: Transport type (`stdio` or `sse`)
- `MCP_SSE_HOST`: Host for SSE transport (default: `0.0.0.0`)
- `MCP_SSE_PORT`: Port for SSE transport (default: `8000`)

## Integration with MCP Clients

### Claude Desktop
Add to your configuration:
```json
{
  "parallel-sort-mcp": {
    "command": "uv",
    "args": [
      "--directory", "/path/to/scientific-mcps/Parallel_Sort",
      "run", "parallel-sort-mcp"
    ]
  }
}
```

### Other MCP Clients
The server uses stdio transport by default and is compatible with any MCP client.

## Project Structure

```
Parallel_Sort/
├── README.md
├── pyproject.toml
├── uv.lock
├── src/
│   └── parallel_sort/
│       ├── __init__.py
│       ├── server.py
│       ├── mcp_handlers.py
│       └── implementation/
│           ├── __init__.py
│           ├── sort_handler.py
│           ├── statistics_handler.py
│           ├── pattern_detection.py
│           ├── filter_handler.py
│           ├── export_handler.py
│           └── parallel_processor.py
└── tests/
    ├── __init__.py
    ├── test_sort_handler.py
    ├── test_statistics_handler.py
    ├── test_pattern_detection.py
    ├── test_filter_handler.py
    ├── test_export_handler.py
    ├── test_mcp_handlers.py
    └── test_server.py
```

## Filter Presets

Available predefined filter presets:

- `errors_only`: Show only ERROR, FATAL, and CRITICAL entries
- `warnings_and_errors`: Show WARNING and error level entries
- `exclude_debug`: Exclude DEBUG and TRACE entries
- `connection_issues`: Find connection-related issues
- `authentication_events`: Find authentication-related events

## Performance Features

### Parallel Processing
- Automatic detection of large files (>100MB default)
- Configurable chunk sizes for memory efficiency
- Multi-core processing with worker pools
- Intelligent merging of sorted chunks

### Memory Optimization
- Streaming file processing for large datasets
- Temporary file cleanup
- Configurable memory usage limits
- Efficient data structures for sorting

## Use Cases

- **DevOps & System Administration**: Analyze application logs, monitor system health
- **Security Analysis**: Detect authentication failures, identify anomalous patterns
- **Performance Monitoring**: Analyze response times, identify bottlenecks
- **Data Science & Analytics**: Process large log datasets, extract patterns for ML

## Documentation

- [Project Structure](src/parallel_sort/)
- [Test Examples](tests/)
- [Capabilities Documentation](src/parallel_sort/implementation/)

## License

MIT License - see the main repository for details.