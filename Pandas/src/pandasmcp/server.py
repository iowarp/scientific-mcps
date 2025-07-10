#!/usr/bin/env python3
"""
Enhanced Pandas MCP Server with comprehensive data analysis capabilities.
Provides data loading, statistical analysis, cleaning, and transformation capabilities.
"""
import os
import sys
import json
import argparse
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging
from typing import Optional, List, Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from . import mcp_handlers

# Initialize MCP server
mcp = FastMCP("PandasMCP")

# Data I/O Tools
@mcp.tool(
    name="load_data",
    description="Load data from various file formats (CSV, Excel, JSON, Parquet, HDF5)"
)
async def load_data_tool(
    file_path: str,
    file_format: Optional[str] = None,
    sheet_name: Optional[str] = None,
    encoding: Optional[str] = None,
    columns: Optional[List[str]] = None,
    nrows: Optional[int] = None
) -> dict:
    """Load data from file"""
    logger.info(f"Loading data from: {file_path}")
    return mcp_handlers.load_data_handler(file_path, file_format, sheet_name, encoding, columns, nrows)

@mcp.tool(
    name="save_data",
    description="Save data to various file formats (CSV, Excel, JSON, Parquet, HDF5)"
)
async def save_data_tool(
    data: dict,
    file_path: str,
    file_format: Optional[str] = None,
    index: bool = True
) -> dict:
    """Save data to file"""
    logger.info(f"Saving data to: {file_path}")
    return mcp_handlers.save_data_handler(data, file_path, file_format, index)

# Statistical Analysis Tools
@mcp.tool(
    name="statistical_summary",
    description="Generate comprehensive statistical summaries (mean, median, std, percentiles, distributions)"
)
async def statistical_summary_tool(
    file_path: str,
    columns: Optional[List[str]] = None,
    include_distributions: bool = False
) -> dict:
    """Generate statistical summary"""
    logger.info(f"Generating statistical summary for: {file_path}")
    return mcp_handlers.statistical_summary_handler(file_path, columns, include_distributions)

@mcp.tool(
    name="correlation_analysis",
    description="Perform correlation analysis (Pearson, Spearman correlation matrices)"
)
async def correlation_analysis_tool(
    file_path: str,
    method: str = "pearson",
    columns: Optional[List[str]] = None
) -> dict:
    """Perform correlation analysis"""
    logger.info(f"Performing correlation analysis on: {file_path}")
    return mcp_handlers.correlation_analysis_handler(file_path, method, columns)

# Data Cleaning Tools
@mcp.tool(
    name="handle_missing_data",
    description="Handle missing data (detection, imputation, removal strategies)"
)
async def handle_missing_data_tool(
    file_path: str,
    strategy: str = "detect",
    method: Optional[str] = None,
    columns: Optional[List[str]] = None
) -> dict:
    """Handle missing data"""
    logger.info(f"Handling missing data in: {file_path}")
    return mcp_handlers.handle_missing_data_handler(file_path, strategy, method, columns)

@mcp.tool(
    name="clean_data",
    description="Clean data (outlier detection, duplicate removal, type conversion)"
)
async def clean_data_tool(
    file_path: str,
    remove_duplicates: bool = False,
    detect_outliers: bool = False,
    convert_types: bool = False
) -> dict:
    """Clean data"""
    logger.info(f"Cleaning data in: {file_path}")
    return mcp_handlers.clean_data_handler(file_path, remove_duplicates, detect_outliers, convert_types)

# Data Transformation Tools
@mcp.tool(
    name="groupby_operations",
    description="Perform groupby operations (aggregations, transformations, filtering)"
)
async def groupby_operations_tool(
    file_path: str,
    group_by: List[str],
    operations: Dict[str, str],
    filter_condition: Optional[str] = None
) -> dict:
    """Perform groupby operations"""
    logger.info(f"Performing groupby operations on: {file_path}")
    return mcp_handlers.groupby_operations_handler(file_path, group_by, operations, filter_condition)

@mcp.tool(
    name="merge_datasets",
    description="Merge/join datasets (inner, outer, left, right joins)"
)
async def merge_datasets_tool(
    left_file: str,
    right_file: str,
    join_type: str = "inner",
    left_on: Optional[str] = None,
    right_on: Optional[str] = None,
    on: Optional[str] = None
) -> dict:
    """Merge datasets"""
    logger.info(f"Merging datasets: {left_file} and {right_file}")
    return mcp_handlers.merge_datasets_handler(left_file, right_file, join_type, left_on, right_on, on)

@mcp.tool(
    name="pivot_table",
    description="Create pivot tables and cross-tabulations"
)
async def pivot_table_tool(
    file_path: str,
    index: List[str],
    columns: Optional[List[str]] = None,
    values: Optional[List[str]] = None,
    aggfunc: str = "mean"
) -> dict:
    """Create pivot table"""
    logger.info(f"Creating pivot table for: {file_path}")
    return mcp_handlers.pivot_table_handler(file_path, index, columns, values, aggfunc)

# Time Series Tools
@mcp.tool(
    name="time_series_operations",
    description="Perform time series operations (resampling, rolling windows, lag features)"
)
async def time_series_operations_tool(
    file_path: str,
    date_column: str,
    operation: str,
    window_size: Optional[int] = None,
    frequency: Optional[str] = None
) -> dict:
    """Perform time series operations"""
    logger.info(f"Performing time series operations on: {file_path}")
    return mcp_handlers.time_series_operations_handler(file_path, date_column, operation, window_size, frequency)

# Data Validation Tools
@mcp.tool(
    name="validate_data",
    description="Validate data (range checks, consistency validation)"
)
async def validate_data_tool(
    file_path: str,
    validation_rules: Dict[str, Dict[str, Any]]
) -> dict:
    """Validate data"""
    logger.info(f"Validating data in: {file_path}")
    return mcp_handlers.validate_data_handler(file_path, validation_rules)

# Hypothesis Testing Tools
@mcp.tool(
    name="hypothesis_testing",
    description="Perform hypothesis testing (t-tests, chi-square tests)"
)
async def hypothesis_testing_tool(
    file_path: str,
    test_type: str,
    column1: str,
    column2: Optional[str] = None,
    alpha: float = 0.05
) -> dict:
    """Perform hypothesis testing"""
    logger.info(f"Performing hypothesis testing on: {file_path}")
    return mcp_handlers.hypothesis_testing_handler(file_path, test_type, column1, column2, alpha)

# Memory Optimization Tools
@mcp.tool(
    name="optimize_memory",
    description="Optimize memory usage (efficient dtypes, chunking for large data)"
)
async def optimize_memory_tool(
    file_path: str,
    optimize_dtypes: bool = True,
    chunk_size: Optional[int] = None
) -> dict:
    """Optimize memory usage"""
    logger.info(f"Optimizing memory usage for: {file_path}")
    return mcp_handlers.optimize_memory_handler(file_path, optimize_dtypes, chunk_size)

# Data Profiling Tools
@mcp.tool(
    name="profile_data",
    description="Quick data profiling (shape, info, describe, value counts)"
)
async def profile_data_tool(
    file_path: str,
    include_correlations: bool = False,
    sample_size: Optional[int] = None
) -> dict:
    """Profile data"""
    logger.info(f"Profiling data in: {file_path}")
    return mcp_handlers.profile_data_handler(file_path, include_correlations, sample_size)

# Data Filtering Tools
@mcp.tool(
    name="filter_data",
    description="Filter data using boolean indexing"
)
async def filter_data_tool(
    file_path: str,
    filter_conditions: Dict[str, Any],
    output_file: Optional[str] = None
) -> dict:
    """Filter data"""
    logger.info(f"Filtering data in: {file_path}")
    return mcp_handlers.filter_data_handler(file_path, filter_conditions, output_file)

def main():
    """
    Main entry point for the Pandas MCP server.
    Supports both stdio and SSE transports based on environment variables or command line arguments.
    """
    parser = argparse.ArgumentParser(description="Pandas MCP Server")
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
        logger.info("Starting Pandas MCP Server")
        
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
