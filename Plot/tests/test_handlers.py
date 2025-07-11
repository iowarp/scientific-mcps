"""
Unit tests for Plot MCP handlers.
Tests the MCP handler functions.
"""
import pytest
import sys
import os
import tempfile
import pandas as pd
from pathlib import Path

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'plot'))

from mcp_handlers import (
    data_info_handler,
    line_plot_handler,
    bar_plot_handler,
    scatter_plot_handler,
    histogram_plot_handler,
    heatmap_plot_handler
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
        'timestamp': pd.date_range('2024-01-01', periods=20, freq='D'),
        'temperature': [20 + i * 0.5 for i in range(20)],
        'humidity': [50 + i * 1.5 for i in range(20)],
        'pressure': [1013 + i * 0.2 for i in range(20)],
        'city': ['New York', 'Chicago', 'Los Angeles', 'Houston', 'Phoenix'] * 4
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
    print("\n=== Testing Data Info Handler Success ===")
    result = data_info_handler(sample_csv_file)
    print("Handler result:", result)
    
    assert result["status"] == "success"
    assert result["shape"] == (20, 5)
    assert "timestamp" in result["columns"]
    assert "temperature" in result["columns"]
    assert "humidity" in result["columns"]
    assert "pressure" in result["columns"]
    assert "city" in result["columns"]


def test_data_info_handler_error():
    """Test data_info_handler with invalid file."""
    print("\n=== Testing Data Info Handler Error ===")
    result = data_info_handler("nonexistent_file.csv")
    print("Error result:", result)
    
    assert result["status"] == "error"
    assert "error" in result


def test_line_plot_handler_success(sample_csv_file, output_dir):
    """Test line_plot_handler with valid parameters."""
    print("\n=== Testing Line Plot Handler Success ===")
    output_path = os.path.join(output_dir, "handler_line_plot.png")
    
    result = line_plot_handler(
        sample_csv_file, "timestamp", "temperature", "Temperature Over Time", output_path
    )
    print("Handler result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "timestamp"
    assert result["y_column"] == "temperature"
    assert result["title"] == "Temperature Over Time"
    assert result["data_points"] == 20
    assert os.path.exists(output_path)


def test_line_plot_handler_invalid_column(sample_csv_file, output_dir):
    """Test line_plot_handler with invalid column."""
    print("\n=== Testing Line Plot Handler Invalid Column ===")
    output_path = os.path.join(output_dir, "handler_line_plot_error.png")
    
    result = line_plot_handler(
        sample_csv_file, "invalid_column", "temperature", "Test Plot", output_path
    )
    print("Error result:", result)
    
    assert result["status"] == "error"
    assert "error" in result


def test_bar_plot_handler_success(sample_csv_file, output_dir):
    """Test bar_plot_handler with valid parameters."""
    print("\n=== Testing Bar Plot Handler Success ===")
    output_path = os.path.join(output_dir, "handler_bar_plot.png")
    
    result = bar_plot_handler(
        sample_csv_file, "city", "temperature", "Temperature by City", output_path
    )
    print("Handler result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "city"
    assert result["y_column"] == "temperature"
    assert result["title"] == "Temperature by City"
    assert result["data_points"] == 20
    assert os.path.exists(output_path)


def test_scatter_plot_handler_success(sample_csv_file, output_dir):
    """Test scatter_plot_handler with valid parameters."""
    print("\n=== Testing Scatter Plot Handler Success ===")
    output_path = os.path.join(output_dir, "handler_scatter_plot.png")
    
    result = scatter_plot_handler(
        sample_csv_file, "temperature", "humidity", "Temperature vs Humidity", output_path
    )
    print("Handler result:", result)
    
    assert result["status"] == "success"
    assert result["x_column"] == "temperature"
    assert result["y_column"] == "humidity"
    assert result["title"] == "Temperature vs Humidity"
    assert result["data_points"] == 20
    assert os.path.exists(output_path)


def test_histogram_plot_handler_success(sample_csv_file, output_dir):
    """Test histogram_plot_handler with valid parameters."""
    print("\n=== Testing Histogram Plot Handler Success ===")
    output_path = os.path.join(output_dir, "handler_histogram.png")
    
    result = histogram_plot_handler(
        sample_csv_file, "temperature", 15, "Temperature Distribution", output_path
    )
    print("Handler result:", result)
    
    assert result["status"] == "success"
    assert result["column"] == "temperature"
    assert result["bins"] == 15
    assert result["title"] == "Temperature Distribution"
    assert result["data_points"] == 20
    assert os.path.exists(output_path)


def test_heatmap_plot_handler_success(sample_csv_file, output_dir):
    """Test heatmap_plot_handler with valid parameters."""
    print("\n=== Testing Heatmap Plot Handler Success ===")
    output_path = os.path.join(output_dir, "handler_heatmap.png")
    
    result = heatmap_plot_handler(
        sample_csv_file, "Weather Data Correlation", output_path
    )
    print("Handler result:", result)
    
    assert result["status"] == "success"
    assert result["title"] == "Weather Data Correlation"
    assert result["data_points"] == 20
    assert "numeric_columns" in result
    assert os.path.exists(output_path)


def test_heatmap_plot_handler_file_not_found(output_dir):
    """Test heatmap_plot_handler with file not found."""
    print("\n=== Testing Heatmap Plot Handler File Not Found ===")
    output_path = os.path.join(output_dir, "handler_heatmap_error.png")
    
    result = heatmap_plot_handler(
        "nonexistent_file.csv", "Test Heatmap", output_path
    )
    print("Error result:", result)
    
    assert result["status"] == "error"
    assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
