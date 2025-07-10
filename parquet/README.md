# Parquet MCP Server

A comprehensive Model Context Protocol (MCP) server for Parquet file operations using PyArrow. This server enables LLMs to read, write, analyze, and convert Parquet files with advanced features like schema management, statistics, and data quality checks.

## Key Features

- **Complete Parquet Operations**  
  Uses PyArrow to read, write, and manipulate Parquet files with support for all standard data types and compression algorithms.

- **Advanced Analytics**  
  Provides statistical analysis, data quality checks, and comprehensive metadata extraction for data exploration.

- **Format Conversion**  
  Seamlessly converts between Parquet, CSV, and JSON formats for maximum interoperability.

- **Schema Management**  
  Inspect, validate, and manage Parquet schemas with detailed type information and column metadata.

- **Memory Optimization**  
  Handles large datasets efficiently with batch processing and column pruning capabilities.

- **Standardized MCP Interface**  
  Exposes all functionality via the MCP JSON-RPC protocol for seamless integration with language models.

## Capabilities

1. **read_parquet**: Read Parquet files with optional column selection and row limits.

2. **write_parquet**: Write data to Parquet files with configurable compression algorithms.

3. **get_parquet_schema**: Extract detailed schema information including column types and metadata.

4. **get_parquet_metadata**: Retrieve comprehensive file metadata including row counts and compression stats.

5. **get_column_statistics**: Calculate statistical measures for specified columns (min, max, mean, std, etc.).

6. **check_data_quality**: Perform data quality assessment including null counts and uniqueness checks.

7. **convert_parquet_to_csv**: Convert Parquet files to CSV format with customizable options.

8. **convert_csv_to_parquet**: Convert CSV files to Parquet format with schema inference.

9. **convert_parquet_to_json**: Export Parquet data to JSON format with proper type handling.

10. **convert_json_to_parquet**: Import JSON data into Parquet format with automatic schema detection.

11. **get_compression_stats**: Analyze compression efficiency and storage statistics.

---

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Setup

### 1. Navigate to Plot Directory
```bash
cd /path/to/scientific-mcps/parquet
```
### 2.Install Dependencies
Using UV (recommended):
```bash
uv sync
```

Using pip:
```bash
pip install -e .
```
**Run the MCP Server directly:**

   ```bash
   uv run parquet-mcp
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.

--- 

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Parquet MCP server, use the main `wrp.py` client. You will need to configure it to point to the Parquet server.

1.  **Configure:** Ensure that `Parquet` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Parquet
      # - Adios
      # - HDF5
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```
    
    For detailed setup with local LLMs and other providers, see the [Complete Installation Guide](../bin/docs/Installation.md).

### Running the Server on Claude Command Line Interface Tool.

1. Install the Claude Code using NPM,
Install [NodeJS 18+](https://nodejs.org/en/download), then run:

```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp parquet -- uv --directory ~/scientific-mcps/parquet run parquet-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"parquet-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/scientific-mcps/parquet/",
        "run",
        "parquet-mcp"
    ]
}
```

---

## Examples

**Note: Use absolute paths for all file operations to ensure proper file access.**

1. **Read Parquet file with specific columns**

   ```python
   # Read temperature and humidity columns from weather data
   result = read_parquet("/data/weather.parquet", columns=["temperature", "humidity"])
   ```

2. **Get comprehensive statistics for numerical columns**

   ```python
   # Analyze sales data statistics
   stats = get_column_statistics("/data/sales.parquet", columns=["revenue", "quantity"])
   ```

3. **Convert formats and analyze data quality**

   ```python
   # Convert CSV to Parquet and check data quality
   convert_csv_to_parquet("/data/raw_data.csv", "/data/processed_data.parquet")
   quality = check_data_quality("/data/processed_data.parquet")
   ```

4. **Schema management and metadata extraction**

   ```python
   # Inspect file structure and metadata
   schema = get_parquet_schema("/data/dataset.parquet")
   metadata = get_parquet_metadata("/data/dataset.parquet")
   ```

**For detailed examples and use cases, see the [capability_test.py](capability_test.py) file.**

## Project Structure
```text
parquet/
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Project documentation
├── pytest.ini              # Test configuration
├── capability_test.py       # Comprehensive functionality tests
├── data/                    # Sample data directory
├── docs/                    # Additional documentation
├── src/                     # Source code directory
│   └── parquet/
│       ├── __init__.py      # Package init
│       ├── server.py        # Main MCP server with FastMCP
│       ├── mcp_handlers.py  # MCP protocol handlers
│       └── capabilities/
│           ├── __init__.py
│           ├── parquet_io.py           # Core read/write operations
│           ├── metadata.py             # Schema and metadata extraction
│           ├── statistics.py           # Statistical analysis
│           └── format_conversion.py    # Format conversion utilities
├── tests/                   # Test suite
│   ├── test_capabilities.py # Unit tests for capabilities
│   ├── test_mcp_handlers.py # Integration tests for MCP handlers
│   └── conftest.py          # Test fixtures
└── uv.lock                  # Dependency lock file
```
## Data Types Support

The server supports all standard PyArrow/Parquet data types:
- **Numeric types**: int8, int16, int32, int64, uint8, uint16, uint32, uint64, float32, float64
- **String types**: string, large_string
- **Boolean type**: bool
- **Temporal types**: date32, date64, timestamp, time32, time64
- **Binary types**: binary, large_binary
- **Complex types**: list, struct, map

## Compression Algorithms

Supported compression algorithms:
- **snappy** (default) - Fast compression/decompression
- **gzip** - Good compression ratio
- **lz4** - Very fast compression
- **brotli** - High compression ratio
- **zstd** - Balanced speed and compression

## Testing

### Run Capability Tests
```bash
uv run python capability_test.py
```

### Run Unit Tests
```bash
uv run pytest tests/ -v
```

All tests pass with zero warnings, ensuring reliable functionality across all capabilities.

## Error Handling

The server provides comprehensive error handling with:
- Detailed error messages for debugging
- Error type classification for different failure modes
- Validation for file paths and data formats
- Graceful handling of memory limitations
- Schema validation and type checking errors

## Performance Features

- **Memory optimization** for large files
- **Batch processing** capabilities
- **Lazy loading** of data
- **Column pruning** for efficient reads
- **Predicate pushdown** support
- **Parallel processing** where applicable

## Dependencies

Key dependencies managed through `pyproject.toml`:
- `fastmcp>=0.1.0` - FastMCP framework for MCP server implementation
- `pyarrow>=19.0.1` - Apache Arrow Python library for Parquet operations
- `pandas>=2.2.3` - Data manipulation and analysis library
- `pytest>=8.3.5` - Testing framework
- `pytest-asyncio>=0.26.0` - Async testing support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Submit a pull request

## License

This project is part of the Scientific MCPs collection and follows the same licensing terms.

