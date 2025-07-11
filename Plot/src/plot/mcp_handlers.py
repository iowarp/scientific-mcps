"""
MCP handlers for Plot functionality.
"""
import os
import sys
import logging
from typing import Dict, Any, Optional

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

from capabilities.plot_capabilities import (
    get_data_info,
    create_line_plot,
    create_bar_plot,
    create_scatter_plot,
    create_histogram,
    create_heatmap
)

logger = logging.getLogger(__name__)

def data_info_handler(file_path: str) -> Dict[str, Any]:
    """
    Handler for getting data information.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        Dictionary with data information
    """
    logger.info(f"Getting data info for: {file_path}")
    return get_data_info(file_path)

def line_plot_handler(
    file_path: str, 
    x_column: str, 
    y_column: str, 
    title: str = "Line Plot",
    output_path: str = "line_plot.png"
) -> Dict[str, Any]:
    """
    Handler for creating line plots.
    
    Args:
        file_path: Path to the data file
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating line plot: {file_path} -> {output_path}")
    return create_line_plot(file_path, x_column, y_column, title, output_path)

def bar_plot_handler(
    file_path: str, 
    x_column: str, 
    y_column: str, 
    title: str = "Bar Plot",
    output_path: str = "bar_plot.png"
) -> Dict[str, Any]:
    """
    Handler for creating bar plots.
    
    Args:
        file_path: Path to the data file
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating bar plot: {file_path} -> {output_path}")
    return create_bar_plot(file_path, x_column, y_column, title, output_path)

def scatter_plot_handler(
    file_path: str, 
    x_column: str, 
    y_column: str, 
    title: str = "Scatter Plot",
    output_path: str = "scatter_plot.png"
) -> Dict[str, Any]:
    """
    Handler for creating scatter plots.
    
    Args:
        file_path: Path to the data file
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating scatter plot: {file_path} -> {output_path}")
    return create_scatter_plot(file_path, x_column, y_column, title, output_path)

def histogram_plot_handler(
    file_path: str, 
    column: str, 
    bins: int = 30,
    title: str = "Histogram",
    output_path: str = "histogram.png"
) -> Dict[str, Any]:
    """
    Handler for creating histograms.
    
    Args:
        file_path: Path to the data file
        column: Column name for histogram
        bins: Number of bins
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating histogram: {file_path} -> {output_path}")
    return create_histogram(file_path, column, bins, title, output_path)

def heatmap_plot_handler(
    file_path: str, 
    title: str = "Heatmap",
    output_path: str = "heatmap.png"
) -> Dict[str, Any]:
    """
    Handler for creating heatmaps.
    
    Args:
        file_path: Path to the data file
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating heatmap: {file_path} -> {output_path}")
    return create_heatmap(file_path, title, output_path)
