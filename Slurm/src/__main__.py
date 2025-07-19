#!/usr/bin/env python3
"""
Entry point for the Slurm MCP Server package.
Enables running the server with `python -m slurm_mcp`.
"""

from .server import main

if __name__ == "__main__":
    main()
