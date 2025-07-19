#!/usr/bin/env python3
"""
Entry point for Plot MCP Server.
"""
import sys
import os

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

from server import main

if __name__ == "__main__":
    main()
