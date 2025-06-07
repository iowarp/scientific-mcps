# MCP Server

---

## Overview
This project implements a basic **Model Context Protocol (MCP)** server in Python, exposing the following MCP capabilities:

1. **HDF5 Listing** (`list_hdf5`): List all `.hdf5` files in a specified directory.
2. **inspect hdf5 file** Inspect HDF5 file structure: lists groups, datasets, and attributes.
3. **preview data** Preview first N elements of each dataset in an HDF5 file.
4. **read all data**: Read every element of every dataset in an HDF5 file.

The server is built on **FastMCP**. Unit tests using **pytest** cover success and error cases for each capability and endpoint.

---

## Setup
1. Create and activate an `uv` virtual environment:
   ```bash
   uv venv           # create a virtual environment based on pyproject.toml
   source .venv/bin/activate
   uv sync           # install dependencies into the venv
   ```
   This will create a `.venv/` folder and install all required packages.

--- 
## Running the Server with wrp_chat
Start the server with **wrp_chat**:
```bash
python3 ../bin/wrp_chat.py --servers=Adios
```

## Running the Server open source LLM client
Put the following in settings.json:
```bash
"adios-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/src/mcpserver/",
        "run",
        "server.py"
    ]
}
```

---

## Examples

1. Inspect Tool 

 ![](https://github.com/iowarp/scientific-mcps/blob/main/HDF5/assets/inspect.png)

2. Read Dataset Tool

 ![](https://github.com/iowarp/scientific-mcps/blob/main/HDF5/assets/read.png)


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

## Project Structure
```text
HDF5/
├── pyproject.toml           # Project metadata & dependencies
├── data/                    # Sample data directory
│   ├── sample1.hdf5     # HDF5 files for testing
│   └── sample2.hdf5
├── README.md                # This file
├── src/
│   └── mcp_server/
│       ├── __init__.py      # Package init
│       ├── server.py        # FastAPI app
│       ├── mcp_handlers.py  # MCP method dispatch
│       └── capabilities/
│           ├── __init__.py  # Subpackage init
│           ├── hdf5_list.py    
│           ├── inspect_hdf5.py
│           ├── preview_hdf5.py 
│           ├── read_all_hdf5.py
└── tests/
    ├── test_hdf5_list.py    # Tests for HDF5 listing
    ├── test_mcp_handlers.py # Tests for MCP handlers
    └── test_server.py       # Tests for HTTP endpoints
```

---
## Assumptions & Notes
- HDF5 listing is simulated via filesystem globbing.  
