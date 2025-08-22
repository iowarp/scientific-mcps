"""
Unit tests for read_all_hdf5.read_all_hdf5_datasets function.

Covers:
 - Complete dataset reading
 - Multiple datasets handling
 - Different data types (numeric, string, VLEN)
 - Multidimensional arrays
 - File not found error handling
"""

import os
import sys
import pytest
import h5py
import tempfile
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from capabilities import read_all_hdf5


def test_read_all_hdf5_basic():
    """Test basic complete dataset reading."""
    print("\n=== Running test_read_all_hdf5_basic ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create test HDF5 file with datasets
        with h5py.File(fname, "w") as f:
            # Simple numeric datasets
            f.create_dataset("integers", data=[1, 2, 3, 4, 5])
            f.create_dataset("floats", data=[1.1, 2.2, 3.3])

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Read all result:", result)

        assert "integers" in result
        assert "floats" in result
        assert result["integers"] == [1, 2, 3, 4, 5]
        assert result["floats"] == [1.1, 2.2, 3.3]

    finally:
        os.unlink(fname)


def test_read_all_hdf5_multidimensional():
    """Test reading multidimensional datasets."""
    print("\n=== Running test_read_all_hdf5_multidimensional ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create multidimensional datasets
        with h5py.File(fname, "w") as f:
            # 2D array
            matrix = [[1, 2, 3], [4, 5, 6]]
            f.create_dataset("matrix", data=matrix)

            # 3D array
            cube = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
            f.create_dataset("cube", data=cube)

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Multidimensional read result:", result)

        assert "matrix" in result
        assert "cube" in result
        assert result["matrix"] == [[1, 2, 3], [4, 5, 6]]
        assert result["cube"] == [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]

    finally:
        os.unlink(fname)


def test_read_all_hdf5_multiple_datasets():
    """Test reading multiple datasets from different groups."""
    print("\n=== Running test_read_all_hdf5_multiple_datasets ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create multiple datasets in different groups
        with h5py.File(fname, "w") as f:
            # Root level datasets
            f.create_dataset("root_data", data=[1, 2, 3])

            # Group level datasets
            grp1 = f.create_group("group1")
            grp1.create_dataset("data1", data=[10, 20, 30])

            grp2 = f.create_group("group2")
            grp2.create_dataset("data2", data=[100, 200])

            # Nested group
            nested = grp1.create_group("nested")
            nested.create_dataset("deep_data", data=[1000])

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Multiple datasets read result:", result)

        assert "root_data" in result
        assert "group1/data1" in result
        assert "group2/data2" in result
        assert "group1/nested/deep_data" in result

        assert result["root_data"] == [1, 2, 3]
        assert result["group1/data1"] == [10, 20, 30]
        assert result["group2/data2"] == [100, 200]
        assert result["group1/nested/deep_data"] == [1000]

    finally:
        os.unlink(fname)


def test_read_all_hdf5_string_data():
    """Test reading string datasets."""
    print("\n=== Running test_read_all_hdf5_string_data ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create string dataset
        with h5py.File(fname, "w") as f:
            string_data = ["hello", "world", "test"]
            f.create_dataset("strings", data=string_data, dtype=h5py.string_dtype())

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("String data read result:", result)

        assert "strings" in result
        assert isinstance(result["strings"], list)
        # Result should contain the string data
        assert len(result["strings"]) == 3

    finally:
        os.unlink(fname)


def test_read_all_hdf5_scalar_data():
    """Test reading scalar (single value) datasets."""
    print("\n=== Running test_read_all_hdf5_scalar_data ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create scalar datasets
        with h5py.File(fname, "w") as f:
            f.create_dataset("scalar_int", data=42)
            f.create_dataset("scalar_float", data=3.14159)
            f.create_dataset(
                "scalar_string", data="single_string", dtype=h5py.string_dtype()
            )

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Scalar data read result:", result)

        assert "scalar_int" in result
        assert "scalar_float" in result
        assert "scalar_string" in result

        assert result["scalar_int"] == 42
        assert result["scalar_float"] == 3.14159

    finally:
        os.unlink(fname)


def test_read_all_hdf5_empty_datasets():
    """Test reading empty datasets."""
    print("\n=== Running test_read_all_hdf5_empty_datasets ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create empty datasets
        with h5py.File(fname, "w") as f:
            f.create_dataset("empty_array", data=np.array([]))
            f.create_dataset("zero_shape", shape=(0,), dtype="f")

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Empty datasets read result:", result)

        assert "empty_array" in result
        assert "zero_shape" in result
        assert result["empty_array"] == []
        assert result["zero_shape"] == []

    finally:
        os.unlink(fname)


def test_read_all_hdf5_large_dataset():
    """Test reading large dataset."""
    print("\n=== Running test_read_all_hdf5_large_dataset ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create large dataset
        with h5py.File(fname, "w") as f:
            large_data = list(range(1000))
            f.create_dataset("large_data", data=large_data)

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Large dataset read result length:", len(result["large_data"]))

        assert "large_data" in result
        assert len(result["large_data"]) == 1000
        assert result["large_data"][:5] == [0, 1, 2, 3, 4]
        assert result["large_data"][-5:] == [995, 996, 997, 998, 999]

    finally:
        os.unlink(fname)


def test_read_all_hdf5_empty_file():
    """Test reading empty HDF5 file."""
    print("\n=== Running test_read_all_hdf5_empty_file ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create empty HDF5 file
        with h5py.File(fname, "w"):
            pass

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Empty file read result:", result)

        assert isinstance(result, dict)
        assert len(result) == 0

    finally:
        os.unlink(fname)


def test_read_all_hdf5_groups_only():
    """Test reading file with groups but no datasets."""
    print("\n=== Running test_read_all_hdf5_groups_only ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create file with groups only
        with h5py.File(fname, "w") as f:
            grp1 = f.create_group("group1")
            grp1.create_group("subgroup")
            grp1.attrs["attr"] = "value"

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Groups-only read result:", result)

        assert isinstance(result, dict)
        assert len(result) == 0  # No datasets to read

    finally:
        os.unlink(fname)


def test_read_all_hdf5_mixed_types():
    """Test reading datasets with mixed data types."""
    print("\n=== Running test_read_all_hdf5_mixed_types ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create datasets with different types
        with h5py.File(fname, "w") as f:
            # Boolean data
            f.create_dataset("booleans", data=[True, False, True])

            # Complex numbers
            f.create_dataset("complex", data=[1 + 2j, 3 + 4j])

            # Different integer types
            f.create_dataset("int8", data=np.array([1, 2, 3], dtype=np.int8))
            f.create_dataset("uint64", data=np.array([100, 200], dtype=np.uint64))

        result = read_all_hdf5.read_all_hdf5_datasets(fname)
        print("Mixed types read result:", result)

        assert "booleans" in result
        assert "complex" in result
        assert "int8" in result
        assert "uint64" in result

        # All should be converted to Python lists
        assert isinstance(result["booleans"], list)
        assert isinstance(result["complex"], list)
        assert isinstance(result["int8"], list)
        assert isinstance(result["uint64"], list)

    finally:
        os.unlink(fname)


def test_read_all_hdf5_file_not_found():
    """Test reading non-existent file."""
    print("\n=== Running test_read_all_hdf5_file_not_found ===")

    with pytest.raises(OSError):
        read_all_hdf5.read_all_hdf5_datasets("nonexistent_file.h5")


def test_read_all_hdf5_sample_files():
    """Test reading using existing sample files if available."""
    print("\n=== Running test_read_all_hdf5_sample_files ===")

    # Try to use sample files from data directory
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    sample1 = os.path.join(data_dir, "sample1.h5")

    if os.path.exists(sample1):
        result = read_all_hdf5.read_all_hdf5_datasets(sample1)
        print(f"Sample file {sample1} read result:", result)
        assert isinstance(result, dict)
        # Don't assert specific content since we don't know the sample file structure
    else:
        print(f"Sample file {sample1} not found, skipping this test")
