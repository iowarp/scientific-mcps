"""
MCP handlers for Node Hardware monitoring.
These handlers wrap the hardware capabilities for MCP protocol compliance.
"""
import json
from typing import Optional
from capabilities.cpu_info import get_cpu_info
from capabilities.memory_info import get_memory_info
from capabilities.disk_info import get_disk_info
from capabilities.network_info import get_network_info
from capabilities.system_info import get_system_info
from capabilities.process_info import get_process_info
from capabilities.hardware_summary import get_hardware_summary
from capabilities.performance_monitor import monitor_performance
from capabilities.gpu_info import get_gpu_info
from capabilities.sensor_info import get_sensor_info


def get_cpu_info_handler() -> dict:
    """
    Handler wrapping the CPU info capability for MCP.
    Returns CPU information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_cpu_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_cpu_info", "error": type(e).__name__},
            "isError": True
        }


def get_memory_info_handler() -> dict:
    """
    Handler wrapping the memory info capability for MCP.
    Returns memory information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_memory_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_memory_info", "error": type(e).__name__},
            "isError": True
        }


def get_disk_info_handler() -> dict:
    """
    Handler wrapping the disk info capability for MCP.
    Returns disk information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_disk_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_disk_info", "error": type(e).__name__},
            "isError": True
        }


def get_network_info_handler() -> dict:
    """
    Handler wrapping the network info capability for MCP.
    Returns network information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_network_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_network_info", "error": type(e).__name__},
            "isError": True
        }


def get_system_info_handler() -> dict:
    """
    Handler wrapping the system info capability for MCP.
    Returns system information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_system_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_system_info", "error": type(e).__name__},
            "isError": True
        }


def get_process_info_handler(limit: int = 10) -> dict:
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
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_process_info", "error": type(e).__name__},
            "isError": True
        }


def get_hardware_summary_handler() -> dict:
    """
    Handler wrapping the hardware summary capability for MCP.
    Returns comprehensive hardware summary or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_hardware_summary()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_hardware_summary", "error": type(e).__name__},
            "isError": True
        }


def monitor_performance_handler(duration: int = 5) -> dict:
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
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "monitor_performance", "error": type(e).__name__},
            "isError": True
        }


def get_gpu_info_handler() -> dict:
    """
    Handler wrapping the GPU info capability for MCP.
    Returns GPU information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_gpu_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_gpu_info", "error": type(e).__name__},
            "isError": True
        }


def get_sensor_info_handler() -> dict:
    """
    Handler wrapping the sensor info capability for MCP.
    Returns sensor information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_sensor_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_sensor_info", "error": type(e).__name__},
            "isError": True
        }
