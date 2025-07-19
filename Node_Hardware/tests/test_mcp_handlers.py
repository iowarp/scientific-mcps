"""
Tests for Node Hardware MCP handlers.
"""
import pytest
from src.mcp_handlers import get_node_info_handler, health_check_handler


def test_get_node_info_handler():
    """Test the node info handler."""
    result = get_node_info_handler()
    assert result is not None
    assert isinstance(result, dict)
    assert "content" in result
    assert "_meta" in result


def test_health_check_handler():
    """Test the health check handler."""
    result = health_check_handler()
    assert result is not None
    assert isinstance(result, dict)
    assert "content" in result
    assert "_meta" in result


def test_get_node_info_handler_with_filters():
    """Test the node info handler with filters."""
    result = get_node_info_handler(
        include_filters=['cpu', 'memory'],
        exclude_filters=['processes']
    )
    assert result is not None
    assert isinstance(result, dict)