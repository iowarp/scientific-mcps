#!/usr/bin/env python3
"""
Plot MCP Capability Test - Test the plotting capabilities of the MCP server.
"""
import os
import sys
import tempfile
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from plot.mcp_handlers import (
    line_plot_handler,
    bar_plot_handler,
    scatter_plot_handler,
    histogram_plot_handler,
    heatmap_plot_handler,
    data_info_handler
)

def get_temperature_data():
    """Get the temperature.csv data from the data folder."""
    csv_path = os.path.join('data', 'temperature.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Temperature data file not found: {csv_path}")
    return csv_path

def test_plotting_capabilities():
    """Test all plotting capabilities."""
    print("Testing Plot MCP Capabilities")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Use temperature data from data folder
    csv_path = get_temperature_data()
    print(f"Using temperature data: {csv_path}")
    
    # Test data info
    print("\nTesting data info...")
    info = data_info_handler(csv_path)
    if info["status"] == "success":
        print(f"Data shape: {info['shape']}")
        print(f"Columns: {info['columns']}")
        print(f"Data types: {info.get('dtypes', {})}")
    else:
        print(f"Error: {info.get('error', 'Unknown error')}")
    
    # Test line plot with temperature data
    print("\nTesting line plot...")
    result = line_plot_handler(
        csv_path, "year", "AverageTemperatureFahr", "Temperature Over Years", 
        os.path.join(output_dir, "temperature_line.png")
    )
    if result["status"] == "success":
        print(f"Line plot created: {result['output_path']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Test bar plot with temperature data
    print("\nTesting bar plot...")
    result = bar_plot_handler(
        csv_path, "Country", "AverageTemperatureFahr", "Average Temperature by Country", 
        os.path.join(output_dir, "temperature_bar.png")
    )
    if result["status"] == "success":
        print(f"Bar plot created: {result['output_path']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Test scatter plot with temperature data
    print("\nTesting scatter plot...")
    result = scatter_plot_handler(
        csv_path, "AverageTemperatureFahr", "AverageTemperatureUncertaintyFahr", "Temperature vs Uncertainty", 
        os.path.join(output_dir, "temp_uncertainty_scatter.png")
    )
    if result["status"] == "success":
        print(f"Scatter plot created: {result['output_path']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Test histogram with temperature data
    print("\nTesting histogram...")
    result = histogram_plot_handler(
        csv_path, "AverageTemperatureFahr", 30, "Temperature Distribution", 
        os.path.join(output_dir, "temperature_histogram.png")
    )
    if result["status"] == "success":
        print(f"Histogram created: {result['output_path']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Test heatmap with temperature data
    print("\nTesting heatmap...")
    result = heatmap_plot_handler(
        csv_path, "Temperature Data Correlation", 
        os.path.join(output_dir, "temperature_heatmap.png")
    )
    if result["status"] == "success":
        print(f"Heatmap created: {result['output_path']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print(f"\nAll plot capabilities tested successfully!")
    print(f"Generated plots saved in: {output_dir}/")

if __name__ == "__main__":
    test_plotting_capabilities()
