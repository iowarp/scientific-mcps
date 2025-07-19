"""
Unit tests for mcp_handlers module.

Covers:
 - list_resources() returning correct resource count
 - call_tool dispatch for various HDF5 operations
 - Unknown-tool error handling
 - Handler function validation
"""
import json
import pytest
import sys
import os

# Path setup for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import mcp_handlers


class TestMCPHandlers:
    """Test class for MCP handlers functionality."""

    def test_list_resources(self):
        """Test that list_resources returns correct resource count."""
        print("\n=== Running test_list_resources ===")
        res = mcp_handlers.list_resources()
        print("Resources returned:", res)
        assert res['_meta']['count'] == 3

    @pytest.mark.asyncio
    async def test_call_tool_list_hdf5(self, tmp_path):
        """Test call_tool dispatch for list_hdf5."""
        print("\n=== Running test_call_tool_list_hdf5 ===")
        
        # Create test directory with HDF5 files
        test_dir = tmp_path / "test_hdf5_dir"
        test_dir.mkdir()
        (test_dir / "file1.hdf5").write_text("")
        (test_dir / "file2.hdf5").write_text("")
        
        # Test the handler
        result = await mcp_handlers.call_tool("list_hdf5", {"directory": str(test_dir)})
        print("Handler result:", result)
        
        assert isinstance(result, list)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self):
        """Test call_tool with unknown tool name."""
        print("\n=== Running test_call_tool_unknown_tool ===")
        
        with pytest.raises(mcp_handlers.UnknownToolError) as excinfo:
            await mcp_handlers.call_tool("unknown_tool", {})
        
        print("Caught exception:", excinfo.value)
        assert "unknown_tool" in str(excinfo.value)

    @pytest.mark.asyncio 
    async def test_call_tool_inspect_hdf5(self, tmp_path):
        """Test call_tool dispatch for inspect_hdf5."""
        print("\n=== Running test_call_tool_inspect_hdf5 ===")
        
        # Create a test HDF5 file path (handler should handle non-existent gracefully)
        test_file = tmp_path / "test.hdf5"
        
        # Test the handler - should handle missing file gracefully
        result = await mcp_handlers.call_tool("inspect_hdf5", {"file_path": str(test_file)})
        print("Handler result:", result)
        
        # Should return some result structure even if file doesn't exist
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_call_tool_preview_hdf5(self, tmp_path):
        """Test call_tool dispatch for preview_hdf5."""
        print("\n=== Running test_call_tool_preview_hdf5 ===")
        
        # Create a test HDF5 file path
        test_file = tmp_path / "preview_test.hdf5"
        
        # Test the handler
        result = await mcp_handlers.call_tool("preview_hdf5", {"file_path": str(test_file)})
        print("Handler result:", result)
        
        # Should return some result structure
        assert isinstance(result, dict)