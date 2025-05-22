
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
## Setup

- Run the following command:
  ```bash
  ..\mcp-server\Scripts\activate     # On Windows: to activate env
  ../source mcp-server/bin/activate  # On macOS/Linux: to activate env

  # Once activated, 
  uv pip install .                   # To install current mcp server
  ```
---

## Running the server

To run **Jarvis-MCP** on **ARES** or any **root node**, use:

```bash
python3 src/jarvis_mcp/server.py # for Linux/macOS
# or
python src/jarvis_mcp/server.py # for Windows
```

This command will start Jarivs MCP server.

"OR" simply type
```bash
jarvis-mcp-server
```

Refer to Installation and setup [guide.](./docs/GUIDE.md)


---

## Operations and Screenshots 

To use Jarvis MCP connect it with a client or enter dev command to do the tool calling. 

```bash 
mcp dev src/jarvis_mcp/server.py
```

Below are the outputs of Jarvis MCP connected with a simple Gemini Client script. 

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
