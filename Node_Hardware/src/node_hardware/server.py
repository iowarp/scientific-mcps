#!/usr/bin/env python3
"""
Enhanced Node Hardware MCP Server with comprehensive hardware monitoring.
Provides hardware information retrieval, system monitoring, and performance metrics.
"""
import os
import sys
import json
from fastmcp import FastMCP
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from . import mcp_handlers

# Initialize MCP server
mcp = FastMCP("NodeHardwareServer")

# Export for tests
app = mcp

@mcp.tool(
    name="cpu_info",
    description="Get comprehensive CPU information including processor architecture, core counts, frequencies, cache sizes, and performance capabilities. Provides detailed insights into CPU specifications, instruction sets, and thermal characteristics."
)
async def cpu_info_tool() -> dict:
    """
    Get comprehensive CPU information and specifications.
    
    Returns:
        Dictionary containing:
        - processor_info: CPU model, architecture, and manufacturer details
        - core_info: Physical and logical core counts, thread information
        - frequency_info: Base, boost, and current frequency measurements
        - cache_info: L1, L2, L3 cache sizes and configurations
        - feature_flags: Supported CPU instructions and capabilities
        - thermal_info: Temperature readings and thermal design power (TDP)
    """
    logger.info("Getting CPU information")
    return mcp_handlers.cpu_info_handler()


@mcp.tool(
    name="memory_info",
    description="Get comprehensive memory information including total capacity, available memory, usage statistics, swap information, and memory performance metrics. Provides detailed insights into RAM specifications, utilization patterns, and system memory health."
)
async def memory_info_tool() -> dict:
    """
    Get comprehensive memory information and statistics.
    
    Returns:
        Dictionary containing:
        - memory_capacity: Total, available, and used memory in various units
        - memory_usage: Current usage statistics and percentage utilization
        - memory_types: RAM specifications including type, speed, and configuration
        - swap_info: Swap space allocation, usage, and performance metrics
        - memory_performance: Memory bandwidth and latency characteristics
        - memory_health: Error rates and stability indicators
    """
    logger.info("Getting memory information")
    return mcp_handlers.memory_info_handler()


@mcp.tool(
    name="disk_info",
    description="Get comprehensive disk and storage information including disk usage, mount points, file system types, I/O statistics, and storage device specifications. Provides detailed insights into storage capacity, performance, and health metrics."
)
async def disk_info_tool() -> dict:
    """
    Get comprehensive disk and storage information.
    
    Returns:
        Dictionary containing:
        - disk_usage: Space utilization for all mounted file systems
        - mount_points: All mounted devices with file system information
        - storage_devices: Physical storage device specifications and models
        - io_statistics: Read/write performance metrics and IOPS data
        - disk_health: SMART data and device health indicators
        - file_system_info: File system types, features, and configuration
    """
    logger.info("Getting disk information")
    return mcp_handlers.disk_info_handler()


@mcp.tool(
    name="network_info",
    description="Get comprehensive network information including interface configurations, bandwidth statistics, connection details, and network performance metrics. Provides detailed insights into network adapters, protocols, and communication patterns."
)
async def network_info_tool() -> dict:
    """
    Get comprehensive network information and statistics.
    
    Returns:
        Dictionary containing:
        - network_interfaces: All network adapters with configuration details
        - bandwidth_stats: Network throughput and utilization metrics
        - connection_info: Active connections and protocol statistics
        - network_performance: Latency, packet loss, and quality metrics
        - interface_specs: Hardware specifications of network adapters
        - protocol_info: Supported protocols and network stack information
    """
    logger.info("Getting network information")
    return mcp_handlers.network_info_handler()


@mcp.tool(
    name="system_info",
    description="Get comprehensive system information including operating system details, hardware architecture, boot information, system uptime, and environmental metrics. Provides detailed insights into system configuration, performance, and operational status."
)
async def system_info_tool() -> dict:
    """
    Get comprehensive system information and operational metrics.
    
    Returns:
        Dictionary containing:
        - os_info: Operating system version, distribution, and kernel details
        - hardware_info: System architecture, motherboard, and BIOS information
        - boot_info: Boot time, uptime, and system initialization details
        - performance_metrics: Load averages, process counts, and system utilization
        - environmental_info: Temperature sensors, fan speeds, and power consumption
        - system_health: Error logs, stability indicators, and diagnostic information
    """
    logger.info("Getting system information")
    return mcp_handlers.system_info_handler()


@mcp.tool(
    name="process_info",
    description="Get comprehensive running process information with detailed resource usage analysis and process monitoring capabilities. Provides insights into CPU, memory, and I/O utilization patterns with process hierarchy and performance metrics."
)
async def process_info_tool(limit: int = 10) -> dict:
    """
    Get comprehensive process information with detailed resource analysis.
    
    Args:
        limit: Maximum number of processes to return (default: 10, sorted by resource usage)
        
    Returns:
        Dictionary containing:
        - process_list: Detailed information about running processes
        - resource_usage: CPU, memory, and I/O usage statistics per process
        - process_hierarchy: Parent-child process relationships and trees
        - performance_insights: Resource bottlenecks and optimization recommendations
    """
    logger.info(f"Getting process information (limit: {limit})")
    return mcp_handlers.process_info_handler(limit)


@mcp.tool(
    name="hardware_summary",
    description="Get a comprehensive hardware summary with integrated analysis of all system components including CPU, memory, disk, network, and peripheral devices. Provides holistic system overview with performance correlations and optimization insights."
)
async def hardware_summary_tool() -> dict:
    """
    Get comprehensive hardware summary with integrated system analysis.
    
    Returns:
        Dictionary containing:
        - system_overview: Complete hardware configuration summary
        - performance_baseline: Current performance metrics and baselines
        - component_health: Health status of all hardware components
        - optimization_recommendations: System-wide optimization suggestions
    """
    logger.info("Getting hardware summary")
    return mcp_handlers.hardware_summary_handler()


@mcp.tool(
    name="monitor_performance",
    description="Monitor system performance metrics in real-time with comprehensive tracking of CPU, memory, disk, and network utilization. Provides continuous performance monitoring with trend analysis and anomaly detection capabilities."
)
async def monitor_performance_tool(duration: int = 5) -> dict:
    """
    Monitor system performance with real-time tracking and analysis.
    
    Args:
        duration: Duration in seconds to monitor (default: 5, range: 1-300)
        
    Returns:
        Dictionary containing:
        - performance_timeline: Time-series data of system metrics
        - utilization_stats: Average, peak, and minimum utilization levels
        - trend_analysis: Performance trends and pattern identification
        - anomaly_detection: Unusual behavior and performance spikes
    """
    logger.info(f"Monitoring performance for {duration} seconds")
    return mcp_handlers.performance_monitor_handler(duration)


@mcp.tool(
    name="gpu_info",
    description="Get comprehensive GPU information including graphics card specifications, memory usage, compute capabilities, and performance metrics. Provides detailed insights into GPU hardware, driver information, and utilization patterns for graphics and compute workloads."
)
async def gpu_info_tool() -> dict:
    """
    Get comprehensive GPU information with detailed specifications and performance data.
    
    Returns:
        Dictionary containing:
        - gpu_specifications: Graphics card models, memory, and compute capabilities
        - driver_info: Driver versions, compatibility, and feature support
        - utilization_metrics: GPU usage, memory consumption, and thermal data
        - compute_capabilities: CUDA cores, OpenCL support, and parallel processing specs
    """
    logger.info("Getting GPU information")
    return mcp_handlers.gpu_info_handler()


@mcp.tool(
    name="sensor_info",
    description="Get comprehensive temperature and sensor information including thermal monitoring, fan speeds, voltage readings, and environmental metrics. Provides detailed insights into system health monitoring and environmental conditions."
)
async def sensor_info_tool() -> dict:
    """
    Get comprehensive sensor information with detailed environmental monitoring.
    
    Returns:
        Dictionary containing:
        - temperature_sensors: CPU, GPU, and system temperature readings
        - fan_information: Fan speeds, RPM, and cooling system status
        - voltage_readings: Power supply voltages and electrical metrics
        - environmental_data: Humidity, pressure, and ambient conditions
    """
    logger.info("Getting sensor information")
    return mcp_handlers.sensor_info_handler()


def main():
    """
    Main entry point for the Node Hardware MCP server.
    Supports both stdio and SSE transports based on environment variables.
    """
    try:
        logger.info("Starting Node Hardware MCP Server")
        
        # Determine which transport to use
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport == "sse":
            # SSE transport for web-based clients
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = int(os.getenv("MCP_SSE_PORT", "8000"))
            logger.info(f"Starting SSE transport on {host}:{port}")
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            # Default stdio transport
            logger.info("Starting stdio transport")
            print(json.dumps({"message": "Starting stdio transport"}), file=sys.stderr)
            mcp.run(transport="stdio")

    except Exception as e:
        logger.error(f"Server error: {e}")
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
