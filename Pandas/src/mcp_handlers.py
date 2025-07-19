"""
MCP handlers for Pandas operations.
These handlers wrap the pandas capabilities for MCP protocol compliance.
"""
import json
from typing import Optional, List, Any, Dict

# Import the beautiful formatter
try:
    from implementation.output_formatter import create_beautiful_response
except ImportError:
    # Fallback for development/testing
    def create_beautiful_response(operation: str, success: bool, data=None, **kwargs):
        return {
            "content": [{"text": json.dumps({"operation": operation, "success": success, "data": data}, indent=2)}],
            "_meta": {"tool": operation, "success": success},
            "isError": not success
        }

from implementation.data_io import load_data_file, save_data_file
from implementation.pandas_statistics import get_statistical_summary, get_correlation_analysis
from implementation.data_cleaning import handle_missing_data, clean_data
from implementation.data_profiling import profile_data
from implementation.transformations import groupby_operations, merge_datasets, create_pivot_table
from implementation.time_series import time_series_operations
from implementation.memory_optimization import optimize_memory_usage
from implementation.validation import validate_data, hypothesis_testing
from implementation.filtering import filter_data


def load_data_handler(file_path: str, file_format: Optional[str] = None,
                     sheet_name: Optional[str] = None, encoding: Optional[str] = None,
                     columns: Optional[List[str]] = None, nrows: Optional[int] = None) -> dict:
    """Handler for loading data from files with beautiful formatting"""
    try:
        result = load_data_file(file_path, file_format, sheet_name, encoding, columns, nrows)
        
        if result.get("success"):
            summary = {
                "total_rows": result.get("total_rows", 0),
                "file_format": result.get("file_format", "unknown"),
                "memory_usage": result.get("info", {}).get("memory_usage", 0),
                "columns_loaded": len(result.get("info", {}).get("columns", []))
            }
            
            metadata = {
                "file_path": result.get("file_path", ""),
                "encoding": encoding or "auto-detected",
                "sheet_name": sheet_name or "default"
            }
            
            insights = [
                f"Successfully loaded {result.get('total_rows', 0):,} rows from {file_path}",
                f"Dataset contains {len(result.get('info', {}).get('columns', []))} columns",
                f"Memory usage: {result.get('info', {}).get('memory_usage', 0) / 1024 / 1024:.2f} MB"
            ]
            
            return create_beautiful_response(
                operation="load_data",
                success=True,
                data=result.get("data", []),
                summary=summary,
                metadata=metadata,
                insights=insights
            )
        else:
            suggestions = [
                "Check if the file path exists and is accessible",
                "Verify the file format is supported (CSV, Excel, JSON, Parquet, HDF5)",
                "Try specifying the encoding parameter for text files",
                "Check file permissions and ensure the file is not locked"
            ]
            
            return create_beautiful_response(
                operation="load_data",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=suggestions
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="load_data",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__,
            suggestions=["Check file path and permissions", "Verify file format compatibility"]
        )


def save_data_handler(data: dict, file_path: str, file_format: Optional[str] = None,
                     index: bool = True) -> dict:
    """Handler for saving data to files with beautiful formatting"""
    try:
        result = save_data_file(data, file_path, file_format, index)
        
        if result.get("success"):
            summary = {
                "file_saved": result.get("file_path", ""),
                "file_format": result.get("file_format", "unknown"),
                "file_size": result.get("file_size", 0),
                "rows_saved": result.get("rows_saved", 0)
            }
            
            metadata = {
                "compression": result.get("compression", "none"),
                "index_included": index,
                "save_time": result.get("save_time", 0)
            }
            
            insights = [
                f"Successfully saved {result.get('rows_saved', 0):,} rows to {file_path}",
                f"File size: {result.get('file_size', 0) / 1024 / 1024:.2f} MB",
                f"Format: {result.get('file_format', 'unknown').upper()}"
            ]
            
            return create_beautiful_response(
                operation="save_data",
                success=True,
                data={"file_path": result.get("file_path", "")},
                summary=summary,
                metadata=metadata,
                insights=insights
            )
        else:
            suggestions = [
                "Check if the directory exists and is writable",
                "Verify sufficient disk space is available",
                "Ensure the file format is supported",
                "Check file permissions for the target location"
            ]
            
            return create_beautiful_response(
                operation="save_data",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=suggestions
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="save_data",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__,
            suggestions=["Check file path and permissions", "Verify data format compatibility"]
        )


def statistical_summary_handler(file_path: str, columns: Optional[List[str]] = None,
                               include_distributions: bool = False) -> dict:
    """Handler for statistical summary with beautiful formatting"""
    try:
        result = get_statistical_summary(file_path, columns, include_distributions)
        
        if result.get("success"):
            summary = {
                "columns_analyzed": len(result.get("descriptive_stats", {})),
                "total_rows": result.get("total_rows", 0),
                "missing_values_found": sum(result.get("missing_values", {}).values()),
                "distributions_analyzed": include_distributions
            }
            
            metadata = {
                "analysis_type": "descriptive_statistics",
                "include_distributions": include_distributions,
                "columns_requested": columns or "all_numeric"
            }
            
            insights = []
            if result.get("descriptive_stats"):
                for col, stats in result.get("descriptive_stats", {}).items():
                    mean_val = stats.get("mean", 0)
                    std_val = stats.get("std", 0)
                    insights.append(f"{col}: Mean={mean_val:.2f}, Std={std_val:.2f}")
            
            return create_beautiful_response(
                operation="statistical_summary",
                success=True,
                data=result,
                summary=summary,
                metadata=metadata,
                insights=insights[:5]  # Top 5 insights
            )
        else:
            suggestions = [
                "Check if the file contains numerical columns",
                "Verify the file path is correct and accessible",
                "Try specifying specific columns to analyze",
                "Ensure the data is properly formatted"
            ]
            
            return create_beautiful_response(
                operation="statistical_summary",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=suggestions
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="statistical_summary",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__,
            suggestions=["Check file format and data quality", "Verify column names and types"]
        )


def correlation_analysis_handler(file_path: str, method: str = "pearson",
                                columns: Optional[List[str]] = None) -> dict:
    """Handler for correlation analysis with beautiful formatting"""
    try:
        result = get_correlation_analysis(file_path, method, columns)
        
        if result.get("success"):
            corr_matrix = result.get("correlation_matrix", {})
            strong_correlations = []
            
            # Find strong correlations
            for col1, correlations in corr_matrix.items():
                for col2, corr in correlations.items():
                    if col1 != col2 and abs(corr) > 0.7:
                        strong_correlations.append(f"{col1} ↔ {col2}: {corr:.3f}")
            
            summary = {
                "correlation_method": method,
                "variables_analyzed": len(corr_matrix),
                "strong_correlations_found": len(strong_correlations),
                "correlation_threshold": 0.7
            }
            
            metadata = {
                "method": method,
                "columns_analyzed": list(corr_matrix.keys()) if corr_matrix else [],
                "matrix_size": f"{len(corr_matrix)}×{len(corr_matrix)}"
            }
            
            insights = [
                f"Found {len(strong_correlations)} strong correlations (|r| > 0.7)",
                f"Analyzed {len(corr_matrix)} variables using {method} method"
            ] + strong_correlations[:3]  # Top 3 strong correlations
            
            return create_beautiful_response(
                operation="correlation_analysis",
                success=True,
                data=result,
                summary=summary,
                metadata=metadata,
                insights=insights
            )
        else:
            suggestions = [
                "Ensure the dataset contains numerical variables",
                "Check if there are at least 2 columns for correlation",
                "Try a different correlation method (pearson, spearman, kendall)",
                "Verify data quality and remove missing values"
            ]
            
            return create_beautiful_response(
                operation="correlation_analysis",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=suggestions
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="correlation_analysis",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__,
            suggestions=["Check data types and missing values", "Verify column selection"]
        )


def handle_missing_data_handler(file_path: str, strategy: str = "detect",
                               method: Optional[str] = None, columns: Optional[List[str]] = None) -> dict:
    """Handler for missing data with beautiful formatting"""
    try:
        result = handle_missing_data(file_path, strategy, method, columns)
        
        if result.get("success"):
            summary = {
                "strategy_used": strategy,
                "imputation_method": method or "none",
                "columns_processed": len(result.get("processed_columns", [])),
                "missing_values_handled": result.get("missing_values_handled", 0)
            }
            
            metadata = {
                "original_missing_count": result.get("original_missing_count", 0),
                "final_missing_count": result.get("final_missing_count", 0),
                "columns_affected": result.get("processed_columns", [])
            }
            
            insights = [
                f"Strategy: {strategy.title()}",
                f"Processed {len(result.get('processed_columns', []))} columns",
                f"Handled {result.get('missing_values_handled', 0)} missing values"
            ]
            
            if method:
                insights.append(f"Used {method} imputation method")
            
            return create_beautiful_response(
                operation="handle_missing_data",
                success=True,
                data=result,
                summary=summary,
                metadata=metadata,
                insights=insights
            )
        else:
            suggestions = [
                "Check if the file contains missing values",
                "Try a different strategy (detect, impute, remove, analyze)",
                "Specify appropriate imputation method for your data type",
                "Verify column names and data types"
            ]
            
            return create_beautiful_response(
                operation="handle_missing_data",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=suggestions
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="handle_missing_data",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__,
            suggestions=["Check data format and column types", "Verify missing data patterns"]
        )


def clean_data_handler(file_path: str, remove_duplicates: bool = False,
                      detect_outliers: bool = False, convert_types: bool = False) -> dict:
    """Handler for data cleaning with beautiful formatting"""
    try:
        result = clean_data(file_path, remove_duplicates, detect_outliers, convert_types)
        
        if result.get("success"):
            summary = {
                "duplicates_removed": result.get("duplicates_removed", 0),
                "outliers_detected": result.get("outliers_detected", 0),
                "types_converted": result.get("types_converted", 0),
                "data_quality_improved": True
            }
            
            insights = [
                f"Removed {result.get('duplicates_removed', 0)} duplicate records",
                f"Detected {result.get('outliers_detected', 0)} outliers",
                f"Converted {result.get('types_converted', 0)} data types"
            ]
            
            return create_beautiful_response(
                operation="clean_data",
                success=True,
                data=result,
                summary=summary,
                insights=insights
            )
        else:
            return create_beautiful_response(
                operation="clean_data",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=["Check data format and quality", "Verify cleaning parameters"]
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="clean_data",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__
        )


def groupby_operations_handler(file_path: str, group_by: List[str], operations: Dict[str, str],
                              filter_condition: Optional[str] = None) -> dict:
    """Handler for groupby operations with beautiful formatting"""
    try:
        result = groupby_operations(file_path, group_by, operations, filter_condition)
        return create_beautiful_response("groupby_operations", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("groupby_operations", False, error_message=str(e), error_type=type(e).__name__)


def merge_datasets_handler(left_file: str, right_file: str, join_type: str = "inner",
                          left_on: Optional[str] = None, right_on: Optional[str] = None,
                          on: Optional[str] = None) -> dict:
    """Handler for dataset merging with beautiful formatting"""
    try:
        result = merge_datasets(left_file, right_file, join_type, left_on, right_on, on)
        return create_beautiful_response("merge_datasets", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("merge_datasets", False, error_message=str(e), error_type=type(e).__name__)


def pivot_table_handler(file_path: str, index: List[str], columns: Optional[List[str]] = None,
                       values: Optional[List[str]] = None, aggfunc: str = "mean") -> dict:
    """Handler for pivot tables with beautiful formatting"""
    try:
        result = create_pivot_table(file_path, index, columns, values, aggfunc)
        return create_beautiful_response("pivot_table", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("pivot_table", False, error_message=str(e), error_type=type(e).__name__)


def time_series_operations_handler(file_path: str, date_column: str, operation: str,
                                  window_size: Optional[int] = None, frequency: Optional[str] = None) -> dict:
    """Handler for time series operations with beautiful formatting"""
    try:
        result = time_series_operations(file_path, date_column, operation, window_size, frequency)
        return create_beautiful_response("time_series_operations", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("time_series_operations", False, error_message=str(e), error_type=type(e).__name__)


def validate_data_handler(file_path: str, validation_rules: Dict[str, Dict[str, Any]]) -> dict:
    """Handler for data validation with beautiful formatting"""
    try:
        result = validate_data(file_path, validation_rules)
        return create_beautiful_response("validate_data", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("validate_data", False, error_message=str(e), error_type=type(e).__name__)


def hypothesis_testing_handler(file_path: str, test_type: str, column1: str,
                              column2: Optional[str] = None, alpha: float = 0.05) -> dict:
    """Handler for hypothesis testing with beautiful formatting"""
    try:
        result = hypothesis_testing(file_path, test_type, column1, column2, alpha)
        return create_beautiful_response("hypothesis_testing", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("hypothesis_testing", False, error_message=str(e), error_type=type(e).__name__)


def optimize_memory_handler(file_path: str, optimize_dtypes: bool = True,
                           chunk_size: Optional[int] = None) -> dict:
    """Handler for memory optimization with beautiful formatting"""
    try:
        result = optimize_memory_usage(file_path, optimize_dtypes, chunk_size)
        return create_beautiful_response("optimize_memory", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("optimize_memory", False, error_message=str(e), error_type=type(e).__name__)


def profile_data_handler(file_path: str, include_correlations: bool = False,
                        sample_size: Optional[int] = None) -> dict:
    """Handler for data profiling with beautiful formatting"""
    try:
        result = profile_data(file_path, include_correlations, sample_size)
        
        if result.get("success"):
            summary = {
                "total_rows": result.get("shape", [0, 0])[0],
                "total_columns": result.get("shape", [0, 0])[1],
                "memory_usage": result.get("memory_usage", 0),
                "data_quality_score": result.get("data_quality_score", 0)
            }
            
            insights = [
                f"Dataset shape: {result.get('shape', [0, 0])[0]:,} rows × {result.get('shape', [0, 0])[1]:,} columns",
                f"Memory usage: {result.get('memory_usage', 0) / 1024 / 1024:.2f} MB",
                f"Data quality score: {result.get('data_quality_score', 0):.1%}"
            ]
            
            return create_beautiful_response(
                operation="profile_data",
                success=True,
                data=result,
                summary=summary,
                insights=insights
            )
        else:
            return create_beautiful_response(
                operation="profile_data",
                success=False,
                error_message=result.get("error", "Unknown error"),
                error_type=result.get("error_type", "UnknownError"),
                suggestions=["Check file format and accessibility", "Verify data structure"]
            )
            
    except Exception as e:
        return create_beautiful_response(
            operation="profile_data",
            success=False,
            error_message=str(e),
            error_type=type(e).__name__
        )


def filter_data_handler(file_path: str, filter_conditions: Dict[str, Any],
                       output_file: Optional[str] = None) -> dict:
    """Handler for data filtering with beautiful formatting"""
    try:
        result = filter_data(file_path, filter_conditions, output_file)
        return create_beautiful_response("filter_data", result.get("success", False), result)
    except Exception as e:
        return create_beautiful_response("filter_data", False, error_message=str(e), error_type=type(e).__name__)
