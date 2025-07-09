#!/usr/bin/env python3
"""
Enhanced Node Hardware MCP Server with comprehensive hardware monitoring.
Provides hardware information retrieval, system monitoring, and performance metrics.
"""
import os
import sys
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

import mcp_handlers

# Initialize MCP server
mcp = FastMCP("NodeHardwareMCP")

@mcp.tool(
    name="get_cpu_info",
    description="Get detailed CPU information including cores, frequency, and architecture."
)
async def get_cpu_info_tool() -> dict:
    """
    Get comprehensive CPU information.
    
    Returns:
        Dictionary with CPU information
    """
    logger.info("Getting CPU information")
    return mcp_handlers.get_cpu_info_handler()


@mcp.tool(
    name="get_memory_info",
    description="Get memory information including total, available, and usage statistics."
)
async def get_memory_info_tool() -> dict:
    """
    Get memory information.
    
    Returns:
        Dictionary with memory information
    """
    logger.info("Getting memory information")
    return mcp_handlers.get_memory_info_handler()


@mcp.tool(
    name="get_disk_info",
    description="Get disk information including usage and mount points."
)
async def get_disk_info_tool() -> dict:
    """
    Get disk information.
    
    Returns:
        Dictionary with disk information
    """
    logger.info("Getting disk information")
    return mcp_handlers.get_disk_info_handler()


@mcp.tool(
    name="get_network_info",
    description="Get network interfaces and statistics."
)
async def get_network_info_tool() -> dict:
    """
    Get network information.
    
    Returns:
        Dictionary with network information
    """
    logger.info("Getting network information")
    return mcp_handlers.get_network_info_handler()


@mcp.tool(
    name="get_system_info",
    description="Get general system information including OS, architecture, and uptime."
)
async def get_system_info_tool() -> dict:
    """
    Get system information.
    
    Returns:
        Dictionary with system information
    """
    logger.info("Getting system information")
    return mcp_handlers.get_system_info_handler()


@mcp.tool(
    name="get_process_info",
    description="Get running process information and resource usage."
)
async def get_process_info_tool(limit: int = 10) -> dict:
    """
    Get process information.
    
    Args:
        limit: Maximum number of processes to return (default: 10)
        
    Returns:
        Dictionary with process information
    """
    logger.info(f"Getting process information (limit: {limit})")
    return mcp_handlers.get_process_info_handler(limit)


@mcp.tool(
    name="get_hardware_summary",
    description="Get a comprehensive hardware summary including CPU, memory, disk, and network."
)
async def get_hardware_summary_tool() -> dict:
    """
    Get comprehensive hardware summary.
    
    Returns:
        Dictionary with complete hardware summary
    """
    logger.info("Getting hardware summary")
    return mcp_handlers.get_hardware_summary_handler()


@mcp.tool(
    name="monitor_performance",
    description="Monitor system performance metrics in real-time."
)
async def monitor_performance_tool(duration: int = 5) -> dict:
    """
    Monitor system performance.
    
    Args:
        duration: Duration in seconds to monitor (default: 5)
        
    Returns:
        Dictionary with performance metrics
    """
    logger.info(f"Monitoring performance for {duration} seconds")
    return mcp_handlers.monitor_performance_handler(duration)


@mcp.tool(
    name="get_gpu_info",
    description="Get GPU information if available."
)
async def get_gpu_info_tool() -> dict:
    """
    Get GPU information.
    
    Returns:
        Dictionary with GPU information
    """
    logger.info("Getting GPU information")
    return mcp_handlers.get_gpu_info_handler()


@mcp.tool(
    name="get_sensor_info",
    description="Get temperature and sensor information."
)
async def get_sensor_info_tool() -> dict:
    """
    Get sensor information.
    
    Returns:
        Dictionary with sensor information
    """
    logger.info("Getting sensor information")
    return mcp_handlers.get_sensor_info_handler()


def main():
    """
    Main entry point for the Node Hardware MCP server.
    Supports both stdio and SSE transports based on environment variables.
    """
    try:
        logger.info("Starting Node Hardware MCP Server")
        
        # Determine which transport to use
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport == "sse":
            # SSE transport for web-based clients
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = int(os.getenv("MCP_SSE_PORT", "8000"))
            logger.info(f"Starting SSE transport on {host}:{port}")
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            # Default stdio transport
            logger.info("Starting stdio transport")
            print(json.dumps({"message": "Starting stdio transport"}), file=sys.stderr)
            mcp.run(transport="stdio")

    except Exception as e:
        logger.error(f"Server error: {e}")
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
