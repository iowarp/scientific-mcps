"""
Test plot_capabilities.py module for complete coverage of all edge cases and error paths.
"""

import os
import sys
import tempfile
import pandas as pd
import pytest
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from implementation.plot_capabilities import (  # noqa: E402
    create_line_plot,
    create_bar_plot,
    create_scatter_plot,
    create_histogram,
    create_heatmap,
    get_data_info,
)


class TestCapabilitiesCoverage:
    """Test plot capabilities for complete coverage including error paths"""

    @pytest.fixture
    def sample_data_file(self):
        """Create a sample CSV file for testing."""
        data = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10],
                "category": ["A", "B", "A", "B", "A"],
                "value": [10, 20, 15, 25, 30],
                "numeric_col": [1.1, 2.2, 3.3, 4.4, 5.5],
            }
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            data.to_csv(f.name, index=False)
            yield f.name
        os.unlink(f.name)

    @pytest.fixture
    def empty_data_file(self):
        """Create an empty CSV file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("col1,col2\n")  # Header only
            yield f.name
        os.unlink(f.name)

    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary directory for output files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def test_get_data_info_complete_coverage(self, sample_data_file):
        """Test get_data_info with comprehensive coverage"""
        result = get_data_info(sample_data_file)
        assert result["status"] == "success"
        assert result["shape"] == (5, 5)
        assert len(result["columns"]) == 5
        assert "dtypes" in result

    def test_get_data_info_file_not_found(self):
        """Test get_data_info with non-existent file"""
        result = get_data_info("nonexistent_file.csv")
        assert result["status"] == "error"
        assert "error" in result

    def test_get_data_info_empty_file(self, empty_data_file):
        """Test get_data_info with empty file"""
        result = get_data_info(empty_data_file)
        assert result["status"] == "error"  # Empty file should cause error

    def test_create_line_plot_edge_cases(self, sample_data_file, temp_output_dir):
        """Test create_line_plot with edge cases"""
        output_path = os.path.join(temp_output_dir, "test_line.png")

        # Test with minimal parameters
        result = create_line_plot(
            file_path=sample_data_file,
            x_column="x",
            y_column="y",
            output_path=output_path,
        )
        assert result["status"] == "success"
        assert os.path.exists(output_path)

    def test_create_line_plot_invalid_column(self, sample_data_file, temp_output_dir):
        """Test create_line_plot with invalid column"""
        output_path = os.path.join(temp_output_dir, "test_line_error.png")
        result = create_line_plot(
            file_path=sample_data_file,
            x_column="invalid_column",
            y_column="y",
            output_path=output_path,
        )
        assert result["status"] == "error"
        assert "error" in result

    def test_create_bar_plot_edge_cases(self, sample_data_file, temp_output_dir):
        """Test create_bar_plot edge cases"""
        output_path = os.path.join(temp_output_dir, "test_bar.png")
        result = create_bar_plot(
            file_path=sample_data_file,
            x_column="category",
            y_column="value",
            output_path=output_path,
        )
        assert result["status"] == "success"
        assert os.path.exists(output_path)

    def test_create_scatter_plot_edge_cases(self, sample_data_file, temp_output_dir):
        """Test create_scatter_plot edge cases"""
        output_path = os.path.join(temp_output_dir, "test_scatter.png")
        result = create_scatter_plot(
            file_path=sample_data_file,
            x_column="x",
            y_column="y",
            output_path=output_path,
        )
        assert result["status"] == "success"
        assert os.path.exists(output_path)

    def test_create_histogram_edge_cases(self, sample_data_file, temp_output_dir):
        """Test create_histogram edge cases"""
        output_path = os.path.join(temp_output_dir, "test_histogram.png")

        # Test with default bins
        result = create_histogram(
            file_path=sample_data_file, column="value", output_path=output_path
        )
        assert result["status"] == "success"
        assert os.path.exists(output_path)

    def test_create_histogram_invalid_column(self, sample_data_file, temp_output_dir):
        """Test create_histogram with invalid column"""
        output_path = os.path.join(temp_output_dir, "test_histogram_error.png")
        result = create_histogram(
            file_path=sample_data_file, column="invalid_column", output_path=output_path
        )
        assert result["status"] == "error"
        assert "error" in result

    def test_create_heatmap_edge_cases(self, sample_data_file, temp_output_dir):
        """Test create_heatmap edge cases"""
        output_path = os.path.join(temp_output_dir, "test_heatmap.png")
        result = create_heatmap(file_path=sample_data_file, output_path=output_path)
        assert result["status"] == "success"
        assert os.path.exists(output_path)

    def test_create_heatmap_no_numeric_data(self, temp_output_dir):
        """Test create_heatmap with non-numeric data"""
        # Create file with only string columns
        data = pd.DataFrame({"text1": ["a", "b", "c"], "text2": ["x", "y", "z"]})
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            data.to_csv(f.name, index=False)

            output_path = os.path.join(temp_output_dir, "test_heatmap_no_numeric.png")
            result = create_heatmap(file_path=f.name, output_path=output_path)

            # Should handle the case gracefully
            assert result["status"] == "error"
            assert "error" in result

        os.unlink(f.name)

    def test_file_loading_errors(self):
        """Test various file loading error scenarios"""
        # Test with completely invalid file path
        result = get_data_info("/invalid/path/that/does/not/exist.csv")
        assert result["status"] == "error"

        # Test plotting functions with invalid files
        result = create_line_plot("/invalid/file.csv", "x", "y", "output.png")
        assert result["status"] == "error"

        result = create_bar_plot("/invalid/file.csv", "x", "y", "output.png")
        assert result["status"] == "error"

        result = create_scatter_plot("/invalid/file.csv", "x", "y", "output.png")
        assert result["status"] == "error"

        result = create_histogram("/invalid/file.csv", "col", "output.png")
        assert result["status"] == "error"

        result = create_heatmap("/invalid/file.csv", "output.png")
        assert result["status"] == "error"
