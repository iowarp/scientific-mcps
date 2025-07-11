"""
MCP handlers for Node Hardware monitoring.
These handlers wrap the hardware capabilities for MCP protocol compliance.
"""
import json
from typing import Optional
from .capabilities.cpu_info import get_cpu_info
from .capabilities.memory_info import get_memory_info
from .capabilities.disk_info import get_disk_info
from .capabilities.network_info import get_network_info
from .capabilities.system_info import get_system_info
from .capabilities.process_info import get_process_info
from .capabilities.hardware_summary import get_hardware_summary
from .capabilities.performance_monitor import monitor_performance
from .capabilities.gpu_info import get_gpu_info
from .capabilities.sensor_info import get_sensor_info


def cpu_info_handler() -> dict:
    """
    Handler wrapping the CPU info capability for MCP.
    Returns CPU information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_cpu_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "cpu_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "cpu_info", "error": type(e).__name__},
            "isError": True
        }


def memory_info_handler() -> dict:
    """
    Handler wrapping the memory info capability for MCP.
    Returns memory information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_memory_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "memory_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "memory_info", "error": type(e).__name__},
            "isError": True
        }


def disk_info_handler() -> dict:
    """
    Handler wrapping the disk info capability for MCP.
    Returns disk information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_disk_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "disk_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "disk_info", "error": type(e).__name__},
            "isError": True
        }


def network_info_handler() -> dict:
    """
    Handler wrapping the network info capability for MCP.
    Returns network information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_network_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "network_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "network_info", "error": type(e).__name__},
            "isError": True
        }


def system_info_handler() -> dict:
    """
    Handler wrapping the system info capability for MCP.
    Returns system information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_system_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "system_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "system_info", "error": type(e).__name__},
            "isError": True
        }


def process_info_handler(limit: int = 10) -> dict:
    """
    Handler wrapping the process info capability for MCP.
    Returns process information or an error payload on failure.
    
    Args:
        limit: Maximum number of processes to return
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_process_info(limit)
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "process_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "process_info", "error": type(e).__name__},
            "isError": True
        }


def hardware_summary_handler() -> dict:
    """
    Handler wrapping the hardware summary capability for MCP.
    Returns comprehensive hardware summary or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_hardware_summary()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "hardware_summary"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "hardware_summary", "error": type(e).__name__},
            "isError": True
        }


def performance_monitor_handler(duration: int = 5) -> dict:
    """
    Handler wrapping the performance monitoring capability for MCP.
    Returns performance metrics or an error payload on failure.
    
    Args:
        duration: Duration in seconds to monitor
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = monitor_performance(duration)
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "performance_monitor"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "performance_monitor", "error": type(e).__name__},
            "isError": True
        }


def gpu_info_handler() -> dict:
    """
    Handler wrapping the GPU info capability for MCP.
    Returns GPU information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_gpu_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "gpu_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "gpu_info", "error": type(e).__name__},
            "isError": True
        }


def sensor_info_handler() -> dict:
    """
    Handler wrapping the sensor info capability for MCP.
    Returns sensor information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_sensor_info()
        return {
            "content": [{"text": json.dumps(result)}],
            "_meta": {"tool": "sensor_info"}
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "sensor_info", "error": type(e).__name__},
            "isError": True
        }
