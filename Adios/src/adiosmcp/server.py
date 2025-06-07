# server.py
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
from capabilities import bp5 as bp5_module
import mcp_handlers

# Initialize FastMCP server
mcp = FastMCP("ADIOSMCP")

# ─── ADIOS BP5 TOOLS ─────────────────────────────────────────────────────────

@mcp.tool(
    name="read_bp5",
    description="Read all steps/variables from a BP5 file using ADIOS2 Stream API."
)
async def read_bp5_tool(filename: str) -> dict:
    """
    MCP‐exposed tool that reads a BP5 file (any shape/dtype) and returns
    a nested dict of step→ variables, metadata, and attributes.
    """
    try:
        return await mcp_handlers.read_bp5_handler(filename)
    except Exception as e:
        # If something goes really wrong in the handler itself
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_bp5", "error": type(e).__name__},
            "isError": True
        }

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
