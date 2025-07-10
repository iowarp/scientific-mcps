"""
Format conversion capabilities for Parquet files.
Provides conversion to/from CSV, JSON, and other formats.
"""
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as csv
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union


def parquet_to_csv(parquet_path: str, csv_path: str, 
                  columns: Optional[list] = None, 
                  limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Convert Parquet file to CSV format.
    
    Args:
        parquet_path: Path to input Parquet file
        csv_path: Path for output CSV file
        columns: List of columns to include (None for all)
        limit: Maximum number of rows to convert
    
    Returns:
        Dictionary with conversion result
    """
    try:
        parquet_path = Path(parquet_path)
        csv_path = Path(csv_path)
        
        if not parquet_path.exists():
            raise FileNotFoundError(f"Parquet file not found: {parquet_path}")
        
        # Read parquet file
        table = pq.read_table(parquet_path, columns=columns)
        
        # Apply row limit if specified
        if limit:
            table = table.slice(0, limit)
        
        # Create output directory if needed
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to pandas and save as CSV
        df = table.to_pandas()
        df.to_csv(csv_path, index=False)
        
        return {
            "success": True,
            "input_file": str(parquet_path),
            "output_file": str(csv_path),
            "rows_converted": len(df),
            "columns_converted": len(df.columns),
            "output_size_bytes": csv_path.stat().st_size
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def csv_to_parquet(csv_path: str, parquet_path: str, 
                  compression: str = "snappy") -> Dict[str, Any]:
    """
    Convert CSV file to Parquet format.
    
    Args:
        csv_path: Path to input CSV file
        parquet_path: Path for output Parquet file
        compression: Compression algorithm to use
    
    Returns:
        Dictionary with conversion result
    """
    try:
        csv_path = Path(csv_path)
        parquet_path = Path(parquet_path)
        
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Read CSV file
        table = csv.read_csv(csv_path)
        
        # Create output directory if needed
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write as parquet
        pq.write_table(table, parquet_path, compression=compression)
        
        return {
            "success": True,
            "input_file": str(csv_path),
            "output_file": str(parquet_path),
            "rows_converted": len(table),
            "columns_converted": len(table.column_names),
            "compression": compression,
            "output_size_bytes": parquet_path.stat().st_size
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def parquet_to_json(parquet_path: str, json_path: str,
                   columns: Optional[list] = None,
                   limit: Optional[int] = None,
                   orient: str = "records") -> Dict[str, Any]:
    """
    Convert Parquet file to JSON format.
    
    Args:
        parquet_path: Path to input Parquet file
        json_path: Path for output JSON file
        columns: List of columns to include (None for all)
        limit: Maximum number of rows to convert
        orient: JSON orientation ('records', 'index', 'values', etc.)
    
    Returns:
        Dictionary with conversion result
    """
    try:
        parquet_path = Path(parquet_path)
        json_path = Path(json_path)
        
        if not parquet_path.exists():
            raise FileNotFoundError(f"Parquet file not found: {parquet_path}")
        
        # Read parquet file
        table = pq.read_table(parquet_path, columns=columns)
        
        # Apply row limit if specified
        if limit:
            table = table.slice(0, limit)
        
        # Create output directory if needed
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to pandas and save as JSON
        df = table.to_pandas()
        df.to_json(json_path, orient=orient, indent=2)
        
        return {
            "success": True,
            "input_file": str(parquet_path),
            "output_file": str(json_path),
            "rows_converted": len(df),
            "columns_converted": len(df.columns),
            "json_orient": orient,
            "output_size_bytes": json_path.stat().st_size
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def json_to_parquet(json_path: str, parquet_path: str,
                   compression: str = "snappy") -> Dict[str, Any]:
    """
    Convert JSON file to Parquet format.
    
    Args:
        json_path: Path to input JSON file
        parquet_path: Path for output Parquet file
        compression: Compression algorithm to use
    
    Returns:
        Dictionary with conversion result
    """
    try:
        json_path = Path(json_path)
        parquet_path = Path(parquet_path)
        
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        # Read JSON file
        df = pd.read_json(json_path)
        table = pa.Table.from_pandas(df)
        
        # Create output directory if needed
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write as parquet
        pq.write_table(table, parquet_path, compression=compression)
        
        return {
            "success": True,
            "input_file": str(json_path),
            "output_file": str(parquet_path),
            "rows_converted": len(df),
            "columns_converted": len(df.columns),
            "compression": compression,
            "output_size_bytes": parquet_path.stat().st_size
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_conversion_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about possible conversions for a file.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Dictionary with conversion possibilities
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = file_path.suffix.lower()
        file_size = file_path.stat().st_size
        
        supported_conversions = {
            ".parquet": ["CSV", "JSON"],
            ".csv": ["Parquet"],
            ".json": ["Parquet"]
        }
        
        available_conversions = supported_conversions.get(file_ext, [])
        
        return {
            "success": True,
            "file_path": str(file_path),
            "file_extension": file_ext,
            "file_size_bytes": file_size,
            "supported_output_formats": available_conversions,
            "compression_options": ["snappy", "gzip", "lz4", "brotli", "zstd"] if file_ext != ".parquet" else None
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
