"""
Integration tests for Node Hardware MCP Server.
Tests the server integration and MCP protocol compliance.
"""
import pytest
import asyncio
import json
import sys
import os

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'node_hardware'))


@pytest.mark.asyncio
async def test_mcp_tool_cpu_info():
    """Test CPU info tool via MCP."""
    print("\n=== Testing MCP CPU Info Tool ===")
    
    # Import and call the tool function directly
    try:
        from server import get_cpu_info_tool
        
        result = await get_cpu_info_tool()
        print("CPU Info Tool Result:", result)
        
        assert 'logical_cores' in result
        assert 'physical_cores' in result
        assert isinstance(result['logical_cores'], int)
        print("✅ MCP CPU info tool test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_memory_info():
    """Test memory info tool via MCP."""
    print("\n=== Testing MCP Memory Info Tool ===")
    
    try:
        from server import get_memory_info_tool
        
        result = await get_memory_info_tool()
        print("Memory Info Tool Result:", result)
        
        assert 'virtual_memory' in result
        assert 'swap_memory' in result
        print("✅ MCP memory info tool test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_hardware_summary():
    """Test hardware summary tool via MCP."""
    print("\n=== Testing MCP Hardware Summary Tool ===")
    
    try:
        from server import get_hardware_summary_tool
        
        result = await get_hardware_summary_tool()
        print("Hardware Summary Tool Result:", result)
        
        assert 'summary' in result
        assert 'detailed' in result
        print("✅ MCP hardware summary tool test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_process_info():
    """Test process info tool via MCP."""
    print("\n=== Testing MCP Process Info Tool ===")
    
    try:
        from server import get_process_info_tool
        
        result = await get_process_info_tool(limit=5)
        print("Process Info Tool Result:", result)
        
        assert 'processes' in result
        assert 'total_processes' in result
        assert len(result['processes']) <= 5
        print("✅ MCP process info tool test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_performance_monitor():
    """Test performance monitor tool via MCP."""
    print("\n=== Testing MCP Performance Monitor Tool ===")
    
    try:
        from server import monitor_performance_tool
        
        result = await monitor_performance_tool(duration=1)
        print("Performance Monitor Tool Result:", result)
        
        assert 'monitoring_duration' in result
        assert 'cpu' in result
        assert 'memory' in result
        print("✅ MCP performance monitor tool test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


def test_server_main_function():
    """Test server main function setup."""
    print("\n=== Testing Server Main Function ===")
    
    try:
        # Test that main function exists and can be imported
        from server import main
        
        # Test environment variable handling
        os.environ['MCP_TRANSPORT'] = 'stdio'
        
        # We can't actually run main() as it starts the server
        # But we can test that it exists and is callable
        assert callable(main)
        print("✅ Server main function test passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    print("Running Node Hardware MCP Server Integration Tests")
    print("=" * 60)
    
    # Run async tests
    asyncio.run(test_mcp_tool_cpu_info())
    asyncio.run(test_mcp_tool_memory_info())
    asyncio.run(test_mcp_tool_hardware_summary())
    asyncio.run(test_mcp_tool_process_info())
    asyncio.run(test_mcp_tool_performance_monitor())
    
    # Run sync tests
    test_server_main_function()
    
    print("\n" + "=" * 60)
    print("All server integration tests completed!")
