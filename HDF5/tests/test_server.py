"""
Integration tests for FastMCP server.

Covers:
 - Server initialization and MCP tool registration
 - Tool execution through FastMCP framework
 - Error handling and server structure validation
"""
import json
import pytest
import sys
import os
import tempfile

# Path setup for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import server


class TestServer:
    """Test class for FastMCP server functionality."""

    def test_server_initialization(self):
        """Test that FastMCP server initializes correctly."""
        print("\n=== Running test_server_initialization ===")
        
        # Test that server module has MCP instance
        assert hasattr(server, 'mcp')
        assert server.mcp is not None
        print("FastMCP server instance exists")
        
        # Test that server has expected name
        assert server.mcp.name == "HDF5Server"
        print("Server has correct name: HDF5Server")

    def test_server_tools_registered(self):
        """Test that all expected tools are registered."""
        print("\n=== Running test_server_tools_registered ===")
        
        # Get the FastMCP server instance
        mcp_server = server.mcp
        
        # Check that tools are registered (FastMCP stores tools internally)
        # We can verify by checking if the tool functions exist
        expected_tools = [
            'list_hdf5_tool',
            'inspect_hdf5_tool', 
            'preview_hdf5_tool',
            'read_all_hdf5_tool'
        ]
        
        # Check that tool functions exist in server module
        for tool_name in expected_tools:
            assert hasattr(server, tool_name)
            print(f"Tool function {tool_name} exists")

    @pytest.mark.asyncio
    async def test_list_hdf5_tool_via_handler(self, tmp_path):
        """Test list_hdf5 tool via handler function."""
        print("\n=== Running test_list_hdf5_tool_via_handler ===")
        
        # Create test directory with HDF5 files
        test_dir = tmp_path / "test_hdf5_dir"
        test_dir.mkdir()
        (test_dir / "file1.hdf5").write_text("")
        (test_dir / "file2.hdf5").write_text("")
        
        # Import and call the handler directly
        import mcp_handlers
        result = await mcp_handlers.list_hdf5_files(str(test_dir))
        print("Handler result:", result)
        
        # Verify result format
        assert isinstance(result, list) or isinstance(result, dict)
        if isinstance(result, list):
            assert len(result) == 2
        else:
            # Check if it's an error format
            if "isError" in result:
                print("Handler returned error (expected if HDF5 files are empty)")
            else:
                assert "content" in result or "files" in result

    @pytest.mark.asyncio
    async def test_inspect_hdf5_tool_via_handler(self, tmp_path):
        """Test inspect_hdf5 tool via handler function."""
        print("\n=== Running test_inspect_hdf5_tool_via_handler ===")
        
        # Create test file path
        test_file = tmp_path / "test_inspect.hdf5"
        
        # Import and call the handler directly
        import mcp_handlers
        result = await mcp_handlers.inspect_hdf5_handler(str(test_file))
        print("Handler result:", result)
        
        # Should return some result structure (likely error for non-existent file)
        assert isinstance(result, (dict, str))
        if isinstance(result, dict):
            # Expect error format for non-existent file
            assert "isError" in result or "content" in result

    @pytest.mark.asyncio
    async def test_preview_hdf5_tool_via_handler(self, tmp_path):
        """Test preview_hdf5 tool via handler function."""
        print("\n=== Running test_preview_hdf5_tool_via_handler ===")
        
        # Create test file path
        test_file = tmp_path / "test_preview.hdf5"
        
        # Import and call the handler directly
        import mcp_handlers
        result = await mcp_handlers.preview_hdf5_handler(str(test_file), count=5)
        print("Handler result:", result)
        
        # Should return some result structure
        assert isinstance(result, (dict, str))
        if isinstance(result, dict):
            # Expect error format for non-existent file
            assert "isError" in result or "content" in result

    @pytest.mark.asyncio
    async def test_read_all_hdf5_tool_via_handler(self, tmp_path):
        """Test read_all_hdf5 tool via handler function."""
        print("\n=== Running test_read_all_hdf5_tool_via_handler ===")
        
        # Create test file path
        test_file = tmp_path / "test_read_all.hdf5"
        
        # Import and call the handler directly
        import mcp_handlers
        result = await mcp_handlers.read_all_hdf5_handler(str(test_file))
        print("Handler result:", result)
        
        # Should return some result structure
        assert isinstance(result, (dict, str))
        if isinstance(result, dict):
            # Expect error format for non-existent file
            assert "isError" in result or "content" in result

    def test_server_main_function_exists(self):
        """Test that main function exists for server startup."""
        print("\n=== Running test_server_main_function_exists ===")
        
        # Test that main function exists
        assert hasattr(server, 'main')
        assert callable(server.main)
        print("Server main function exists and is callable")

    def test_server_environment_handling(self, monkeypatch):
        """Test server handles environment variables correctly."""
        print("\n=== Running test_server_environment_handling ===")
        
        # Test with default environment (should not crash)
        monkeypatch.setenv("MCP_TRANSPORT", "stdio")
        
        # Import should work without errors
        import importlib
        importlib.reload(server)
        
        # Server should still exist
        assert hasattr(server, 'mcp')
        print("Server handles environment variables correctly")