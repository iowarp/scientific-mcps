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
    description="Read and extract data from Parquet files with advanced filtering options. Supports selective column reading, row limiting, and efficient memory usage for large datasets. Returns structured data with metadata information."
)
async def read_parquet_tool(
    file_path: str,
    columns: Optional[List[str]] = None,
    limit: Optional[int] = None
) -> dict:
    """
    Read data from a Parquet file with optional column selection and row limiting.
    
    Args:
        file_path: Absolute path to the Parquet file to read
        columns: List of specific column names to read (None reads all columns, useful for large files)
        limit: Maximum number of rows to return (None returns all rows, useful for data preview)
    
    Returns:
        Dictionary containing:
        - data: Structured data from the file
        - metadata: File information, schema details, and read statistics
        - row_count: Number of rows read
        - column_info: Details about columns and data types
    """
    logger.info(f"Reading Parquet file: {file_path}")
    return mcp_handlers.read_parquet_handler(file_path, columns, None, limit)


@mcp.tool(
    name="write_parquet",
    description="Write data to Parquet files with customizable compression algorithms. Supports multiple data formats (dict, list of dicts, JSON strings) and various compression options for optimal storage efficiency."
)
async def write_parquet_tool(
    data: Any,
    file_path: str,
    compression: str = "snappy"
) -> dict:
    """
    Write data to a Parquet file with specified compression algorithm.
    
    Args:
        data: Data to write - accepts dict, list of dicts, or JSON string format
        file_path: Absolute path where the Parquet file will be created
        compression: Compression algorithm to use (snappy, gzip, lz4, brotli, zstd)
                    - snappy: Fast compression/decompression (default)
                    - gzip: Good compression ratio, slower than snappy
                    - lz4: Very fast compression/decompression
                    - brotli: Excellent compression ratio, slower processing
                    - zstd: Good balance of speed and compression ratio
    
    Returns:
        Dictionary containing:
        - status: Success/failure status
        - file_info: Created file details including size and compression stats
        - write_stats: Performance metrics for the write operation
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
    description="Extract detailed schema information from a Parquet file including column names, data types, nullable constraints, and nested structure details for complex data types."
)
async def get_schema_tool(file_path: str) -> dict:
    """
    Get comprehensive schema information from a Parquet file.
    
    Args:
        file_path: Absolute path to the Parquet file
    
    Returns:
        Dictionary containing:
        - columns: List of column definitions with names and types
        - schema_tree: Hierarchical schema structure
        - metadata: Schema-level metadata and statistics
        - data_types: Detailed type information for each column
    """
    logger.info(f"Getting schema for: {file_path}")
    return mcp_handlers.get_schema_handler(file_path)


@mcp.tool(
    name="get_parquet_metadata",
    description="Extract comprehensive metadata from a Parquet file including file size, row groups, column chunks, compression statistics, and encoding information for performance analysis."
)
async def get_metadata_tool(file_path: str) -> dict:
    """
    Get detailed metadata from a Parquet file.
    
    Args:
        file_path: Absolute path to the Parquet file
    
    Returns:
        Dictionary containing:
        - file_metadata: File-level information (size, version, creator)
        - row_groups: Information about row group structure and statistics
        - column_chunks: Details about column storage and compression
        - performance_stats: Metrics for optimization analysis
    """
    logger.info(f"Getting metadata for: {file_path}")
    return mcp_handlers.get_metadata_handler(file_path)


@mcp.tool(
    name="get_column_statistics",
    description="Calculate detailed statistics for columns in a Parquet file including min/max values, null counts, distinct value counts, and data distribution metrics for numerical and categorical columns."
)
async def get_statistics_tool(
    file_path: str,
    columns: Optional[List[str]] = None
) -> dict:
    """
    Get column statistics from a Parquet file.
    
    Args:
        file_path: Absolute path to the Parquet file
        columns: List of specific columns to analyze (None analyzes all columns)
    
    Returns:
        Dictionary containing:
        - column_stats: Statistical summary for each column
        - numeric_stats: Mean, median, std dev for numerical columns
        - categorical_stats: Frequency counts for categorical columns
        - data_quality: Null counts and data completeness metrics
    """
    logger.info(f"Getting statistics for: {file_path}")
    return mcp_handlers.get_statistics_handler(file_path, columns)


@mcp.tool(
    name="check_data_quality",
    description="Perform comprehensive data quality checks on a Parquet file including null value analysis, duplicate detection, data type validation, and consistency checks across columns."
)
async def check_quality_tool(file_path: str) -> dict:
    """
    Check data quality of a Parquet file.
    
    Args:
        file_path: Absolute path to the Parquet file
    
    Returns:
        Dictionary containing:
        - quality_score: Overall data quality assessment
        - null_analysis: Null value patterns and percentages
        - duplicate_check: Duplicate row detection results
        - data_consistency: Cross-column consistency validation
    """
    logger.info(f"Checking data quality for: {file_path}")
    return mcp_handlers.check_quality_handler(file_path)


@mcp.tool(
    name="convert_parquet_to_csv",
    description="Convert Parquet files to CSV format with optional column selection and row limiting. Maintains data integrity while providing human-readable output format."
)
async def convert_to_csv_tool(
    parquet_path: str,
    csv_path: str,
    columns: Optional[List[str]] = None,
    limit: Optional[int] = None
) -> dict:
    """
    Convert Parquet file to CSV format.
    
    Args:
        parquet_path: Absolute path to input Parquet file
        csv_path: Absolute path for output CSV file
        columns: List of specific columns to include (None includes all columns)
        limit: Maximum number of rows to convert (None converts all rows)
    
    Returns:
        Dictionary containing:
        - status: Conversion success/failure status
        - input_info: Source file information
        - output_info: Generated CSV file details
        - conversion_stats: Performance metrics and data summary
    """
    logger.info(f"Converting {parquet_path} to CSV: {csv_path}")
    return mcp_handlers.convert_format_handler(
        parquet_path, csv_path, "csv", columns=columns, limit=limit
    )


@mcp.tool(
    name="convert_csv_to_parquet",
    description="Convert CSV files to Parquet format with configurable compression algorithms. Optimizes storage space and query performance while preserving data types and structure."
)
async def convert_from_csv_tool(
    csv_path: str,
    parquet_path: str,
    compression: str = "snappy"
) -> dict:
    """
    Convert CSV file to Parquet format.
    
    Args:
        csv_path: Absolute path to input CSV file
        parquet_path: Absolute path for output Parquet file
        compression: Compression algorithm to use (snappy, gzip, lz4, brotli, zstd)
    
    Returns:
        Dictionary containing:
        - status: Conversion success/failure status
        - input_info: Source CSV file information
        - output_info: Generated Parquet file details
        - compression_stats: Space savings and performance metrics
    """
    logger.info(f"Converting {csv_path} to Parquet: {parquet_path}")
    return mcp_handlers.convert_format_handler(
        csv_path, parquet_path, "parquet", compression=compression
    )


@mcp.tool(
    name="convert_parquet_to_json",
    description="Convert Parquet files to JSON format with flexible output orientations. Supports various JSON structures including records, indexed, and nested formats for different use cases."
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
        parquet_path: Absolute path to input Parquet file
        json_path: Absolute path for output JSON file
        columns: List of columns to include (None for all columns)
        limit: Maximum number of rows to convert (None converts all rows)
        orient: JSON orientation format:
                - 'records': List of dictionaries (default)
                - 'index': Dictionary with index as keys
                - 'values': Just the values array
                - 'table': Table-like structure with schema
    
    Returns:
        Dictionary containing:
        - status: Conversion success/failure status
        - input_info: Source file information
        - output_info: Generated JSON file details
        - conversion_stats: Performance metrics and data summary
    """
    logger.info(f"Converting {parquet_path} to JSON: {json_path}")
    return mcp_handlers.convert_format_handler(
        parquet_path, json_path, "json", columns=columns, limit=limit, orient=orient
    )


@mcp.tool(
    name="convert_json_to_parquet",
    description="Convert JSON files to Parquet format with configurable compression algorithms. Handles various JSON structures and optimizes them for efficient columnar storage."
)
async def convert_from_json_tool(
    json_path: str,
    parquet_path: str,
    compression: str = "snappy"
) -> dict:
    """
    Convert JSON file to Parquet format.
    
    Args:
        json_path: Absolute path to input JSON file
        parquet_path: Absolute path for output Parquet file
        compression: Compression algorithm to use (snappy, gzip, lz4, brotli, zstd)
    
    Returns:
        Dictionary containing:
        - status: Conversion success/failure status
        - input_info: Source JSON file information
        - output_info: Generated Parquet file details
        - compression_stats: Space savings and performance metrics
    """
    logger.info(f"Converting {json_path} to Parquet: {parquet_path}")
    return mcp_handlers.convert_format_handler(
        json_path, parquet_path, "parquet", compression=compression
    )


@mcp.tool(
    name="get_compression_stats",
    description="Get detailed compression statistics and efficiency metrics for a Parquet file including compression ratios, encoded sizes, and performance impact analysis for different compression algorithms."
)
async def get_compression_tool(file_path: str) -> dict:
    """
    Get compression statistics for a Parquet file.
    
    Args:
        file_path: Absolute path to the Parquet file
    
    Returns:
        Dictionary containing:
        - compression_info: Detailed compression statistics
        - efficiency_metrics: Compression ratio and space savings
        - performance_impact: Read/write performance implications
        - algorithm_comparison: Comparative analysis of compression options
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
