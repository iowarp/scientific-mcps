"""
Tests for Node Hardware capabilities.
"""
import pytest
from src.implementation.remote_node_info import get_node_info


def test_get_node_info_basic():
    """Test basic node info collection."""
    result = get_node_info()
    assert result is not None
    assert isinstance(result, dict)


def test_get_node_info_with_filters():
    """Test node info collection with filters."""
    result = get_node_info(include_filters=['cpu', 'memory'])
    assert result is not None
    assert isinstance(result, dict)


def test_get_node_info_with_exclude_filters():
    """Test node info collection with exclude filters."""
    result = get_node_info(exclude_filters=['processes'])
    assert result is not None
    assert isinstance(result, dict)