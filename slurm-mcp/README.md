# Slurm MCP Server

📖 **For complete usage, installation, and API documentation, see: [documentation/MCP_SERVER_GUIDE.md](documentation/MCP_SERVER_GUIDE.md)**  
📖 **For native Slurm installation, see: [slurm_installation/SLURM_INSTALLATION_GUIDE.md](slurm_installation/SLURM_INSTALLATION_GUIDE.md)**

A comprehensive Model Context Protocol (MCP) server implementation for submitting and managing Slurm jobs. This server provides a standardized interface for interacting with Slurm workload manager through the MCP protocol, enabling seamless integration with AI assistants and other MCP clients.

## Quick Start

```bash
# Clone and setup
cd slurm-mcp
uv sync

# Start the MCP server
./server_manager.sh start

# Test functionality  
python comprehensive_capability_test.py

# Stop the server
./server_manager.sh stop
```

## Features

- **🚀 Job Submission**: Submit Slurm jobs with specified core counts and resource requirements
- **📋 Job Management**: List, monitor, cancel, and get detailed information about jobs
- **🔧 Input Validation**: Comprehensive validation of script paths and resource requirements
- **⚡ Fast Performance**: Optimized for high-throughput job submissions
- **🛡️ Error Handling**: Robust error handling with detailed error messages
- **📊 Multiple Transports**: Support for both stdio and SSE (Server-Sent Events) transports
- **🧪 Comprehensive Testing**: Full test suite with unit, integration, and performance tests
- **🎯 Real Slurm Integration**: Direct integration with actual Slurm workload manager
- **📁 Organized Output**: All SLURM job outputs (.out/.err files) are automatically organized in `logs/slurm_output/`
- **🔧 Modular Architecture**: Separated capabilities for better maintainability and extensibility
- **🔄 Array Job Support**: Submit and manage Slurm array jobs with ease
- **📊 Cluster Monitoring**: Real-time cluster and node information retrieval

## Output Organization

All SLURM job output files are automatically organized in the `logs/slurm_output/` directory:

```
logs/
└── slurm_output/
    ├── slurm_1234.out       # Job stdout files
    ├── slurm_1234.err       # Job stderr files
    ├── slurm_5678_1.out     # Array job outputs (format: slurm_<array_id>_<task_id>.out)
    └── slurm_5678_1.err     # Array job errors
```

### File Naming Convention
- **Single Jobs**: `slurm_<job_id>.out` and `slurm_<job_id>.err`
- **Array Jobs**: `slurm_<array_job_id>_<task_id>.out` and `slurm_<array_job_id>_<task_id>.err`


## Architecture

### High-Level Architecture

The Slurm MCP Server follows a modular, layered architecture designed for scalability, maintainability, and extensibility:

```
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Client Layer                           │
│            (AI Assistants, CLI Tools, Web Apps)               │
└─────────────────────┬───────────────────────────────────────────┘
                      │ MCP Protocol (JSON-RPC 2.0)
┌─────────────────────▼───────────────────────────────────────────┐
│                   MCP Server Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Transport     │  │   Protocol      │  │   Tool          │ │
│  │   (stdio/SSE)   │  │   Handlers      │  │   Registry      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Function Calls
┌─────────────────────▼───────────────────────────────────────────┐
│                 Capabilities Layer                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐  │
│  │ Job Submit  │ │ Job Monitor │ │ Job Control │ │ Cluster  │  │
│  │ job_submiss │ │ job_status  │ │ job_cancel  │ │ cluster_ │  │
│  │ ion.py      │ │ job_details │ │ job_listing │ │ info.py  │  │
│  │ array_jobs  │ │ job_output  │ │             │ │ node_    │  │
│  │ .py         │ │ .py         │ │             │ │ info.py  │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │ System Calls
┌─────────────────────▼───────────────────────────────────────────┐
│                    System Layer                                │
│            SLURM Workload Manager (sbatch, squeue, etc.)       │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Project Structure

```
slurm-mcp/
├── README.md                          # Project documentation
├── pyproject.toml                     # Project configuration and dependencies
├── uv.lock                           # Dependency lock file
├── server_manager.sh                 # Server start/stop management script
├── move_slurm_outputs.sh             # Utility to organize output files
├── comprehensive_capability_test.py  # Complete functionality test
├── comprehensive_test.sh             # SLURM test job script
├── mcp_capabilities_demo.py          # MCP capabilities demonstration
├── test_real_functionality.py       # Real SLURM integration tests
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── server.py                     # Main MCP server implementation
│   ├── mcp_handlers.py              # MCP protocol handlers
│   └── capabilities/                 # Modular SLURM capabilities
│       ├── __init__.py              # Capability exports
│       ├── utils.py                 # Common utility functions
│       ├── slurm_handler.py         # Backward compatibility module
│       ├── job_submission.py        # Job submission functionality
│       ├── job_status.py            # Job status checking
│       ├── job_details.py           # Detailed job information
│       ├── job_output.py            # Job output retrieval
│       ├── job_listing.py           # Job queue listing
│       ├── job_cancellation.py      # Job cancellation
│       ├── cluster_info.py          # Cluster information
│       ├── queue_info.py            # Queue monitoring
│       ├── node_info.py             # Node information
│       └── array_jobs.py            # Array job submission
│
├── tests/                            # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py                  # Test configuration and fixtures
│   ├── test_capabilities.py         # Unit tests for SLURM capabilities
│   ├── test_mcp_handlers.py         # Unit tests for MCP handlers
│   ├── test_server_tools.py         # Tests for server async tools
│   ├── test_integration.py          # End-to-end integration tests
│   └── test_performance.py          # Performance and load tests
│
├── logs/                             # Organized output directory
│   └── slurm_output/                # SLURM job outputs (.out/.err files)
│       ├── slurm_<job_id>.out       # Single job stdout
│       ├── slurm_<job_id>.err       # Single job stderr
│       ├── slurm_<array_id>_<task>.out  # Array job outputs
│       └── slurm_<array_id>_<task>.err  # Array job errors
│
├── documentation/                    # Additional documentation
│   └── MCP_SERVER_GUIDE.md          # Complete usage guide
│
├── slurm_installation/               # SLURM installation utilities
│   ├── SLURM_INSTALLATION_GUIDE.md  # Installation instructions
│   ├── install_slurm.sh             # Automated installation script
│   ├── parallel_job.sh              # Example parallel job
│   ├── quick_native_test.sh         # Quick SLURM test
│   └── final_verification.sh        # Installation verification
│
└── slurm_mcp.egg-info/              # Package metadata
```

### Modular Capabilities Design

The capabilities are organized into focused, single-responsibility modules:

#### Core Job Management
- **`job_submission.py`**: Handles job submission with full parameter support
- **`job_status.py`**: Provides real-time job status checking
- **`job_details.py`**: Retrieves comprehensive job information
- **`job_output.py`**: Manages job output file access and retrieval
- **`job_listing.py`**: Lists and filters jobs in the queue
- **`job_cancellation.py`**: Handles job cancellation and termination

#### Advanced Features
- **`array_jobs.py`**: Specialized support for SLURM array jobs
- **`cluster_info.py`**: Provides cluster-wide information and status
- **`queue_info.py`**: Monitors partition and queue states
- **`node_info.py`**: Retrieves node status and resource information

#### Utilities and Compatibility
- **`utils.py`**: Common functions and utilities
- **`slurm_handler.py`**: Backward compatibility wrapper

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Installation

### Quick Setup

```bash
# Clone and navigate to the project
cd slurm-mcp

# Install dependencies using uv
uv sync

# Install development dependencies (if not already installed)
uv add pytest pytest-asyncio --dev
```

### Manual Setup

```bash
# Initialize uv environment
uv init slurm-mcp
cd slurm-mcp

# Add production dependencies
uv add "mcp[cli]"
uv add python-dotenv

# Add development dependencies
uv add pytest pytest-asyncio --dev
```

## Usage

### 1. Running the MCP Server

#### Stdio Transport (Default)
```bash
# Start server with stdio transport
uv run python src/server.py
```

#### SSE Transport (for web clients)
```bash
# Set environment variables for SSE transport
export MCP_TRANSPORT=sse
export MCP_SSE_HOST=0.0.0.0
export MCP_SSE_PORT=8000

# Start server with SSE transport
uv run python src/server.py
```

### 2. Testing the Server

#### Run All Tests
```bash
# Run the complete test suite
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=src
```

#### Run Integration Tests
```bash
# Run end-to-end integration tests
python tests/test_integration.py
```

#### Test Individual Components
```bash
# Test Slurm capabilities
uv run pytest tests/test_capabilities.py -v

# Test MCP handlers
uv run pytest tests/test_mcp_handlers.py -v

# Test server tools
uv run pytest tests/test_server_tools.py -v
```

### 3. Interactive Testing

```bash
# Start server with MCP inspector (for development)
uv run mcp dev src/server.py

# Direct JSON-RPC testing
cd slurm-mcp
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}}}' | uv run python src/server.py
```

## API Reference

### Available Tools

The Slurm MCP Server provides a comprehensive set of tools for managing SLURM jobs and cluster resources:

#### Job Management Tools

#### `submit_slurm_job`
Submits a Slurm job script with specified resource requirements.

**Parameters:**
- `script_path` (string, required): Path to the job script file
- `cores` (integer, required): Number of CPU cores to request (must be > 0)
- `memory` (string, optional): Memory requirement (e.g., "4G", "2048M")
- `time_limit` (string, optional): Time limit (e.g., "1:00:00")
- `job_name` (string, optional): Name for the job
- `partition` (string, optional): Slurm partition to use

**Returns:**
```json
{
  "job_id": "1234",
  "status": "submitted",
  "script_path": "my_job.sh",
  "cores": 4,
  "memory": "4G",
  "time_limit": "1:00:00",
  "job_name": "my_job",
  "partition": "compute",
  "message": "Job 1234 submitted successfully"
}
```

#### `check_job_status`
Check the status of a specific job.

**Parameters:**
- `job_id` (string, required): The Slurm job ID to check

**Returns:**
```json
{
  "job_id": "1234",
  "status": "RUNNING",
  "real_slurm": true
}
```

#### `get_job_details`
Get comprehensive details about a specific job.

**Parameters:**
- `job_id` (string, required): The Slurm job ID

**Returns:**
```json
{
  "job_id": "1234",
  "details": {
    "jobname": "my_job",
    "jobstate": "RUNNING",
    "partition": "compute",
    "runtime": "00:05:30",
    "timelimit": "01:00:00",
    "numnodes": "1",
    "numcpus": "4"
  },
  "real_slurm": true
}
```

#### `get_job_output`
Retrieve job output files (stdout/stderr).

**Parameters:**
- `job_id` (string, required): The Slurm job ID
- `output_type` (string, optional): Type of output ("stdout" or "stderr", default: "stdout")

**Returns:**
```json
{
  "job_id": "1234",
  "output_type": "stdout",
  "file_path": "logs/slurm_output/slurm_1234.out",
  "content": "Job output content...",
  "real_slurm": true
}
```

#### `cancel_slurm_job`
Cancel a running or pending job.

**Parameters:**
- `job_id` (string, required): The Slurm job ID to cancel

**Returns:**
```json
{
  "job_id": "1234",
  "status": "cancelled",
  "message": "Job 1234 cancelled successfully",
  "real_slurm": true
}
```

#### `list_slurm_jobs`
List jobs in the queue with optional filtering.

**Parameters:**
- `user_filter` (string, optional): Filter by username
- `state_filter` (string, optional): Filter by job state (e.g., "RUNNING", "PENDING")

**Returns:**
```json
{
  "jobs": [
    {
      "job_id": "1234",
      "state": "RUNNING",
      "name": "my_job",
      "user": "username",
      "time": "00:05:30",
      "nodes": "1",
      "cpus": "4"
    }
  ],
  "count": 1,
  "real_slurm": true
}
```

#### Cluster Information Tools

#### `get_slurm_info`
Get cluster information and status.

**Returns:**
```json
{
  "cluster_name": "my-cluster",
  "partitions": [
    {
      "partition": "compute",
      "avail_idle": "5/10",
      "timelimit": "infinite",
      "nodes": "10",
      "state": "up"
    }
  ],
  "real_slurm": true,
  "version": "slurm-wlm 23.11.4"
}
```

#### `get_queue_info`
Get queue and partition information.

**Parameters:**
- `partition` (string, optional): Specific partition to query

**Returns:**
```json
{
  "partitions": [
    {
      "partition": "compute",
      "state": "up",
      "nodes": "10",
      "cpus": "320",
      "memory": "1280GB"
    }
  ],
  "real_slurm": true
}
```

#### `get_node_info`
Get detailed node information.

**Parameters:**
- `node_name` (string, optional): Specific node to query

**Returns:**
```json
{
  "nodes": [
    {
      "nodename": "node001",
      "state": "idle",
      "cpus": "32",
      "memory": "128GB",
      "features": "gpu,nvme"
    }
  ],
  "real_slurm": true
}
```

#### Advanced Features

#### `submit_array_job`
Submit a Slurm array job.

**Parameters:**
- `script_path` (string, required): Path to the job script
- `array_range` (string, required): Array range (e.g., "1-10", "1-100:2")
- `cores` (integer, optional): Cores per array task (default: 1)
- `memory` (string, optional): Memory per array task
- `time_limit` (string, optional): Time limit per array task
- `job_name` (string, optional): Base name for the array job
- `partition` (string, optional): Slurm partition to use

**Returns:**
```json
{
  "array_job_id": "1234",
  "array_range": "1-10",
  "status": "submitted",
  "total_tasks": 10,
  "cores_per_task": 2,
  "message": "Array job 1234 with 10 tasks submitted successfully",
  "real_slurm": true
}
```

### Error Responses

All tools return standardized error responses:

```json
{
  "content": [{"text": "{\"error\": \"Error description\"}"}],
  "_meta": {"tool": "tool_name", "error": "ErrorType"},
  "isError": true
}
```

### MCP Protocol Flow

1. **Initialize**: Client sends initialization request
2. **List Tools**: Client requests available tools
3. **Call Tool**: Client calls tool with parameters
4. **Response**: Server returns results or error

## Examples

### Basic Job Submission

Create a job script and submit it via MCP:
```bash
# Create job script
cat > my_job.sh << 'EOF'
#!/bin/bash
#SBATCH --job-name=test_job
echo "Hello from Slurm job!"
sleep 10
echo "Job completed"
EOF

# Submit via comprehensive test
python comprehensive_capability_test.py
```

### Using Python Client

```python
import json
import subprocess

def submit_job(script_path, cores):
    # MCP protocol requests
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", 
         "params": {"protocolVersion": "2024-11-05", "capabilities": {}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": "submit_slurm_job", 
                   "arguments": {"script_path": script_path, "cores": cores}}}
    ]
    
    # Submit to MCP server
    input_str = '\n'.join(json.dumps(req) for req in requests) + '\n'
    result = subprocess.run(['uv', 'run', 'python', 'src/server.py'],
                          input=input_str, capture_output=True, text=True)
    
    # Parse response
    responses = [json.loads(line) for line in result.stdout.strip().split('\n') if line.strip()]
    return responses[-1]

# Usage
response = submit_job("my_job.sh", 4)
print(f"Job submitted: {response}")
```

## Configuration

### Environment Variables

- `MCP_TRANSPORT`: Transport type (`stdio` or `sse`, default: `stdio`)
- `MCP_SSE_HOST`: Host for SSE transport (default: `0.0.0.0`)
- `MCP_SSE_PORT`: Port for SSE transport (default: `8000`)

### Configuration File

Create a `.env` file in the project root:
```env
MCP_TRANSPORT=stdio
MCP_SSE_HOST=localhost
MCP_SSE_PORT=8000
```

## Testing

### Quick Testing
```bash
# Run comprehensive capability test
python comprehensive_capability_test.py

# Run all tests
uv run pytest tests/ -v

# Run specific test categories
uv run pytest tests/test_capabilities.py -v
uv run pytest tests/test_mcp_handlers.py -v
```

## Development

### Adding New Features

1. **Add Capability**: Implement core logic in `src/capabilities/`
2. **Add Handler**: Create MCP wrapper in `src/mcp_handlers.py`
3. **Add Tool**: Register tool in `src/server.py`
4. **Add Tests**: Create comprehensive tests in `tests/`

### Development Workflow

```bash
# Setup development environment
git clone <repository>
cd slurm-mcp
uv sync

# Make changes and test
uv run pytest tests/ -v
python comprehensive_capability_test.py
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure proper Python path
2. **MCP Protocol Errors**: Check server logs
3. **SLURM Not Available**: Install SLURM or run in mock mode

### Debug Mode

```bash
export PYTHONPATH="$(pwd)/src"
export MCP_DEBUG=1
uv run python src/server.py
```


## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For questions and support:
- Create an issue in the repository
- Check the troubleshooting section
- Review test examples for usage patterns

