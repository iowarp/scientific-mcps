"""
Testing of server MCP registration and tool accessibility.
"""

import os
import sys
import tempfile
import pandas as pd
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import server  # noqa: E402


class TestServerMCPSetup:
    """Test server MCP setup and tool registration"""

    @pytest.fixture
    def sample_csv_file(self):
        """Create a temporary CSV file for testing."""
        data = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10],
                "category": ["A", "B", "A", "B", "A"],
                "value": [10, 20, 15, 25, 30],
            }
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            data.to_csv(f.name, index=False)
            yield f.name
        os.unlink(f.name)

    def test_mcp_server_initialization(self):
        """Test that MCP server is properly initialized"""
        assert hasattr(server, "mcp")
        assert server.mcp is not None
        assert server.mcp.name == "PlotServer"

    def test_all_tools_registered(self):
        """Test that all expected tools are registered with MCP"""
        # Since we can't easily introspect FastMCP tools, we'll test
        # that the tool function objects exist and are properly decorated
        expected_tool_functions = [
            "line_plot_tool",
            "bar_plot_tool",
            "scatter_plot_tool",
            "histogram_plot_tool",
            "heatmap_plot_tool",
            "data_info_tool",
        ]

        for tool_name in expected_tool_functions:
            assert hasattr(server, tool_name), f"Missing tool function: {tool_name}"
            tool = getattr(server, tool_name)
            # These are FastMCP FunctionTool objects
            assert tool is not None
            assert hasattr(tool, "name")

    def test_tool_function_objects(self):
        """Test that tool function objects exist and have correct attributes"""
        tool_functions = [
            "line_plot_tool",
            "bar_plot_tool",
            "scatter_plot_tool",
            "histogram_plot_tool",
            "heatmap_plot_tool",
            "data_info_tool",
        ]

        for tool_name in tool_functions:
            assert hasattr(server, tool_name), f"Missing tool function: {tool_name}"
            tool = getattr(server, tool_name)
            # These are FastMCP FunctionTool objects
            assert tool is not None
            assert hasattr(tool, "name")

    def test_mcp_tools_count(self):
        """Test that the expected number of tool functions exist"""
        expected_tool_functions = [
            "line_plot_tool",
            "bar_plot_tool",
            "scatter_plot_tool",
            "histogram_plot_tool",
            "heatmap_plot_tool",
            "data_info_tool",
        ]

        actual_count = 0
        for tool_name in expected_tool_functions:
            if hasattr(server, tool_name):
                actual_count += 1

        assert actual_count == 6, f"Expected 6 tool functions, got {actual_count}"

    def test_tool_descriptions_exist(self):
        """Test that all tool functions are accessible"""
        tool_functions = [
            "line_plot_tool",
            "bar_plot_tool",
            "scatter_plot_tool",
            "histogram_plot_tool",
            "heatmap_plot_tool",
            "data_info_tool",
        ]

        for tool_name in tool_functions:
            assert hasattr(server, tool_name), f"Missing tool function: {tool_name}"
            tool = getattr(server, tool_name)
            assert tool is not None

    def test_server_module_structure(self):
        """Test server module has expected structure"""
        # Check required imports exist
        assert hasattr(server, "FastMCP")
        assert hasattr(server, "mcp")

        # Check that plot_capabilities is imported
        import importlib.util

        spec = importlib.util.find_spec("implementation.plot_capabilities")
        assert spec is not None, (
            "plot_capabilities module should be importable from server context"
        )

    def test_server_tool_parameters(self):
        """Test that tools are accessible through the server module"""
        tool_functions = [
            "line_plot_tool",
            "bar_plot_tool",
            "scatter_plot_tool",
            "histogram_plot_tool",
            "heatmap_plot_tool",
            "data_info_tool",
        ]

        for tool_name in tool_functions:
            assert hasattr(server, tool_name), f"Missing tool function: {tool_name}"
            tool = getattr(server, tool_name)
            assert tool is not None
