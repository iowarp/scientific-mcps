#!/usr/bin/env python3
"""
Parallel Sort MCP Server implementation using Model Context Protocol.
Provides log file sorting capabilities by timestamp.
"""
import os
import sys
import json
from fastmcp import FastMCP
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
mcp = FastMCP("ParallelSortMCP")

@mcp.tool(
    name="sort_log_by_timestamp",
    description="Sort log file lines by timestamps in YYYY-MM-DD HH:MM:SS format. Handles edge cases like empty files and invalid timestamps."
)
async def sort_log_tool(file_path: str) -> dict:
    """
    Sort log file entries by timestamp.
    
    Args:
        file_path: Path to the log file to sort
        
    Returns:
        Dictionary with sorted log entries and processing statistics
    """
    logger.info(f"Sorting log file: {file_path}")
    return await mcp_handlers.sort_log_handler(file_path)


@mcp.tool(
    name="parallel_sort_large_file",
    description="Sort large log files using parallel processing with chunked approach for improved performance."
)
async def parallel_sort_tool(file_path: str, chunk_size_mb: int = 100, max_workers: int = None) -> dict:
    """
    Sort large log files using parallel processing.
    
    Args:
        file_path: Path to the log file to sort
        chunk_size_mb: Size of each chunk in MB (default: 100)
        max_workers: Maximum number of worker processes (default: CPU count)
        
    Returns:
        Dictionary with sorted log entries and processing statistics
    """
    logger.info(f"Parallel sorting large file: {file_path}")
    return await mcp_handlers.parallel_sort_handler(file_path, chunk_size_mb, max_workers)


@mcp.tool(
    name="analyze_log_statistics",
    description="Generate comprehensive statistics and analysis for log files including temporal patterns, log levels, and quality metrics."
)
async def analyze_statistics_tool(file_path: str) -> dict:
    """
    Analyze log file statistics.
    
    Args:
        file_path: Path to the log file to analyze
        
    Returns:
        Dictionary with comprehensive log analysis and statistics
    """
    logger.info(f"Analyzing log statistics: {file_path}")
    return await mcp_handlers.analyze_statistics_handler(file_path)


@mcp.tool(
    name="detect_log_patterns",
    description="Detect patterns in log files including anomalies, error clusters, trending issues, and repeated patterns."
)
async def detect_patterns_tool(file_path: str, detection_config: dict = None) -> dict:
    """
    Detect patterns in log files.
    
    Args:
        file_path: Path to the log file to analyze
        detection_config: Configuration for pattern detection algorithms
        
    Returns:
        Dictionary with detected patterns and analysis
    """
    logger.info(f"Detecting patterns in: {file_path}")
    return await mcp_handlers.detect_patterns_handler(file_path, detection_config)


@mcp.tool(
    name="filter_logs",
    description="Filter log entries based on multiple conditions with support for complex logical operations."
)
async def filter_logs_tool(file_path: str, filter_conditions: list, logical_operator: str = "and") -> dict:
    """
    Filter log entries based on conditions.
    
    Args:
        file_path: Path to the log file to filter
        filter_conditions: List of filter condition dictionaries
        logical_operator: How to combine conditions ("and", "or")
        
    Returns:
        Dictionary with filtered log entries
    """
    logger.info(f"Filtering logs: {file_path}")
    return await mcp_handlers.filter_logs_handler(file_path, filter_conditions, logical_operator)


@mcp.tool(
    name="filter_by_time_range",
    description="Filter log entries by time range using start and end timestamps."
)
async def filter_time_range_tool(file_path: str, start_time: str, end_time: str) -> dict:
    """
    Filter log entries by time range.
    
    Args:
        file_path: Path to the log file
        start_time: Start time in ISO format or 'YYYY-MM-DD HH:MM:SS'
        end_time: End time in ISO format or 'YYYY-MM-DD HH:MM:SS'
        
    Returns:
        Dictionary with filtered log entries
    """
    logger.info(f"Filtering by time range: {file_path}")
    return await mcp_handlers.filter_time_range_handler(file_path, start_time, end_time)


@mcp.tool(
    name="filter_by_log_level",
    description="Filter log entries by log level (ERROR, WARN, INFO, DEBUG, etc.)."
)
async def filter_level_tool(file_path: str, levels: str, exclude: bool = False) -> dict:
    """
    Filter log entries by log level.
    
    Args:
        file_path: Path to the log file
        levels: Comma-separated list of levels to filter
        exclude: If True, exclude these levels instead of including
        
    Returns:
        Dictionary with filtered log entries
    """
    logger.info(f"Filtering by level: {file_path}")
    level_list = [level.strip() for level in levels.split(",")]
    return await mcp_handlers.filter_level_handler(file_path, level_list, exclude)


@mcp.tool(
    name="filter_by_keyword",
    description="Filter log entries by keywords in the message content with support for multiple keywords and logical operations."
)
async def filter_keyword_tool(file_path: str, keywords: str, case_sensitive: bool = False, match_all: bool = False) -> dict:
    """
    Filter log entries by keywords.
    
    Args:
        file_path: Path to the log file
        keywords: Comma-separated list of keywords
        case_sensitive: Whether to perform case-sensitive matching
        match_all: If True, all keywords must be present (AND), else any (OR)
        
    Returns:
        Dictionary with filtered log entries
    """
    logger.info(f"Filtering by keywords: {file_path}")
    keyword_list = [keyword.strip() for keyword in keywords.split(",")]
    return await mcp_handlers.filter_keyword_handler(file_path, keyword_list, case_sensitive, match_all)


@mcp.tool(
    name="apply_filter_preset",
    description="Apply predefined filter presets like 'errors_only', 'warnings_and_errors', 'connection_issues', etc."
)
async def filter_preset_tool(file_path: str, preset_name: str) -> dict:
    """
    Apply a predefined filter preset.
    
    Args:
        file_path: Path to the log file
        preset_name: Name of the preset to apply
        
    Returns:
        Dictionary with filtered log entries
    """
    logger.info(f"Applying filter preset '{preset_name}': {file_path}")
    return await mcp_handlers.filter_preset_handler(file_path, preset_name)


@mcp.tool(
    name="export_to_json",
    description="Export log processing results to JSON format with optional metadata."
)
async def export_json_tool(data: dict, include_metadata: bool = True) -> dict:
    """
    Export results to JSON format.
    
    Args:
        data: Processing results to export
        include_metadata: Whether to include processing metadata
        
    Returns:
        Dictionary with JSON export results
    """
    logger.info("Exporting to JSON format")
    return await mcp_handlers.export_json_handler(data, include_metadata)


@mcp.tool(
    name="export_to_csv",
    description="Export log entries to CSV format with structured columns for timestamp, level, and message."
)
async def export_csv_tool(data: dict, include_headers: bool = True) -> dict:
    """
    Export results to CSV format.
    
    Args:
        data: Processing results to export
        include_headers: Whether to include CSV headers
        
    Returns:
        Dictionary with CSV export results
    """
    logger.info("Exporting to CSV format")
    return await mcp_handlers.export_csv_handler(data, include_headers)


@mcp.tool(
    name="export_to_text",
    description="Export log entries to plain text format with optional processing summary."
)
async def export_text_tool(data: dict, include_summary: bool = True) -> dict:
    """
    Export results to text format.
    
    Args:
        data: Processing results to export
        include_summary: Whether to include processing summary
        
    Returns:
        Dictionary with text export results
    """
    logger.info("Exporting to text format")
    return await mcp_handlers.export_text_handler(data, include_summary)


@mcp.tool(
    name="generate_summary_report",
    description="Generate a comprehensive summary report of log processing results with statistics and analysis."
)
async def summary_report_tool(data: dict) -> dict:
    """
    Generate a summary report.
    
    Args:
        data: Processing results to summarize
        
    Returns:
        Dictionary with summary report
    """
    logger.info("Generating summary report")
    return await mcp_handlers.summary_report_handler(data)


def main():
    """
    Main entry point for the Parallel Sort MCP server.
    Supports both stdio and SSE transports based on environment variables.
    """
    try:
        logger.info("Starting Parallel Sort MCP Server")
        
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