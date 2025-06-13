# server.py

#  Created on: 2nd June, 2025
#      Author: Soham Sonar ssonar2@hawk.iit.edu



import os
import sys
import json
from fastmcp import FastMCP
from dotenv import load_dotenv

# Ensure parent directory is on PYTHONPATH so "capabilities" can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env variables, if any
load_dotenv()

# Import our ADIOS BP5 capability and handler
import mcp_handlers

# Initialize FastMCP server
mcp = FastMCP("ADIOSMCP")

# ─── ADIOS BP5 TOOLS ─────────────────────────────────────────────────────────

# List BP5 Files Tool
@mcp.tool(
    name="list_bp5",
    description="List all the bp5 files in a directory. [Args: directorypath] \n"
)
async def list_bp5_tool(directory: str = "data/") -> dict:
    """List all bp5 files in the specified directory."""
    try:
        return await mcp_handlers.list_bp5_files(directory)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "list_bp5", "error": type(e).__name__},
            "isError": True
        }

# ─── INSPECT VARIABLES ─────────────────────────────────────────────────────── 
@mcp.tool(
    name="inspect_variables",
    description="Inspect all variables in a BP5 file (type, shape, available steps)  [Args: filename]. \n"
)
async def inspect_variables_tool(filename: str) -> dict:
    try:
        return await mcp_handlers.inspect_variables_handler(filename)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "inspect_variables", "error": type(e).__name__},
            "isError": True
        }

# ─── INSPECT ATTRIBUTES ──────────────────────────────────────────────────────
@mcp.tool(
    name="inspect_attributes",
    description="Read global or variable-specific attributes from a BP5 file. [Args: filename, optional: variable_name]. \n"
)
async def inspect_attributes_tool(
    filename: str,
    variable_name: str = None
) -> dict:
    try:
        return await mcp_handlers.inspect_attributes_handler(filename, variable_name)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "inspect_attributes", "error": type(e).__name__},
            "isError": True
        }

import mcp_handlers

# ─── READ VARIABLE AT STEP ────────────────────────────────────────────────────
@mcp.tool(
    name="read_variable_at_step",
    description="Read a named variable at a specific step from a BP5 file.  [Args: filename, variable_name, target_step]. \n"
)
async def read_variable_at_step_tool(
    filename: str, variable_name: str, target_step: int
) -> dict:
    return await mcp_handlers.read_variable_at_step_handler(
        filename, variable_name, target_step
    )

# ─── READ ALL VARIABLES ───────────────────────────────────────────────────────
@mcp.tool(
    name="read_bp5",
    description="Reads all the variables/data and their steps from a BP5 file. [Args: filename]. \n"
)
async def read_bp5_tool(filename: str) -> dict:
    """
    MCP‐exposed tool that reads a BP5 file and returns
    a nested dict of step→ variables and their values.
    """
    try:
        return await mcp_handlers.read_all_variables_handler(filename)
    except Exception as e:
        # If something goes really wrong in the handler itself
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_bp5", "error": type(e).__name__},
            "isError": True
        }

# ─── GET MIN / MAX ──────────────────────────────────────────────────────────────
@mcp.tool(
    name="get_min_max",
    description=(
        "Get minimum and maximum of a variable in a BP5 file. [Args: filename, variable_name, optional: step]. \n"
    ),
)
async def get_min_max_tool(
    filename: str, variable_name: str, step: int = None
) -> dict:
    return await mcp_handlers.get_min_max_handler(
        filename, variable_name, step
    )


# ─── ADD VARIABLES ──────────────────────────────────────────────────────────────
@mcp.tool(
    name="add_variables",
    description=(
        "Sum two variables in a BP5 file, either globally or at specific steps. [Args: filename, var1, var2, optional: step1, step2]. \n"
    ),
)
async def add_variables_tool(
    filename: str,
    var1: str,
    var2: str,
    step1: int = None,
    step2: int = None,
) -> dict:
    return await mcp_handlers.add_variables_handler(
        filename, var1, var2, step1, step2
    )


def main():
    """
    Main entry point to run the ADIOS MCP server.
    Chooses between stdio or SSE transport based on MCP_TRANSPORT.
    """
    try:
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport == "sse":
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = int(os.getenv("MCP_SSE_PORT", "8000"))
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            print(json.dumps({"message": "Starting stdio transport"}), file=sys.stderr)
            mcp.run(transport="stdio")
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
