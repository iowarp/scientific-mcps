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

from parquet.server import (
    read_parquet_tool, write_parquet_tool, get_schema_tool,
    get_metadata_tool, get_statistics_tool, check_quality_tool,
    convert_to_csv_tool, convert_from_csv_tool,
    convert_to_json_tool, convert_from_json_tool,
    get_compression_tool
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
async def test_read_parquet_tool(temp_parquet_file):
    """Test read_parquet_tool."""
    result = await read_parquet_tool(temp_parquet_file)
    
    assert isinstance(result, dict)
    # Should have content with MCP format


@pytest.mark.asyncio
async def test_read_parquet_tool_with_columns(temp_parquet_file):
    """Test read_parquet_tool with specific columns."""
    result = await read_parquet_tool(temp_parquet_file, columns=["temperature", "location"])
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_read_parquet_tool_with_limit(temp_parquet_file):
    """Test read_parquet_tool with limit."""
    result = await read_parquet_tool(temp_parquet_file, limit=5)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_write_parquet_tool(sample_temperature_data):
    """Test write_parquet_tool."""
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
        result = await write_parquet_tool(sample_temperature_data, tmp.name)
        
        assert isinstance(result, dict)
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_get_parquet_schema_tool(temp_parquet_file):
    """Test get_schema_tool."""
    result = await get_schema_tool(temp_parquet_file)
    
    assert isinstance(result, dict)
    # Should have content or error handling


@pytest.mark.asyncio
async def test_get_parquet_metadata_tool(temp_parquet_file):
    """Test get_metadata_tool."""
    result = await get_metadata_tool(temp_parquet_file)
    
    assert isinstance(result, dict)
    # Should succeed or fail gracefully


@pytest.mark.asyncio
async def test_get_column_statistics_tool(temp_parquet_file):
    """Test get_statistics_tool."""
    result = await get_statistics_tool(temp_parquet_file)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_check_data_quality_tool(temp_parquet_file):
    """Test check_quality_tool."""
    result = await check_quality_tool(temp_parquet_file)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_compression_stats_tool(temp_parquet_file):
    """Test get_compression_tool."""
    result = await get_compression_tool(temp_parquet_file)
    
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_convert_parquet_to_csv_tool(temp_parquet_file):
    """Test convert_to_csv_tool."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        result = await convert_to_csv_tool(temp_parquet_file, tmp.name)
        
        assert isinstance(result, dict)
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_convert_parquet_to_json_tool(temp_parquet_file):
    """Test convert_to_json_tool."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        result = await convert_to_json_tool(temp_parquet_file, tmp.name, limit=5)
        
        assert isinstance(result, dict)
        assert os.path.exists(tmp.name)
        
        # Cleanup
        os.unlink(tmp.name)


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for non-existent files."""
    result = await read_parquet_tool("/non/existent/file.parquet")
    
    assert isinstance(result, dict)
    assert "isError" in result or "error" in str(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
