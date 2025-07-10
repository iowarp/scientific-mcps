#!/usr/bin/env python3
"""
Comprehensive testing of all Pandas MCP capabilities with all data formats.
"""
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pandasmcp.capabilities.data_io import load_data_file, save_data_file
from pandasmcp.capabilities.statistics import get_statistical_summary, get_correlation_analysis
from pandasmcp.capabilities.data_cleaning import handle_missing_data, clean_data
from pandasmcp.capabilities.data_profiling import profile_data
from pandasmcp.capabilities.transformations import groupby_operations, merge_datasets, create_pivot_table
from pandasmcp.capabilities.time_series import time_series_operations
from pandasmcp.capabilities.filtering import filter_data, sample_data
from pandasmcp.capabilities.memory_optimization import optimize_memory_usage
from pandasmcp.capabilities.validation import validate_data, hypothesis_testing

def test_data_io_capabilities():
    """Test data I/O capabilities with all formats."""
    print("\n" + "="*60)
    print("TESTING DATA I/O CAPABILITIES")
    print("="*60)
    
    results = {}
    data_dir = Path("data")
    
    # Get all available files
    file_patterns = {
        'csv': '*.csv',
        'json': '*.json', 
        'parquet': '*.parquet',
        'excel': '*.xlsx',
        'hdf5': '*.h5'
    }
    
    for format_name, pattern in file_patterns.items():
        files = list(data_dir.glob(pattern))
        if not files:
            continue
            
        print(f"\nTesting {format_name.upper()} format:")
        results[format_name] = {}
        
        for file_path in files[:2]:  # Test first 2 files of each format
            print(f"  Testing {file_path.name}...")
            
            try:
                # Test loading
                load_result = load_data_file(str(file_path))
                if load_result.get('success'):
                    print(f"    ✓ Load: {load_result['total_rows']} rows, {len(load_result['info']['columns'])} columns")
                    results[format_name][file_path.stem] = {'load': 'success'}
                    
                    # Test saving (only for CSV to avoid format conversion issues)
                    if format_name == 'csv':
                        save_path = f"data/test_save_{file_path.stem}.csv"
                        save_result = save_data_file(load_result['data'][:10], save_path)  # Save first 10 rows
                        if save_result.get('success'):
                            print(f"    ✓ Save: {save_path}")
                            results[format_name][file_path.stem]['save'] = 'success'
                            # Clean up
                            if os.path.exists(save_path):
                                os.remove(save_path)
                        else:
                            print(f"    ✗ Save failed: {save_result.get('error')}")
                            results[format_name][file_path.stem]['save'] = 'failed'
                else:
                    print(f"    ✗ Load failed: {load_result.get('error')}")
                    results[format_name][file_path.stem] = {'load': 'failed'}
                    
            except Exception as e:
                print(f"    ✗ Error: {e}")
                results[format_name][file_path.stem] = {'error': str(e)}
    
    return results

def test_statistical_capabilities():
    """Test statistical analysis capabilities."""
    print("\n" + "="*60)
    print("TESTING STATISTICAL CAPABILITIES")
    print("="*60)
    
    results = {}
    test_files = [
        "data/employees.csv",
        "data/sales.csv", 
        "data/weather.csv",
        "data/inventory.csv"
    ]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            continue
            
        dataset_name = Path(file_path).stem
        print(f"\nTesting statistical analysis on {dataset_name}:")
        results[dataset_name] = {}
        
        try:
            # Statistical summary
            stats_result = get_statistical_summary(file_path)
            if stats_result.get('success'):
                print(f"  ✓ Statistical summary: {len(stats_result['basic_statistics'])} numeric columns")
                results[dataset_name]['statistical_summary'] = 'success'
            else:
                print(f"  ✗ Statistical summary failed: {stats_result.get('error')}")
                results[dataset_name]['statistical_summary'] = 'failed'
                
            # Correlation analysis
            corr_result = get_correlation_analysis(file_path, method='pearson')
            if corr_result.get('success'):
                print(f"  ✓ Correlation analysis: {len(corr_result['correlation_matrix'])} columns")
                results[dataset_name]['correlation_analysis'] = 'success'
            else:
                print(f"  ✗ Correlation analysis failed: {corr_result.get('error')}")
                results[dataset_name]['correlation_analysis'] = 'failed'
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[dataset_name]['error'] = str(e)
    
    return results

def test_data_cleaning_capabilities():
    """Test data cleaning capabilities."""
    print("\n" + "="*60)
    print("TESTING DATA CLEANING CAPABILITIES")
    print("="*60)
    
    results = {}
    test_files = [
        "data/employees.csv",
        "data/sales.csv"
    ]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            continue
            
        dataset_name = Path(file_path).stem
        print(f"\nTesting data cleaning on {dataset_name}:")
        results[dataset_name] = {}
        
        try:
            # Missing data handling
            missing_result = handle_missing_data(file_path, strategy='detect')
            if missing_result.get('success'):
                missing_info = missing_result.get('missing_data_info', {})
                total_missing = missing_info.get('total_missing_values', 0)
                print(f"  ✓ Missing data detection: {total_missing} missing values found")
                results[dataset_name]['missing_data'] = 'success'
            else:
                print(f"  ✗ Missing data detection failed: {missing_result.get('error')}")
                results[dataset_name]['missing_data'] = 'failed'
                
            # Data cleaning
            clean_result = clean_data(file_path, remove_duplicates=True, detect_outliers=True)
            if clean_result.get('success'):
                clean_info = clean_result.get('cleaning_summary', {})
                duplicates = clean_info.get('duplicates_removed', 0)
                outliers = clean_info.get('outliers_detected', 0)
                print(f"  ✓ Data cleaning: {duplicates} duplicates, {outliers} outliers")
                results[dataset_name]['data_cleaning'] = 'success'
            else:
                print(f"  ✗ Data cleaning failed: {clean_result.get('error')}")
                results[dataset_name]['data_cleaning'] = 'failed'
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[dataset_name]['error'] = str(e)
    
    return results

def test_transformation_capabilities():
    """Test data transformation capabilities."""
    print("\n" + "="*60)
    print("TESTING TRANSFORMATION CAPABILITIES")
    print("="*60)
    
    results = {}
    
    # Test groupby operations
    print("\nTesting groupby operations:")
    try:
        groupby_result = groupby_operations(
            "data/employees.csv",
            group_by=['department'],
            operations={'salary': 'mean', 'age': 'median', 'employee_id': 'count'}
        )
        if groupby_result.get('success'):
            group_info = groupby_result.get('group_info', {})
            print(f"  ✓ Groupby: {group_info.get('number_of_groups', 0)} groups created")
            results['groupby'] = 'success'
        else:
            print(f"  ✗ Groupby failed: {groupby_result.get('error')}")
            results['groupby'] = 'failed'
    except Exception as e:
        print(f"  ✗ Groupby error: {e}")
        results['groupby'] = 'error'
    
    # Test dataset merging
    print("\nTesting dataset merging:")
    try:
        merge_result = merge_datasets(
            "data/employees.csv",
            "data/sales.csv",
            join_type='inner',
            on='employee_id'
        )
        if merge_result.get('success'):
            merge_stats = merge_result.get('merge_stats', {})
            print(f"  ✓ Merge: {merge_stats.get('merged_shape', [0,0])[0]} rows merged")
            results['merge'] = 'success'
        else:
            print(f"  ✗ Merge failed: {merge_result.get('error')}")
            results['merge'] = 'failed'
    except Exception as e:
        print(f"  ✗ Merge error: {e}")
        results['merge'] = 'error'
    
    # Test pivot table
    print("\nTesting pivot table:")
    try:
        pivot_result = create_pivot_table(
            "data/sales.csv",
            index=['region'],
            columns=['product'],
            values=['total_amount'],
            aggfunc='sum'
        )
        if pivot_result.get('success'):
            pivot_info = pivot_result.get('pivot_info', {})
            print(f"  ✓ Pivot: {pivot_info.get('pivot_shape', [0,0])[0]} rows in pivot")
            results['pivot'] = 'success'
        else:
            print(f"  ✗ Pivot failed: {pivot_result.get('error')}")
            results['pivot'] = 'failed'
    except Exception as e:
        print(f"  ✗ Pivot error: {e}")
        results['pivot'] = 'error'
    
    return results

def test_time_series_capabilities():
    """Test time series capabilities."""
    print("\n" + "="*60)
    print("TESTING TIME SERIES CAPABILITIES")
    print("="*60)
    
    results = {}
    weather_file = "data/weather.csv"
    
    if not os.path.exists(weather_file):
        print("  ✗ Weather data not found, skipping time series tests")
        return results
    
    print(f"\nTesting time series operations on weather data:")
    
    try:
        # Rolling window operations
        rolling_result = time_series_operations(
            weather_file,
            date_column='date',
            operation='rolling',
            window_size=7
        )
        if rolling_result.get('success'):
            print(f"  ✓ Rolling window: 7-day moving averages calculated")
            results['rolling'] = 'success'
        else:
            print(f"  ✗ Rolling window failed: {rolling_result.get('error')}")
            results['rolling'] = 'failed'
            
        # Resampling operations
        resample_result = time_series_operations(
            weather_file,
            date_column='date',
            operation='resample',
            frequency='W'
        )
        if resample_result.get('success'):
            print(f"  ✓ Resampling: Weekly aggregation completed")
            results['resample'] = 'success'
        else:
            print(f"  ✗ Resampling failed: {resample_result.get('error')}")
            results['resample'] = 'failed'
            
    except Exception as e:
        print(f"  ✗ Time series error: {e}")
        results['error'] = str(e)
    
    return results

def test_filtering_capabilities():
    """Test data filtering capabilities."""
    print("\n" + "="*60)
    print("TESTING FILTERING CAPABILITIES")
    print("="*60)
    
    results = {}
    test_files = [
        ("data/employees.csv", {'salary': {'min_value': 30000}}),
        ("data/sales.csv", {'total_amount': {'min_value': 100}})
    ]
    
    for file_path, filter_conditions in test_files:
        if not os.path.exists(file_path):
            continue
            
        dataset_name = Path(file_path).stem
        print(f"\nTesting filtering on {dataset_name}:")
        
        try:
            # Data filtering
            filter_result = filter_data(file_path, filter_conditions)
            if filter_result.get('success'):
                filter_info = filter_result.get('filter_stats', {})
                final_shape = filter_info.get('final_shape', [0, 0])
                print(f"  ✓ Filtering: {final_shape[0]} rows after filtering")
                results[f'{dataset_name}_filter'] = 'success'
            else:
                print(f"  ✗ Filtering failed: {filter_result.get('error')}")
                results[f'{dataset_name}_filter'] = 'failed'
                
            # Data sampling
            sample_result = sample_data(file_path, sample_size=50, method='random')
            if sample_result.get('success'):
                sample_info = sample_result.get('sample_stats', {})
                sampled_rows = sample_info.get('sample_size', 0)
                print(f"  ✓ Sampling: {sampled_rows} rows sampled")
                results[f'{dataset_name}_sample'] = 'success'
            else:
                print(f"  ✗ Sampling failed: {sample_result.get('error')}")
                results[f'{dataset_name}_sample'] = 'failed'
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[f'{dataset_name}_error'] = str(e)
    
    return results

def test_memory_optimization():
    """Test memory optimization capabilities."""
    print("\n" + "="*60)
    print("TESTING MEMORY OPTIMIZATION")
    print("="*60)
    
    results = {}
    test_files = ["data/employees.csv", "data/sales.csv"]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            continue
            
        dataset_name = Path(file_path).stem
        print(f"\nTesting memory optimization on {dataset_name}:")
        
        try:
            memory_result = optimize_memory_usage(file_path, optimize_dtypes=True)
            if memory_result.get('success'):
                memory_info = memory_result.get('memory_info', {})
                reduction = memory_info.get('reduction_percentage', 0)
                print(f"  ✓ Memory optimization: {reduction:.1f}% reduction")
                results[dataset_name] = 'success'
            else:
                print(f"  ✗ Memory optimization failed: {memory_result.get('error')}")
                results[dataset_name] = 'failed'
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[dataset_name] = str(e)
    
    return results

def test_validation_capabilities():
    """Test data validation capabilities."""
    print("\n" + "="*60)
    print("TESTING VALIDATION CAPABILITIES")
    print("="*60)
    
    results = {}
    
    # Test data validation
    print("\nTesting data validation on employees:")
    try:
        validation_rules = {
            'age': {'min_value': 18, 'max_value': 70},
            'salary': {'min_value': 20000, 'max_value': 200000}
        }
        
        validation_result = validate_data("data/employees.csv", validation_rules)
        if validation_result.get('success'):
            validation_summary = validation_result.get('validation_summary', {})
            violations = validation_summary.get('total_violations', 0)
            print(f"  ✓ Data validation: {violations} violations found")
            results['validation'] = 'success'
        else:
            print(f"  ✗ Data validation failed: {validation_result.get('error')}")
            results['validation'] = 'failed'
            
    except Exception as e:
        print(f"  ✗ Validation error: {e}")
        results['validation'] = str(e)
    
    # Test hypothesis testing
    print("\nTesting hypothesis testing:")
    try:
        hypothesis_result = hypothesis_testing(
            "data/employees.csv",
            test_type='ttest_ind',
            column1='salary',
            column2='age'
        )
        if hypothesis_result.get('success'):
            test_results = hypothesis_result.get('test_results', {})
            p_value = test_results.get('p_value', 0)
            print(f"  ✓ Hypothesis testing: p-value = {p_value:.4f}")
            results['hypothesis'] = 'success'
        else:
            print(f"  ✗ Hypothesis testing failed: {hypothesis_result.get('error')}")
            results['hypothesis'] = 'failed'
            
    except Exception as e:
        print(f"  ✗ Hypothesis testing error: {e}")
        results['hypothesis'] = str(e)
    
    return results

def test_data_profiling():
    """Test data profiling capabilities."""
    print("\n" + "="*60)
    print("TESTING DATA PROFILING")
    print("="*60)
    
    results = {}
    test_files = ["data/employees.csv", "data/sales.csv", "data/weather.csv"]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            continue
            
        dataset_name = Path(file_path).stem
        print(f"\nTesting data profiling on {dataset_name}:")
        
        try:
            profile_result = profile_data(file_path, include_correlations=True)
            if profile_result.get('success'):
                basic_info = profile_result.get('basic_info', {})
                shape = basic_info.get('shape', [0, 0])
                print(f"  ✓ Data profiling: {shape[0]} rows, {shape[1]} columns profiled")
                results[dataset_name] = 'success'
            else:
                print(f"  ✗ Data profiling failed: {profile_result.get('error')}")
                results[dataset_name] = 'failed'
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[dataset_name] = str(e)
    
    return results

def is_success(status):
    """Check if a status indicates success."""
    if status == 'success':
        return True
    if isinstance(status, dict):
        # For dictionaries, check recursively
        for key, value in status.items():
            if isinstance(value, dict):
                # Check nested dictionaries
                if not all(v == 'success' for v in value.values()):
                    return False
            elif value != 'success':
                return False
        return True
    return False

def generate_test_report(all_results):
    """Generate comprehensive test report."""
    print("\n" + "="*80)
    print("COMPREHENSIVE TESTING REPORT")
    print("="*80)
    
    total_tests = 0
    passed_tests = 0
    
    for capability, results in all_results.items():
        print(f"\n{capability.upper().replace('_', ' ')} Results:")
        print("-" * 40)
        
        if isinstance(results, dict):
            for test_name, status in results.items():
                total_tests += 1
                if is_success(status):
                    passed_tests += 1
                    print(f"  ✓ {test_name}: {status}")
                else:
                    print(f"  ✗ {test_name}: {status}")
        else:
            total_tests += 1
            if is_success(results):
                passed_tests += 1
                print(f"  ✓ {capability}: {results}")
            else:
                print(f"  ✗ {capability}: {results}")
    
    # Overall summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY")
    print("="*80)
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed Tests: {passed_tests}")
    print(f"Failed Tests: {total_tests - passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🎉 EXCELLENT: All major functionalities working correctly!")
    elif success_rate >= 75:
        print("\n✅ GOOD: Most functionalities working, minor issues detected")
    elif success_rate >= 50:
        print("\n⚠️ PARTIAL: Some functionalities working, needs attention")
    else:
        print("\n❌ POOR: Major issues detected, requires investigation")
    
    return success_rate

def main():
    """Main testing function."""
    print("Pandas MCP Server - Comprehensive Capability Testing")
    print("="*70)
    
    # Ensure data directory exists
    if not os.path.exists("data"):
        print("Data directory not found. Creating sample data first...")
        from create_sample_data import main as create_data
        create_data()
    
    # Run all capability tests
    all_results = {}
    
    print("Starting comprehensive capability testing...")
    
    # Test all capabilities
    all_results['data_io'] = test_data_io_capabilities()
    all_results['statistical'] = test_statistical_capabilities()
    all_results['data_cleaning'] = test_data_cleaning_capabilities()
    all_results['transformations'] = test_transformation_capabilities()
    all_results['time_series'] = test_time_series_capabilities()
    all_results['filtering'] = test_filtering_capabilities()
    all_results['memory_optimization'] = test_memory_optimization()
    all_results['validation'] = test_validation_capabilities()
    all_results['data_profiling'] = test_data_profiling()
    
    # Generate comprehensive report
    success_rate = generate_test_report(all_results)
    
    return all_results, success_rate

if __name__ == "__main__":
    results, rate = main()
