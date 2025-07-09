"""
Unit tests for Node Hardware capabilities.
Tests the individual capability modules.
"""
import pytest
import sys
import os

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'node_hardware'))

from capabilities.cpu_info import get_cpu_info
from capabilities.memory_info import get_memory_info
from capabilities.disk_info import get_disk_info
from capabilities.network_info import get_network_info
from capabilities.system_info import get_system_info
from capabilities.process_info import get_process_info
from capabilities.hardware_summary import get_hardware_summary
from capabilities.performance_monitor import monitor_performance
from capabilities.gpu_info import get_gpu_info
from capabilities.sensor_info import get_sensor_info


def test_cpu_info():
    """Test CPU information retrieval."""
    print("\n=== Testing CPU Info ===")
    result = get_cpu_info()
    print("CPU Info:", result)
    
    assert 'logical_cores' in result
    assert 'physical_cores' in result
    assert 'architecture' in result
    assert isinstance(result['logical_cores'], int)
    assert result['logical_cores'] > 0
    print("✅ CPU info test passed")


def test_memory_info():
    """Test memory information retrieval."""
    print("\n=== Testing Memory Info ===")
    result = get_memory_info()
    print("Memory Info:", result)
    
    assert 'virtual_memory' in result
    assert 'swap_memory' in result
    
    vm = result['virtual_memory']
    assert 'total' in vm
    assert 'available' in vm
    assert 'used' in vm
    assert 'percent' in vm
    assert vm['total'] > 0
    print("✅ Memory info test passed")


def test_disk_info():
    """Test disk information retrieval."""
    print("\n=== Testing Disk Info ===")
    result = get_disk_info()
    print("Disk Info:", result)
    
    assert 'partitions' in result
    assert 'total_partitions' in result
    assert 'summary' in result
    assert isinstance(result['partitions'], list)
    assert result['total_partitions'] >= 0
    print("✅ Disk info test passed")


def test_network_info():
    """Test network information retrieval."""
    print("\n=== Testing Network Info ===")
    result = get_network_info()
    print("Network Info:", result)
    
    assert 'interfaces' in result
    assert 'total_interfaces' in result
    assert 'io_statistics' in result
    assert isinstance(result['interfaces'], list)
    assert result['total_interfaces'] >= 0
    print("✅ Network info test passed")


def test_system_info():
    """Test system information retrieval."""
    print("\n=== Testing System Info ===")
    result = get_system_info()
    print("System Info:", result)
    
    assert 'os_info' in result
    assert 'hostname' in result
    assert 'uptime' in result
    assert 'boot_time' in result
    
    os_info = result['os_info']
    assert 'system' in os_info
    assert 'platform' in os_info
    print("✅ System info test passed")


def test_process_info():
    """Test process information retrieval."""
    print("\n=== Testing Process Info ===")
    result = get_process_info(limit=5)
    print("Process Info:", result)
    
    assert 'processes' in result
    assert 'total_processes' in result
    assert 'statistics' in result
    assert isinstance(result['processes'], list)
    assert len(result['processes']) <= 5
    assert result['total_processes'] >= 0
    print("✅ Process info test passed")


def test_hardware_summary():
    """Test hardware summary retrieval."""
    print("\n=== Testing Hardware Summary ===")
    result = get_hardware_summary()
    print("Hardware Summary:", result)
    
    assert 'summary' in result
    assert 'detailed' in result
    
    summary = result['summary']
    assert 'cpu' in summary
    assert 'memory' in summary
    assert 'disk' in summary
    assert 'network' in summary
    assert 'system' in summary
    
    detailed = result['detailed']
    assert 'cpu' in detailed
    assert 'memory' in detailed
    assert 'disk' in detailed
    assert 'network' in detailed
    assert 'system' in detailed
    print("✅ Hardware summary test passed")


def test_performance_monitor():
    """Test performance monitoring."""
    print("\n=== Testing Performance Monitor ===")
    result = monitor_performance(duration=1)
    print("Performance Monitor:", result)
    
    assert 'monitoring_duration' in result
    assert 'cpu' in result
    assert 'memory' in result
    assert 'disk_io' in result
    assert 'network_io' in result
    assert 'timestamp' in result
    
    duration = result['monitoring_duration']
    assert 'requested' in duration
    assert 'actual' in duration
    assert duration['requested'] == 1
    print("✅ Performance monitor test passed")


def test_gpu_info():
    """Test GPU information retrieval."""
    print("\n=== Testing GPU Info ===")
    result = get_gpu_info()
    print("GPU Info:", result)
    
    assert 'gpus' in result
    assert 'nvidia_available' in result
    assert 'amd_available' in result
    assert 'intel_available' in result
    assert isinstance(result['gpus'], list)
    print("✅ GPU info test passed")


def test_sensor_info():
    """Test sensor information retrieval."""
    print("\n=== Testing Sensor Info ===")
    result = get_sensor_info()
    print("Sensor Info:", result)
    
    assert 'temperatures' in result
    assert 'fans' in result
    assert 'battery' in result
    assert 'sensors_available' in result
    assert isinstance(result['temperatures'], dict)
    assert isinstance(result['fans'], dict)
    print("✅ Sensor info test passed")


if __name__ == "__main__":
    print("Running Node Hardware Capability Tests")
    print("=" * 60)
    
    test_cpu_info()
    test_memory_info()
    test_disk_info()
    test_network_info()
    test_system_info()
    test_process_info()
    test_hardware_summary()
    test_performance_monitor()
    test_gpu_info()
    test_sensor_info()
    
    print("\n" + "=" * 60)
    print("All capability tests completed!")
