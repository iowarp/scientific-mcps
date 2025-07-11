#!/usr/bin/env python3
"""
Simple demonstration of Node Hardware MCP Server capabilities.
"""
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'node_hardware'))

def demonstrate_capabilities():
    """Demonstrate various hardware capabilities"""
    print("Node Hardware MCP Server - Capability Demonstration")
    print("=" * 60)
    
    # Import capabilities directly
    try:
        from capabilities.cpu_info import get_cpu_info
        from capabilities.memory_info import get_memory_info
        
        print("\nCPU Information:")
        cpu_info = get_cpu_info()
        print(f"   Logical cores: {cpu_info.get('logical_cores', 'N/A')}")
        print(f"   Physical cores: {cpu_info.get('physical_cores', 'N/A')}")
        print(f"   CPU model: {cpu_info.get('cpu_model', 'N/A')}")
        print(f"   Architecture: {cpu_info.get('architecture', 'N/A')}")
        
        print("\nMemory Information:")
        memory_info = get_memory_info()
        vm = memory_info.get('virtual_memory', {})
        print(f"   Total memory: {vm.get('total_formatted', 'N/A')}")
        print(f"   Available memory: {vm.get('available_formatted', 'N/A')}")
        print(f"   Memory usage: {vm.get('percent_formatted', 'N/A')}")
        
        print("\nMCP Tools Available:")
        tools = [
            "cpu_info - Get detailed CPU information",
            "memory_info - Get memory usage statistics", 
            "disk_info - Get disk usage and partition information",
            "network_info - Get network interface information",
            "system_info - Get general system information",
            "process_info - Get running process information",
            "hardware_summary - Get comprehensive hardware summary",
            "performance_monitor - Monitor real-time performance metrics",
            "gpu_info - Get GPU information (if available)",
            "sensor_info - Get temperature and sensor information"
        ]
        
        for i, tool in enumerate(tools, 1):
            print(f"   {i:2d}. {tool}")
        
        print("\nNode Hardware MCP Server is ready to use!")
        print("   Start the server with: uv run python src/node_hardware/server.py")
        print("   Or use the script: uv run node-hardware-mcp")
        print("   The server uses MCP protocol via stdio transport by default")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("   Make sure all dependencies are installed with: uv sync")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    demonstrate_capabilities()
