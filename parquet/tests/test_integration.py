"""
Integration tests for Parquet MCP server.
Tests the complete workflow from data processing to format conversion.
"""
import pytest
import sys
import os
import tempfile
import pandas as pd
import numpy as np
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parquet.mcp_handlers import (
    read_parquet_handler,
    write_parquet_handler,
    schema_handler,
    metadata_handler,
    statistics_handler,
    check_quality_handler,
    convert_format_handler,
    compression_handler
)


@pytest.fixture
def comprehensive_data():
    """Create comprehensive test data simulating real-world scenarios."""
    np.random.seed(42)
    
    # Simulate financial data
    dates = pd.date_range('2020-01-01', periods=1000, freq='D')
    data = {
        'date': dates,
        'stock_price': 100 + np.cumsum(np.random.randn(1000) * 0.02),
        'volume': np.random.lognormal(mean=10, sigma=1, size=1000),
        'market_cap': np.random.lognormal(mean=20, sigma=0.5, size=1000),
        'sector': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer'], 1000),
        'company_size': np.random.choice(['Small', 'Medium', 'Large'], 1000),
        'dividend_yield': np.random.uniform(0, 0.08, 1000),
        'pe_ratio': np.random.lognormal(mean=3, sigma=0.5, size=1000),
        'is_profitable': np.random.choice([True, False], 1000, p=[0.7, 0.3]),
        'employee_count': np.random.lognormal(mean=8, sigma=1, size=1000).astype(int),
        'revenue': np.random.lognormal(mean=18, sigma=1, size=1000),
        'profit_margin': np.random.uniform(-0.2, 0.3, 1000)
    }
    return pd.DataFrame(data)


@pytest.fixture
def weather_data():
    """Create weather data for testing."""
    np.random.seed(123)
    
    # Simulate weather station data
    dates = pd.date_range('2023-01-01', periods=8760, freq='H')  # One year of hourly data
    data = {
        'timestamp': dates,
        'temperature': 15 + 10 * np.sin(np.arange(8760) * 2 * np.pi / (24 * 365)) + \
                      5 * np.sin(np.arange(8760) * 2 * np.pi / 24) + np.random.normal(0, 2, 8760),
        'humidity': np.clip(60 + 20 * np.sin(np.arange(8760) * 2 * np.pi / (24 * 365) + np.pi/4) + \
                           np.random.normal(0, 5, 8760), 0, 100),
        'pressure': 1013 + 10 * np.sin(np.arange(8760) * 2 * np.pi / (24 * 7)) + np.random.normal(0, 3, 8760),
        'wind_speed': np.abs(np.random.normal(8, 4, 8760)),
        'wind_direction': np.random.uniform(0, 360, 8760),
        'precipitation': np.random.exponential(0.5, 8760),
        'visibility': np.clip(np.random.normal(10, 2, 8760), 0, 20),
        'weather_condition': np.random.choice(['Clear', 'Cloudy', 'Rainy', 'Snowy', 'Foggy'], 8760),
        'station_id': np.random.choice(['STATION_001', 'STATION_002', 'STATION_003'], 8760)
    }
    return pd.DataFrame(data)


@pytest.fixture
def sales_data():
    """Create sales data for testing."""
    np.random.seed(456)
    
    # Simulate e-commerce sales data
    data = {
        'order_id': range(1, 5001),
        'customer_id': np.random.randint(1, 1000, 5000),
        'product_id': np.random.randint(1, 200, 5000),
        'order_date': pd.date_range('2023-01-01', periods=5000, freq='2H'),
        'quantity': np.random.randint(1, 10, 5000),
        'unit_price': np.random.lognormal(mean=3, sigma=1, size=5000),
        'total_amount': None,  # Will be calculated
        'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], 5000),
        'brand': np.random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE'], 5000),
        'discount_percent': np.random.uniform(0, 0.3, 5000),
        'shipping_cost': np.random.uniform(0, 20, 5000),
        'customer_segment': np.random.choice(['Premium', 'Regular', 'Budget'], 5000),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 5000),
        'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash'], 5000),
        'is_return': np.random.choice([True, False], 5000, p=[0.1, 0.9])
    }
    
    df = pd.DataFrame(data)
    df['total_amount'] = df['quantity'] * df['unit_price'] * (1 - df['discount_percent']) + df['shipping_cost']
    return df


@pytest.fixture
def output_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestDataProcessingWorkflow:
    """Test complete data processing workflows."""
    
    def test_financial_data_workflow(self, comprehensive_data, output_dir):
        """Test complete workflow with financial data."""
        print("\n=== Testing Financial Data Workflow ===")
        
        # Step 1: Write data to Parquet
        parquet_path = os.path.join(output_dir, "financial_data.parquet")
        result = write_parquet_handler(comprehensive_data.to_dict('records'), parquet_path)
        assert result.get('_meta', {}).get('success', False)
        print(f"✓ Wrote {comprehensive_data.shape[0]} rows to Parquet")
        
        # Step 2: Read back and verify
        read_result = read_parquet_handler(parquet_path)
        assert read_result.get('_meta', {}).get('success', False)
        data_content = json.loads(read_result['content'][0]['text'])
        assert data_content['num_rows'] == 1000
        print(f"✓ Read back {data_content['num_rows']} rows successfully")
        
        # Step 3: Get schema information
        schema_result = schema_handler(parquet_path)
        assert schema_result.get('_meta', {}).get('success', False)
        print("✓ Retrieved schema information")
        
        # Step 4: Get metadata
        metadata_result = metadata_handler(parquet_path)
        assert metadata_result.get('_meta', {}).get('success', False)
        print("✓ Retrieved metadata")
        
        # Step 5: Get statistics
        stats_result = statistics_handler(parquet_path, columns=['stock_price', 'volume', 'market_cap'])
        assert stats_result.get('_meta', {}).get('success', False)
        print("✓ Calculated statistics for numeric columns")
        
        # Step 6: Check data quality
        quality_result = check_quality_handler(parquet_path)
        assert quality_result.get('_meta', {}).get('success', False)
        print("✓ Performed data quality checks")
        
        # Step 7: Convert to CSV
        csv_path = os.path.join(output_dir, "financial_data.csv")
        csv_result = convert_format_handler(parquet_path, csv_path, "csv")
        assert csv_result.get('_meta', {}).get('success', False)
        print("✓ Converted to CSV format")
        
        # Step 8: Convert to JSON (limited)
        json_path = os.path.join(output_dir, "financial_data_sample.json")
        json_result = convert_format_handler(parquet_path, json_path, "json", limit=100)
        assert json_result.get('_meta', {}).get('success', False)
        print("✓ Converted sample to JSON format")
        
        print("✓ Complete financial data workflow successful")
    
    def test_weather_data_workflow(self, weather_data, output_dir):
        """Test complete workflow with weather data."""
        print("\n=== Testing Weather Data Workflow ===")
        
        # Step 1: Write weather data
        parquet_path = os.path.join(output_dir, "weather_data.parquet")
        result = write_parquet_handler(weather_data.to_dict('records'), parquet_path, compression="gzip")
        assert result.get('_meta', {}).get('success', False)
        print(f"✓ Wrote {weather_data.shape[0]} weather records with GZIP compression")
        
        # Step 2: Test compression efficiency
        compression_result = compression_handler(parquet_path)
        assert compression_result.get('_meta', {}).get('success', False)
        compression_data = json.loads(compression_result['content'][0]['text'])
        print(f"✓ Compression ratio: {compression_data.get('compression_ratio', 'N/A')}")
        
        # Step 3: Read with column selection
        read_result = read_parquet_handler(parquet_path, columns=['timestamp', 'temperature', 'humidity'])
        assert read_result.get('_meta', {}).get('success', False)
        print("✓ Read specific columns successfully")
        
        # Step 4: Read with row limit
        limited_result = read_parquet_handler(parquet_path, limit=168)  # One week of hourly data
        assert limited_result.get('_meta', {}).get('success', False)
        limited_data = json.loads(limited_result['content'][0]['text'])
        assert limited_data['num_rows'] == 168
        print(f"✓ Read limited data: {limited_data['num_rows']} rows")
        
        # Step 5: Statistical analysis
        stats_result = statistics_handler(parquet_path, columns=['temperature', 'humidity', 'pressure'])
        assert stats_result.get('_meta', {}).get('success', False)
        print("✓ Calculated weather statistics")
        
        print("✓ Complete weather data workflow successful")
    
    def test_sales_data_workflow(self, sales_data, output_dir):
        """Test complete workflow with sales data."""
        print("\n=== Testing Sales Data Workflow ===")
        
        # Step 1: Write sales data with different compression
        parquet_path = os.path.join(output_dir, "sales_data.parquet")
        result = write_parquet_handler(sales_data.to_dict('records'), parquet_path, compression="snappy")
        assert result.get('_meta', {}).get('success', False)
        print(f"✓ Wrote {sales_data.shape[0]} sales records with Snappy compression")
        
        # Step 2: Data quality analysis
        quality_result = check_quality_handler(parquet_path)
        assert quality_result.get('_meta', {}).get('success', False)
        quality_data = json.loads(quality_result['content'][0]['text'])
        print(f"✓ Data quality score: {quality_data.get('data_quality_score', 'N/A')}")
        
        # Step 3: Business metrics analysis
        stats_result = statistics_handler(parquet_path, columns=['total_amount', 'quantity', 'unit_price'])
        assert stats_result.get('_meta', {}).get('success', False)
        print("✓ Calculated business metrics")
        
        # Step 4: Export high-value orders to CSV
        csv_path = os.path.join(output_dir, "sales_data.csv")
        csv_result = convert_format_handler(parquet_path, csv_path, "csv", limit=1000)
        assert csv_result.get('_meta', {}).get('success', False)
        print("✓ Exported top orders to CSV")
        
        print("✓ Complete sales data workflow successful")


class TestPerformanceAndScalability:
    """Test performance and scalability scenarios."""
    
    def test_large_dataset_performance(self, output_dir):
        """Test performance with large dataset."""
        print("\n=== Testing Large Dataset Performance ===")
        
        # Create large dataset
        np.random.seed(789)
        large_data = pd.DataFrame({
            'id': range(100000),
            'value1': np.random.randn(100000),
            'value2': np.random.randn(100000),
            'value3': np.random.randn(100000),
            'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 100000),
            'timestamp': pd.date_range('2020-01-01', periods=100000, freq='min')
        })
        
        # Test write performance
        parquet_path = os.path.join(output_dir, "large_dataset.parquet")
        import time
        start_time = time.time()
        result = write_parquet_handler(large_data.to_dict('records'), parquet_path)
        write_time = time.time() - start_time
        assert result.get('_meta', {}).get('success', False)
        print(f"✓ Wrote 100K rows in {write_time:.2f} seconds")
        
        # Test read performance with limit
        start_time = time.time()
        read_result = read_parquet_handler(parquet_path, limit=10000)
        read_time = time.time() - start_time
        assert read_result.get('_meta', {}).get('success', False)
        print(f"✓ Read 10K rows in {read_time:.2f} seconds")
        
        # Test column selection performance
        start_time = time.time()
        column_result = read_parquet_handler(parquet_path, columns=['id', 'value1', 'category'])
        column_time = time.time() - start_time
        assert column_result.get('_meta', {}).get('success', False)
        print(f"✓ Read 3 columns in {column_time:.2f} seconds")
        
        print("✓ Large dataset performance test successful")
    
    def test_multiple_compression_formats(self, comprehensive_data, output_dir):
        """Test different compression formats."""
        print("\n=== Testing Multiple Compression Formats ===")
        
        compressions = ['snappy', 'gzip', 'brotli', 'lz4']
        results = {}
        
        for compression in compressions:
            parquet_path = os.path.join(output_dir, f"data_{compression}.parquet")
            
            # Write with compression
            result = write_parquet_handler(comprehensive_data.to_dict('records'), parquet_path, compression=compression)
            assert result.get('_meta', {}).get('success', False)
            
            # Get compression stats
            stats_result = compression_handler(parquet_path)
            assert stats_result.get('_meta', {}).get('success', False)
            stats_data = json.loads(stats_result['content'][0]['text'])
            
            results[compression] = {
                'file_size': stats_data.get('file_size_bytes', 0),
                'compression_ratio': stats_data.get('compression_ratio', 1.0)
            }
            
            print(f"✓ {compression}: {results[compression]['file_size']} bytes, ratio: {results[compression]['compression_ratio']:.2f}")
        
        # Find most efficient compression
        best_compression = min(results.keys(), key=lambda x: results[x]['file_size'])
        print(f"✓ Most efficient compression: {best_compression}")
        
        print("✓ Multiple compression formats test successful")


class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases."""
    
    def test_invalid_file_operations(self):
        """Test operations with invalid files."""
        print("\n=== Testing Invalid File Operations ===")
        
        # Test reading non-existent file
        result = read_parquet_handler("/nonexistent/file.parquet")
        assert result.get('isError', False)
        print("✓ Properly handled non-existent file")
        
        # Test schema of non-existent file
        result = schema_handler("/nonexistent/file.parquet")
        assert result.get('isError', False)
        print("✓ Properly handled schema request for non-existent file")
        
        # Test statistics of non-existent file
        result = statistics_handler("/nonexistent/file.parquet")
        assert result.get('isError', False)
        print("✓ Properly handled statistics request for non-existent file")
        
        print("✓ Invalid file operations test successful")
    
    def test_empty_and_minimal_data(self, output_dir):
        """Test with empty and minimal data."""
        print("\n=== Testing Empty and Minimal Data ===")
        
        # Test with single row
        minimal_data = pd.DataFrame({
            'id': [1],
            'name': ['Test'],
            'value': [42.0]
        })
        
        parquet_path = os.path.join(output_dir, "minimal_data.parquet")
        result = write_parquet_handler(minimal_data.to_dict('records'), parquet_path)
        assert result.get('_meta', {}).get('success', False)
        print("✓ Handled single-row data")
        
        # Test reading it back
        read_result = read_parquet_handler(parquet_path)
        assert read_result.get('_meta', {}).get('success', False)
        data_content = json.loads(read_result['content'][0]['text'])
        assert data_content['num_rows'] == 1
        print("✓ Successfully read single-row data")
        
        print("✓ Empty and minimal data test successful")
    
    def test_special_data_types(self, output_dir):
        """Test with special data types."""
        print("\n=== Testing Special Data Types ===")
        
        # Create data with various special types
        special_data = pd.DataFrame({
            'integers': [1, 2, 3, 4, 5],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5],
            'strings': ['hello', 'world', 'test', 'data', 'parquet'],
            'booleans': [True, False, True, False, True],
            'dates': pd.date_range('2024-01-01', periods=5),
            'nulls': [1, None, 3, None, 5],
            'large_numbers': [1e10, 2e10, 3e10, 4e10, 5e10],
            'unicode': ['café', '数据', '🚀', 'test', 'normal']
        })
        
        parquet_path = os.path.join(output_dir, "special_types.parquet")
        result = write_parquet_handler(special_data.to_dict('records'), parquet_path)
        assert result.get('_meta', {}).get('success', False)
        print("✓ Handled special data types")
        
        # Test statistics with nulls
        stats_result = statistics_handler(parquet_path)
        assert stats_result.get('_meta', {}).get('success', False)
        print("✓ Calculated statistics with null values")
        
        # Test data quality with nulls
        quality_result = check_quality_handler(parquet_path)
        assert quality_result.get('_meta', {}).get('success', False)
        print("✓ Performed quality checks with null values")
        
        print("✓ Special data types test successful")


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""
    
    def test_data_pipeline_simulation(self, output_dir):
        """Simulate a real data pipeline."""
        print("\n=== Testing Data Pipeline Simulation ===")
        
        # Stage 1: Raw data ingestion
        raw_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=1000, freq='H'),
            'sensor_id': np.random.choice(['S001', 'S002', 'S003'], 1000),
            'temperature': np.random.normal(25, 5, 1000),
            'humidity': np.random.normal(60, 10, 1000),
            'pressure': np.random.normal(1013, 10, 1000),
            'status': np.random.choice(['OK', 'WARNING', 'ERROR'], 1000, p=[0.8, 0.15, 0.05])
        })
        
        raw_path = os.path.join(output_dir, "raw_sensor_data.parquet")
        result = write_parquet_handler(raw_data.to_dict('records'), raw_path)
        assert result.get('_meta', {}).get('success', False)
        print("✓ Stage 1: Raw data ingested")
        
        # Stage 2: Data quality assessment
        quality_result = check_quality_handler(raw_path)
        assert quality_result.get('_meta', {}).get('success', False)
        print("✓ Stage 2: Data quality assessed")
        
        # Stage 3: Statistical analysis
        stats_result = statistics_handler(raw_path, columns=['temperature', 'humidity', 'pressure'])
        assert stats_result.get('_meta', {}).get('success', False)
        print("✓ Stage 3: Statistical analysis completed")
        
        # Stage 4: Export for reporting
        csv_path = os.path.join(output_dir, "sensor_report.csv")
        csv_result = convert_format_handler(raw_path, csv_path, "csv")
        assert csv_result.get('_meta', {}).get('success', False)
        print("✓ Stage 4: Data exported for reporting")
        
        # Stage 5: Archive with compression
        archive_path = os.path.join(output_dir, "sensor_archive.parquet")
        archive_result = write_parquet_handler(raw_data.to_dict('records'), archive_path, compression="brotli")
        assert archive_result.get('_meta', {}).get('success', False)
        print("✓ Stage 5: Data archived with compression")
        
        print("✓ Data pipeline simulation successful")
    
    def test_analytics_workflow(self, sales_data, output_dir):
        """Test analytics workflow."""
        print("\n=== Testing Analytics Workflow ===")
        
        # Prepare analytics data
        parquet_path = os.path.join(output_dir, "analytics_data.parquet")
        result = write_parquet_handler(sales_data.to_dict('records'), parquet_path)
        assert result.get('_meta', {}).get('success', False)
        print("✓ Analytics data prepared")
        
        # Analyze key metrics
        metrics_result = statistics_handler(parquet_path, columns=['total_amount', 'quantity', 'discount_percent'])
        assert metrics_result.get('_meta', {}).get('success', False)
        print("✓ Key metrics analyzed")
        
        # Generate sample for detailed analysis
        sample_json_path = os.path.join(output_dir, "analytics_sample.json")
        sample_result = convert_format_handler(parquet_path, sample_json_path, "json", limit=500)
        assert sample_result.get('_meta', {}).get('success', False)
        print("✓ Sample generated for detailed analysis")
        
        # Create summary report
        summary_csv_path = os.path.join(output_dir, "analytics_summary.csv")
        summary_result = convert_format_handler(parquet_path, summary_csv_path, "csv", limit=1000)
        assert summary_result.get('_meta', {}).get('success', False)
        print("✓ Summary report created")
        
        print("✓ Analytics workflow successful")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
