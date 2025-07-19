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

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Setup
**Run the Mcp Server directly:**

   ```bash
   uv run hdf5-mcp
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.
--- 

## Running the Server with different types of Clients:

### Running the Server with the WARP Client
To interact with the Jarvis MCP server, use the main `wrp.py` client. You will need to configure it to point to the Jarvis server.

1.  **Configure:** Ensure that `Jarvis` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Jarvis
      
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```
    For quick setup with Gemini, see our [Quick Start Guide](docs/basic_install.md).
    
    
    For detailed setup with local LLMs and other providers, see the [Complete Installation Guide](../bin/docs/Installation.md).

### Running the Server on Claude Command Line Interface Tool.

1. Install the Claude Code using NPM,
Install [NodeJS 18+](https://nodejs.org/en/download), then run:

```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp jarvis -- uv --directory ~/scientific-mcps/Jarvis run jarvis-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```bash
"jarvis-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/src/hdf5/",
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
