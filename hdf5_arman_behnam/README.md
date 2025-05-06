# HDF5 MCP Capability

## Overview
This MCP capability provides file system interaction for HDF5 files, allowing AI agents to search for and retrieve information about HDF5 files.

## Features
- File searching using path patterns
- File metadata retrieval
- Simulated file operations with mock data

## API
The capability is exposed through JSON-RPC 2.0 and can be accessed via:
- Resource ID: `hdf5`
- Method: `mcp/getResource`

### Example Request
```json
{
  "jsonrpc": "2.0",
  "method": "mcp/getResource",
  "params": {
    "resource_id": "hdf5",
    "parameters": {
      "path_pattern": "*_00.hdf5",
      "base_dir": "/data/sim_run_123"
    }
  },
  "id": 1
}
```

## Implementation Details
The implementation simulates HDF5 file operations without requiring real HDF5 files, making it suitable for testing and development.