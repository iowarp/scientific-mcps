"""
Unit tests for Node Hardware MCP handlers.
Tests the MCP protocol compliance and handler functionality.
"""
import json
import pytest
import sys
import os

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'node_hardware'))

import mcp_handlers


def test_get_cpu_info_handler():
    """Test CPU info handler returns proper structure."""
    print("\n=== Testing CPU Info Handler ===")
    result = mcp_handlers.get_cpu_info_handler()
    print("CPU Info Result:", result)
    
    # Should contain basic CPU information
    assert 'logical_cores' in result
    assert 'physical_cores' in result
    assert 'architecture' in result
    assert isinstance(result['logical_cores'], int)
    print("✅ CPU info handler test passed")


def test_get_memory_info_handler():
    """Test memory info handler returns proper structure."""
    print("\n=== Testing Memory Info Handler ===")
    result = mcp_handlers.get_memory_info_handler()
    print("Memory Info Result:", result)
    
    # Should contain memory information
    assert 'virtual_memory' in result
    assert 'swap_memory' in result
    assert 'total' in result['virtual_memory']
    assert 'available' in result['virtual_memory']
    print("✅ Memory info handler test passed")


def test_get_disk_info_handler():
    """Test disk info handler returns proper structure."""
    print("\n=== Testing Disk Info Handler ===")
    result = mcp_handlers.get_disk_info_handler()
    print("Disk Info Result:", result)
    
    # Should contain disk information
    assert 'partitions' in result
    assert 'total_partitions' in result
    assert 'summary' in result
    assert isinstance(result['partitions'], list)
    print("✅ Disk info handler test passed")


def test_get_network_info_handler():
    """Test network info handler returns proper structure."""
    print("\n=== Testing Network Info Handler ===")
    result = mcp_handlers.get_network_info_handler()
    print("Network Info Result:", result)
    
    # Should contain network information
    assert 'interfaces' in result
    assert 'total_interfaces' in result
    assert 'io_statistics' in result
    assert isinstance(result['interfaces'], list)
    print("✅ Network info handler test passed")


def test_get_system_info_handler():
    """Test system info handler returns proper structure."""
    print("\n=== Testing System Info Handler ===")
    result = mcp_handlers.get_system_info_handler()
    print("System Info Result:", result)
    
    # Should contain system information
    assert 'os_info' in result
    assert 'hostname' in result
    assert 'uptime' in result
    assert 'system' in result['os_info']
    print("✅ System info handler test passed")


def test_get_process_info_handler():
    """Test process info handler returns proper structure."""
    print("\n=== Testing Process Info Handler ===")
    result = mcp_handlers.get_process_info_handler(limit=5)
    print("Process Info Result:", result)
    
    # Should contain process information
    assert 'processes' in result
    assert 'total_processes' in result
    assert 'statistics' in result
    assert isinstance(result['processes'], list)
    assert len(result['processes']) <= 5
    print("✅ Process info handler test passed")


def test_get_hardware_summary_handler():
    """Test hardware summary handler returns proper structure."""
    print("\n=== Testing Hardware Summary Handler ===")
    result = mcp_handlers.get_hardware_summary_handler()
    print("Hardware Summary Result:", result)
    
    # Should contain comprehensive hardware summary
    assert 'summary' in result
    assert 'detailed' in result
    assert 'cpu' in result['summary']
    assert 'memory' in result['summary']
    assert 'disk' in result['summary']
    assert 'network' in result['summary']
    assert 'system' in result['summary']
    print("✅ Hardware summary handler test passed")


def test_monitor_performance_handler():
    """Test performance monitoring handler returns proper structure."""
    print("\n=== Testing Performance Monitor Handler ===")
    result = mcp_handlers.monitor_performance_handler(duration=1)
    print("Performance Monitor Result:", result)
    
    # Should contain performance metrics
    assert 'monitoring_duration' in result
    assert 'cpu' in result
    assert 'memory' in result
    assert 'disk_io' in result
    assert 'network_io' in result
    print("✅ Performance monitor handler test passed")


def test_get_gpu_info_handler():
    """Test GPU info handler returns proper structure."""
    print("\n=== Testing GPU Info Handler ===")
    result = mcp_handlers.get_gpu_info_handler()
    print("GPU Info Result:", result)
    
    # Should contain GPU information structure (may be empty if no GPU)
    assert 'gpus' in result
    assert 'nvidia_available' in result
    assert 'amd_available' in result
    assert 'intel_available' in result
    assert isinstance(result['gpus'], list)
    print("✅ GPU info handler test passed")


def test_get_sensor_info_handler():
    """Test sensor info handler returns proper structure."""
    print("\n=== Testing Sensor Info Handler ===")
    result = mcp_handlers.get_sensor_info_handler()
    print("Sensor Info Result:", result)
    
    # Should contain sensor information structure
    assert 'temperatures' in result
    assert 'fans' in result
    assert 'battery' in result
    assert 'sensors_available' in result
    assert isinstance(result['temperatures'], dict)
    print("✅ Sensor info handler test passed")


def test_error_handling():
    """Test error handling in handlers."""
    print("\n=== Testing Error Handling ===")
    
    # Test with invalid limit for process info
    result = mcp_handlers.get_process_info_handler(limit=-1)
    
    # Should still return a valid structure, possibly with error
    assert 'processes' in result
    assert 'total_processes' in result
    print("✅ Error handling test passed")


if __name__ == "__main__":
    print("Running Node Hardware MCP Handler Tests")
    print("=" * 60)
    
    test_get_cpu_info_handler()
    test_get_memory_info_handler()
    test_get_disk_info_handler()
    test_get_network_info_handler()
    test_get_system_info_handler()
    test_get_process_info_handler()
    test_get_hardware_summary_handler()
    test_monitor_performance_handler()
    test_get_gpu_info_handler()
    test_get_sensor_info_handler()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
