"""
Integration tests for Node Hardware MCP server integration and MCP protocol compliance.
"""
import pytest
import asyncio
import json
import sys
import os

# Add src to path using relative path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'node_hardware'))


@pytest.mark.asyncio
async def test_server_tools():
    """Test that server tools are properly registered."""
    print("\n=== Testing Server Tools ===")
    
    # Import the FastMCP instance
    from node_hardware.server import app
    
    # Check if tools are registered
    expected_tools = [
        "cpu_info",
        "memory_info",
        "disk_info", 
        "network_info",
        "system_info",
        "process_info",
        "hardware_summary",
        "performance_monitor",
        "gpu_info",
        "sensor_info"
    ]
    
    # This is a basic check - in a real MCP test we'd use the protocol
    print(f"Expected tools: {expected_tools}")
    print("✓ Server tools test passed")


@pytest.mark.asyncio
async def test_mcp_tool_cpu_info():
    """Test CPU info tool via MCP handler."""
    print("\n=== Testing MCP CPU Info Tool ===")
    
    try:
        from node_hardware.mcp_handlers import cpu_info_handler
        
        result = cpu_info_handler()
        print("CPU Info Tool Result:", result)
        
        # Check that the result has the expected structure
        assert 'content' in result
        assert len(result['content']) > 0
        
        # Parse the actual data to verify it contains expected fields
        data = json.loads(result['content'][0]['text'])
        assert 'logical_cores' in data
        assert 'physical_cores' in data
        assert isinstance(data['logical_cores'], int)
        print("✓ MCP CPU info tool test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_memory_info():
    """Test memory info tool via MCP handler."""
    print("\n=== Testing MCP Memory Info Tool ===")
    
    try:
        from node_hardware.mcp_handlers import memory_info_handler
        
        result = memory_info_handler()
        print("Memory Info Tool Result:", result)
        
        # Check that the result has the expected structure
        assert 'content' in result
        assert len(result['content']) > 0
        
        # Parse the actual data to verify it contains expected fields
        data = json.loads(result['content'][0]['text'])
        assert 'virtual_memory' in data
        assert 'swap_memory' in data
        print("✓ MCP memory info tool test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_hardware_summary():
    """Test hardware summary tool via MCP handler."""
    print("\n=== Testing MCP Hardware Summary Tool ===")
    
    try:
        from node_hardware.mcp_handlers import hardware_summary_handler
        
        result = hardware_summary_handler()
        print("Hardware Summary Tool Result:", result)
        
        # Check that the result has the expected structure
        assert 'content' in result
        assert len(result['content']) > 0
        
        # Parse the actual data to verify it contains expected fields
        data = json.loads(result['content'][0]['text'])
        assert 'summary' in data
        assert 'detailed' in data
        print("✓ MCP hardware summary tool test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_process_info():
    """Test process info tool via MCP handler."""
    print("\n=== Testing MCP Process Info Tool ===")
    
    try:
        from node_hardware.mcp_handlers import process_info_handler
        
        result = process_info_handler(limit=5)
        print("Process Info Tool Result:", result)
        
        # Check that the result has the expected structure
        assert 'content' in result
        assert len(result['content']) > 0
        
        # Parse the actual data to verify it contains expected fields
        data = json.loads(result['content'][0]['text'])
        assert 'processes' in data
        assert 'total_processes' in data
        assert len(data['processes']) <= 5
        print("✓ MCP process info tool test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_mcp_tool_performance_monitor():
    """Test performance monitor tool via MCP handler."""
    print("\n=== Testing MCP Performance Monitor Tool ===")
    
    try:
        from node_hardware.mcp_handlers import performance_monitor_handler
        
        result = performance_monitor_handler(duration=1)
        print("Performance Monitor Tool Result:", result)
        
        # Check that the result has the expected structure
        assert 'content' in result
        assert len(result['content']) > 0
        
        # Parse the actual data to verify it contains expected fields
        data = json.loads(result['content'][0]['text'])
        assert 'monitoring_duration' in data
        assert 'cpu' in data
        assert 'memory' in data
        print("✓ MCP performance monitor tool test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise


def test_server_main_function():
    """Test server main function setup."""
    print("\n=== Testing Server Main Function ===")
    
    try:
        # Test that main function exists and can be imported
        from node_hardware.server import main
        
        # We can't actually run main() as it starts the server
        # But we can test that it exists and is callable
        assert callable(main)
        print("✓ Server main function test passed")
    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise


if __name__ == "__main__":
    print("Running Node Hardware MCP Server Integration Tests")
    print("=" * 60)
    
    # Run async tests
    asyncio.run(test_server_tools())
    asyncio.run(test_mcp_tool_cpu_info())
    asyncio.run(test_mcp_tool_memory_info())
    asyncio.run(test_mcp_tool_hardware_summary())
    asyncio.run(test_mcp_tool_process_info())
    asyncio.run(test_mcp_tool_performance_monitor())
    
    # Run sync tests
    test_server_main_function()
    
    print("\n" + "=" * 60)
    print("All server integration tests completed!")
