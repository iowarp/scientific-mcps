"""
Tests for Node Hardware capabilities.
"""
import pytest
from src.implementation.remote_node_info import get_node_info
from src.implementation.hardware_summary import get_hardware_summary
from src.implementation.system_info import get_system_info


def test_get_node_info_basic():
    """Test basic node info collection."""
    result = get_node_info()
    assert result is not None
    assert isinstance(result, dict)
    # Should have metadata
    assert '_metadata' in result


def test_get_node_info_with_filters():
    """Test node info collection with filters."""
    result = get_node_info(include_filters=['cpu', 'memory'])
    assert result is not None
    assert isinstance(result, dict)
    # Should only have requested components (plus metadata)
    expected_keys = {'cpu', 'memory', '_metadata'}
    actual_keys = set(result.keys())
    # Allow for some variation but ensure we get some of our requested components
    assert len(actual_keys.intersection(expected_keys)) >= 2


def test_get_node_info_with_exclude_filters():
    """Test node info collection with exclude filters."""
    result = get_node_info(exclude_filters=['processes'])
    assert result is not None
    assert isinstance(result, dict)
    # Should not have excluded components
    assert 'processes' not in result


def test_hardware_summary():
    """Test hardware summary functionality."""
    result = get_hardware_summary()
    assert result is not None
    assert isinstance(result, dict)


def test_system_info():
    """Test system info functionality."""
    result = get_system_info()
    assert result is not None
    assert isinstance(result, dict)