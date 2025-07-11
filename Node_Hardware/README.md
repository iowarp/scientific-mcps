# Node Hardware MCP Server

A comprehensive Model Context Protocol (MCP) server for hardware monitoring and system information retrieval. This server enables LLMs to access detailed hardware information, monitor system performance, and analyze resource utilization through standardized MCP protocols.

## Key Features

- **Complete Hardware Monitoring**  
  Provides detailed information about CPU, memory, disk, network, and GPU components with real-time statistics and performance metrics.

- **System Information**  
  Retrieves comprehensive OS details, uptime, user information, and system configuration data for complete system analysis.

- **Process Management**  
  Monitors running processes with resource usage statistics, providing insights into system performance and application behavior.

- **Performance Analytics**  
  Offers real-time performance monitoring with CPU usage, memory utilization, and I/O statistics for system optimization.

- **Sensor Integration**  
  Accesses temperature sensors and hardware monitoring data where available for thermal management insights.

- **Standardized MCP Interface**  
  Exposes all functionality via the MCP JSON-RPC protocol for seamless integration with language models.

## Capabilities

1. **cpu_info**: Get detailed CPU information including cores, frequency, architecture, and usage statistics.

2. **memory_info**: Retrieve comprehensive memory usage including virtual memory, swap usage, and available memory.

3. **disk_info**: Get disk usage statistics, partition information, and I/O performance metrics.

4. **network_info**: Monitor network interfaces, connection statistics, and network performance data.

5. **system_info**: Retrieve general system information including OS details, uptime, and system configuration.

6. **process_info**: Monitor running processes with resource usage, PIDs, and process details.

7. **hardware_summary**: Get comprehensive hardware overview combining all system components.

8. **performance_monitor**: Monitor real-time performance metrics including CPU, memory, and I/O utilization.

9. **gpu_info**: Get GPU information and statistics where available.

10. **sensor_info**: Access temperature sensors and hardware monitoring data.

---

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Setup

### 1. Navigate to Node Hardware Directory
```bash
cd /path/to/scientific-mcps/Node_Hardware
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
   uv run node-hardware-mcp
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.

--- 

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Node Hardware MCP server, use the main `wrp.py` client. You will need to configure it to point to the Node Hardware server.

1.  **Configure:** Ensure that `Node_Hardware` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Node_Hardware
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
claude add mcp node-hardware -- uv --directory ~/scientific-mcps/Node_Hardware run node-hardware-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"node-hardware-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/scientific-mcps/Node_Hardware/",
        "run",
        "node-hardware-mcp"
    ]
}
```

---

## Examples

**Note: Use absolute paths for all file operations to ensure proper file access.**

1. **Get comprehensive CPU information**

   ```python
   # Get detailed CPU specifications and current usage
   cpu_info = cpu_info()
   ```

2. **Monitor system performance in real-time**

   ```python
   # Get current performance metrics
   performance = performance_monitor()
   ```

3. **Analyze memory usage and availability**

   ```python
   # Get detailed memory statistics
   memory_info = memory_info()
   
   # Get comprehensive hardware overview
   hardware_summary = hardware_summary()
   ```

4. **Monitor running processes and resource usage**

   ```python
   # Get running process information
   processes = process_info()
   
   # Get disk usage and I/O statistics
   disk_info = disk_info()
   ```

**For detailed examples and use cases, see the [capability_test.py](capability_test.py) and [demo.py](demo.py) files.**

## Project Structure
```text
Node_Hardware/
├── pyproject.toml                 # Project metadata & dependencies
├── README.md                      # Project documentation
├── capability_test.py             # Comprehensive functionality tests
├── demo.py                        # Demo script for capabilities
├── src/                           # Source code directory
│   └── node_hardware/             # Main package directory
│       ├── __init__.py            # Package init
│       ├── server.py              # Main MCP server with FastMCP
│       ├── mcp_handlers.py        # MCP protocol handlers
│       └── capabilities/          # Individual capability modules
│           ├── __init__.py
│           ├── utils.py           # Utility functions
│           ├── cpu_info.py        # CPU information
│           ├── memory_info.py     # Memory information
│           ├── disk_info.py       # Disk information
│           ├── network_info.py    # Network information
│           ├── system_info.py     # System information
│           ├── process_info.py    # Process information
│           ├── hardware_summary.py # Hardware summary
│           ├── performance_monitor.py # Performance monitoring
│           ├── gpu_info.py        # GPU information
│           └── sensor_info.py     # Sensor information
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_mcp_handlers.py       # Integration tests for MCP handlers
│   └── test_server.py             # Server tests
└── uv.lock                        # Dependency lock file
```

## Hardware Information Support

The server provides comprehensive information about:
- **CPU**: Architecture, cores, threads, frequency, cache, instruction sets
- **Memory**: Total RAM, available memory, swap usage, memory type
- **Storage**: Disk usage, partition information, filesystem details, I/O statistics
- **Network**: Interface information, IP addresses, connection statistics
- **GPU**: Graphics card information, memory, driver details (where available)
- **Sensors**: Temperature monitoring, fan speeds, voltage readings

## System Monitoring Features

Supported monitoring capabilities:
- **Real-time metrics** - Current CPU, memory, and I/O usage
- **Process monitoring** - Running processes with resource consumption
- **Performance analytics** - Historical and current performance data
- **System health** - Temperature, load averages, uptime statistics
- **Resource utilization** - Detailed breakdown of system resource usage

## Testing

### Run Capability Tests
```bash
uv run python capability_test.py
```

### Run Demo Script
```bash
uv run python demo.py
```

### Run Unit Tests
```bash
uv run pytest tests/ -v
```

All tests pass with zero warnings, ensuring reliable functionality across all hardware monitoring capabilities.

## Error Handling

The server provides comprehensive error handling with:
- Detailed error messages for debugging
- Error type classification for different failure modes
- Graceful handling of missing hardware components
- Platform-specific error handling for different operating systems
- Permission-based error handling for restricted system information

## Performance Features

- **Efficient data collection** using psutil library
- **Caching mechanisms** for frequently accessed data
- **Async operations** for non-blocking system queries
- **Resource optimization** for minimal system impact
- **Cross-platform compatibility** with Linux, macOS, and Windows

## Dependencies

Key dependencies managed through `pyproject.toml`:
- `fastmcp>=0.1.0` - FastMCP framework for MCP server implementation
- `psutil>=5.9.0` - System and process utilities for hardware monitoring
- `pytest>=7.2.0` - Testing framework
- `pytest-asyncio>=1.0.0` - Async testing support
- `python-dotenv>=1.0.0` - Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Submit a pull request

## License

This project is part of the Scientific MCPs collection and follows the same licensing terms.

