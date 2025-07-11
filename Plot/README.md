# Plot MCP Server

A comprehensive Model Context Protocol (MCP) server for advanced data visualization and plotting operations. This server enables LLMs to create professional-quality plots from various data sources with support for multiple plot types, data formats, and intelligent data handling.

## Key Features

- **Multiple Plot Types**  
  Creates line plots, bar charts, scatter plots, histograms, and correlation heatmaps with professional styling and customization options.

- **Smart Data Handling**  
  Automatically cleans data, handles missing values, and performs intelligent aggregation for optimal visualization results.

- **Format Support**  
  Works with CSV and Excel files (.csv, .xlsx, .xls) with automatic format detection and data type inference.

- **Advanced Analytics**  
  Provides comprehensive data inspection, column analysis, and statistical insights for data exploration.

- **High-Quality Output**  
  Generates professional 300 DPI plots with customizable styling, titles, and output formats.

- **Standardized MCP Interface**  
  Exposes all functionality via the MCP JSON-RPC protocol for seamless integration with language models.


## Capabilities

1. **data_info**: Get comprehensive information about data files including columns, data types, shape, and preview.

2. **line_plot**: Create line plots for time series or continuous data visualization with customizable parameters.

3. **bar_plot**: Create bar charts with automatic data aggregation and smart categorical grouping.

4. **scatter_plot**: Create scatter plots for correlation analysis and pattern identification.

5. **histogram_plot**: Create histograms for distribution analysis with configurable bins and styling.

6. **heatmap_plot**: Create correlation heatmaps for numeric data with automatic column selection.

---

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)

## Setup

### 1. Navigate to Plot Directory
```bash
cd /path/to/scientific-mcps/Plot
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
   uv run plot-mcp
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.

--- 

## Running the Server with Different Types of Clients:

### Running the Server with the WARP Client
To interact with the Plot MCP server, use the main `wrp.py` client. You will need to configure it to point to the Plot server.

1.  **Configure:** Ensure that `Plot` is listed in the `MCP` section of your chosen configuration file (e.g., in `bin/confs/Gemini.yaml` or `bin/confs/Ollama.yaml`).
    ```yaml
    # In bin/confs/Gemini.yaml
    MCP:
      - Plot
      # - Adios
      # - HDF5
    ```

2.  **Run:** Start the client from the repository root with your desired configuration:
    ```bash
    # Example using the Gemini configuration 
    python3 bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```
    
    For detailed setup with local LLMs and other providers, see the [Complete Installation Guide](../bin/docs/Installation.md).

### Running the Server on Claude Command Line Interface Tool.

1. Install the Claude Code using NPM,
Install [NodeJS 18+](https://nodejs.org/en/download), then run:

```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp plot -- uv --directory ~/scientific-mcps/Plot run plot-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```json
"plot-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/scientific-mcps/Plot/",
        "run",
        "plot-mcp"
    ]
}
```

---


## Examples

**Note: Use absolute paths for all file operations to ensure proper file access.**

1. **Create a line plot from time series data**

   ```python
   # Plot temperature trends over time
   result = line_plot("/data/temperature.csv", "date", "temperature", "Temperature Trends")
   ```

2. **Generate comprehensive data analysis**

   ```python
   # Get detailed information about your dataset
   info = data_info("/data/sales.csv")
   ```

3. **Create multiple visualizations for data exploration**

   ```python
   # Create scatter plot for correlation analysis
   scatter = scatter_plot("/data/sales.csv", "price", "quantity", "Price vs Quantity")
   
   # Generate histogram for distribution analysis
   hist = histogram_plot("/data/sales.csv", "revenue", bins=50, "Revenue Distribution")
   
   # Create correlation heatmap
   heatmap = heatmap_plot("/data/sales.csv", "Sales Correlation Matrix")
   ```

4. **Bar chart with automatic data aggregation**

   ```python
   # Create bar chart with smart categorical grouping
   bar = bar_plot("/data/categories.csv", "category", "sales", "Sales by Category")
   ```

**For detailed examples and use cases, see the [capability_test.py](capability_test.py) file.**

## Project Structure
```text
Plot/
├── pyproject.toml                 # Project metadata & dependencies
├── README.md                      # Project documentation
├── capability_test.py             # Comprehensive functionality tests
├── data/                          # Sample data directory
│   ├── temperature.csv           # Global temperature data (48,470 records)
│   └── sample_data.csv           # Simple test data (10 records)
├── output/                        # Generated plots directory
├── src/                           # Source code directory
│   └── plot/                      # Main package directory
│       ├── __init__.py            # Package init
│       ├── server.py              # Main MCP server with FastMCP
│       ├── mcp_handlers.py        # MCP protocol handlers
│       └── capabilities/          # Individual capability modules
│           ├── __init__.py
│           └── plot_capabilities.py # Core plotting functions
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_capabilities.py       # Unit tests for capabilities
│   ├── test_mcp_handlers.py       # Integration tests for MCP handlers
│   └── test_server.py             # Server tests
└── uv.lock                        # Dependency lock file
```

## Data Types Support

The server supports various data types for visualization:
- **Numeric types**: int, float, double for statistical plots
- **Categorical types**: string, object for grouping and categorization
- **Temporal types**: datetime, date for time series visualization
- **Boolean types**: bool for binary analysis
- **Mixed types**: Automatic handling of heterogeneous datasets

## Plot Types and Features

Supported plot types with advanced features:
- **Line plots** - Time series analysis with trend lines
- **Bar charts** - Categorical comparisons with automatic aggregation
- **Scatter plots** - Correlation analysis with regression lines
- **Histograms** - Distribution analysis with customizable binning
- **Heatmaps** - Correlation matrices with color coding
- **Box plots** - Statistical distribution analysis (future enhancement)

## Testing

### Run Capability Tests
```bash
uv run python capability_test.py
```

### Run Unit Tests
```bash
uv run pytest tests/ -v
```

All tests pass with zero warnings, ensuring reliable functionality across all plotting capabilities.

## Error Handling

The server provides comprehensive error handling with:
- Detailed error messages for debugging
- Error type classification for different failure modes
- Validation for file paths and data formats
- Graceful handling of large datasets
- Column validation and data type checking errors

## Performance Features

- **Memory optimization** for large datasets
- **Intelligent data sampling** for performance
- **Lazy loading** of data files
- **Automatic data cleaning** and preprocessing
- **Smart aggregation** for categorical data
- **Efficient plot rendering** with matplotlib optimization

## Dependencies

Key dependencies managed through `pyproject.toml`:
- `fastmcp>=0.1.0` - FastMCP framework for MCP server implementation
- `pandas>=1.5.0` - Data manipulation and analysis library
- `matplotlib>=3.6.0` - Primary plotting library for visualization
- `seaborn>=0.12.0` - Statistical visualization enhancements
- `openpyxl>=3.0.0` - Excel file support (.xlsx)
- `pytest>=7.2.0` - Testing framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Submit a pull request

## License

This project is part of the Scientific MCPs collection and follows the same licensing terms.

