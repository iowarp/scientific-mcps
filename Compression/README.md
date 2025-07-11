# Compression MCP Server

A comprehensive Model Context Protocol (MCP) server for file compression and decompression operations. This server enables LLMs to compress, decompress, and manage compressed files with support for multiple compression formats and advanced features like batch processing, integrity verification, and password protection.

## Key Features

- **Multi-Format Support**  
  Supports gzip, bz2, zip, zlib, tar.gz, and tar.bz2 compression formats with automatic format detection.

- **Advanced Compression Operations**  
  Provides single file compression, directory compression, batch processing, and memory-efficient streaming for large files.

- **Integrity & Security**  
  Includes checksum verification, password-protected archives, and comprehensive error handling.

- **Performance Optimization**  
  Configurable compression levels, progress tracking, and memory-efficient streaming for optimal performance.

- **Cross-Platform Compatibility**  
  Works seamlessly across Windows, Linux, and macOS with consistent behavior and file handling.

- **Standardized MCP Interface**  
  Exposes all functionality via the MCP JSON-RPC protocol for seamless integration with language models.

## Capabilities

1. **compress_file**: Compress single files using gzip, bz2, zip, or zlib formats.

2. **decompress_file**: Decompress compressed files with automatic format detection.

3. **compress_directory**: Compress entire directories into zip, tar.gz, or tar.bz2 archives.

4. **extract_archive**: Extract files from various archive formats.

5. **list_archive_contents**: List archive contents without extracting files.

6. **batch_compress**: Compress multiple files in batch with progress tracking.

7. **verify_integrity**: Verify file integrity using MD5, SHA1, or SHA256 checksums.

8. **get_compression_stats**: Analyze compression efficiency and get format recommendations.

9. **create_password_protected_archive**: Create password-protected ZIP archives.

10. **stream_compress**: Memory-efficient streaming compression for large files.

11. **detect_compression_format**: Auto-detect compression format from file headers.

---

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Setup

### 1. Navigate to Compression Directory
```bash
cd /path/to/scientific-mcps/Compression
```
### 2. Install Dependencies
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
   uv run compression-mcp
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.

--- 

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Compression MCP server, use the main `wrp.py` client. You will need to configure it to point to the Compression server.

1.  **Configure:** Ensure that `Compression` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Compression
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
claude add mcp compression -- uv --directory ~/scientific-mcps/Compression run compression-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"compression-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/scientific-mcps/Compression/",
        "run",
        "compression-mcp"
    ]
}
```

---

## Examples

**Note: Use absolute paths for all file operations to ensure proper file access.**

1. **Compress a single file with gzip**

   ```python
   # Compress a large log file with high compression
   result = compress_file("/data/server.log", compression_type="gzip", compression_level=9)
   ```

2. **Compress entire directory to archive**

   ```python
   # Archive project directory excluding temporary files
   result = compress_directory("/data/project", compression_type="zip", exclude_patterns=["*.tmp", "*.log"])
   ```

3. **Batch compress multiple files**

   ```python
   # Compress multiple data files with progress tracking
   result = batch_compress(["/data/file1.txt", "/data/file2.txt"], compression_type="bz2")
   ```

4. **Create password-protected archive**

   ```python
   # Create secure archive with password protection
   result = create_password_protected_archive(["/data/sensitive.txt"], "/data/secure.zip", "mypassword")
   ```

5. **Verify file integrity and get compression statistics**

   ```python
   # Verify compressed file integrity and analyze compression efficiency
   integrity = verify_integrity("/data/compressed.gz", checksum_type="sha256")
   stats = get_compression_stats("/data/compressed.gz")
   ```

**For detailed examples and use cases, see the [capability_test.py](capability_test.py) file.**

## Supported Compression Formats

| Format | Extensions | Description | Best For |
|--------|------------|-------------|----------|
| **gzip** | `.gz` | Fast compression/decompression | General purpose, streaming |
| **bz2** | `.bz2` | High compression ratio | Storage optimization |
| **zip** | `.zip` | Archive format with password support | Multiple files, security |
| **zlib** | `.zlib` | Raw compression for memory efficiency | In-memory operations |
| **tar.gz** | `.tar.gz`, `.tgz` | Compressed tar archive | Unix/Linux directories |
| **tar.bz2** | `.tar.bz2`, `.tbz2` | High-ratio compressed tar | Long-term storage |

## Performance Characteristics

### Compression Levels
- **Level 1**: Fastest compression, lower ratio
- **Level 6**: Balanced speed and compression (default)
- **Level 9**: Maximum compression, slower speed

### Memory Usage
- **Standard compression**: Loads entire file into memory
- **Streaming compression**: Processes files in chunks (configurable)
- **Large file support**: Automatic streaming for files > 100MB

### Speed Comparison (typical)
1. **zlib**: Fastest
2. **gzip**: Fast
3. **bz2**: Slower, better compression
4. **zip**: Moderate (depends on content)

## Error Handling

The server provides comprehensive error handling with:
- Detailed error messages for debugging
- Error type classification for different failure modes
- Validation for file paths and compression formats
- Graceful handling of memory limitations
- Permission and access control validation
- Integrity verification and corruption detection

## Project Structure
```text
Compression/
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Project documentation
├── pytest.ini              # Test configuration
├── capability_test.py       # Comprehensive functionality tests
├── data/                    # Sample data directory
├── src/                     # Source code directory
│   └── compression/
│       ├── __init__.py      # Package init
│       ├── server.py        # Main MCP server with FastMCP
│       ├── mcp_handlers.py  # MCP protocol handlers
│       └── capabilities/
│           ├── __init__.py
│           └── compression_utils.py    # Core compression utilities
├── tests/                   # Test suite
│   ├── test_compression_handlers.py # Unit tests for handlers
│   └── conftest.py          # Test fixtures
└── uv.lock                  # Dependency lock file
```

### Adding New Compression Formats

1. Add format definition to `compression_utils.py`
2. Implement handlers in `mcp_handlers.py`
3. Add format detection logic
4. Update tests and documentation

## Testing

### Run Capability Tests
```bash
uv run python capability_test.py
```

### Run Unit Tests
```bash
uv run pytest tests/ -v
```

All tests pass with zero warnings, ensuring reliable functionality across all compression capabilities.

## Performance Features

- **Memory optimization** for large files with streaming compression
- **Batch processing** capabilities for multiple files
- **Configurable compression levels** (1-9) for speed/ratio balance
- **Progress tracking** with visual progress bars
- **Cross-platform compatibility** with consistent behavior
- **Automatic format detection** from file headers

## Dependencies

Key dependencies managed through `pyproject.toml`:
- `fastmcp>=0.1.0` - FastMCP framework for MCP server implementation
- `tqdm>=4.66.0` - Progress bars for batch operations
- `tabulate>=0.9.0` - Table formatting for statistics
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