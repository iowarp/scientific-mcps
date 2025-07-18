# Compression MCP Server

A comprehensive Model Context Protocol (MCP) server for file compression capabilities. Provides efficient gzip compression with detailed statistics and error handling.

## Implemented MCP Capabilities

| Capability | Type | Description |
|------------|------|-------------|
| `compress_file` | Tool | Compress files using gzip compression with detailed statistics |

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iowarp/scientific-mcps.git
   cd scientific-mcps/Compression
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Test the installation:**
   ```bash
   uv run python -c "from src.compression_mcp.server import main; print('Installation successful')"
   ```

### Running the Server

```bash
# Using the script
uv run compression-mcp

# Direct execution
uv run python src/compression_mcp/server.py
```

## Usage Examples

### Compress a File
```python
# Compress a log file
compress_file("/path/to/file.log")
```

### Compress with Custom Path
```python
# Compress any file type
compress_file("/path/to/data.csv")
```

### Example Response
```json
{
  "content": [{
    "text": "File compressed successfully!\n\nOriginal file: /path/to/file.txt\nCompressed file: /path/to/file.txt.gz\nOriginal size: 1,024 bytes\nCompressed size: 512 bytes\nCompression ratio: 50.00%"
  }],
  "_meta": {
    "tool": "compress_file",
    "original_file": "/path/to/file.txt",
    "compressed_file": "/path/to/file.txt.gz",
    "original_size": 1024,
    "compressed_size": 512,
    "compression_ratio": 50.0
  },
  "isError": false
}
```

## Common Use Cases

- **Log File Compression** - Compress large log files to save storage space
- **Data Archival** - Archive CSV, text, and other data files
- **Backup Preparation** - Compress files before backup operations
- **Storage Optimization** - Reduce file sizes for better storage efficiency
- **Transfer Preparation** - Compress files for faster network transfers

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run specific test files
uv run pytest tests/test_compression_handler.py
uv run pytest tests/test_integration.py

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
  "compression-mcp": {
    "command": "uv",
    "args": [
      "--directory", "/path/to/scientific-mcps/Compression",
      "run", "compression-mcp"
    ]
  }
}
```

### Other MCP Clients
The server uses stdio transport by default and is compatible with any MCP client.

## Project Structure

```
Compression/
├── README.md
├── pyproject.toml
├── pytest.ini
├── data/
│   ├── data.csv
│   ├── huge_log.txt
│   ├── output.log
│   ├── small_log.txt
│   └── weather_data.parquet
├── src/
│   └── compression_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── mcp_handlers.py
│       └── capabilities/
│           ├── __init__.py
│           └── compression_base.py
└── tests/
    ├── __init__.py
    ├── test_compression_handler.py
    ├── test_mcp_handlers.py
    └── test_integration.py
```

## Features

- **Efficient Compression**: Gzip compression with optimal performance
- **Detailed Statistics**: Compression ratio and file size information
- **Error Handling**: Robust error handling with informative messages
- **Comprehensive Testing**: Full test coverage with integration tests
- **Empty File Support**: Handles empty files gracefully
- **Async Support**: Fully asynchronous for optimal performance

## Documentation

- [Core Compression Logic](src/compression_mcp/capabilities/compression_base.py)
- [MCP Handlers](src/compression_mcp/mcp_handlers.py)
- [Test Examples](tests/)

## License

MIT License - see the main repository for details.