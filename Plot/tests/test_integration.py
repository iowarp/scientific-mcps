"""
Integration tests for Plot MCP server.
Tests the complete workflow from data loading to plot generation.
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

from server import (
    create_line_plot_tool,
    create_bar_plot_tool,
    create_scatter_plot_tool,
    create_histogram_tool,
    create_heatmap_tool,
    get_data_info_tool
)


@pytest.fixture
def comprehensive_data():
    """Create comprehensive test data."""
    import numpy as np
    
    # Create more realistic data
    np.random.seed(42)
    data = {
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
        'temperature': 20 + 10 * np.sin(np.arange(100) * 2 * np.pi / 24) + np.random.normal(0, 2, 100),
        'humidity': 60 + 20 * np.sin(np.arange(100) * 2 * np.pi / 24 + np.pi/4) + np.random.normal(0, 5, 100),
        'pressure': 1013 + 5 * np.sin(np.arange(100) * 2 * np.pi / 48) + np.random.normal(0, 1, 100),
        'wind_speed': np.abs(np.random.normal(10, 5, 100)),
        'weather_station': np.random.choice(['Station_A', 'Station_B', 'Station_C'], 100)
    }
    return pd.DataFrame(data)


@pytest.fixture
def excel_file(comprehensive_data):
    """Create a temporary Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        comprehensive_data.to_excel(f.name, index=False)
        yield f.name
    
    # Cleanup
    os.unlink(f.name)


@pytest.fixture
def csv_file(comprehensive_data):
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        comprehensive_data.to_csv(f.name, index=False)
        yield f.name
    
    # Cleanup
    os.unlink(f.name)


@pytest.fixture
def output_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestDataFormats:
    """Test different data formats."""
    
    @pytest.mark.asyncio
    async def test_csv_format(self, csv_file):
        """Test CSV file format support."""
        print("\n=== Testing CSV Format ===")
        result = await get_data_info_tool(csv_file)
        print("CSV result:", result)
        
        assert result["status"] == "success"
        assert result["shape"] == (100, 6)
        assert "timestamp" in result["columns"]
        assert "temperature" in result["columns"]
    
    @pytest.mark.asyncio
    async def test_excel_format(self, excel_file):
        """Test Excel file format support."""
        print("\n=== Testing Excel Format ===")
        result = await get_data_info_tool(excel_file)
        print("Excel result:", result)
        
        assert result["status"] == "success"
        assert result["shape"] == (100, 6)
        assert "timestamp" in result["columns"]
        assert "temperature" in result["columns"]


class TestPlotWorkflow:
    """Test complete plotting workflow."""
    
    @pytest.mark.asyncio
    async def test_complete_analysis_workflow(self, csv_file, output_dir):
        """Test complete data analysis workflow."""
        print("\n=== Testing Complete Analysis Workflow ===")
        
        # Step 1: Get data info
        info_result = await get_data_info_tool(csv_file)
        assert info_result["status"] == "success"
        print("Data info retrieved successfully")
        
        # Step 2: Create line plot for time series
        line_plot_path = os.path.join(output_dir, "workflow_line_plot.png")
        line_result = await create_line_plot_tool(
            csv_file, "timestamp", "temperature", "Temperature Over Time", line_plot_path
        )
        assert line_result["status"] == "success"
        assert os.path.exists(line_plot_path)
        print("Line plot created successfully")
        
        # Step 3: Create bar plot for categorical data
        bar_plot_path = os.path.join(output_dir, "workflow_bar_plot.png")
        bar_result = await create_bar_plot_tool(
            csv_file, "weather_station", "temperature", "Average Temperature by Station", bar_plot_path
        )
        assert bar_result["status"] == "success"
        assert os.path.exists(bar_plot_path)
        print("Bar plot created successfully")
        
        # Step 4: Create scatter plot for correlation
        scatter_plot_path = os.path.join(output_dir, "workflow_scatter_plot.png")
        scatter_result = await create_scatter_plot_tool(
            csv_file, "temperature", "humidity", "Temperature vs Humidity", scatter_plot_path
        )
        assert scatter_result["status"] == "success"
        assert os.path.exists(scatter_plot_path)
        print("Scatter plot created successfully")
        
        # Step 5: Create histogram for distribution
        histogram_path = os.path.join(output_dir, "workflow_histogram.png")
        histogram_result = await create_histogram_tool(
            csv_file, "wind_speed", 25, "Wind Speed Distribution", histogram_path
        )
        assert histogram_result["status"] == "success"
        assert os.path.exists(histogram_path)
        print("Histogram created successfully")
        
        # Step 6: Create heatmap for correlation matrix
        heatmap_path = os.path.join(output_dir, "workflow_heatmap.png")
        heatmap_result = await create_heatmap_tool(
            csv_file, "Weather Data Correlation Matrix", heatmap_path
        )
        assert heatmap_result["status"] == "success"
        assert os.path.exists(heatmap_path)
        print("Heatmap created successfully")
        
        print("Complete workflow test passed!")


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_file_not_found_errors(self, output_dir):
        """Test error handling for missing files."""
        print("\n=== Testing File Not Found Errors ===")
        
        # Test all plot types with non-existent file
        nonexistent_file = "this_file_does_not_exist.csv"
        output_path = os.path.join(output_dir, "error_test.png")
        
        # Line plot
        result = await create_line_plot_tool(nonexistent_file, "x", "y", "Test", output_path)
        assert result["status"] == "error"
        print("Line plot error handling: PASS")
        
        # Bar plot
        result = await create_bar_plot_tool(nonexistent_file, "x", "y", "Test", output_path)
        assert result["status"] == "error"
        print("Bar plot error handling: PASS")
        
        # Scatter plot
        result = await create_scatter_plot_tool(nonexistent_file, "x", "y", "Test", output_path)
        assert result["status"] == "error"
        print("Scatter plot error handling: PASS")
        
        # Histogram
        result = await create_histogram_tool(nonexistent_file, "x", 10, "Test", output_path)
        assert result["status"] == "error"
        print("Histogram error handling: PASS")
        
        # Heatmap
        result = await create_heatmap_tool(nonexistent_file, "Test", output_path)
        assert result["status"] == "error"
        print("Heatmap error handling: PASS")
    
    @pytest.mark.asyncio
    async def test_invalid_column_errors(self, csv_file, output_dir):
        """Test error handling for invalid column names."""
        print("\n=== Testing Invalid Column Errors ===")
        
        output_path = os.path.join(output_dir, "error_test.png")
        
        # Test invalid x column
        result = await create_line_plot_tool(csv_file, "invalid_x", "temperature", "Test", output_path)
        assert result["status"] == "error"
        print("Invalid x column error handling: PASS")
        
        # Test invalid y column
        result = await create_line_plot_tool(csv_file, "timestamp", "invalid_y", "Test", output_path)
        assert result["status"] == "error"
        print("Invalid y column error handling: PASS")
        
        # Test invalid histogram column
        result = await create_histogram_tool(csv_file, "invalid_column", 10, "Test", output_path)
        assert result["status"] == "error"
        print("Invalid histogram column error handling: PASS")


class TestPerformance:
    """Test performance with larger datasets."""
    
    @pytest.mark.asyncio
    async def test_large_dataset_performance(self, output_dir):
        """Test performance with larger dataset."""
        print("\n=== Testing Large Dataset Performance ===")
        
        # Create larger dataset
        import numpy as np
        np.random.seed(42)
        large_data = {
            'x': np.arange(10000),
            'y': np.random.normal(0, 1, 10000),
            'category': np.random.choice(['A', 'B', 'C', 'D'], 10000)
        }
        large_df = pd.DataFrame(large_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            large_df.to_csv(f.name, index=False)
            large_csv_file = f.name
        
        try:
            # Test line plot with large dataset
            line_plot_path = os.path.join(output_dir, "large_line_plot.png")
            result = await create_line_plot_tool(
                large_csv_file, "x", "y", "Large Dataset Line Plot", line_plot_path
            )
            assert result["status"] == "success"
            assert result["data_points"] == 10000
            assert os.path.exists(line_plot_path)
            print("Large dataset line plot: PASS")
            
            # Test histogram with large dataset
            histogram_path = os.path.join(output_dir, "large_histogram.png")
            result = await create_histogram_tool(
                large_csv_file, "y", 50, "Large Dataset Histogram", histogram_path
            )
            assert result["status"] == "success"
            assert result["data_points"] == 10000
            assert os.path.exists(histogram_path)
            print("Large dataset histogram: PASS")
            
        finally:
            os.unlink(large_csv_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
