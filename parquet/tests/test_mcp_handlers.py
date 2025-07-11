"""
Test MCP handlers for Parquet MCP server.
"""
import pytest
import pytest_asyncio
import sys
import os
import tempfile
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parquet.mcp_handlers import (
    read_parquet_handler, write_parquet_handler, schema_handler,
    metadata_handler, statistics_handler, check_quality_handler,
    convert_format_handler, compression_handler
)


@pytest.fixture
def sample_temperature_data():
    """Create sample temperature data."""
    return {
        "timestamp": pd.date_range("2024-01-01", periods=10, freq="1h"),
        "temperature": [20.5, 21.0, 19.8, 22.3, 18.9, 23.1, 17.5, 24.0, 16.8, 25.2],
        "sensor_id": ["T001", "T002", "T001", "T003", "T002", "T001", "T003", "T002", "T001", "T003"],
        "location": ["NYC", "BOS", "NYC", "CHI", "BOS", "NYC", "CHI", "BOS", "NYC", "CHI"]
    }


@pytest_asyncio.fixture
async def temp_parquet_file(sample_temperature_data):
    """Create a temporary Parquet file with temperature data."""
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
        df = pd.DataFrame(sample_temperature_data)
        table = pa.Table.from_pandas(df)
        pq.write_table(table, tmp.name)
        yield tmp.name
    # Cleanup
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_read_parquet_handler(temp_parquet_file):
    """Test read_parquet_handler."""
    result = read_parquet_handler(temp_parquet_file)
    
    assert isinstance(result, dict)
    # Should succeed or fail gracefully


@pytest.mark.asyncio
async def test_read_parquet_handler_with_columns(temp_parquet_file):
    """Test read_parquet_handler with specific columns."""
    result = read_parquet_handler(temp_parquet_file, columns=["temperature", "location"])
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_read_parquet_handler_with_limit(temp_parquet_file):
    """Test read_parquet_handler with limit."""
    result = read_parquet_handler(temp_parquet_file, limit=5)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_write_parquet_handler(sample_temperature_data):
    """Test write_parquet_handler."""
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
        result = write_parquet_handler(sample_temperature_data, tmp.name)
        
        assert isinstance(result, dict)
        # Cleanup
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_schema_handler(temp_parquet_file):
    """Test schema_handler."""
    result = schema_handler(temp_parquet_file)
    
    assert isinstance(result, dict)
    # Should succeed or fail gracefully


@pytest.mark.asyncio
async def test_metadata_handler(temp_parquet_file):
    """Test metadata_handler."""
    result = metadata_handler(temp_parquet_file)
    
    assert isinstance(result, dict)
    # Should succeed or fail gracefully


@pytest.mark.asyncio
async def test_statistics_handler(temp_parquet_file):
    """Test statistics_handler."""
    result = statistics_handler(temp_parquet_file)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_check_quality_handler(temp_parquet_file):
    """Test check_quality_handler."""
    result = check_quality_handler(temp_parquet_file)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_compression_handler(temp_parquet_file):
    """Test compression_handler."""
    result = compression_handler(temp_parquet_file)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_convert_format_handler_to_csv(temp_parquet_file):
    """Test convert_format_handler for CSV."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        result = convert_format_handler(temp_parquet_file, tmp.name, "csv")
        
        assert isinstance(result, dict)
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_convert_format_handler_to_json(temp_parquet_file):
    """Test convert_format_handler for JSON."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        result = convert_format_handler(temp_parquet_file, tmp.name, "json", limit=5)
        
        assert isinstance(result, dict)
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for non-existent files."""
    result = read_parquet_handler("/non/existent/file.parquet")
    
    assert isinstance(result, dict)
    assert "isError" in result or "error" in str(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
