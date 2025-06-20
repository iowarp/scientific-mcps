#!/usr/bin/env python3
"""
Enhanced Slurm MCP Server with comprehensive job management.
Provides job submission, status checking, queue monitoring, and job cancellation capabilities.
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

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

import mcp_handlers

# Initialize MCP server
mcp = FastMCP("SlurmMCP")

@mcp.tool(
    name="submit_slurm_job",
    description="Submit a script to Slurm with specified number of cores and optional parameters."
)
async def submit_slurm_job_tool(
    script_path: str, 
    cores: int = 1, 
    memory: str = "1GB",
    time_limit: str = "01:00:00",
    job_name: str = None,
    partition: str = None
) -> dict:
    """
    Submit a job script to Slurm scheduler with advanced options.
    
    Args:
        script_path: Path to the job script file
        cores: Number of CPU cores to request (default: 1)
        memory: Memory requirement (default: "1GB")
        time_limit: Time limit in HH:MM:SS format (default: "01:00:00")
        job_name: Custom job name (default: derived from script)
        partition: Slurm partition to use (default: system default)
        
    Returns:
        Dictionary with job submission results
    """
    logger.info(f"Submitting job: {script_path} with {cores} cores")
    return mcp_handlers.submit_slurm_job_handler(
        script_path, cores, memory, time_limit, job_name, partition
    )


@mcp.tool(
    name="check_job_status",
    description="Check the status of a submitted Slurm job by job ID."
)
async def check_job_status_tool(job_id: str) -> dict:
    """
    Check the status of a Slurm job.
    
    Args:
        job_id: The Slurm job ID to check
        
    Returns:
        Dictionary with job status information
    """
    logger.info(f"Checking status for job: {job_id}")
    return mcp_handlers.check_job_status_handler(job_id)


@mcp.tool(
    name="cancel_slurm_job",
    description="Cancel a running or pending Slurm job."
)
async def cancel_slurm_job_tool(job_id: str) -> dict:
    """
    Cancel a Slurm job.
    
    Args:
        job_id: The Slurm job ID to cancel
        
    Returns:
        Dictionary with cancellation results
    """
    logger.info(f"Cancelling job: {job_id}")
    return mcp_handlers.cancel_slurm_job_handler(job_id)


@mcp.tool(
    name="list_slurm_jobs",
    description="List all jobs for the current user."
)
async def list_slurm_jobs_tool(user: str = None, state: str = None) -> dict:
    """
    List Slurm jobs with optional filtering.
    
    Args:
        user: Username to filter by (default: current user)
        state: Job state to filter by (PENDING, RUNNING, COMPLETED, etc.)
        
    Returns:
        Dictionary with list of jobs
    """
    logger.info(f"Listing jobs for user: {user}, state: {state}")
    return mcp_handlers.list_slurm_jobs_handler(user, state)


@mcp.tool(
    name="get_slurm_info",
    description="Get Slurm cluster information and resource availability."
)
async def get_slurm_info_tool() -> dict:
    """
    Get information about the Slurm cluster.
    
    Args:
        None
        
    Returns:
        Dictionary with cluster information
    """
    logger.info("Getting Slurm cluster information")
    return mcp_handlers.get_slurm_info_handler()


@mcp.tool(
    name="get_job_details",
    description="Get detailed information about a specific Slurm job."
)
async def get_job_details_tool(job_id: str) -> dict:
    """
    Get detailed information about a Slurm job.
    
    Args:
        job_id: The Slurm job ID
        
    Returns:
        Dictionary with detailed job information
    """
    logger.info(f"Getting detailed information for job: {job_id}")
    return mcp_handlers.get_job_details_handler(job_id)


@mcp.tool(
    name="get_job_output",
    description="Get job output files (stdout/stderr) for a Slurm job."
)
async def get_job_output_tool(job_id: str, output_type: str = "stdout") -> dict:
    """
    Get job output content.
    
    Args:
        job_id: The Slurm job ID
        output_type: Type of output ("stdout" or "stderr")
        
    Returns:
        Dictionary with job output content
    """
    logger.info(f"Getting {output_type} for job: {job_id}")
    return mcp_handlers.get_job_output_handler(job_id, output_type)


@mcp.tool(
    name="get_queue_info",
    description="Get information about the Slurm job queue with optional partition filtering."
)
async def get_queue_info_tool(partition: str = None) -> dict:
    """
    Get job queue information.
    
    Args:
        partition: Specific partition to query (optional)
        
    Returns:
        Dictionary with queue information
    """
    logger.info(f"Getting queue information for partition: {partition}")
    return mcp_handlers.get_queue_info_handler(partition)


@mcp.tool(
    name="submit_array_job",
    description="Submit a Slurm array job with specified parameters."
)
async def submit_array_job_tool(
    script_path: str, 
    array_range: str,
    cores: int = 1,
    memory: str = "1GB",
    time_limit: str = "01:00:00",
    job_name: str = None,
    partition: str = None
) -> dict:
    """
    Submit an array job to Slurm scheduler.
    
    Args:
        script_path: Path to the job script file
        array_range: Array range specification (e.g., "1-10", "1-100:2")
        cores: Number of cores per array task (default: 1)
        memory: Memory per array task (default: "1GB")
        time_limit: Time limit per array task in HH:MM:SS format (default: "01:00:00")
        job_name: Base name for the array job (default: derived from script)
        partition: Slurm partition to use (default: system default)
        
    Returns:
        Dictionary with array job submission results
    """
    logger.info(f"Submitting array job: {script_path}, range: {array_range}, cores: {cores}")
    return mcp_handlers.submit_array_job_handler(
        script_path, array_range, cores, memory, time_limit, job_name, partition
    )


@mcp.tool(
    name="get_node_info",
    description="Get information about cluster nodes and their status."
)
async def get_node_info_tool() -> dict:
    """
    Get cluster node information.
    
    Args:
        None
        
    Returns:
        Dictionary with node information
    """
    logger.info("Getting cluster node information")
    return mcp_handlers.get_node_info_handler()


def main():
    """
    Main entry point for the Slurm MCP server.
    Supports both stdio and SSE transports based on environment variables.
    """
    try:
        logger.info("Starting Slurm MCP Server")
        
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