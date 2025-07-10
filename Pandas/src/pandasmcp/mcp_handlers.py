"""
MCP handlers for Pandas operations.
These handlers wrap the pandas capabilities for MCP protocol compliance.
"""
import json
from typing import Optional, List, Any, Dict
from .capabilities.data_io import load_data_file, save_data_file
from .capabilities.statistics import get_statistical_summary, get_correlation_analysis
from .capabilities.data_cleaning import handle_missing_data, clean_data
from .capabilities.data_profiling import profile_data
from .capabilities.transformations import groupby_operations, merge_datasets, create_pivot_table
from .capabilities.time_series import time_series_operations
from .capabilities.memory_optimization import optimize_memory_usage
from .capabilities.validation import validate_data, hypothesis_testing
from .capabilities.filtering import filter_data


def load_data_handler(file_path: str, file_format: Optional[str] = None,
                     sheet_name: Optional[str] = None, encoding: Optional[str] = None,
                     columns: Optional[List[str]] = None, nrows: Optional[int] = None) -> dict:
    """Handler for loading data from files"""
    try:
        result = load_data_file(file_path, file_format, sheet_name, encoding, columns, nrows)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "load_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "load_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "load_data", "error": type(e).__name__},
            "isError": True
        }


def save_data_handler(data: dict, file_path: str, file_format: Optional[str] = None,
                     index: bool = True) -> dict:
    """Handler for saving data to files"""
    try:
        result = save_data_file(data, file_path, file_format, index)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "save_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "save_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "save_data", "error": type(e).__name__},
            "isError": True
        }


def statistical_summary_handler(file_path: str, columns: Optional[List[str]] = None,
                               include_distributions: bool = False) -> dict:
    """Handler for statistical summaries"""
    try:
        result = get_statistical_summary(file_path, columns, include_distributions)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "statistical_summary", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "statistical_summary", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "statistical_summary", "error": type(e).__name__},
            "isError": True
        }


def correlation_analysis_handler(file_path: str, method: str = "pearson",
                                columns: Optional[List[str]] = None) -> dict:
    """Handler for correlation analysis"""
    try:
        result = get_correlation_analysis(file_path, method, columns)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "correlation_analysis", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "correlation_analysis", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "correlation_analysis", "error": type(e).__name__},
            "isError": True
        }


def handle_missing_data_handler(file_path: str, strategy: str = "detect",
                               method: Optional[str] = None, columns: Optional[List[str]] = None) -> dict:
    """Handler for missing data operations"""
    try:
        result = handle_missing_data(file_path, strategy, method, columns)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "handle_missing_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "handle_missing_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "handle_missing_data", "error": type(e).__name__},
            "isError": True
        }


def clean_data_handler(file_path: str, remove_duplicates: bool = False,
                      detect_outliers: bool = False, convert_types: bool = False) -> dict:
    """Handler for data cleaning operations"""
    try:
        result = clean_data(file_path, remove_duplicates, detect_outliers, convert_types)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "clean_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "clean_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "clean_data", "error": type(e).__name__},
            "isError": True
        }


def groupby_operations_handler(file_path: str, group_by: List[str], operations: Dict[str, str],
                              filter_condition: Optional[str] = None) -> dict:
    """Handler for groupby operations"""
    try:
        result = groupby_operations(file_path, group_by, operations, filter_condition)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "groupby_operations", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "groupby_operations", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "groupby_operations", "error": type(e).__name__},
            "isError": True
        }


def merge_datasets_handler(left_file: str, right_file: str, join_type: str = "inner",
                          left_on: Optional[str] = None, right_on: Optional[str] = None,
                          on: Optional[str] = None) -> dict:
    """Handler for merging datasets"""
    try:
        result = merge_datasets(left_file, right_file, join_type, left_on, right_on, on)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "merge_datasets", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "merge_datasets", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "merge_datasets", "error": type(e).__name__},
            "isError": True
        }


def pivot_table_handler(file_path: str, index: List[str], columns: Optional[List[str]] = None,
                       values: Optional[List[str]] = None, aggfunc: str = "mean") -> dict:
    """Handler for pivot table operations"""
    try:
        result = create_pivot_table(file_path, index, columns, values, aggfunc)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "pivot_table", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "pivot_table", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "pivot_table", "error": type(e).__name__},
            "isError": True
        }


def time_series_operations_handler(file_path: str, date_column: str, operation: str,
                                  window_size: Optional[int] = None, frequency: Optional[str] = None) -> dict:
    """Handler for time series operations"""
    try:
        result = time_series_operations(file_path, date_column, operation, window_size, frequency)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "time_series_operations", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "time_series_operations", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "time_series_operations", "error": type(e).__name__},
            "isError": True
        }


def validate_data_handler(file_path: str, validation_rules: Dict[str, Dict[str, Any]]) -> dict:
    """Handler for data validation"""
    try:
        result = validate_data(file_path, validation_rules)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "validate_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "validate_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "validate_data", "error": type(e).__name__},
            "isError": True
        }


def hypothesis_testing_handler(file_path: str, test_type: str, column1: str,
                              column2: Optional[str] = None, alpha: float = 0.05) -> dict:
    """Handler for hypothesis testing"""
    try:
        result = hypothesis_testing(file_path, test_type, column1, column2, alpha)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "hypothesis_testing", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "hypothesis_testing", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "hypothesis_testing", "error": type(e).__name__},
            "isError": True
        }


def optimize_memory_handler(file_path: str, optimize_dtypes: bool = True,
                           chunk_size: Optional[int] = None) -> dict:
    """Handler for memory optimization"""
    try:
        result = optimize_memory_usage(file_path, optimize_dtypes, chunk_size)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "optimize_memory", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "optimize_memory", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "optimize_memory", "error": type(e).__name__},
            "isError": True
        }


def profile_data_handler(file_path: str, include_correlations: bool = False,
                        sample_size: Optional[int] = None) -> dict:
    """Handler for data profiling"""
    try:
        result = profile_data(file_path, include_correlations, sample_size)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "profile_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "profile_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "profile_data", "error": type(e).__name__},
            "isError": True
        }


def filter_data_handler(file_path: str, filter_conditions: Dict[str, Any],
                       output_file: Optional[str] = None) -> dict:
    """Handler for data filtering"""
    try:
        result = filter_data(file_path, filter_conditions, output_file)
        if result.get("success"):
            return {
                "content": [{"text": json.dumps(result, indent=2)}],
                "_meta": {"tool": "filter_data", "success": True}
            }
        else:
            return {
                "content": [{"text": json.dumps(result)}],
                "_meta": {"tool": "filter_data", "error": result.get("error_type", "Unknown")},
                "isError": True
            }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "filter_data", "error": type(e).__name__},
            "isError": True
        }
