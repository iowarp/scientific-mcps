# Pandas MCP Server

A comprehensive Model Context Protocol (MCP) server for advanced data analysis and manipulation using Pandas. This server provides LLMs with powerful data science capabilities including statistical analysis, data cleaning, transformation, time series operations, and comprehensive data quality assessment.



## Key Features

- **Universal Data I/O**  
  Load and save data in multiple formats (CSV, Excel, JSON, Parquet, HDF5) with intelligent format detection and encoding handling.

- **Statistical Analysis**  
  Comprehensive statistical summaries, correlation analysis, hypothesis testing, and distribution analysis for data exploration.

- **Data Cleaning & Quality**  
  Advanced missing data handling, outlier detection, duplicate removal, and data validation with customizable rules.

- **Data Transformation**  
  Groupby operations, dataset merging, pivot tables, and complex data reshaping for analysis workflows.

- **Time Series Operations**  
  Specialized time series analysis including resampling, rolling windows, lag features, and seasonality detection.

- **Memory Optimization**  
  Intelligent dtype optimization, chunked processing, and memory usage analysis for large datasets.

- **Data Profiling**  
  Automated data profiling with comprehensive reports on data quality, distributions, and relationships.

- **Advanced Filtering**  
  Flexible data filtering with boolean indexing, sampling, and query-based selection.

- **Standardized MCP Interface**  
  All functionality exposed via the MCP JSON-RPC protocol for seamless integration with language models.



## Capabilities

1. **load_data**: Load data from various formats (CSV, Excel, JSON, Parquet, HDF5) with custom parameters and encoding detection.

2. **save_data**: Export DataFrames to multiple formats with configurable compression and formatting options.

3. **statistical_summary**: Calculate comprehensive statistical summaries including mean, median, std, percentiles, and distribution metrics.

4. **correlation_analysis**: Perform correlation analysis with Pearson, Spearman, and Kendall methods for relationship discovery.

5. **handle_missing_data**: Advanced missing data detection and imputation strategies including forward fill, backward fill, and statistical imputation.

6. **clean_data**: Intelligent data cleaning with outlier detection, duplicate removal, and data type optimization.

7. **profile_data**: Quick data profiling with shape information, data types, missing values, and basic statistics.

8. **groupby_operations**: Advanced GroupBy operations with multiple aggregation functions and complex grouping logic.

9. **merge_datasets**: Merge and join datasets with various join types (inner, outer, left, right) and key handling.

10. **create_pivot_table**: Create pivot tables and cross-tabulations with flexible aggregation and indexing.

11. **filter_data**: Advanced data filtering with boolean indexing, conditional filtering, and complex query expressions.

12. **sample_data**: Data sampling with multiple methods (random, systematic, stratified) for analysis and testing.

13. **rolling_analysis**: Rolling window calculations for time series analysis with customizable window sizes and functions.

14. **resample_timeseries**: Time series resampling with various frequencies and aggregation methods.

15. **optimize_memory**: Memory usage optimization through efficient data types, chunking, and sparse data handling.

16. **validate_data**: Comprehensive data validation with range checks, consistency validation, and quality reporting.

17. **hypothesis_testing**: Statistical hypothesis testing including t-tests, chi-square tests, and ANOVA for inference.

---

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Setup

### 1. Navigate to Pandas Directory
```bash
cd /path/to/scientific-mcps/Pandas
```

### 2. Install Dependencies
Using UV (recommended):
```bash
uv sync
```

Using pip:
```bash
pip install -e .
```

**Run the MCP Server directly:**

```bash
uv run pandas-mcp
```

This will create a `.venv/` folder, install all required packages, and run the server directly.

---

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Pandas MCP server, use the main `wrp.py` client. You will need to configure it to point to the Pandas server.

1. **Configure:** Ensure that `Pandas` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
   ```yaml
   # In bin/confs/Gemini.yaml
   MCP:
     - Pandas
     # - Adios
     # - HDF5
   ```

2. **Run:** Start the client from the repository root with your desired configuration:
   ```bash
   # Example using the Gemini configuration 
   python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
   ```
   
   For detailed setup with local LLMs and other providers, see the [Complete Installation Guide](../bin/docs/Installation.md).

### Running the Server on Claude Command Line Interface Tool

1. Install the Claude Code using NPM,
Install [NodeJS 18+](https://nodejs.org/en/download), then run:

```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp pandas -- uv --directory ~/scientific-mcps/Pandas run pandas-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"pandas-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/scientific-mcps/Pandas/",
        "run",
        "pandas-mcp"
    ]
}
```

---

## Examples

**Note: Use absolute paths for all file operations to ensure proper file access.**

1. **Load and analyze CSV data with statistical summary**

   ```python
   # Load employee data and get comprehensive statistics
   result = load_data("/data/employees.csv", encoding="utf-8")
   stats = statistical_summary("/data/employees.csv", columns=["salary", "age", "years_experience"])
   ```

2. **Data cleaning and quality assessment**

   ```python
   # Handle missing data and detect outliers
   cleaned = handle_missing_data("/data/dataset.csv", strategy="mean", columns=["price", "quantity"])
   quality = clean_data("/data/dataset.csv", remove_duplicates=True, detect_outliers=True)
   ```

3. **Advanced data transformations and grouping**

   ```python
   # Group sales data by region and calculate aggregations
   grouped = groupby_operations("/data/sales.csv", 
                               group_columns=["region", "category"], 
                               agg_functions={"revenue": "sum", "quantity": "mean"})
   
   # Create pivot table for cross-tabulation
   pivot = create_pivot_table("/data/sales.csv", 
                             index="date", columns="category", values="revenue")
   ```

4. **Time series analysis and resampling**

   ```python
   # Resample time series data to monthly frequency
   resampled = resample_timeseries("/data/timeseries.csv", 
                                  date_column="timestamp", 
                                  frequency="1M", agg_method="mean")
   
   # Calculate rolling averages
   rolling = rolling_analysis("/data/timeseries.csv", 
                             columns=["price"], window_size=7, functions=["mean", "std"])
   ```

5. **Memory optimization for large datasets**

   ```python
   # Optimize memory usage and get recommendations
   optimized = optimize_memory("/data/large_dataset.csv", 
                              optimize_dtypes=True, chunk_size=10000)
   ```

**For detailed examples and use cases, see the [test_all_capabilities.py](test_all_capabilities.py) file.**

## Project Structure
```text
Pandas/
├── pyproject.toml              # Project metadata & dependencies
├── README.md                   # Project documentation
├── pytest.ini                 # Test configuration
├── test_all_capabilities.py    # Comprehensive functionality tests
├── create_sample_data.py       # Sample data generation script
├── data/                       # Sample data directory
│   ├── employees.csv           # Employee dataset
│   ├── sales.parquet           # Sales data in Parquet format
│   ├── weather.xlsx            # Weather data in Excel format
│   ├── inventory.h5            # Inventory data in HDF5 format
│   └── ...                     # Additional sample datasets
├── src/                        # Source code directory
│   └── pandasmcp/
│       ├── __init__.py         # Package init
│       ├── server.py           # Main MCP server with FastMCP
│       ├── mcp_handlers.py     # MCP protocol handlers
│       └── capabilities/
│           ├── __init__.py
│           ├── data_io.py              # Universal data I/O operations
│           ├── statistics.py           # Statistical analysis
│           ├── data_cleaning.py        # Data cleaning and preprocessing
│           ├── data_profiling.py       # Data profiling and exploration
│           ├── transformations.py      # Data transformation operations
│           ├── time_series.py          # Time series analysis
│           ├── filtering.py            # Data filtering and sampling
│           ├── memory_optimization.py  # Memory optimization
│           └── validation.py           # Data validation and testing
├── tests/                      # Test suite
│   ├── test_capabilities.py    # Unit tests for capabilities
│   ├── test_mcp_handlers.py    # Integration tests for MCP handlers
│   └── conftest.py             # Test fixtures
└── uv.lock                     # Dependency lock file
```

## Data Formats Support

The server supports comprehensive data format handling:
- **CSV**: With encoding detection, delimiter inference, and custom parsing options
- **Excel**: Multiple sheets, custom ranges, and format preservation (.xlsx, .xls)
- **JSON**: Nested structures, custom orientations, and large file handling
- **Parquet**: Columnar storage with compression and metadata preservation
- **HDF5**: Hierarchical data format with dataset and group management
- **SQL**: Database connectivity and query execution
- **Pickle**: Python object serialization for complex data structures

## Statistical Capabilities

Comprehensive statistical analysis features:
- **Descriptive Statistics**: Mean, median, mode, standard deviation, variance, skewness, kurtosis
- **Correlation Analysis**: Pearson, Spearman, Kendall correlation coefficients
- **Hypothesis Testing**: t-tests, chi-square tests, ANOVA, normality tests
- **Distribution Analysis**: Histogram generation, distribution fitting, outlier detection
- **Time Series Statistics**: Trend analysis, seasonality detection, autocorrelation

## Data Quality Features

Advanced data quality assessment and improvement:
- **Missing Data**: Detection patterns, imputation strategies, missing data visualization
- **Outlier Detection**: IQR method, Z-score analysis, Isolation Forest, Local Outlier Factor
- **Duplicate Detection**: Exact duplicates, fuzzy matching, similarity-based detection
- **Data Validation**: Type checking, range validation, consistency checks, business rule validation
- **Data Profiling**: Automated quality reports, data lineage tracking, anomaly detection

## Testing

### Run Comprehensive Capability Tests
```bash
uv run python test_all_capabilities.py
```

### Run Unit Tests
```bash
uv run pytest tests/ -v
```

### Test Coverage
```bash
uv run pytest tests/ --cov=pandasmcp --cov-report=html
```

## Error Handling

The server provides comprehensive error handling with:
- **File Operation Errors**: Detailed messages for file not found, permission issues, format errors
- **Data Type Errors**: Type conversion failures, schema mismatches, encoding issues
- **Memory Errors**: Graceful handling of memory limitations with chunking fallbacks
- **Statistical Errors**: Edge cases in statistical computations, insufficient data warnings
- **Validation Errors**: Data validation failures with specific constraint violations

## Performance Features

- **Memory optimization** through efficient data types and sparse arrays
- **Chunked processing** for large datasets exceeding memory limits
- **Lazy evaluation** for efficient computation chains
- **Parallel processing** for CPU-intensive operations
- **Caching mechanisms** for repeated operations
- **Progress tracking** for long-running operations

## Configuration

The server can be configured through environment variables:

- `PANDAS_MAX_ROWS`: Maximum number of rows to process (default: 100000)
- `PANDAS_CHUNK_SIZE`: Default chunk size for large datasets (default: 10000)
- `PANDAS_MEMORY_LIMIT`: Memory limit in MB (default: 1000)
- `PANDAS_CACHE_SIZE`: Cache size for repeated operations (default: 100)
- `PANDAS_TEMP_DIR`: Temporary directory for intermediate files

## Dependencies

Key dependencies managed through `pyproject.toml`:
- `mcp>=0.1.0` - Model Context Protocol framework
- `pandas>=2.2.0` - Core data manipulation library
- `numpy>=1.24.0` - Numerical computing foundation
- `scipy>=1.11.0` - Scientific computing and statistics
- `scikit-learn>=1.3.0` - Machine learning algorithms for outlier detection
- `openpyxl>=3.1.0` - Excel file handling
- `pyarrow>=15.0.0` - Parquet and Arrow format support
- `tables>=3.9.0` - HDF5 file format support
- `psutil>=5.9.0` - System and process utilities for memory monitoring
- `pytest>=7.2.0` - Testing framework
- `pytest-asyncio>=1.0.0` - Async testing support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Run capability tests: `uv run python test_all_capabilities.py`
6. Submit a pull request

## License

This project is part of the Scientific MCPs collection and follows the same licensing terms.
