# IoWarp MCPs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IoWarp](https://img.shields.io/badge/IoWarp-GitHub-blue.svg)](http://github.com/iowarp)
[![GRC](https://img.shields.io/badge/GRC-Website-blue.svg)](https://grc.iit.edu/)
[![MCP](https://img.shields.io/badge/MCP-Protocol-purple.svg)](https://modelcontextprotocol.io/)
[![PyPI](https://img.shields.io/badge/PyPI-Package-green.svg)](https://pypi.org/project/iowarp-mcps/)

Collection of MCP servers specifically designed for scientific computing research that enable AI agents and LLMs to interact with data analysis tools, HPC resources, and research datasets through a standardized protocol.

**More info at**: [https://iowarp.github.io/iowarp-mcps/](https://iowarp.github.io/iowarp-mcps/)

## Quick Installation

All our packages are released on [PyPI](https://pypi.org/project/iowarp-mcps/) for easy installation and usage.

### Simple Command

```bash
# Run any MCP server directly
uvx iowarp-mcps <server-name>
```

### List All MCPs

```bash
# See all available MCP servers
uvx iowarp-mcps
```

### Get Started with a Simple Command

```bash
# Example: Run the pandas MCP server
uvx iowarp-mcps pandas

# Example: Run the plot MCP server  
uvx iowarp-mcps plot

# Example: Run the slurm MCP server
uvx iowarp-mcps slurm
```

## Available Packages

<div align="center">

| 📦 **Package** | 🔧 **System** | 📋 **Description** | ⚡ **Install Command** |
|:---|:---:|:---|:---|
| **`adios`** | Data I/O | Read data using ADIOS2 engine | `uvx iowarp-mcps adios` |
| **`arxiv`** | Research | Fetch research papers from ArXiv | `uvx iowarp-mcps arxiv` |
| **`chronolog`** | Logging | Log and retrieve data from ChronoLog | `uvx iowarp-mcps chronolog` |
| **`compression`** | Utilities | File compression with gzip | `uvx iowarp-mcps compression` |
| **`darshan`** | Performance | I/O performance trace analysis | `uvx iowarp-mcps darshan` |
| **`hdf5`** | Data I/O | List HDF5 files from directories | `uvx iowarp-mcps hdf5` |
| **`jarvis`** | Workflow | Data pipeline lifecycle management | `uvx iowarp-mcps jarvis` |
| **`lmod`** | Environment | Environment module management | `uvx iowarp-mcps lmod` |
| **`node-hardware`** | System | System hardware information | `uvx iowarp-mcps node-hardware` |
| **`pandas`** | Data Analysis | CSV data loading and filtering | `uvx iowarp-mcps pandas` |
| **`parallel-sort`** | Computing | Large file sorting simulation | `uvx iowarp-mcps parallel-sort` |
| **`parquet`** | Data I/O | Read Parquet file columns | `uvx iowarp-mcps parquet` |
| **`plot`** | Visualization | Generate plots from CSV data | `uvx iowarp-mcps plot` |
| **`slurm`** | HPC | Job submission simulation | `uvx iowarp-mcps slurm` |

</div>

## Members

**Primary Institution:**
- 🏛️ **[GRC (Gnosis Research Center)](https://grc.iit.edu/)** - [Illinois Institute of Technology](https://www.iit.edu/)

**Collaborating Institutions:**
- 📊 **[HDF Group](https://www.hdfgroup.org/)** - Data format and library developers
<!-- - **[University of Utah](https://www.utah.edu/)** - Research collaboration   -->


## Sponsors

🇺🇸 **[NSF (National Science Foundation)](https://www.nsf.gov/)** - Supporting scientific computing research and AI integration initiatives

## Contributing

We welcome contributions in any form!

### Ways to Contribute:

- **Submit Issues**: Report any problems or bugs you encounter
- **Request Features**: Submit an issue requesting a new MCP server or functionality
- **Develop**: Try your hand at developing new MCP servers

Find our comprehensive **contribution/development/debugging guide** [here](CONTRIBUTING.md).

### Get Help & Connect

**Reach out to us on Zulip**: [IoWarp-mcp Community Chat]()

---

