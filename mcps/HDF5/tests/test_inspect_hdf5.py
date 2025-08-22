"""
Unit tests for inspect_hdf5.inspect_hdf5_file function.

Covers:
 - Successful inspection of HDF5 file structure
 - Groups, datasets, and attributes inspection
 - File not found error handling
"""

import os
import sys
import pytest
import h5py
import tempfile

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from capabilities import inspect_hdf5


def test_inspect_hdf5_basic():
    """Test basic HDF5 file inspection with groups and datasets."""
    print("\n=== Running test_inspect_hdf5_basic ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create a test HDF5 file
        with h5py.File(fname, "w") as f:
            # Create a group with attributes
            grp = f.create_group("test_group")
            grp.attrs["group_attr"] = "test_value"

            # Create a dataset with attributes
            data = [1, 2, 3, 4, 5]
            dset = f.create_dataset("test_dataset", data=data)
            dset.attrs["dataset_attr"] = "test_data"

            # Create nested structure
            subgrp = grp.create_group("subgroup")
            subdset = subgrp.create_dataset("nested_data", data=[10, 20])
            subdset.attrs["nested_attr"] = 42

        # Test the inspection function
        result = inspect_hdf5.inspect_hdf5_file(fname)
        print("Inspection result:", result)

        # Verify the output contains expected elements
        result_str = "\n".join(result)
        assert "GROUP   /test_group/" in result_str
        assert "DATASET /test_dataset" in result_str
        assert "GROUP   /test_group/subgroup/" in result_str
        assert "DATASET /test_group/subgroup/nested_data" in result_str
        assert "group_attr" in result_str
        assert "dataset_attr" in result_str
        assert "nested_attr" in result_str

    finally:
        os.unlink(fname)


def test_inspect_hdf5_empty_file():
    """Test inspection of empty HDF5 file."""
    print("\n=== Running test_inspect_hdf5_empty_file ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create an empty HDF5 file
        with h5py.File(fname, "w"):
            pass

        result = inspect_hdf5.inspect_hdf5_file(fname)
        print("Empty file inspection result:", result)

        # Empty file should return empty list
        assert isinstance(result, list)
        assert len(result) == 0

    finally:
        os.unlink(fname)


def test_inspect_hdf5_with_attributes_only():
    """Test inspection of HDF5 file with root attributes only."""
    print("\n=== Running test_inspect_hdf5_with_attributes_only ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create HDF5 file with only root attributes
        with h5py.File(fname, "w") as f:
            f.attrs["root_attr"] = "root_value"
            f.attrs["version"] = 1.0

        result = inspect_hdf5.inspect_hdf5_file(fname)
        print("Attributes-only inspection result:", result)

        # Should be empty since visititems doesn't visit root
        assert isinstance(result, list)
        assert len(result) == 0

    finally:
        os.unlink(fname)


def test_inspect_hdf5_complex_structure():
    """Test inspection of complex HDF5 file structure."""
    print("\n=== Running test_inspect_hdf5_complex_structure ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create complex HDF5 structure
        with h5py.File(fname, "w") as f:
            # Multiple groups and datasets
            g1 = f.create_group("group1")
            g1.attrs["type"] = "primary"

            g2 = f.create_group("group2")
            g2.attrs["type"] = "secondary"

            # Datasets in groups
            g1.create_dataset("data1", data=[1, 2, 3])
            g2.create_dataset("data2", data=[[1, 2], [3, 4]])

            # Nested groups
            nested = g1.create_group("nested")
            nested.create_dataset(
                "deep_data", data="string_data", dtype=h5py.string_dtype()
            )

        result = inspect_hdf5.inspect_hdf5_file(fname)
        print("Complex structure inspection result:", result)

        result_str = "\n".join(result)
        assert "GROUP   /group1/" in result_str
        assert "GROUP   /group2/" in result_str
        assert "DATASET /group1/data1" in result_str
        assert "DATASET /group2/data2" in result_str
        assert "GROUP   /group1/nested/" in result_str
        assert "DATASET /group1/nested/deep_data" in result_str
        assert "shape=(3,)" in result_str
        assert "shape=(2, 2)" in result_str

    finally:
        os.unlink(fname)


def test_inspect_hdf5_file_not_found():
    """Test inspection of non-existent file."""
    print("\n=== Running test_inspect_hdf5_file_not_found ===")

    with pytest.raises(OSError):
        inspect_hdf5.inspect_hdf5_file("nonexistent_file.h5")


def test_inspect_hdf5_sample_files():
    """Test inspection using existing sample files if available."""
    print("\n=== Running test_inspect_hdf5_sample_files ===")

    # Try to use sample files from data directory
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    sample1 = os.path.join(data_dir, "sample1.h5")

    if os.path.exists(sample1):
        result = inspect_hdf5.inspect_hdf5_file(sample1)
        print(f"Sample file {sample1} inspection result:", result)
        assert isinstance(result, list)
        # Don't assert specific content since we don't know the sample file structure
    else:
        print(f"Sample file {sample1} not found, skipping this test")
