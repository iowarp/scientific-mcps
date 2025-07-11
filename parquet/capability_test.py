#!/usr/bin/env python3
"""
Comprehensive capability test for Parquet MCP.
Tests all core functionality including I/O, metadata, statistics, and conversions.
"""
import asyncio
import json
import tempfile
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parquet.mcp_handlers import (
    read_parquet_handler, write_parquet_handler, schema_handler,
    metadata_handler, statistics_handler, check_quality_handler,
    convert_format_handler, compression_handler
)


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")


def print_result(operation, result):
    """Print operation result in a formatted way."""
    print(f"\n{operation}:")
    print("-" * 40)
    
    if "isError" in result and result["isError"]:
        print("ERROR:")
        content = json.loads(result["content"][0]["text"])
        print(f"   {content.get('error', 'Unknown error')}")
    else:
        print("SUCCESS")
        content = json.loads(result["content"][0]["text"])
        if content.get("success"):
            # Print key information
            for key in ["num_rows", "num_columns", "file_size_bytes", "compression_ratio"]:
                if key in content:
                    print(f"   {key}: {content[key]}")


def create_sample_data():
    """Create sample Parquet files for testing."""
    print_section("CREATING SAMPLE DATA")
    
    # Sample data with various data types
    sample_data = [
        {
            "id": 1,
            "name": "Alice Johnson",
            "age": 28,
            "salary": 75000.50,
            "department": "Engineering",
            "active": True,
            "hire_date": "2020-01-15",
            "performance_score": 4.5
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "age": 34,
            "salary": 82000.00,
            "department": "Marketing",
            "active": True,
            "hire_date": "2019-03-22",
            "performance_score": 4.2
        },
        {
            "id": 3,
            "name": "Charlie Brown",
            "age": 41,
            "salary": 95000.75,
            "department": "Engineering",
            "active": False,
            "hire_date": "2017-07-10",
            "performance_score": 3.8
        },
        {
            "id": 4,
            "name": "Diana Prince",
            "age": 29,
            "salary": 68000.25,
            "department": "HR",
            "active": True,
            "hire_date": "2021-05-03",
            "performance_score": 4.7
        },
        {
            "id": 5,
            "name": "Eve Wilson",
            "age": 36,
            "salary": 78000.00,
            "department": "Finance",
            "active": True,
            "hire_date": "2018-11-18",
            "performance_score": 4.1
        }
    ]
    
    # Create temporary parquet file
    temp_parquet = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    temp_parquet.close()
    
    # Write sample data
    result = write_parquet_handler(sample_data, temp_parquet.name, "snappy")
    print_result("Writing sample Parquet file", result)
    
    return temp_parquet.name, sample_data


def test_basic_io(parquet_file):
    """Test basic I/O operations."""
    print_section("BASIC I/O OPERATIONS")
    
    # Test reading entire file
    result = read_parquet_handler(parquet_file)
    print_result("Reading entire Parquet file", result)
    
    # Test reading specific columns
    result = read_parquet_handler(parquet_file, columns=["name", "age", "salary"])
    print_result("Reading specific columns", result)
    
    # Test reading with limit
    result = read_parquet_handler(parquet_file, limit=3)
    print_result("Reading with row limit", result)
    
    # Test writing with different compression
    temp_file = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    temp_file.close()
    
    test_data = [{"test": "value", "number": 123}]
    result = write_parquet_handler(test_data, temp_file.name, "gzip")
    print_result("Writing with GZIP compression", result)
    
    os.unlink(temp_file.name)


def test_metadata_operations(parquet_file):
    """Test metadata extraction capabilities."""
    print_section("METADATA OPERATIONS")
    
    # Test schema extraction
    result = schema_handler(parquet_file)
    print_result("Getting file schema", result)
    
    # Test comprehensive metadata
    result = metadata_handler(parquet_file)
    print_result("Getting comprehensive metadata", result)
    
    # Test compression statistics
    result = compression_handler(parquet_file)
    print_result("Getting compression statistics", result)


def test_statistical_analysis(parquet_file):
    """Test statistical analysis capabilities."""
    print_section("STATISTICAL ANALYSIS")
    
    # Test column statistics
    result = statistics_handler(parquet_file)
    print_result("Getting column statistics", result)
    
    # Test statistics for specific columns
    result = statistics_handler(parquet_file, columns=["age", "salary", "performance_score"])
    print_result("Getting statistics for numeric columns", result)
    
    # Test data quality checks
    result = check_quality_handler(parquet_file)
    print_result("Checking data quality", result)


def test_format_conversions(parquet_file):
    """Test format conversion capabilities."""
    print_section("FORMAT CONVERSIONS")
    
    # Test Parquet to CSV
    csv_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    csv_file.close()
    
    result = convert_format_handler(parquet_file, csv_file.name, "csv")
    print_result("Converting Parquet to CSV", result)
    
    # Test CSV to Parquet
    new_parquet = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    new_parquet.close()
    
    result = convert_format_handler(csv_file.name, new_parquet.name, "parquet")
    print_result("Converting CSV back to Parquet", result)
    
    # Test Parquet to JSON
    json_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    json_file.close()
    
    result = convert_format_handler(parquet_file, json_file.name, "json", limit=3)
    print_result("Converting Parquet to JSON (limited)", result)
    
    # Test JSON to Parquet
    json_parquet = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    json_parquet.close()
    
    result = convert_format_handler(json_file.name, json_parquet.name, "parquet")
    print_result("Converting JSON back to Parquet", result)
    
    # Cleanup
    for temp_file in [csv_file.name, new_parquet.name, json_file.name, json_parquet.name]:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_with_existing_data():
    """Test all capabilities with existing parquet files."""
    print_section("TESTING WITH EXISTING DATA FILES")
    
    data_dir = Path(__file__).parent / "data"
    parquet_files = list(data_dir.glob("*.parquet"))
    
    for parquet_file in parquet_files:
        print(f"\n--- Testing with {parquet_file.name} ---")
        
        # Basic read test
        result = read_parquet_handler(str(parquet_file))
        print_result(f"Reading {parquet_file.name}", result)
        
        # Schema test
        result = schema_handler(str(parquet_file))
        print_result(f"Schema of {parquet_file.name}", result)
        
        # Statistics test
        result = statistics_handler(str(parquet_file))
        print_result(f"Statistics of {parquet_file.name}", result)
        
        # Quality check
        result = check_quality_handler(str(parquet_file))
        print_result(f"Quality check of {parquet_file.name}", result)
        
        # Compression stats
        result = compression_handler(str(parquet_file))
        print_result(f"Compression stats of {parquet_file.name}", result)


def test_memory_optimization():
    """Test memory optimization with larger datasets."""
    print_section("MEMORY OPTIMIZATION")
    
    # Create a larger dataset
    large_data = []
    for i in range(1000):
        large_data.append({
            "id": i,
            "name": f"User_{i:04d}",
            "value": i * 1.5,
            "category": f"Cat_{i % 10}",
            "active": i % 2 == 0
        })
    
    # Write large dataset
    large_file = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    large_file.close()
    
    result = write_parquet_handler(large_data, large_file.name)
    print_result("Writing large dataset (1000 rows)", result)
    
    # Test reading with limits
    result = read_parquet_handler(large_file.name, limit=10)
    print_result("Reading large file with limit", result)
    
    # Test compression efficiency
    result = compression_handler(large_file.name)
    print_result("Compression analysis for large file", result)
    
    os.unlink(large_file.name)


def main():
    """Run comprehensive capability tests."""
    print("Starting Parquet MCP Comprehensive Capability Test")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    try:
        # Test with existing data first
        test_with_existing_data()
        
        # Create sample data
        parquet_file, sample_data = create_sample_data()
        
        # Run all tests
        test_basic_io(parquet_file)
        test_metadata_operations(parquet_file)
        test_statistical_analysis(parquet_file)
        test_format_conversions(parquet_file)
        test_memory_optimization()
        
        print_section("TEST COMPLETION")
        print("All capability tests completed successfully!")
        print(f"Sample file created at: {parquet_file}")
        print("Cleaning up...")
        
        # Cleanup
        if os.path.exists(parquet_file):
            os.unlink(parquet_file)
            print("   Sample file cleaned up")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\nParquet MCP capability test completed!")
    return 0


if __name__ == "__main__":
    exit_code = main()
