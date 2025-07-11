"""
MCP handlers for Parquet operations.
These handlers wrap the parquet capabilities for MCP protocol compliance.
"""
import json
from typing import Optional, List, Any, Dict
from .capabilities.parquet_io import read_parquet_file, write_parquet_file, get_parquet_schema
from .capabilities.metadata import get_file_metadata, get_compression_stats
from .capabilities.statistics import get_column_statistics, check_data_quality
from .capabilities.format_conversion import (
    parquet_to_csv, csv_to_parquet, parquet_to_json, json_to_parquet, get_conversion_info
)


def read_parquet_handler(file_path: str, columns: Optional[List[str]] = None, 
                        filters: Optional[List] = None, limit: Optional[int] = None) -> dict:
    """
    Handler for reading Parquet files with optional filtering.
    
    Args:
        file_path: Path to the Parquet file
        columns: List of columns to read
        filters: List of filters to apply
        limit: Maximum number of rows to return
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = read_parquet_file(file_path, columns, filters, limit)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "read_parquet", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "read_parquet", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_parquet", "error": type(e).__name__},
            "isError": True
        }


def write_parquet_handler(data: Any, file_path: str, compression: str = "snappy") -> dict:
    """
    Handler for writing data to Parquet files.
    
    Args:
        data: Data to write
        file_path: Output file path
        compression: Compression algorithm
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = write_parquet_file(data, file_path, compression)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "write_parquet", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "write_parquet", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "write_parquet", "error": type(e).__name__},
            "isError": True
        }


def schema_handler(file_path: str) -> dict:
    """
    Handler for getting Parquet file schema information.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_parquet_schema(file_path)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "schema", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "schema", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "schema", "error": type(e).__name__},
            "isError": True
        }


def metadata_handler(file_path: str) -> dict:
    """
    Handler for extracting file metadata.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_file_metadata(file_path)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "metadata", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "metadata", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "metadata", "error": type(e).__name__},
            "isError": True
        }


def statistics_handler(file_path: str, columns: Optional[List[str]] = None) -> dict:
    """
    Handler for getting column statistics.
    
    Args:
        file_path: Path to the Parquet file
        columns: List of columns to analyze
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_column_statistics(file_path, columns)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "statistics", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "statistics", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "statistics", "error": type(e).__name__},
            "isError": True
        }


def check_quality_handler(file_path: str) -> dict:
    """
    Handler for data quality checks.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = check_data_quality(file_path)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "check_quality", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "check_quality", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "check_quality", "error": type(e).__name__},
            "isError": True
        }


def convert_format_handler(input_path: str, output_path: str, 
                          output_format: str, **kwargs) -> dict:
    """
    Handler for format conversion operations.
    
    Args:
        input_path: Path to input file
        output_path: Path for output file
        output_format: Target format ('csv', 'json', 'parquet')
        **kwargs: Additional conversion parameters
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        format_map = {
            'csv': {
                'parquet': parquet_to_csv,
                'from_csv': csv_to_parquet
            },
            'json': {
                'parquet': parquet_to_json,
                'from_json': json_to_parquet
            }
        }
        
        # Determine conversion function based on file extensions
        input_ext = input_path.split('.')[-1].lower()
        output_ext = output_format.lower()
        
        if input_ext == 'parquet' and output_ext in format_map:
            conversion_func = format_map[output_ext]['parquet']
            result = conversion_func(input_path, output_path, **kwargs)
        elif output_ext == 'parquet' and f'from_{input_ext}' in format_map.get(input_ext, {}):
            conversion_func = format_map[input_ext][f'from_{input_ext}']
            result = conversion_func(input_path, output_path, **kwargs)
        else:
            result = {
                "success": False,
                "error": f"Unsupported conversion from {input_ext} to {output_ext}",
                "error_type": "UnsupportedConversion"
            }
        
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "convert_format", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "convert_format", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "convert_format", "error": type(e).__name__},
            "isError": True
        }


def compression_handler(file_path: str) -> dict:
    """
    Handler for getting compression statistics.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_compression_stats(file_path)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "compression", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "compression", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "compression", "error": type(e).__name__},
            "isError": True
        }
