# Node Hardware MCP Capability

## Overview
This MCP capability provides system information retrieval functionality, enabling AI agents to obtain hardware details of the host system.

## Features
- CPU cores count retrieval
- System memory information
- Platform details reporting

## API
- Tool ID: `node_hardware`
- Method: `mcp/callTool`

### Example Request
```json
{
  "jsonrpc": "2.0",
  "method": "mcp/callTool",
  "params": {
    "tool_id": "node_hardware",
    "parameters": {}
  },
  "id": 1
}
```