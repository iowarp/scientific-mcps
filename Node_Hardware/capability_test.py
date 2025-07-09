#!/usr/bin/env python3
"""
Simple test to verify the Node Hardware MCP Server is working
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'node_hardware'))

# Import the capabilities to test them directly
from capabilities.cpu_info import get_cpu_info
from capabilities.memory_info import get_memory_info
from capabilities.system_info import get_system_info
from capabilities.hardware_summary import get_hardware_summary
from capabilities.process_info import get_process_info

def test_capabilities():
    """Test the hardware monitoring capabilities"""
    print("🔧 Testing Node Hardware MCP Server Capabilities")
    print("=" * 50)
    
    # Test CPU info
    print("\n1. Testing CPU Information:")
    try:
        cpu_info = get_cpu_info()
        print(f"   ✅ CPU Model: {cpu_info.get('cpu_model', 'N/A')}")
        print(f"   ✅ Logical Cores: {cpu_info.get('logical_cores', 'N/A')}")
        print(f"   ✅ Physical Cores: {cpu_info.get('physical_cores', 'N/A')}")
        print(f"   ✅ Architecture: {cpu_info.get('architecture', 'N/A')}")
    except Exception as e:
        print(f"   ❌ CPU Info Error: {e}")
    
    # Test Memory info
    print("\n2. Testing Memory Information:")
    try:
        memory_info = get_memory_info()
        vm = memory_info.get('virtual_memory', {})
        print(f"   ✅ Total Memory: {vm.get('total_formatted', 'N/A')}")
        print(f"   ✅ Available Memory: {vm.get('available_formatted', 'N/A')}")
        print(f"   ✅ Memory Usage: {vm.get('percent_formatted', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Memory Info Error: {e}")
    
    # Test System info
    print("\n3. Testing System Information:")
    try:
        system_info = get_system_info()
        os_info = system_info.get('os_info', {})
        print(f"   ✅ OS: {os_info.get('system', 'N/A')}")
        print(f"   ✅ Platform: {os_info.get('platform', 'N/A')}")
        print(f"   ✅ Hostname: {system_info.get('hostname', 'N/A')}")
        print(f"   ✅ Uptime: {system_info.get('uptime', {}).get('formatted', 'N/A')}")
    except Exception as e:
        print(f"   ❌ System Info Error: {e}")
    
    # Test Hardware summary
    print("\n4. Testing Hardware Summary:")
    try:
        summary = get_hardware_summary()
        summary_info = summary.get('summary', {})
        print(f"   ✅ System: {summary_info.get('system', {}).get('os', 'N/A')}")
        print(f"   ✅ CPU: {summary_info.get('cpu', {}).get('model', 'N/A')}")
        print(f"   ✅ Memory: {summary_info.get('memory', {}).get('total', 'N/A')}")
        print(f"   ✅ Disk Partitions: {summary_info.get('disk', {}).get('total_partitions', 'N/A')}")
        print(f"   ✅ Network Interfaces: {summary_info.get('network', {}).get('total_interfaces', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Hardware Summary Error: {e}")
    
    # Test Process info
    print("\n5. Testing Process Information:")
    try:
        process_info = get_process_info(limit=5)
        print(f"   ✅ Process Count: {process_info.get('total_processes', 'N/A')}")
        print(f"   ✅ Top Processes: {len(process_info.get('processes', []))}")
        if process_info.get('processes'):
            for i, proc in enumerate(process_info['processes'][:3], 1):
                print(f"      {i}. {proc.get('name', 'N/A')} - {proc.get('cpu_percent', 'N/A')}% CPU")
    except Exception as e:
        print(f"   ❌ Process Info Error: {e}")
    
    print("\n✅ All capability tests completed!")

if __name__ == "__main__":
    test_capabilities()
