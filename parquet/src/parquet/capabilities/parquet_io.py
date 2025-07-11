"""
Core Parquet file operations using PyArrow.
Provides read/write functionality with schema inference.
"""
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


def read_parquet_file(file_path: str, columns: Optional[List[str]] = None, 
                     filters: Optional[List] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Read Parquet file with optional column selection and filtering.
    
    Args:
        file_path: Path to the Parquet file
        columns: List of columns to read (None for all)
        filters: List of filters to apply
        limit: Maximum number of rows to return
    
    Returns:
        Dictionary with data and metadata
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read the parquet file
        table = pq.read_table(
            file_path,
            columns=columns,
            filters=filters
        )
        
        # Apply row limit if specified
        if limit:
            table = table.slice(0, limit)
        
        # Convert to pandas for easier JSON serialization
        df = table.to_pandas()
        
        # Convert any datetime/timestamp/date columns to strings for JSON serialization
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
            elif pd.api.types.is_object_dtype(df[col]):
                # Check if object column contains date/datetime objects
                if len(df[col].dropna()) > 0:
                    first_val = df[col].dropna().iloc[0]
                    if isinstance(first_val, (pd.Timestamp, pd.Timedelta, pd.Period)):
                        df[col] = df[col].astype(str)
        
        # Additional safety: ensure all data is JSON serializable
        try:
            data_dict = df.to_dict(orient='records')
            # Test serialization to catch any remaining issues
            json.dumps(data_dict[:1])  # Test with first record
        except (TypeError, ValueError) as e:
            # If serialization fails, convert all object columns to strings
            for col in df.columns:
                if pd.api.types.is_object_dtype(df[col]):
                    df[col] = df[col].astype(str)
            data_dict = df.to_dict(orient='records')
        
        return {
            "success": True,
            "data": data_dict,
            "schema": {col: str(table.schema.field(col).type) for col in table.column_names},
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "columns": list(df.columns),
            "file_path": str(file_path)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def write_parquet_file(data: Any, file_path: str, compression: str = "snappy") -> Dict[str, Any]:
    """
    Write data to Parquet file with specified compression.
    
    Args:
        data: Data to write (dict, list of dicts, or pandas DataFrame)
        file_path: Output file path
        compression: Compression algorithm (snappy, gzip, lz4, etc.)
    
    Returns:
        Dictionary with operation result
    """
    try:
        # Convert data to pandas DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")
        
        # Create output directory if it doesn't exist
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to parquet
        table = pa.Table.from_pandas(df)
        pq.write_table(table, output_path, compression=compression)
        
        return {
            "success": True,
            "file_path": str(output_path),
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "compression": compression,
            "file_size_bytes": output_path.stat().st_size
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_parquet_schema(file_path: str) -> Dict[str, Any]:
    """
    Get detailed schema information from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with schema information
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read just the schema without loading data
        parquet_file = pq.ParquetFile(file_path)
        schema = parquet_file.schema.to_arrow_schema()
        
        schema_info = {
            "columns": [],
            "num_columns": len(schema),
            "metadata": {}
        }
        
        # Handle metadata safely
        if schema.metadata:
            try:
                metadata_dict = {}
                for key, value in schema.metadata.items():
                    # Convert bytes keys/values to strings
                    key_str = key.decode('utf-8') if isinstance(key, bytes) else str(key)
                    value_str = value.decode('utf-8') if isinstance(value, bytes) else str(value)
                    metadata_dict[key_str] = value_str
                schema_info["metadata"] = metadata_dict
            except Exception:
                schema_info["metadata"] = {}
        
        for i, field in enumerate(schema):
            field_metadata = {}
            if field.metadata:
                try:
                    for key, value in field.metadata.items():
                        key_str = key.decode('utf-8') if isinstance(key, bytes) else str(key)
                        value_str = value.decode('utf-8') if isinstance(value, bytes) else str(value)
                        field_metadata[key_str] = value_str
                except Exception:
                    field_metadata = {}
            
            schema_info["columns"].append({
                "name": field.name,
                "type": str(field.type),
                "nullable": field.nullable,
                "metadata": field_metadata
            })
        
        return {
            "success": True,
            "schema": schema_info,
            "file_path": str(file_path)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
