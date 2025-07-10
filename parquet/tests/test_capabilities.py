"""
Test capabilities for Parquet MCP server.
"""
import pytest
import sys
import os
from pathlib import Path
import tempfile
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parquet.capabilities.parquet_io import read_parquet_file, write_parquet_file
from parquet.capabilities.metadata import get_file_metadata, get_compression_stats
from parquet.capabilities.statistics import get_column_statistics, check_data_quality
from parquet.capabilities.format_conversion import (
    parquet_to_csv, csv_to_parquet,
    parquet_to_json, json_to_parquet
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return {
        "temperature": [20.5, 21.0, 19.8, 22.3, 18.9],
        "humidity": [65, 68, 62, 70, 60],
        "pressure": [1013.25, 1012.8, 1014.2, 1011.5, 1015.0],
        "location": ["New York", "Boston", "Chicago", "Miami", "Seattle"]
    }


@pytest.fixture
def temp_parquet_file(sample_data):
    """Create a temporary Parquet file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
        df = pd.DataFrame(sample_data)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, tmp.name)
        yield tmp.name
    # Cleanup
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)


def test_read_parquet_file(temp_parquet_file):
    """Test reading a Parquet file."""
    result = read_parquet_file(temp_parquet_file)
    
    assert result["success"] is True
    assert result["num_rows"] == 5
    assert result["num_columns"] == 4
    assert "temperature" in result["columns"]
    assert "humidity" in result["columns"]


def test_read_parquet_with_columns(temp_parquet_file):
    """Test reading specific columns from a Parquet file."""
    result = read_parquet_file(temp_parquet_file, columns=["temperature", "humidity"])
    
    assert result["success"] is True
    assert result["num_rows"] == 5
    assert result["num_columns"] == 2
    assert set(result["columns"]) == {"temperature", "humidity"}


def test_read_parquet_with_limit(temp_parquet_file):
    """Test reading with row limit."""
    result = read_parquet_file(temp_parquet_file, limit=3)
    
    assert result["success"] is True
    assert result["num_rows"] == 3
    assert result["num_columns"] == 4


def test_write_parquet_file(sample_data):
    """Test writing data to a Parquet file."""
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
        # Convert dict data to list of rows for multiple rows
        df = pd.DataFrame(sample_data)
        result = write_parquet_file(df, tmp.name)
        
        assert result["success"] is True
        assert result["num_rows"] == 5
        assert result["num_columns"] == 4
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


def test_write_parquet_with_compression(sample_data):
    """Test writing with different compression."""
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
        result = write_parquet_file(sample_data, tmp.name, compression="gzip")
        
        assert result["success"] is True
        assert result["compression"] == "gzip"
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


def test_get_file_metadata(temp_parquet_file):
    """Test getting file metadata."""
    result = get_file_metadata(temp_parquet_file)
    
    assert result["success"] is True
    assert result["file_info"]["num_rows"] == 5
    assert result["file_info"]["num_columns"] == 4
    assert "schema" in result


def test_get_compression_stats(temp_parquet_file):
    """Test getting compression statistics."""
    result = get_compression_stats(temp_parquet_file)
    
    assert result["success"] is True
    assert "compression_ratio" in result
    assert "file_size_bytes" in result


def test_get_column_statistics(temp_parquet_file):
    """Test getting column statistics."""
    result = get_column_statistics(temp_parquet_file)
    
    assert result["success"] is True
    assert "column_statistics" in result
    assert "temperature" in result["column_statistics"]


def test_check_data_quality(temp_parquet_file):
    """Test data quality check."""
    result = check_data_quality(temp_parquet_file)
    
    assert result["success"] is True
    assert "quality_report" in result


def test_convert_parquet_to_csv(temp_parquet_file):
    """Test converting Parquet to CSV."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        result = parquet_to_csv(temp_parquet_file, tmp.name)
        
        assert result["success"] is True
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


def test_convert_csv_to_parquet():
    """Test converting CSV to Parquet."""
    # Create a CSV file first
    csv_data = pd.DataFrame({
        "temperature": [20.5, 21.0, 19.8],
        "humidity": [65, 68, 62]
    })
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_tmp, \
         tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as parquet_tmp:
        
        csv_data.to_csv(csv_tmp.name, index=False)
        result = csv_to_parquet(csv_tmp.name, parquet_tmp.name)
        
        assert result["success"] is True
        assert os.path.exists(parquet_tmp.name)
        
        # Cleanup
        os.unlink(csv_tmp.name)
        os.unlink(parquet_tmp.name)


def test_convert_parquet_to_json(temp_parquet_file):
    """Test converting Parquet to JSON."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        result = parquet_to_json(temp_parquet_file, tmp.name, limit=3)
        
        assert result["success"] is True
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


def test_error_handling():
    """Test error handling for non-existent files."""
    result = read_parquet_file("/non/existent/file.parquet")
    
    assert result["success"] is False
    assert "error" in result
    assert result["error_type"] == "FileNotFoundError"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
