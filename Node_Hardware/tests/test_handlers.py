"""
Unit tests for Node Hardware MCP handlers.
Tests the MCP protocol compliance and handler functionality.
"""
import json
import pytest
import sys
import os

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from node_hardware import mcp_handlers


def test_cpu_info_handler():
    """Test CPU info handler returns proper MCP structure."""
    print("\n=== Testing CPU Info Handler ===")
    result = mcp_handlers.cpu_info_handler()
    print("CPU Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'cpu_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'logical_cores' in data
    assert 'physical_cores' in data
    assert 'architecture' in data
    assert isinstance(data['logical_cores'], int)
    print("✓ CPU Info Handler test passed")


def test_memory_info_handler():
    """Test memory info handler returns proper MCP structure."""
    print("\n=== Testing Memory Info Handler ===")
    result = mcp_handlers.memory_info_handler()
    print("Memory Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'memory_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'virtual_memory' in data
    assert 'swap_memory' in data
    print("✓ Memory Info Handler test passed")


def test_disk_info_handler():
    """Test disk info handler returns proper MCP structure."""
    print("\n=== Testing Disk Info Handler ===")
    result = mcp_handlers.disk_info_handler()
    print("Disk Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'disk_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'partitions' in data
    assert 'total_partitions' in data
    assert isinstance(data['total_partitions'], int)
    print("✓ Disk Info Handler test passed")


def test_network_info_handler():
    """Test network info handler returns proper MCP structure."""
    print("\n=== Testing Network Info Handler ===")
    result = mcp_handlers.network_info_handler()
    print("Network Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'network_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'interfaces' in data
    assert 'total_interfaces' in data
    assert isinstance(data['total_interfaces'], int)
    print("✓ Network Info Handler test passed")


def test_system_info_handler():
    """Test system info handler returns proper MCP structure."""
    print("\n=== Testing System Info Handler ===")
    result = mcp_handlers.system_info_handler()
    print("System Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'system_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'os_info' in data
    assert 'hostname' in data
    assert 'uptime' in data
    print("✓ System Info Handler test passed")


def test_process_info_handler():
    """Test process info handler returns proper MCP structure."""
    print("\n=== Testing Process Info Handler ===")
    result = mcp_handlers.process_info_handler(limit=5)
    print("Process Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'process_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'processes' in data
    assert 'total_processes' in data
    assert isinstance(data['total_processes'], int)
    assert len(data['processes']) <= 5
    print("✓ Process Info Handler test passed")


def test_hardware_summary_handler():
    """Test hardware summary handler returns proper MCP structure."""
    print("\n=== Testing Hardware Summary Handler ===")
    result = mcp_handlers.hardware_summary_handler()
    print("Hardware Summary Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'hardware_summary'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'summary' in data
    assert 'detailed' in data
    print("✓ Hardware Summary Handler test passed")


def test_performance_monitor_handler():
    """Test performance monitor handler returns proper MCP structure."""
    print("\n=== Testing Performance Monitor Handler ===")
    result = mcp_handlers.performance_monitor_handler(duration=1)
    print("Performance Monitor Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'performance_monitor'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'monitoring_duration' in data
    assert 'cpu' in data
    assert 'memory' in data
    print("✓ Performance Monitor Handler test passed")


def test_gpu_info_handler():
    """Test GPU info handler returns proper MCP structure."""
    print("\n=== Testing GPU Info Handler ===")
    result = mcp_handlers.gpu_info_handler()
    print("GPU Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'gpu_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'gpus' in data
    assert 'nvidia_available' in data
    assert 'amd_available' in data
    print("✓ GPU Info Handler test passed")


def test_sensor_info_handler():
    """Test sensor info handler returns proper MCP structure."""
    print("\n=== Testing Sensor Info Handler ===")
    result = mcp_handlers.sensor_info_handler()
    print("Sensor Info Result:", result)
    
    # Should contain MCP compliant structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'sensor_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'temperatures' in data
    assert 'sensors_available' in data
    print("✓ Sensor Info Handler test passed")


def test_error_handling():
    """Test error handling in handlers."""
    print("\n=== Testing Error Handling ===")
    
    # Test with edge case limit for process info
    result = mcp_handlers.process_info_handler(limit=0)
    
    # Should still return a valid MCP structure
    assert 'content' in result
    assert '_meta' in result
    assert result['_meta']['tool'] == 'process_info'
    assert len(result['content']) > 0
    
    # Parse the actual data
    data = json.loads(result['content'][0]['text'])
    assert 'processes' in data
    assert 'total_processes' in data
    print("✓ Error Handling test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
