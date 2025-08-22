"""
Unit tests for preview_hdf5.preview_hdf5_datasets function.

Covers:
 - Dataset preview with default count
 - Dataset preview with custom count
 - Multiple datasets handling
 - Different data types (numeric, string)
 - File not found error handling
"""

import os
import sys
import pytest
import h5py
import tempfile

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from capabilities import preview_hdf5


def test_preview_hdf5_basic():
    """Test basic dataset preview functionality."""
    print("\n=== Running test_preview_hdf5_basic ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create test HDF5 file with datasets
        with h5py.File(fname, "w") as f:
            # Small dataset (less than default count)
            f.create_dataset("small_data", data=[1, 2, 3])

            # Large dataset (more than default count)
            large_data = list(range(20))
            f.create_dataset("large_data", data=large_data)

        # Test with default count (10)
        result = preview_hdf5.preview_hdf5_datasets(fname)
        print("Preview result:", result)

        assert "small_data" in result
        assert "large_data" in result
        assert result["small_data"] == [1, 2, 3]
        assert result["large_data"] == list(range(10))  # First 10 elements
        assert len(result["large_data"]) == 10

    finally:
        os.unlink(fname)


def test_preview_hdf5_custom_count():
    """Test dataset preview with custom count parameter."""
    print("\n=== Running test_preview_hdf5_custom_count ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create test data
        with h5py.File(fname, "w") as f:
            data = list(range(15))
            f.create_dataset("test_data", data=data)

        # Test with custom count
        result = preview_hdf5.preview_hdf5_datasets(fname, count=5)
        print("Custom count preview result:", result)

        assert "test_data" in result
        assert result["test_data"] == [0, 1, 2, 3, 4]
        assert len(result["test_data"]) == 5

    finally:
        os.unlink(fname)


def test_preview_hdf5_multiple_datasets():
    """Test preview of multiple datasets."""
    print("\n=== Running test_preview_hdf5_multiple_datasets ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create multiple datasets
        with h5py.File(fname, "w") as f:
            f.create_dataset("integers", data=[1, 2, 3, 4, 5])
            f.create_dataset("floats", data=[1.1, 2.2, 3.3, 4.4, 5.5])

            # Create group with dataset
            grp = f.create_group("group1")
            grp.create_dataset("nested_data", data=[10, 20, 30])

        result = preview_hdf5.preview_hdf5_datasets(fname)
        print("Multiple datasets preview result:", result)

        assert "integers" in result
        assert "floats" in result
        assert "group1/nested_data" in result

        assert result["integers"] == [1, 2, 3, 4, 5]
        assert result["floats"] == [1.1, 2.2, 3.3, 4.4, 5.5]
        assert result["group1/nested_data"] == [10, 20, 30]

    finally:
        os.unlink(fname)


def test_preview_hdf5_multidimensional():
    """Test preview of multidimensional datasets."""
    print("\n=== Running test_preview_hdf5_multidimensional ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create multidimensional dataset
        with h5py.File(fname, "w") as f:
            matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            f.create_dataset("matrix", data=matrix)

            # 3D array
            cube = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
            f.create_dataset("cube", data=cube)

        result = preview_hdf5.preview_hdf5_datasets(fname, count=5)
        print("Multidimensional preview result:", result)

        assert "matrix" in result
        assert "cube" in result

        # Flattened arrays (ravel() effect)
        assert result["matrix"] == [1, 2, 3, 4, 5]  # First 5 from flattened
        assert result["cube"] == [1, 2, 3, 4, 5]  # First 5 from flattened

    finally:
        os.unlink(fname)


def test_preview_hdf5_string_data():
    """Test preview of string datasets."""
    print("\n=== Running test_preview_hdf5_string_data ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create string dataset
        with h5py.File(fname, "w") as f:
            string_data = ["hello", "world", "test", "data"]
            f.create_dataset("strings", data=string_data, dtype=h5py.string_dtype())

        result = preview_hdf5.preview_hdf5_datasets(fname, count=3)
        print("String data preview result:", result)

        assert "strings" in result
        assert len(result["strings"]) == 3
        # String data should be converted to list
        assert isinstance(result["strings"], list)

    finally:
        os.unlink(fname)


def test_preview_hdf5_empty_file():
    """Test preview of empty HDF5 file."""
    print("\n=== Running test_preview_hdf5_empty_file ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create empty HDF5 file
        with h5py.File(fname, "w"):
            pass

        result = preview_hdf5.preview_hdf5_datasets(fname)
        print("Empty file preview result:", result)

        assert isinstance(result, dict)
        assert len(result) == 0

    finally:
        os.unlink(fname)


def test_preview_hdf5_groups_only():
    """Test preview of file with groups but no datasets."""
    print("\n=== Running test_preview_hdf5_groups_only ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create file with groups only
        with h5py.File(fname, "w") as f:
            grp1 = f.create_group("group1")
            grp1.create_group("subgroup")
            grp1.attrs["attr"] = "value"

        result = preview_hdf5.preview_hdf5_datasets(fname)
        print("Groups-only preview result:", result)

        assert isinstance(result, dict)
        assert len(result) == 0  # No datasets to preview

    finally:
        os.unlink(fname)


def test_preview_hdf5_single_element():
    """Test preview of dataset with single element."""
    print("\n=== Running test_preview_hdf5_single_element ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create single-element dataset
        with h5py.File(fname, "w") as f:
            f.create_dataset("single", data=42)
            f.create_dataset("single_float", data=3.14)

        result = preview_hdf5.preview_hdf5_datasets(fname)
        print("Single element preview result:", result)

        assert "single" in result
        assert "single_float" in result
        assert result["single"] == [42]
        assert result["single_float"] == [3.14]

    finally:
        os.unlink(fname)


def test_preview_hdf5_file_not_found():
    """Test preview of non-existent file."""
    print("\n=== Running test_preview_hdf5_file_not_found ===")

    with pytest.raises(OSError):
        preview_hdf5.preview_hdf5_datasets("nonexistent_file.h5")


def test_preview_hdf5_sample_files():
    """Test preview using existing sample files if available."""
    print("\n=== Running test_preview_hdf5_sample_files ===")

    # Try to use sample files from data directory
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    sample1 = os.path.join(data_dir, "sample1.h5")

    if os.path.exists(sample1):
        result = preview_hdf5.preview_hdf5_datasets(sample1)
        print(f"Sample file {sample1} preview result:", result)
        assert isinstance(result, dict)
        # Don't assert specific content since we don't know the sample file structure
    else:
        print(f"Sample file {sample1} not found, skipping this test")
