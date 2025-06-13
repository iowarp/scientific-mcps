# ADIOS MCP Server

A read-only Model Context Protocol (MCP) server for ADIOS datasets, enabling LLMS to query scientific simulation and real-time data.

## Key Features

- **Read-Only ADIOS Access**  
  Uses the ADIOS2 Python API to list files, inspect variables, and retrieve data slices or full arrays without modifying the source.

- **Standardized MCP Interface**  
  Exposes data-access tools via the MCP JSON-RPC protocol.

- **Local LLM Integration**  
  Connects to local language models through ollama, allowing natural-language queries and inference without internet or cloud dependencies.

- **Cross-Platform**  
  Pure Python implementation runs on Linux, macOS, and Windows. Package installable via `pip` or Spack.

## Architecture

 ![](https://github.com/iowarp/scientific-mcps/blob/main/Adios/assets/architecture.png)

## Capabilities

 1. list_bp5: List all the bp5 files in a directory. [Args: directorypath] 

 2. inspect_variables: Inspect all variables in a BP5 file (type, shape, available steps)  [Args: filename]. 

 3. inspect_attributes: Read global or variable-specific attributes from a BP5 file. [Args: filename, optional: variable_name]. 

 4. read_variable_at_step: Read a named variable at a specific step from a BP5 file.  [Args: filename, variable_name, target_step]. 

 5. read_bp5: Reads all the variables/data and their steps from a BP5 file. [Args: filename].

 6. get_min_max: Get minimum and maximum of a variable in a BP5 file. [Args: filename, variable_name, optional: step]. 

 7. add_variables: Sum two variables in a BP5 file, either globally or at specific steps. [Args: filename, var1, var2, optional: step1, step2].

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
        "path/to/directory/src/adiosmcp/",
        "run",
        "server.py"
    ]
}

```
---

## Few Examples

1. Read variables/data at specific step in a Bp5 File 

 ![](https://github.com/iowarp/scientific-mcps/blob/main/Adios/assets/read_steps.png)

2. Inspect the variables in a BP5 file (type, shape, available steps)

 ![](https://github.com/iowarp/scientific-mcps/blob/main/Adios/assets/steps.png)

3. Inspect and read the attributes of a specific variable

 ![](https://github.com/iowarp/scientific-mcps/blob/main/Adios/assets/attributes.png)

**Detailed demonstration of use cases are available at [Examples](https://github.com/sohamvsonar/scientific-mcps/tree/main/Adios/docs/example_uses.md).**

## Project Structure
```text
Adios/
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Project documentation
├── assets/                  # Images and other assets
├── data/                    # Sample data directory
├── docs/                    # Additional documentation
│     ├── adios_setup        # Detailed guide on installing the Adios2
│     └── example_uses       # Example use cases with prompt, answers and pictures
├── pyproject.toml           # Project metadata & dependencies
├── src/                     # Source code directory
│   └── adiosmcp/
│       ├── __init__.py      # Package init
│       ├── server.py        # The MCP server
│       ├── mcp_handlers.py  # MCP methods
│       └── capabilities/
│           ├── __init__.py
│           ├── bp5_add.py                    # Add variables functionality
│           ├── bp5_attributes.py             # Inspect attributes functionality
│           ├── bp5_inspect_variables.py      # Inspect variables functionality
│           ├── bp5_list.py                   # List BP5 files functionality
│           ├── bp5_minmax.py                 # Get min/max functionality
│           ├── bp5_read_all_variables.py     # Read all variables functionality
│           ├── bp5_read_variable_at_step.py  # Read variable at step functionality
├── uv.lock                  # Dependency lock file
```