"""
Parquet file metadata extraction capabilities.
Provides detailed information about file structure, statistics, and properties.
"""
import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List


def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract comprehensive metadata from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with detailed metadata
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        parquet_file = pq.ParquetFile(file_path)
        metadata = parquet_file.metadata
        
        # Basic file information
        file_info = {
            "file_path": str(file_path),
            "file_size_bytes": file_path.stat().st_size,
            "num_rows": metadata.num_rows,
            "num_columns": metadata.num_columns,
            "num_row_groups": metadata.num_row_groups,
            "format_version": metadata.format_version,
            "created_by": metadata.created_by,
            "serialized_size": metadata.serialized_size
        }
        
        # Schema information
        schema = parquet_file.schema.to_arrow_schema()
        schema_info = {
            "columns": [
                {
                    "name": field.name,
                    "type": str(field.type),
                    "nullable": field.nullable
                }
                for field in schema
            ]
        }
        
        # Row group information
        row_groups = []
        for i in range(metadata.num_row_groups):
            rg = metadata.row_group(i)
            row_group_info = {
                "id": i,
                "num_rows": rg.num_rows,
                "total_byte_size": rg.total_byte_size,
                "columns": []
            }
            
            for j in range(rg.num_columns):
                col = rg.column(j)
                col_info = {
                    "path_in_schema": col.path_in_schema,
                    "physical_type": col.physical_type,
                    "num_values": col.num_values,
                    "total_compressed_size": col.total_compressed_size,
                    "total_uncompressed_size": col.total_uncompressed_size,
                    "compression": col.compression,
                    "statistics": {"available": False, "note": "Statistics access skipped for compatibility"}
                }
                
                # Add optional metadata that might not be available in all PyArrow versions
                try:
                    col_info["has_dictionary_page"] = col.has_dictionary_page
                except Exception:
                    col_info["has_dictionary_page"] = "unknown"
                
                try:
                    col_info["has_index_page"] = col.has_index_page
                except Exception:
                    col_info["has_index_page"] = "unknown"
                
                row_group_info["columns"].append(col_info)
            
            row_groups.append(row_group_info)
        
        return {
            "success": True,
            "file_info": file_info,
            "schema": schema_info,
            "row_groups": row_groups
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_compression_stats(file_path: str) -> Dict[str, Any]:
    """
    Get compression statistics and efficiency metrics.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with compression statistics
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        parquet_file = pq.ParquetFile(file_path)
        metadata = parquet_file.metadata
        
        total_compressed = 0
        total_uncompressed = 0
        compression_types = set()
        
        for i in range(metadata.num_row_groups):
            rg = metadata.row_group(i)
            for j in range(rg.num_columns):
                col = rg.column(j)
                total_compressed += col.total_compressed_size
                total_uncompressed += col.total_uncompressed_size
                compression_types.add(col.compression)
        
        compression_ratio = total_uncompressed / total_compressed if total_compressed > 0 else 0
        space_savings = ((total_uncompressed - total_compressed) / total_uncompressed * 100) if total_uncompressed > 0 else 0
        
        return {
            "success": True,
            "total_compressed_size": total_compressed,
            "total_uncompressed_size": total_uncompressed,
            "compression_ratio": round(compression_ratio, 2),
            "space_savings_percent": round(space_savings, 2),
            "compression_types": list(compression_types),
            "file_size_bytes": file_path.stat().st_size
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
