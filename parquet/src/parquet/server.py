#!/usr/bin/env python3
"""
Enhanced Parquet MCP Server with comprehensive Parquet file operations.
Provides read/write, schema management, statistics, and format conversion capabilities.
"""
import os
import sys
import json
import argparse
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging
from typing import Optional, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from . import mcp_handlers

# Initialize MCP server
mcp = FastMCP("ParquetMCP")

@mcp.tool(
    name="read_parquet",
    description="Read Parquet file with optional column selection, filtering, and row limits."
)
async def read_parquet_tool(
    file_path: str,
    columns: Optional[List[str]] = None,
    limit: Optional[int] = None
) -> dict:
    """
    Read data from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
        columns: List of columns to read (None for all columns)
        limit: Maximum number of rows to return (None for all rows)
    
    Returns:
        Dictionary with file data and metadata
    """
    logger.info(f"Reading Parquet file: {file_path}")
    return mcp_handlers.read_parquet_handler(file_path, columns, None, limit)


@mcp.tool(
    name="write_parquet",
    description="Write data to a Parquet file with specified compression."
)
async def write_parquet_tool(
    data: Any,
    file_path: str,
    compression: str = "snappy"
) -> dict:
    """
    Write data to a Parquet file.
    
    Args:
        data: Data to write (dict, list of dicts, or JSON string)
        file_path: Output file path
        compression: Compression algorithm (snappy, gzip, lz4, brotli, zstd)
    
    Returns:
        Dictionary with write operation result
    """
    logger.info(f"Writing Parquet file: {file_path}")
    
    # Parse JSON string if needed
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return {
                "content": [{"text": json.dumps({"error": "Invalid JSON data"})}],
                "_meta": {"tool": "write_parquet", "error": "JSONDecodeError"},
                "isError": True
            }
    
    return mcp_handlers.write_parquet_handler(data, file_path, compression)


@mcp.tool(
    name="get_parquet_schema",
    description="Get detailed schema information from a Parquet file."
)
async def get_schema_tool(file_path: str) -> dict:
    """
    Get schema information from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with schema details
    """
    logger.info(f"Getting schema for: {file_path}")
    return mcp_handlers.get_schema_handler(file_path)


@mcp.tool(
    name="get_parquet_metadata",
    description="Extract comprehensive metadata from a Parquet file including row groups and compression info."
)
async def get_metadata_tool(file_path: str) -> dict:
    """
    Get detailed metadata from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with comprehensive metadata
    """
    logger.info(f"Getting metadata for: {file_path}")
    return mcp_handlers.get_metadata_handler(file_path)


@mcp.tool(
    name="get_column_statistics",
    description="Calculate detailed statistics for columns in a Parquet file."
)
async def get_statistics_tool(
    file_path: str,
    columns: Optional[List[str]] = None
) -> dict:
    """
    Get column statistics from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
        columns: List of columns to analyze (None for all columns)
    
    Returns:
        Dictionary with column statistics
    """
    logger.info(f"Getting statistics for: {file_path}")
    return mcp_handlers.get_statistics_handler(file_path, columns)


@mcp.tool(
    name="check_data_quality",
    description="Perform comprehensive data quality checks on a Parquet file."
)
async def check_quality_tool(file_path: str) -> dict:
    """
    Check data quality of a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with data quality assessment
    """
    logger.info(f"Checking data quality for: {file_path}")
    return mcp_handlers.check_quality_handler(file_path)


@mcp.tool(
    name="convert_parquet_to_csv",
    description="Convert Parquet file to CSV format."
)
async def convert_to_csv_tool(
    parquet_path: str,
    csv_path: str,
    columns: Optional[List[str]] = None,
    limit: Optional[int] = None
) -> dict:
    """
    Convert Parquet file to CSV.
    
    Args:
        parquet_path: Path to input Parquet file
        csv_path: Path for output CSV file
        columns: List of columns to include (None for all)
        limit: Maximum number of rows to convert
    
    Returns:
        Dictionary with conversion result
    """
    logger.info(f"Converting {parquet_path} to CSV: {csv_path}")
    return mcp_handlers.convert_format_handler(
        parquet_path, csv_path, "csv", columns=columns, limit=limit
    )


@mcp.tool(
    name="convert_csv_to_parquet",
    description="Convert CSV file to Parquet format."
)
async def convert_from_csv_tool(
    csv_path: str,
    parquet_path: str,
    compression: str = "snappy"
) -> dict:
    """
    Convert CSV file to Parquet.
    
    Args:
        csv_path: Path to input CSV file
        parquet_path: Path for output Parquet file
        compression: Compression algorithm to use
    
    Returns:
        Dictionary with conversion result
    """
    logger.info(f"Converting {csv_path} to Parquet: {parquet_path}")
    return mcp_handlers.convert_format_handler(
        csv_path, parquet_path, "parquet", compression=compression
    )


@mcp.tool(
    name="convert_parquet_to_json",
    description="Convert Parquet file to JSON format."
)
async def convert_to_json_tool(
    parquet_path: str,
    json_path: str,
    columns: Optional[List[str]] = None,
    limit: Optional[int] = None,
    orient: str = "records"
) -> dict:
    """
    Convert Parquet file to JSON.
    
    Args:
        parquet_path: Path to input Parquet file
        json_path: Path for output JSON file
        columns: List of columns to include (None for all)
        limit: Maximum number of rows to convert
        orient: JSON orientation ('records', 'index', 'values', etc.)
    
    Returns:
        Dictionary with conversion result
    """
    logger.info(f"Converting {parquet_path} to JSON: {json_path}")
    return mcp_handlers.convert_format_handler(
        parquet_path, json_path, "json", columns=columns, limit=limit, orient=orient
    )


@mcp.tool(
    name="convert_json_to_parquet",
    description="Convert JSON file to Parquet format."
)
async def convert_from_json_tool(
    json_path: str,
    parquet_path: str,
    compression: str = "snappy"
) -> dict:
    """
    Convert JSON file to Parquet.
    
    Args:
        json_path: Path to input JSON file
        parquet_path: Path for output Parquet file
        compression: Compression algorithm to use
    
    Returns:
        Dictionary with conversion result
    """
    logger.info(f"Converting {json_path} to Parquet: {parquet_path}")
    return mcp_handlers.convert_format_handler(
        json_path, parquet_path, "parquet", compression=compression
    )


@mcp.tool(
    name="get_compression_stats",
    description="Get detailed compression statistics and efficiency metrics for a Parquet file."
)
async def get_compression_tool(file_path: str) -> dict:
    """
    Get compression statistics for a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with compression statistics
    """
    logger.info(f"Getting compression stats for: {file_path}")
    return mcp_handlers.get_compression_handler(file_path)


def main():
    """
    Main entry point for the Parquet MCP server.
    Supports both stdio and SSE transports based on environment variables or command line arguments.
    """
    parser = argparse.ArgumentParser(description="Parquet MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default=None,
        help="Transport protocol (stdio or sse)"
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host for SSE transport (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("Starting Parquet MCP Server")
        
        # Use command-line args or environment variables
        transport = args.transport or os.getenv("MCP_TRANSPORT", "stdio").lower()
        
        if transport == "sse":
            # SSE transport for web-based clients
            host = args.host or os.getenv("MCP_SSE_HOST", "localhost")
            port = args.port or int(os.getenv("MCP_SSE_PORT", "8000"))
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
