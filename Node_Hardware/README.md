# Node Hardware MCP Server

## Overview

The Node Hardware MCP Server is a comprehensive Model Context Protocol (MCP) server implementation that provides detailed hardware monitoring and system information capabilities. This server enables AI assistants and other MCP clients to retrieve comprehensive hardware information through a standardized protocol.

The server acts as a bridge between MCP clients and system hardware information, providing detailed CPU, memory, disk, network, and system monitoring capabilities.

## Features

### Core Capabilities
- 🖥️ **CPU Information**: Detailed CPU information including cores, frequency, and usage statistics
- 💾 **Memory Monitoring**: Comprehensive memory usage including virtual and swap memory
- 💿 **Disk Information**: Disk usage, partitions, and I/O statistics
- 🌐 **Network Monitoring**: Network interfaces, statistics, and connection information
- 🖥️ **System Information**: OS details, uptime, users, and system metrics
- 📊 **Process Monitoring**: Running processes with resource usage
- 🔧 **Hardware Summary**: Comprehensive hardware overview
- ⚡ **Performance Monitoring**: Real-time performance metrics
- 🎮 **GPU Information**: GPU detection and information (if available)
- 🌡️ **Sensor Information**: Temperature and sensor monitoring

### MCP Tools Available
1. **get_cpu_info** - Get detailed CPU information
2. **get_memory_info** - Get memory usage statistics
3. **get_disk_info** - Get disk usage and partition information
4. **get_network_info** - Get network interface information
5. **get_system_info** - Get general system information
6. **get_process_info** - Get running process information
7. **get_hardware_summary** - Get comprehensive hardware summary
8. **monitor_performance** - Monitor real-time performance metrics
9. **get_gpu_info** - Get GPU information (if available)
10. **get_sensor_info** - Get temperature and sensor information

## Prerequisites

### System Requirements
- Linux, macOS, or Windows operating system
- Python 3.10 or higher
- UV package manager (recommended) or pip

### Python Dependencies
- `mcp[cli]>=0.1.0` - MCP framework
- `pytest-asyncio>=1.0.0` - Async testing support
- `python-dotenv>=1.0.0` - Environment variable management
- `psutil>=5.9.0` - System and process utilities
- `fastapi>=0.95.0` - Web framework (if using HTTP transport)
- `uvicorn>=0.21.0` - ASGI server
- `pydantic>=1.10.0` - Data validation
- `pytest>=7.2.0` - Testing framework
- `requests>=2.28.0` - HTTP client

## Setup

### 1. Navigate to Node_Hardware Directory
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

### 3. Check Configuration
Ensure `pyproject.toml` is properly configured with all dependencies.

## Quick Start

### 1. Start the MCP Server
```bash
# Using UV
uv run python src/node_hardware/server.py

# Or using Python directly
python src/node_hardware/server.py

# Or using the script entry point
uv run node-hardware-mcp
```

### 2. Test Basic Functionality
The server will start and listen for MCP protocol connections via stdio transport by default.

### 3. Use with MCP Client
Connect any MCP-compatible client to interact with the hardware monitoring tools.

## Project Structure

```
Node_Hardware/
├── README.md                      # This documentation
├── pyproject.toml                 # Project configuration and dependencies
├── src/                           # Source code
│   ├── __init__.py
│   └── node_hardware/              # Main package directory
│       ├── __init__.py
│       ├── server.py              # Main MCP server
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
└── tests/                         # Test suite
    ├── __init__.py
    ├── test_mcp_handlers.py       # MCP handler tests
    └── test_server.py             # Server tests
```

## Configuration

### Environment Variables
- `MCP_TRANSPORT`: Transport type ("stdio" or "sse", default: "stdio")
- `MCP_SSE_HOST`: Host for SSE transport (default: "0.0.0.0")
- `MCP_SSE_PORT`: Port for SSE transport (default: "8000")

### Transport Options
- **stdio**: Standard input/output transport (default)
- **sse**: Server-Sent Events transport for web clients

## Testing

### Running Tests
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test files
uv run pytest tests/test_mcp_handlers.py -v
uv run pytest tests/test_server.py -v


# Run capability demo
uv run python capability_test.py
uv run python demo.py
```

## Development

### Adding New Capabilities
1. Create a new capability module in `src/node_hardware/capabilities/`
2. Add the capability import to `mcp_handlers.py`
3. Create a new handler function in `mcp_handlers.py`
4. Add the MCP tool to `server.py`
5. Write tests for the new capability

### Code Structure
- Each capability is a separate module with a single main function
- Handlers wrap capabilities for MCP protocol compliance
- Server.py defines the MCP tools and routes them to handlers
- All capabilities use common utility functions from `utils.py`

## License

This project is part of the scientific-mcps collection and follows the same licensing terms.

