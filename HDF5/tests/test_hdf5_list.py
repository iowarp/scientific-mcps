"""
Unit tests for hdf5_list module.

Covers:
 - Successful listing of .hdf5 files in a directory
 - Directory-not-found error handling
 - Edge cases with empty directories
"""
import pytest
import sys
import os

# Path setup for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from implementation import hdf5_list


class TestHDF5List:
    """Test class for HDF5 file listing functionality."""

    def test_list_hdf5_basic(self, tmp_path):
        """Test basic HDF5 file listing functionality."""
        print("\n=== Running test_list_hdf5_basic ===")
        d = tmp_path / "dir"
        d.mkdir()
        (d / "a.hdf5").write_text("")
        (d / "b.hdf5").write_text("")
        print(f"Mock directory created at: {d}")

        files = hdf5_list.list_hdf5(str(d))
        print("Files found:", files)
        assert len(files) == 2

    def test_list_hdf5_no_dir(self):
        """Test error handling for non-existent directory."""
        print("\n=== Running test_list_hdf5_no_dir ===")
        with pytest.raises(FileNotFoundError) as excinfo:
            hdf5_list.list_hdf5("no_such_dir")
        print("Caught exception:", excinfo.value)

    def test_list_hdf5_empty_dir(self, tmp_path):
        """Test listing in empty directory."""
        print("\n=== Running test_list_hdf5_empty_dir ===")
        d = tmp_path / "empty_dir"
        d.mkdir()
        
        files = hdf5_list.list_hdf5(str(d))
        print("Files found in empty dir:", files)
        assert len(files) == 0