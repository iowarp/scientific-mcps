"""
Unit tests for Plot MCP server.
Tests the FastMCP server integration.
"""
import pytest
import sys
import os
import tempfile
import pandas as pd
import asyncio
from pathlib import Path

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plot'))

from mcp_handlers import (
    line_plot_handler,
    bar_plot_handler,
    scatter_plot_handler,
    histogram_plot_handler,
    heatmap_plot_handler,
    data_info_handler
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
        'date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'sales': [100 + i * 5 for i in range(30)],
        'profit': [20 + i * 2 for i in range(30)],
        'region': ['North', 'South', 'East', 'West'] * 7 + ['North', 'South']
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_csv_file(sample_data):
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        sample_data.to_csv(f.name, index=False)
        yield f.name
    
    # Cleanup
    os.unlink(f.name)


@pytest.fixture
def output_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir



def test_data_info_handler_success(sample_csv_file):
    """Test data_info_handler with valid file."""
    print("\n=== Testing Data Info Tool Success ===")
    result = data_info_handler(sample_csv_file)
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["shape"] == (30, 4)
    assert "date" in result["columns"]
    assert "sales" in result["columns"]
    assert "profit" in result["columns"]
    assert "region" in result["columns"]



def test_data_info_handler_error():
    """Test data_info_handler with invalid file."""
    print("\n=== Testing Data Info Tool Error ===")
    result = data_info_handler("nonexistent_file.csv")
    print("Error result:", result)
    
    assert result["status"] == "error"
    assert "error" in result



def test_line_plot_handler_success(sample_csv_file, output_dir):
    """Test line_plot_handler with valid parameters."""
    print("\n=== Testing Create Line Plot Tool Success ===")
    output_path = os.path.join(output_dir, "tool_line_plot.png")
    
    result = line_plot_handler(
        sample_csv_file, "date", "sales", "Sales Over Time", output_path
    )
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "date"
    assert result["y_column"] == "sales"
    assert result["title"] == "Sales Over Time"
    assert result["data_points"] == 30
    assert os.path.exists(output_path)



def test_line_plot_handler_default_params(sample_csv_file):
    """Test line_plot_handler with default parameters."""
    print("\n=== Testing Create Line Plot Tool Default Params ===")
    
    result = line_plot_handler(sample_csv_file, "date", "sales")
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "date"
    assert result["y_column"] == "sales"
    assert result["title"] == "Line Plot"
    assert result["output_path"] == "line_plot.png"
    assert result["data_points"] == 30
    
    # Cleanup
    if os.path.exists("line_plot.png"):
        os.unlink("line_plot.png")



def test_bar_plot_handler_success(sample_csv_file, output_dir):
    """Test bar_plot_handler with valid parameters."""
    print("\n=== Testing Create Bar Plot Tool Success ===")
    output_path = os.path.join(output_dir, "tool_bar_plot.png")
    
    result = bar_plot_handler(
        sample_csv_file, "region", "sales", "Sales by Region", output_path
    )
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "region"
    assert result["y_column"] == "sales"
    assert result["title"] == "Sales by Region"
    assert result["data_points"] == 30
    assert os.path.exists(output_path)



def test_scatter_plot_handler_success(sample_csv_file, output_dir):
    """Test scatter_plot_handler with valid parameters."""
    print("\n=== Testing Create Scatter Plot Tool Success ===")
    output_path = os.path.join(output_dir, "tool_scatter_plot.png")
    
    result = scatter_plot_handler(
        sample_csv_file, "sales", "profit", "Sales vs Profit", output_path
    )
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "sales"
    assert result["y_column"] == "profit"
    assert result["title"] == "Sales vs Profit"
    assert result["data_points"] == 30
    assert os.path.exists(output_path)



def test_histogram_plot_handler_success(sample_csv_file, output_dir):
    """Test histogram_plot_handler with valid parameters."""
    print("\n=== Testing Create Histogram Tool Success ===")
    output_path = os.path.join(output_dir, "tool_histogram.png")
    
    result = histogram_plot_handler(
        sample_csv_file, "sales", 20, "Sales Distribution", output_path
    )
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["column"] == "sales"
    assert result["bins"] == 20
    assert result["title"] == "Sales Distribution"
    assert result["data_points"] == 30
    assert os.path.exists(output_path)



def test_histogram_plot_handler_default_bins(sample_csv_file, output_dir):
    """Test histogram_plot_handler with default bins parameter."""
    print("\n=== Testing Create Histogram Tool Default Bins ===")
    output_path = os.path.join(output_dir, "tool_histogram_default.png")
    
    result = histogram_plot_handler(
        sample_csv_file, "sales", title="Sales Distribution", output_path=output_path
    )
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["column"] == "sales"
    assert result["bins"] == 30  # Default value
    assert result["title"] == "Sales Distribution"
    assert result["data_points"] == 30
    assert os.path.exists(output_path)



def test_heatmap_plot_handler_success(sample_csv_file, output_dir):
    """Test heatmap_plot_handler with valid parameters."""
    print("\n=== Testing Create Heatmap Tool Success ===")
    output_path = os.path.join(output_dir, "tool_heatmap.png")
    
    result = heatmap_plot_handler(
        sample_csv_file, "Sales Data Correlation", output_path
    )
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["title"] == "Sales Data Correlation"
    assert result["data_points"] == 30
    assert "numeric_columns" in result
    assert os.path.exists(output_path)



def test_heatmap_plot_handler_default_params(sample_csv_file):
    """Test heatmap_plot_handler with default parameters."""
    print("\n=== Testing Create Heatmap Tool Default Params ===")
    
    result = heatmap_plot_handler(sample_csv_file)
    print("Tool result:", result)
    
    assert result["status"] == "success"
    assert result["title"] == "Heatmap"
    assert result["output_path"] == "heatmap.png"
    assert result["data_points"] == 30
    
    # Cleanup
    if os.path.exists("heatmap.png"):
        os.unlink("heatmap.png")



def test_handler_error_handling():
    """Test error handling in tools."""
    print("\n=== Testing Tool Error Handling ===")
    
    # Test with non-existent file
    result = line_plot_handler("nonexistent_file.csv", "x", "y")
    assert result["status"] == "error"
    assert "error" in result
    
    # Test with invalid column
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
        df = pd.DataFrame(data)
        df.to_csv(f.name, index=False)
        csv_file = f.name
    
    try:
        result = line_plot_handler(csv_file, "invalid_column", "b")
        assert result["status"] == "error"
        assert "error" in result
    finally:
        os.unlink(csv_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
