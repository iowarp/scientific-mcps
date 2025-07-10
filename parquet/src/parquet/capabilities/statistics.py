"""
Statistical analysis capabilities for Parquet files.
Provides column statistics, data quality checks, and analysis functions.
"""
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional


def get_column_statistics(file_path: str, columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for columns in a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
        columns: List of columns to analyze (None for all)
    
    Returns:
        Dictionary with column statistics
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read the table
        table = pq.read_table(file_path, columns=columns)
        
        stats = {}
        for column_name in table.column_names:
            column = table.column(column_name)
            column_stats = {
                "type": str(column.type),
                "length": len(column),
                "null_count": pc.sum(pc.is_null(column)).as_py(),
                "non_null_count": pc.sum(pc.is_valid(column)).as_py(),
                "unique_count": None,
                "min": None,
                "max": None,
                "mean": None,
                "std": None,
                "median": None
            }
            
            # Calculate null percentage
            column_stats["null_percentage"] = float((column_stats["null_count"] / len(column) * 100) if len(column) > 0 else 0)
            
            # Skip further calculations if all values are null
            if column_stats["non_null_count"] == 0:
                stats[column_name] = column_stats
                continue
            
            # Get unique count
            try:
                unique_values = pc.unique(column)
                column_stats["unique_count"] = len(unique_values)
            except Exception:
                pass
            
            # Type-specific statistics
            if pa.types.is_integer(column.type) or pa.types.is_floating(column.type):
                try:
                    column_stats["min"] = float(pc.min(column).as_py())
                    column_stats["max"] = float(pc.max(column).as_py())
                    column_stats["mean"] = float(pc.mean(column).as_py())
                    column_stats["std"] = float(pc.stddev(column).as_py())
                    
                    # Convert to pandas for median calculation
                    pd_series = column.to_pandas()
                    column_stats["median"] = float(pd_series.median())
                    
                    # Additional numeric stats
                    column_stats["sum"] = float(pc.sum(column).as_py())
                    column_stats["variance"] = float(pc.variance(column).as_py())
                    
                except Exception as e:
                    column_stats["error"] = f"Error calculating numeric stats: {str(e)}"
            
            elif pa.types.is_string(column.type) or pa.types.is_large_string(column.type):
                try:
                    # String statistics
                    pd_series = column.to_pandas()
                    column_stats["min_length"] = int(pd_series.str.len().min())
                    column_stats["max_length"] = int(pd_series.str.len().max())
                    column_stats["avg_length"] = float(pd_series.str.len().mean())
                    
                except Exception as e:
                    column_stats["error"] = f"Error calculating string stats: {str(e)}"
            
            elif pa.types.is_temporal(column.type):
                try:
                    column_stats["min"] = str(pc.min(column).as_py())
                    column_stats["max"] = str(pc.max(column).as_py())
                except Exception as e:
                    column_stats["error"] = f"Error calculating temporal stats: {str(e)}"
            
            stats[column_name] = column_stats
        
        return {
            "success": True,
            "file_path": str(file_path),
            "total_rows": len(table),
            "total_columns": len(table.column_names),
            "column_statistics": stats
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def check_data_quality(file_path: str) -> Dict[str, Any]:
    """
    Perform data quality checks on a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
    
    Returns:
        Dictionary with data quality assessment
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        table = pq.read_table(file_path)
        total_rows = len(table)
        
        quality_report = {
            "file_path": str(file_path),
            "total_rows": total_rows,
            "total_columns": len(table.column_names),
            "issues": [],
            "column_quality": {}
        }
        
        for column_name in table.column_names:
            column = table.column(column_name)
            
            null_count = pc.sum(pc.is_null(column)).as_py()
            null_percentage = (null_count / total_rows * 100) if total_rows > 0 else 0
            
            column_quality = {
                "null_count": null_count,
                "null_percentage": round(null_percentage, 2),
                "issues": []
            }
            
            # Check for high null percentage
            if null_percentage > 50:
                issue = f"High null percentage ({null_percentage:.1f}%) in column '{column_name}'"
                column_quality["issues"].append(issue)
                quality_report["issues"].append(issue)
            
            # Check for completely null columns
            if null_percentage == 100:
                issue = f"Column '{column_name}' is completely null"
                column_quality["issues"].append(issue)
                quality_report["issues"].append(issue)
            
            # Check for single-value columns (no variance)
            if null_count < total_rows:  # Only if there are non-null values
                try:
                    unique_values = pc.unique(column)
                    if len(unique_values) == 1:
                        issue = f"Column '{column_name}' has only one unique value"
                        column_quality["issues"].append(issue)
                        quality_report["issues"].append(issue)
                except Exception:
                    pass
            
            quality_report["column_quality"][column_name] = column_quality
        
        # Overall quality score (percentage of columns without issues)
        columns_without_issues = sum(1 for col_quality in quality_report["column_quality"].values() 
                                   if not col_quality["issues"])
        quality_score = (columns_without_issues / len(table.column_names) * 100) if len(table.column_names) > 0 else 0
        
        quality_report["overall_quality_score"] = round(quality_score, 2)
        quality_report["total_issues"] = len(quality_report["issues"])
        
        return {
            "success": True,
            "quality_report": quality_report
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
