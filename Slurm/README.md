# Slurm MCP Server

## Overview

The Slurm MCP Server is a comprehensive Model Context Protocol (MCP) server implementation that provides seamless integration with the Slurm workload manager. This server enables AI assistants and other MCP clients to interact with Slurm clusters through a standardized protocol, offering job submission, monitoring, and management capabilities.

The server acts as a bridge between MCP clients and Slurm, translating MCP requests into appropriate Slurm commands and returning structured responses. It supports both real Slurm environments and provides extensive testing capabilities.

## Features

### Core Capabilities
- 🚀 **Job Submission**: Submit Slurm jobs with customizable resource requirements
- 📋 **Job Management**: List, monitor, cancel, and retrieve detailed job information
- 🔧 **Resource Allocation**: Interactive node allocation using `salloc` command
- 📊 **Cluster Monitoring**: Real-time cluster and node information retrieval
- 🔄 **Array Job Support**: Submit and manage Slurm array jobs efficiently
- 📁 **Output Organization**: Automatic organization of job outputs in structured directories

### Advanced Features
- ⚡ **High Performance**: Optimized for high-throughput job operations
- 🛡️ **Robust Error Handling**: Comprehensive error handling with detailed messages
- 🧪 **Extensive Testing**: Full test suite with unit, integration, and performance tests
- 📊 **Multiple Transports**: Support for stdio and SSE (Server-Sent Events) transports
- 🎯 **Real Slurm Integration**: Direct integration with actual Slurm workload manager
- 🔧 **Modular Architecture**: Clean separation of concerns for maintainability
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
### MCP Tools Available
1. **submit_slurm_job** - Submit jobs to Slurm queue
2. **check_job_status** - Check status of submitted jobs
3. **cancel_slurm_job** - Cancel running or pending jobs
4. **list_slurm_jobs** - List jobs with filtering options
5. **get_slurm_info** - Get cluster information
6. **get_job_details** - Get detailed job information
7. **get_job_output** - Retrieve job output files
8. **get_queue_info** - Get queue/partition information
9. **submit_array_job** - Submit array jobs
10. **get_node_info** - Get node information
11. **allocate_nodes** - Interactive node allocation
12. **deallocate_allocation** - Release allocated nodes
13. **get_allocation_info** - Query allocation status

## Prerequisites

### System Requirements
- Linux operating system
- Python 3.10 or higher
- Slurm workload manager installed and configured
- UV package manager (recommended) or pip

### Slurm Requirements
- Slurm daemons running (`slurmctld`, `slurmd`)
- User access to Slurm commands (`sbatch`, `squeue`, `scancel`, `salloc`, etc.)
- Proper Slurm configuration with at least one partition

### Python Dependencies
- `mcp[cli]>=0.1.0` - MCP framework
- `pytest-asyncio>=1.0.0` - Async testing support
- `python-dotenv>=1.0.0` - Environment variable management
- `psutil>=5.9.0` - System process utilities
- `fastapi>=0.95.0` - Web framework (if using HTTP transport)
- `uvicorn>=0.21.0` - ASGI server
- `pydantic>=1.10.0` - Data validation
- `pytest>=7.2.0` - Testing framework
- `requests>=2.28.0` - HTTP client

## Setup

### 1. Clone and Navigate
```bash
cd /path/to/scientific-mcps/Slurm
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

### 3. Verify Slurm Installation
```bash
sinfo
squeue
sbatch --version
```

### 4. Check Configuration
Ensure `pyproject.toml` is properly configured with all dependencies.

## Quick Start

### 1. Start the MCP Server
```bash
# Using UV
uv run python src/server.py

# Or using the server manager script
./server_manager.sh start
```

### 2. Test Basic Functionality
```bash
# Run comprehensive capability test
uv run python comprehensive_capability_test.py

# Run specific demo
uv run python mcp_capabilities_demo.py
```

### 3. Submit a Test Job
```bash
# Create a simple test script
echo '#!/bin/bash\necho "Hello from Slurm MCP!"' > test.sh
chmod +x test.sh

# The server will handle job submission through MCP protocol
```

### 4. Stop the Server
```bash
./server_manager.sh stop
```

## Test

### Running All Tests
```bash
# Run complete test suite
uv run pytest tests/ -v

# Run specific test categories
uv run pytest tests/test_capabilities.py -v
uv run pytest tests/test_integration.py -v
uv run pytest tests/test_performance.py -v
```

### Test Results Overview
The test suite includes:
- **103 passed tests** with comprehensive coverage
- **Unit tests** for individual capabilities
- **Integration tests** for workflow testing
- **Performance tests** for load testing
- **Real Slurm tests** with actual cluster integration

### Demo Scripts
```bash
# Run all demo scripts
uv run python comprehensive_capability_test.py
uv run python final_demo.py
uv run python mcp_capabilities_demo.py
uv run python node_allocation_demo.py
uv run python node_allocation_demo_new.py
uv run python test_real_functionality.py
```

## Detailed Project Structure

```
slurm-mcp/
├── README.md                          # Original project documentation
├── readme_new.md                      # This comprehensive guide
├── pyproject.toml                     # Project configuration and dependencies
├── uv.lock                           # Dependency lock file
├── execution_commands_log.md         # Log of all executed commands
├── instruction.md                    # Setup instructions
├── IMPLEMENTATION_COMPLETE.md        # Implementation status
├── NODE_ALLOCATION_SUMMARY.md        # Node allocation feature summary
├── server_manager.sh                 # Server management script
├── server_manager.log               # Server logs
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── server.py                     # Main MCP server
│   ├── mcp_handlers.py              # MCP protocol handlers
│   └── capabilities/                 # Individual capability modules
│       ├── __init__.py
│       ├── slurm_handler.py         # Core Slurm handler
│       ├── job_submission.py        # Job submission logic
│       ├── job_status.py            # Job status checking
│       ├── job_cancellation.py      # Job cancellation
│       ├── job_listing.py           # Job listing
│       ├── job_details.py           # Detailed job information
│       ├── job_output.py            # Job output retrieval
│       ├── array_jobs.py            # Array job support
│       ├── cluster_info.py          # Cluster information
│       ├── queue_info.py            # Queue/partition info
│       ├── node_info.py             # Node information
│       ├── node_allocation.py       # Node allocation capabilities
│       └── utils.py                 # Utility functions
│
├── tests/                            # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py                   # Test configuration
│   ├── test_capabilities.py         # Unit tests for capabilities
│   ├── test_mcp_handlers.py         # MCP handler tests
│   ├── test_integration.py          # Integration tests
│   ├── test_performance.py          # Performance tests
│   ├── test_node_allocation.py      # Node allocation tests
│   └── test_server_tools.py         # Server tool tests
│
├── logs/                             # Log files and outputs
│   └── slurm_output/                # Organized SLURM job outputs
│       ├── slurm_<job_id>.out       # Job stdout files
│       └── slurm_<job_id>.err       # Job stderr files
│
├── documentation/                    # Additional documentation
│   └── MCP_SERVER_GUIDE.md          # Detailed usage guide
│
├── slurm_installation/              # Slurm installation guides
│   └── SLURM_INSTALLATION_GUIDE.md  # Native Slurm setup
│
├── old/                             # Legacy files
│
└── demo files                        # Demonstration scripts
    ├── comprehensive_capability_test.py
    ├── final_demo.py
    ├── mcp_capabilities_demo.py
    ├── node_allocation_demo.py
    ├── node_allocation_demo_new.py
    ├── test_real_functionality.py
    └── test_job.sh
```

### Architecture Components

#### MCP Server Layer
- **Transport Handling**: stdio and SSE transport support
- **Protocol Management**: JSON-RPC 2.0 MCP protocol implementation
- **Tool Registry**: Dynamic tool registration and management

#### Capabilities Layer
- **Modular Design**: Each capability in separate module
- **Error Handling**: Consistent error handling across all capabilities
- **Resource Management**: Proper cleanup and resource management

#### System Integration Layer
- **Slurm Commands**: Direct integration with Slurm CLI tools
- **Output Processing**: Structured parsing of Slurm command outputs
- **File Management**: Automatic organization of job files

### Key Features Detail

#### Output Organization
All SLURM job output files are automatically organized:
```
logs/slurm_output/
├── slurm_<job_id>.out        # Single job stdout
├── slurm_<job_id>.err        # Single job stderr
├── slurm_<array_id>_<task>.out  # Array job outputs
└── slurm_<array_id>_<task>.err  # Array job errors
```

#### Node Allocation
Interactive node allocation using `salloc`:
- System default or user-specified time limits
- Partition validation and error handling
- Resource specification (CPU, memory, exclusive access)
- Real-time allocation status monitoring
- Proper cleanup and deallocation

#### Error Handling
Comprehensive error handling includes:
- Slurm command validation
- Resource availability checking
- Permission and access validation
- Detailed error messages with suggestions
- Graceful fallback for edge cases

This Slurm MCP Server provides a production-ready solution for integrating Slurm workload management with MCP-compatible AI assistants and applications.
