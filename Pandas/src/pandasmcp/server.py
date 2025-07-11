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
    description="Load and parse data from multiple file formats with advanced options for data ingestion. Supports CSV, Excel, JSON, Parquet, HDF5 with customizable parsing, encoding detection, and selective column loading for efficient data processing."
)
async def load_data_tool(
    file_path: str,
    file_format: Optional[str] = None,
    sheet_name: Optional[str] = None,
    encoding: Optional[str] = None,
    columns: Optional[List[str]] = None,
    nrows: Optional[int] = None
) -> dict:
    """
    Load data from various file formats with comprehensive parsing options.
    
    Args:
        file_path: Absolute path to the data file
        file_format: File format (csv, excel, json, parquet, hdf5) - auto-detected if None
        sheet_name: Excel sheet name or index (for Excel files)
        encoding: Character encoding (utf-8, latin-1, etc.) - auto-detected if None
        columns: List of specific columns to load (None loads all columns)
        nrows: Maximum number of rows to load (None loads all rows)
    
    Returns:
        Dictionary containing:
        - data: Loaded dataset in structured format
        - metadata: File information, data types, and loading statistics
        - data_info: Shape, columns, and data quality metrics
        - loading_stats: Performance metrics and parsing information
    """
    logger.info(f"Loading data from: {file_path}")
    return mcp_handlers.load_data_handler(file_path, file_format, sheet_name, encoding, columns, nrows)

@mcp.tool(
    name="save_data",
    description="Save processed data to multiple file formats with optimization options for storage efficiency. Supports CSV, Excel, JSON, Parquet, HDF5 with compression, indexing, and format-specific customization for optimal data persistence."
)
async def save_data_tool(
    data: dict,
    file_path: str,
    file_format: Optional[str] = None,
    index: bool = True
) -> dict:
    """
    Save data to various file formats with comprehensive export options.
    
    Args:
        data: Data dictionary to save (structured data format)
        file_path: Absolute path where the file will be saved
        file_format: Output format (csv, excel, json, parquet, hdf5) - auto-detected if None
        index: Whether to include row indices in the output file
    
    Returns:
        Dictionary containing:
        - save_info: File save details including size and format
        - compression_stats: Space savings and compression metrics
        - export_stats: Performance metrics and data integrity checks
        - file_details: Output file specifications and validation
    """
    logger.info(f"Saving data to: {file_path}")
    return mcp_handlers.save_data_handler(data, file_path, file_format, index)

# Statistical Analysis Tools
@mcp.tool(
    name="statistical_summary",
    description="Generate comprehensive statistical summaries with descriptive statistics, distribution analysis, and data profiling. Provides detailed insights into data characteristics including central tendencies, variability, and distribution shapes."
)
async def statistical_summary_tool(
    file_path: str,
    columns: Optional[List[str]] = None,
    include_distributions: bool = False
) -> dict:
    """
    Generate comprehensive statistical summary with advanced analytics.
    
    Args:
        file_path: Absolute path to the data file
        columns: List of specific columns to analyze (None analyzes all numerical columns)
        include_distributions: Whether to include distribution analysis and normality tests
    
    Returns:
        Dictionary containing:
        - descriptive_stats: Mean, median, mode, standard deviation, and percentiles
        - distribution_analysis: Skewness, kurtosis, and normality test results
        - data_profiling: Data types, missing values, and unique value counts
        - outlier_detection: Outlier identification and statistical anomalies
    """
    logger.info(f"Generating statistical summary for: {file_path}")
    return mcp_handlers.statistical_summary_handler(file_path, columns, include_distributions)

@mcp.tool(
    name="correlation_analysis",
    description="Perform comprehensive correlation analysis with multiple correlation methods and significance testing. Provides detailed insights into variable relationships, dependency patterns, and statistical significance of correlations."
)
async def correlation_analysis_tool(
    file_path: str,
    method: str = "pearson",
    columns: Optional[List[str]] = None
) -> dict:
    """
    Perform comprehensive correlation analysis with statistical significance testing.
    
    Args:
        file_path: Absolute path to the data file
        method: Correlation method (pearson, spearman, kendall) for different data types
        columns: List of specific columns to analyze (None analyzes all numerical columns)
    
    Returns:
        Dictionary containing:
        - correlation_matrix: Full correlation matrix with coefficient values
        - significance_tests: P-values and statistical significance indicators
        - correlation_insights: Strong correlations and dependency patterns
        - visualization_data: Data formatted for correlation heatmaps and plots
    """
    logger.info(f"Performing correlation analysis on: {file_path}")
    return mcp_handlers.correlation_analysis_handler(file_path, method, columns)

# Data Cleaning Tools
@mcp.tool(
    name="handle_missing_data",
    description="Comprehensive missing data handling with multiple strategies for detection, imputation, and removal. Provides sophisticated approaches to data completeness including statistical imputation methods and missing data pattern analysis."
)
async def handle_missing_data_tool(
    file_path: str,
    strategy: str = "detect",
    method: Optional[str] = None,
    columns: Optional[List[str]] = None
) -> dict:
    """
    Handle missing data with comprehensive strategies and statistical methods.
    
    Args:
        file_path: Absolute path to the data file
        strategy: Missing data strategy (detect, impute, remove, analyze)
        method: Imputation method (mean, median, mode, forward_fill, backward_fill, interpolate)
        columns: List of specific columns to process (None processes all columns)
    
    Returns:
        Dictionary containing:
        - missing_data_report: Detailed analysis of missing data patterns
        - imputation_results: Results of imputation with quality metrics
        - data_completeness: Before/after comparison of data completeness
        - strategy_recommendations: Suggested approaches for optimal data handling
    """
    logger.info(f"Handling missing data in: {file_path}")
    return mcp_handlers.handle_missing_data_handler(file_path, strategy, method, columns)

@mcp.tool(
    name="clean_data",
    description="Comprehensive data cleaning with advanced outlier detection, duplicate removal, and intelligent type conversion. Provides sophisticated data quality improvement with statistical validation and automated data standardization."
)
async def clean_data_tool(
    file_path: str,
    remove_duplicates: bool = False,
    detect_outliers: bool = False,
    convert_types: bool = False
) -> dict:
    """
    Perform comprehensive data cleaning with advanced quality improvement techniques.
    
    Args:
        file_path: Absolute path to the data file
        remove_duplicates: Whether to identify and remove duplicate records
        detect_outliers: Whether to detect outliers using statistical methods (IQR, Z-score)
        convert_types: Whether to automatically convert data types for optimization
    
    Returns:
        Dictionary containing:
        - cleaning_report: Detailed summary of cleaning operations performed
        - data_quality_metrics: Before/after data quality comparison
        - outlier_analysis: Outlier detection results and recommendations
        - type_conversion_log: Data type changes and optimization results
    """
    logger.info(f"Cleaning data in: {file_path}")
    return mcp_handlers.clean_data_handler(file_path, remove_duplicates, detect_outliers, convert_types)

# Data Transformation Tools
@mcp.tool(
    name="groupby_operations",
    description="Perform sophisticated groupby operations with aggregations, transformations, and filtering. Provides comprehensive data grouping capabilities with multiple aggregation functions and advanced analytical operations."
)
async def groupby_operations_tool(
    file_path: str,
    group_by: List[str],
    operations: Dict[str, str],
    filter_condition: Optional[str] = None
) -> dict:
    """
    Perform sophisticated groupby operations with comprehensive aggregation options.
    
    Args:
        file_path: Absolute path to the data file
        group_by: List of columns to group by
        operations: Dictionary of column:operation pairs (sum, mean, count, min, max, std)
        filter_condition: Optional filter condition to apply before grouping
    
    Returns:
        Dictionary containing:
        - grouped_results: Results of groupby operations with aggregated data
        - group_statistics: Statistics about group sizes and distributions
        - aggregation_summary: Summary of all aggregation operations performed
        - performance_metrics: Groupby operation performance and optimization insights
    """
    logger.info(f"Performing groupby operations on: {file_path}")
    return mcp_handlers.groupby_operations_handler(file_path, group_by, operations, filter_condition)

@mcp.tool(
    name="merge_datasets",
    description="Merge and join datasets with sophisticated join operations and relationship analysis. Supports all SQL-style joins (inner, outer, left, right) with comprehensive data integration capabilities and merge conflict resolution."
)
async def merge_datasets_tool(
    left_file: str,
    right_file: str,
    join_type: str = "inner",
    left_on: Optional[str] = None,
    right_on: Optional[str] = None,
    on: Optional[str] = None
) -> dict:
    """
    Merge and join datasets with comprehensive integration capabilities.
    
    Args:
        left_file: Absolute path to the left dataset file
        right_file: Absolute path to the right dataset file
        join_type: Type of join operation (inner, outer, left, right)
        left_on: Column name in left dataset for joining
        right_on: Column name in right dataset for joining
        on: Common column name for joining (if same in both datasets)
    
    Returns:
        Dictionary containing:
        - merged_data: Results of the merge operation
        - merge_statistics: Statistics about the merge operation and data overlap
        - data_quality_report: Quality assessment of the merged dataset
        - relationship_analysis: Analysis of data relationships and join effectiveness
    """
    logger.info(f"Merging datasets: {left_file} and {right_file}")
    return mcp_handlers.merge_datasets_handler(left_file, right_file, join_type, left_on, right_on, on)

@mcp.tool(
    name="pivot_table",
    description="Create sophisticated pivot tables and cross-tabulations with advanced aggregation capabilities. Provides comprehensive data summarization with multiple aggregation functions and hierarchical data organization."
)
async def pivot_table_tool(
    file_path: str,
    index: List[str],
    columns: Optional[List[str]] = None,
    values: Optional[List[str]] = None,
    aggfunc: str = "mean"
) -> dict:
    """
    Create sophisticated pivot tables with comprehensive aggregation options.
    
    Args:
        file_path: Absolute path to the data file
        index: List of columns to use as row index
        columns: List of columns to use as column headers (None for simple aggregation)
        values: List of columns to aggregate (None uses all numerical columns)
        aggfunc: Aggregation function (mean, sum, count, min, max, std, var)
    
    Returns:
        Dictionary containing:
        - pivot_results: The pivot table with aggregated data
        - summary_statistics: Statistical summary of the pivot operation
        - data_insights: Key insights and patterns from the pivot analysis
        - visualization_data: Data formatted for pivot table visualization
    """
    logger.info(f"Creating pivot table for: {file_path}")
    return mcp_handlers.pivot_table_handler(file_path, index, columns, values, aggfunc)

# Time Series Tools
@mcp.tool(
    name="time_series_operations",
    description="Perform comprehensive time series operations with advanced temporal analysis capabilities. Supports resampling, rolling windows, lag features, trend analysis, and seasonality detection for temporal data insights."
)
async def time_series_operations_tool(
    file_path: str,
    date_column: str,
    operation: str,
    window_size: Optional[int] = None,
    frequency: Optional[str] = None
) -> dict:
    """
    Perform comprehensive time series operations with advanced temporal analysis.
    
    Args:
        file_path: Absolute path to the data file
        date_column: Column name containing datetime information
        operation: Time series operation (resample, rolling_mean, lag, trend, seasonality)
        window_size: Window size for rolling operations (required for rolling operations)
        frequency: Frequency for resampling (D, W, M, Q, Y) (required for resampling)
    
    Returns:
        Dictionary containing:
        - time_series_results: Results of the time series operation
        - temporal_analysis: Trend and seasonality analysis
        - statistical_summary: Time series statistical properties
        - forecasting_insights: Patterns and insights for forecasting applications
    """
    logger.info(f"Performing time series operations on: {file_path}")
    return mcp_handlers.time_series_operations_handler(file_path, date_column, operation, window_size, frequency)

# Data Validation Tools
@mcp.tool(
    name="validate_data",
    description="Comprehensive data validation with advanced constraint checking and quality assessment. Performs range validation, consistency checks, business rule validation, and data integrity verification with detailed validation reports and error identification."
)
async def validate_data_tool(
    file_path: str,
    validation_rules: Dict[str, Dict[str, Any]]
) -> dict:
    """
    Perform comprehensive data validation with advanced constraint checking and quality assessment.
    
    Args:
        file_path: Absolute path to the data file
        validation_rules: Dictionary of validation rules with structure:
                         {column_name: {rule_type: rule_value}}
                         Supported rules: min, max, type, regex, not_null, unique, in_list
    
    Returns:
        Dictionary containing:
        - validation_results: Detailed validation results for each column and rule
        - data_quality_score: Overall data quality score and assessment
        - violation_summary: Summary of validation violations and error patterns
        - recommendations: Suggested actions for data quality improvement
    """
    logger.info(f"Validating data in: {file_path}")
    return mcp_handlers.validate_data_handler(file_path, validation_rules)

# Hypothesis Testing Tools
@mcp.tool(
    name="hypothesis_testing",
    description="Perform comprehensive statistical hypothesis testing with multiple test types and advanced analysis. Supports t-tests, chi-square tests, ANOVA, normality tests, and statistical inference with confidence intervals, p-values, and effect size calculations."
)
async def hypothesis_testing_tool(
    file_path: str,
    test_type: str,
    column1: str,
    column2: Optional[str] = None,
    alpha: float = 0.05
) -> dict:
    """
    Perform comprehensive statistical hypothesis testing with multiple test types and advanced analysis.
    
    Args:
        file_path: Absolute path to the data file
        test_type: Type of hypothesis test (t_test, chi_square, anova, normality, mann_whitney)
        column1: Primary column for testing (numerical or categorical based on test type)
        column2: Secondary column for two-sample tests (None for single-sample tests)
        alpha: Significance level for hypothesis testing (typically 0.05, 0.01, or 0.10)
    
    Returns:
        Dictionary containing:
        - test_results: Statistical test results including test statistic and p-value
        - effect_size: Effect size measures and practical significance assessment
        - confidence_intervals: Confidence intervals for parameters and differences
        - interpretation: Statistical interpretation and practical conclusions
    """
    logger.info(f"Performing hypothesis testing on: {file_path}")
    return mcp_handlers.hypothesis_testing_handler(file_path, test_type, column1, column2, alpha)

# Memory Optimization Tools
@mcp.tool(
    name="optimize_memory",
    description="Advanced memory optimization for large datasets with intelligent type conversion and chunking strategies. Provides automatic dtype optimization, memory usage analysis, sparse data handling, and efficient memory allocation for optimal performance."
)
async def optimize_memory_tool(
    file_path: str,
    optimize_dtypes: bool = True,
    chunk_size: Optional[int] = None
) -> dict:
    """
    Perform advanced memory optimization for large datasets with intelligent strategies.
    
    Args:
        file_path: Absolute path to the data file
        optimize_dtypes: Whether to automatically optimize data types for memory efficiency
        chunk_size: Chunk size for processing large files (None for automatic sizing)
    
    Returns:
        Dictionary containing:
        - memory_optimization_results: Before/after memory usage comparison
        - dtype_optimization_log: Details of data type changes and memory savings
        - chunking_strategy: Optimal chunking recommendations for large datasets
        - performance_metrics: Speed and efficiency improvements achieved
    """
    logger.info(f"Optimizing memory usage for: {file_path}")
    return mcp_handlers.optimize_memory_handler(file_path, optimize_dtypes, chunk_size)

# Data Profiling Tools
@mcp.tool(
    name="profile_data",
    description="Comprehensive data profiling with detailed statistical analysis and quality assessment. Provides dataset overview including shape, data types, missing values, value distributions, statistical summaries, and data quality metrics for thorough data exploration."
)
async def profile_data_tool(
    file_path: str,
    include_correlations: bool = False,
    sample_size: Optional[int] = None
) -> dict:
    """
    Perform comprehensive data profiling with detailed statistical analysis and quality assessment.
    
    Args:
        file_path: Absolute path to the data file
        include_correlations: Whether to include correlation analysis between variables
        sample_size: Number of rows to sample for large datasets (None uses full dataset)
    
    Returns:
        Dictionary containing:
        - data_profile: Comprehensive dataset overview including shape, types, and statistics
        - column_analysis: Detailed analysis of each column including distributions
        - data_quality_metrics: Missing values, duplicates, and data quality indicators
        - correlation_matrix: Variable correlations (if include_correlations is True)
    """
    logger.info(f"Profiling data in: {file_path}")
    return mcp_handlers.profile_data_handler(file_path, include_correlations, sample_size)

# Data Filtering Tools
@mcp.tool(
    name="filter_data",
    description="Advanced data filtering with sophisticated boolean indexing and conditional expressions. Supports complex multi-condition filtering, logical operations, range-based filtering, and pattern matching with flexible query syntax for precise data selection."
)
async def filter_data_tool(
    file_path: str,
    filter_conditions: Dict[str, Any],
    output_file: Optional[str] = None
) -> dict:
    """
    Perform advanced data filtering with sophisticated boolean indexing and conditional expressions.
    
    Args:
        file_path: Absolute path to the data file
        filter_conditions: Dictionary of filtering conditions with structure:
                          {column_name: {operator: value}} or {column_name: value}
                          Supported operators: eq, ne, gt, lt, ge, le, in, not_in, contains, regex
        output_file: Optional absolute path to save filtered data (None returns in memory)
    
    Returns:
        Dictionary containing:
        - filtered_data: Results of filtering operation with matching records
        - filter_statistics: Summary of filtering results including row counts
        - data_quality_report: Quality assessment of filtered dataset
        - performance_metrics: Filtering operation performance and efficiency
    """
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
