"""
Node Hardware MCP Server - Comprehensive Hardware Monitoring and System Analysis

This server provides comprehensive hardware monitoring and system analysis capabilities through 
the Model Context Protocol, enabling users to collect detailed hardware information, monitor 
system performance, and analyze resource utilization across local and remote systems.

Following MCP best practices, this server is designed with a workflow-first approach
providing intelligent, contextual assistance for hardware monitoring, system analysis,
and infrastructure management workflows.
"""

import os
import sys
import logging
from typing import Optional, List, Any, Dict

# Try to import required dependencies with fallbacks
try:
    from fastmcp import FastMCP
except ImportError:
    print("FastMCP not available. Please install with: uv add fastmcp", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not available. Environment variables may not be loaded.", file=sys.stderr)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Import handlers
import mcp_handlers

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server instance
mcp = FastMCP("NodeHardware-MCP-SystemMonitoring")

# Custom exception for hardware monitoring errors
class NodeHardwareMCPError(Exception):
    """Custom exception for Node Hardware MCP-related errors"""
    pass

# ═══════════════════════════════════════════════════════════════════════════════
# LOCAL NODE HARDWARE MONITORING
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool(
    name="get_node_info",
    description="""Get comprehensive local node hardware and system information with advanced filtering and intelligent analysis.

This powerful tool provides complete local system analysis by collecting information from all hardware 
and system components with sophisticated filtering capabilities. It delivers comprehensive 
specifications with intelligent data organization, performance analysis, and optimization recommendations.

**Local Hardware Collection Strategy**:
1. **Comprehensive Discovery**: Automatically detects and analyzes all available local hardware components
2. **Intelligent Filtering**: Applies sophisticated filtering to focus on specific components or exclude unwanted data
3. **Cross-Component Analysis**: Provides integrated analysis across all system subsystems for holistic insights
4. **Performance Optimization**: Delivers organized hardware information with metadata and collection statistics
5. **Predictive Intelligence**: Generates comprehensive insights and optimization recommendations based on collected data

**Available Hardware Components**:
- **cpu**: CPU specifications, core configuration, frequency analysis, cache hierarchy, performance metrics, thermal status
- **memory**: Memory capacity, usage patterns, swap configuration, performance characteristics, health indicators, efficiency analysis
- **disk**: Storage devices, usage analysis, I/O performance, health monitoring, file systems, predictive maintenance
- **network**: Network interfaces, bandwidth analysis, connection details, protocol statistics, security monitoring, performance optimization
- **system**: Operating system details, uptime analysis, user management, configuration, platform information, security status
- **processes**: Running processes, resource consumption, process hierarchy, performance metrics, system load analysis
- **gpu**: GPU specifications, memory analysis, thermal monitoring, performance metrics, driver information, compute capabilities
- **sensors**: Temperature sensors, fan control, voltage monitoring, hardware health, thermal management, predictive maintenance
- **performance**: Real-time performance monitoring, bottleneck analysis, optimization recommendations, trend analysis
- **summary**: Integrated hardware overview with cross-subsystem analysis and comprehensive health assessment

**Advanced Local Filtering Capabilities**:
- **Include Filters**: Specify exactly which components to collect for focused analysis and reduced overhead
- **Exclude Filters**: Remove specific components from collection for streamlined results and improved performance
- **Component Selection**: Choose from comprehensive list of hardware and system components with intelligent organization
- **Intelligent Organization**: Automatically organize collected data for optimal readability and analysis workflow
- **Metadata Tracking**: Track collection process, success rates, error handling, and performance metrics

**Prerequisites**: Local system access with hardware information retrieval capabilities
**Tools to use before this**: health_check() to verify system capabilities and compatibility
**Tools to use after this**: get_remote_node_info() for distributed system analysis, or optimization tools based on results

Use this tool when:
- Getting complete local system overview with selective focus ("Show me local CPU and memory info with performance analysis")
- Collecting comprehensive local hardware information for analysis, reporting, or infrastructure documentation
- Performing local system audits with customizable scope, depth, and intelligent analysis
- Monitoring local system health and performance characteristics with predictive maintenance insights
- Planning local system upgrades and capacity requirements with trend analysis and recommendations
- Troubleshooting local hardware and performance issues with intelligent diagnostic capabilities
- Conducting local infrastructure assessments with comprehensive analysis and optimization guidance"""
)
async def get_node_info_tool(
    components: Optional[List[str]] = None,
    exclude_components: Optional[List[str]] = None,
    include_performance: bool = True,
    include_health: bool = True
) -> dict:
    """
    Get comprehensive local node hardware and system information with intelligent filtering and advanced analysis.
    
    Args:
        components: List of specific components to include in collection for focused analysis
                   Available: ['cpu', 'memory', 'disk', 'network', 'system', 'processes', 'gpu', 'sensors', 'performance', 'summary']
        exclude_components: List of specific components to exclude from collection for streamlined results
        include_performance: Whether to include real-time performance analysis and optimization recommendations
        include_health: Whether to include health assessment and predictive maintenance insights
    
    Returns:
        Dictionary containing comprehensive local hardware and system analysis
    """
    try:
        logger.info(f"Collecting comprehensive local hardware information: components={components}, exclude={exclude_components}")
        
        return mcp_handlers.get_node_info_handler(
            include_filters=components,
            exclude_filters=exclude_components
        )
    except Exception as e:
        logger.error(f"Local hardware information collection error: {e}")
        return {
            "content": [{"text": f'{{"success": false, "error": "{str(e)}", "error_type": "LocalHardwareCollectionError", "troubleshooting": "Check system permissions and component availability"}}'}],
            "_meta": {"tool": "get_node_info", "error": "LocalHardwareCollectionError"},
            "isError": True
        }

@mcp.tool(
    name="get_remote_node_info",
    description="""Get comprehensive remote node hardware and system information via SSH with advanced filtering and intelligent analysis.

This powerful tool provides complete remote system analysis by securely connecting to remote nodes via SSH 
and collecting information from all hardware and system components with sophisticated filtering capabilities. 
It delivers comprehensive specifications with intelligent data organization, performance analysis, and optimization recommendations.

**Prerequisites**: SSH access to remote systems with hardware information retrieval capabilities
**Tools to use before this**: health_check() to verify local system capabilities, get_node_info() for local baseline comparison
**Tools to use after this**: Additional remote analysis tools or optimization tools based on remote system results

Use this tool when:
- Getting complete remote system overview with selective focus ("Show me remote CPU and memory info with performance analysis")
- Collecting comprehensive remote hardware information for distributed analysis, reporting, or infrastructure documentation
- Performing remote system audits with customizable scope, depth, and intelligent analysis across distributed infrastructure
- Monitoring remote system health and performance characteristics with predictive maintenance insights for distributed systems"""
)
async def get_remote_node_info_tool(
    hostname: str,
    username: Optional[str] = None,
    port: int = 22,
    ssh_key: Optional[str] = None,
    timeout: int = 30,
    components: Optional[List[str]] = None,
    exclude_components: Optional[List[str]] = None,
    include_performance: bool = True,
    include_health: bool = True
) -> dict:
    """
    Get comprehensive remote node hardware and system information via SSH with intelligent filtering and advanced analysis.
    
    Args:
        hostname: Target hostname or IP address for remote collection (required)
        username: SSH username for remote authentication (defaults to current user for seamless operation)
        port: SSH port number for remote connection with support for non-standard configurations
        ssh_key: Path to SSH private key file for key-based authentication and enhanced security
        timeout: SSH connection timeout in seconds with adaptive configuration for network conditions
        components: List of specific components to include in collection for focused analysis
        exclude_components: List of specific components to exclude from collection for streamlined results
        include_performance: Whether to include real-time performance analysis and optimization recommendations
        include_health: Whether to include health assessment and predictive maintenance insights
    
    Returns:
        Dictionary containing comprehensive remote hardware and system analysis
    """
    try:
        logger.info(f"Collecting comprehensive remote hardware information from {hostname}: components={components}, exclude={exclude_components}")
        
        return mcp_handlers.get_remote_node_info_handler(
            hostname=hostname,
            username=username,
            port=port,
            ssh_key=ssh_key,
            timeout=timeout,
            include_filters=components,
            exclude_filters=exclude_components
        )
    except Exception as e:
        logger.error(f"Remote hardware information collection error: {e}")
        return {
            "content": [{"text": f'{{"success": false, "error": "{str(e)}", "error_type": "RemoteHardwareCollectionError", "troubleshooting": "Check SSH connectivity, authentication, and remote system permissions"}}'}],
            "_meta": {"tool": "get_remote_node_info", "error": "RemoteHardwareCollectionError"},
            "isError": True
        }

@mcp.tool(
    name="health_check",
    description="""Perform comprehensive health check and system diagnostics with advanced capability verification.

This tool provides complete system health assessment by verifying all hardware monitoring 
capabilities, system compatibility, and performance characteristics. It delivers comprehensive 
health status with diagnostic insights, optimization recommendations, and predictive maintenance guidance.

**Prerequisites**: No special requirements - designed for comprehensive system assessment and compatibility verification
**Tools to use before this**: None - this is typically the first tool to run for system verification
**Tools to use after this**: get_node_info() and get_remote_node_info() based on health check results and recommendations for detailed analysis

Use this tool when:
- Verifying system health and MCP server functionality ("Check system health and capabilities")
- Diagnosing system issues and compatibility problems with comprehensive analysis
- Assessing system performance and optimization opportunities with benchmarking"""
)
async def health_check_tool() -> dict:
    """
    Perform comprehensive health check of the Node Hardware MCP server with advanced system diagnostics.
    
    Returns:
        Dictionary containing comprehensive health assessment
    """
    try:
        logger.info("Performing comprehensive health check and system diagnostics with advanced analysis")
        
        return mcp_handlers.health_check_handler()
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "content": [{"text": f'{{"success": false, "error": "{str(e)}", "error_type": "HealthCheckError", "troubleshooting": "Check system permissions, dependencies, and server configuration"}}'}],
            "_meta": {"tool": "health_check", "error": "HealthCheckError"},
            "isError": True
        }

def main():
    """
    Main entry point to start the FastMCP server using the specified transport.
    Chooses between stdio and SSE based on MCP_TRANSPORT environment variable.
    """
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport == "sse":
        host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SSE_PORT", "8000"))
        print(f"Starting Node Hardware MCP System Monitoring Server on {host}:{port}", file=sys.stderr)
        mcp.run(transport="sse", host=host, port=port)
    else:
        print("Starting Node Hardware MCP System Monitoring Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()