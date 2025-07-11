
# Jarvis-MCP

*A MCP server to interact with Jarvis*

---

## Overview

**Jarvis-MCP** is a python package that allows you to control Jarvis using a Model Context Protocol (MCP) server.

With **Jarvis-MCP**, you can:

* Initialize and configure Jarvis
* Bootstrap from ARES
* Create, list, run, and destroy pipelines
* Add or remove packages from a pipeline
* Update package configurations
* Build and run pipelines

---

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)


## Setup
**Run the Mcp Server directly:**

   ```bash
   uv run jarvis-mcp
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
        "path/to/directory/src/jarvis_mcp/",
        "run",
        "server.py"
    ]
}
```

---

## Operations and Screenshots 

##### 1. **Initialize Jarvis**

The first step is to initialize Jarvis. This prepares the system for interaction.

```bash
# Command to initialize Jarvis
Query: Initialize jarvis with configur, private and shared dir as " . /jarvis—pipelines'
```

**Output Screenshot**

![alt text](<./docs/assets/Screenshot 2025-05-15 160800.png>)

---

##### 2. **Create Pipeline (`ior_test`) and append package**

Create a new pipeline named `ior_test` and append package to it. This will be used for testing purposes.

```bash
# Command to create a pipeline
Query: create a pipeline called ior_test and append package ior to it
```

**Output Screenshot**

![alt text](<./docs/assets/Screenshot 2025-05-15 162219.png>)

---

##### 3. **Change Configuration of Added Package**

You can also see and modify the configuration of the package you've added to the pipeline.

```bash
# Command to change the configuration
Query: show the configuration of ior in ior_test
```

**Output Screenshot**

![alt text](<./docs/assets/Screenshot 2025-05-15 162322.png>)

```bash
# Command to change the configuration
Query: update the nprocs to 8 for package ior in pipeline ior_test
```

![alt text](<./docs/assets/Screenshot 2025-05-15 162545.png>)
---

##### 4. **Build Environment for `ior_test` Pipeline**

After configuring the pipeline, you can build the environment for `ior_test`.

```bash
# Command to build the environment
Query: Build environment for pipeline ior_test 
```

**Output Screenshot**

![alt text](<./docs/assets/Screenshot 2025-05-15 162922.png>)

---

##### 5. **Run the Pipeline (`ior_test`)**

Finally, you can run the pipeline to see everything in action.

```bash
# Command to run the pipeline
Query: select the pipeline ior_test and run it
```

**Output Screenshot**

![alt text](<./docs/assets/Screenshot 2025-05-15 163023.png>)

---

or **write below** to create pipeline, append package to it and run it:
```bash
Query: create a pipeline called ior_test_2. Add package ior with nprocs set to 16. After adding, set the pipeline ior_test_2 as current and build environment for it and run it.
```
![alt text](<./docs/assets/Screenshot 2025-05-15 163759.png>)

---

## Notes

* Ensure your environment is set up with Python 3.10+
* You’ll need an `.env` file if you're using the Gemini API directly
* Use `pip install -e .` in the repo to enable CLI tools like `mcp-server` (optional)
