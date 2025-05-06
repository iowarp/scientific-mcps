# Slurm MCP Capability

## Overview
This MCP capability enables job submission to HPC clusters via Slurm, allowing AI agents to interact with high-performance computing resources.

## Features
- Job submission with script path and core count specification
- Job ID generation and tracking
- Job status monitoring and retrieval

## API
- Tool ID: `slurm`
- Method: `mcp/callTool`

### Example Request
```json
{
  "jsonrpc": "2.0",
  "method": "mcp/callTool",
  "params": {
    "tool_id": "slurm",
    "parameters": {
      "script_path": "/path/to/script.sh",
      "cores": 4
    }
  },
  "id": 1
}
```


## Implementation Details
The implementation simulates Slurm job submission and management for testing and development.