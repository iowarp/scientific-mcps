# MCP Server

---

## Overview
This project implements a basic **Model Context Protocol (MCP)** server in Python, exposing the following MCP capabilities:

1. **HDF5 Listing** (`list_hdf5`): List all `.hdf5` files in a specified directory.  

The server adheres to JSON-RPC 2.0, built on **FastAPI**. Unit tests using **pytest** cover success and error cases for each capability and endpoint.

---

## Project Structure
```text
mcp-server-project/
├── pyproject.toml           # Project metadata & dependencies
├── data/                    # Sample data directory
│   └── sim_run_123/         # HDF5 files for testing
│       ├── run1.hdf5        # ... example files
│       └── run2.hdf5
├── README.md                # This file
├── src/
│   └── mcp_server/
│       ├── __init__.py      # Package init
│       ├── server.py        # FastAPI app
│       ├── mcp_handlers.py  # MCP method dispatch
│       └── capabilities/
│           ├── __init__.py  # Subpackage init
│           ├── hdf5_list.py # HDF5 list logic
└── tests/
    ├── test_hdf5_list.py    # Tests for HDF5 listing
    ├── test_mcp_handlers.py # Tests for MCP handlers
    └── test_server.py       # Tests for HTTP endpoints
```

---

## Setup
<!-- 1. Create and activate an `uv` virtual environment:
   ```bash
   uv venv           # create a virtual environment based on pyproject.toml
   uv lock           # generate or update the lock file
   uv sync           # install dependencies into the venv
   ```
   This will create a `.venv/` folder and install all required packages.

2. Confirm your environment is active (your prompt will show `(venv)`), then install development tools:
   ```bash
   uv sync --dev    # install pytest, psutil, and other dev dependencies
   ``` -->
- Run the following command:
  ```bash
  ..\mcp-server\Scripts\activate     # On Windows: to activate env
  ../source mcp-server/bin/activate  # On macOS/Linux: to activate env

  # Once activated, 
  uv pip install .                   # To install current mcp server
  ```
--- 
## Running the Server
Start the FastAPI server with **uvicorn**:
```bash
uvicorn mcp_server.server:app --reload --host 0.0.0.0 --port 8000
```

- **--reload** enables auto-reload on code changes.  
- The server listens on `http://localhost:8000`.

---

## JSON-RPC Usage Examples
All requests are HTTP POSTs to `/mcp` with JSON-RPC 2.0 payloads.

### 1. List Resources
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp/listResources","id":1}'
```


### 2. List HDF5 Files (`list_hdf5`)
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
        "jsonrpc":"2.0",
        "method":"mcp/callTool",
        "params":{
          "tool":"list_hdf5",
          "directory":"data/sim_run_123"
        },
        "id":3
      }'
```


## Running Tests
Install pytest by 
```bash
uv pip install .[test]
```

Execute the full pytest suite:
<!-- ```bash
pytest -q -v
```

- **-q**: quiet mode (dots for passes)  
- **-v**: verbose (test names with PASS/FAIL)  
- **-s**: (optional) show print() output for debugging -->
```bash
pytest tests
```

All tests cover success paths and edge cases for each capability and endpoint.

---

## Assumptions & Notes
- HDF5 listing is simulated via filesystem globbing.  
- Node hardware info relies on `psutil`; logical count falls back to `os.cpu_count()`.  

