"""
Slurm node allocation and reservation capabilities.
Handles interactive node allocation using salloc command.
"""
import subprocess
import re
from typing import Optional, List
from .utils import check_slurm_available


def allocate_nodes(
    num_nodes: int = 1,
    time_limit: Optional[str] = None,
    job_name: Optional[str] = None,
    exclusive: bool = False,
    specific_nodes: Optional[List[str]] = None,
    partition: Optional[str] = None,
    cpus_per_task: Optional[int] = None,
    memory: Optional[str] = None,
    gres: Optional[str] = None,
    immediate: bool = False
) -> dict:
    """
    Allocate nodes interactively using salloc.
    
    Args:
        num_nodes: Number of nodes to allocate (default: 1)
        time_limit: Time limit for allocation (format: HH:MM:SS, if None uses system default)
        job_name: Optional job name
        exclusive: Whether to request exclusive access to nodes
        specific_nodes: List of specific node names to request
        partition: Partition to submit to
        cpus_per_task: Number of CPUs per task
        memory: Memory requirement (e.g., "4G", "2048M")
        gres: Generic resource requirement (e.g., "gpu:1")
        immediate: Whether to request immediate allocation (fail if not available)
        
    Returns:
        Dictionary with allocation results
    """
    if not check_slurm_available():
        return {
            "status": "error",
            "message": "Slurm is not available on this system. Please install Slurm.",
            "real_slurm": False,
            "allocation_id": None
        }
    
    try:
        # Check partitions first if partition is specified
        if partition:
            # Validate partition exists
            try:
                from .queue_info import get_queue_info
                queue_info = get_queue_info()
                if queue_info.get("real_slurm", False) and "partitions" in queue_info:
                    available_partitions = list(queue_info["partitions"].keys())
                    if partition not in available_partitions:
                        return {
                            "status": "error",
                            "message": f"Unknown partition '{partition}'. Available partitions: {', '.join(available_partitions)}. Please check partitions first with: sinfo -s",
                            "real_slurm": True,
                            "allocation_id": None,
                            "available_partitions": available_partitions
                        }
            except Exception:
                # If we can't check partitions, proceed anyway
                pass
        
        # Build salloc command
        cmd = ["salloc"]
        
        # Add number of nodes
        cmd.extend(["-N", str(num_nodes)])
        
        # Add time limit only if specified by user
        if time_limit is not None:
            cmd.extend(["-t", time_limit])
        
        # Add job name if specified
        if job_name:
            cmd.extend(["-J", job_name])
        
        # Add exclusive flag if requested
        if exclusive:
            cmd.append("--exclusive")
        
        # Add specific nodes if specified
        if specific_nodes:
            node_list = ",".join(specific_nodes)
            cmd.extend(["-w", node_list])
        
        # Add partition if specified
        if partition:
            cmd.extend(["-p", partition])
        
        # Add CPUs per task if specified
        if cpus_per_task:
            cmd.extend(["-c", str(cpus_per_task)])
        
        # Add memory if specified
        if memory:
            cmd.extend(["--mem", memory])
        
        # Add generic resources if specified
        if gres:
            cmd.extend(["--gres", gres])
        
        # Add immediate flag if requested
        if immediate:
            cmd.append("--immediate")
        
        # For immediate allocations, use --no-shell to get allocation info
        # For non-immediate, we'll use a different approach
        if immediate:
            cmd.append("--no-shell")
            timeout_val = 10  # Short timeout for immediate
        else:
            # For non-immediate, we'll allocate and then cancel immediately to get job ID
            cmd.extend(["--no-shell"])
            timeout_val = 30
        
        # Execute salloc command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_val)
        
        if result.returncode == 0:
            # Parse allocation information from output
            allocation_info = _parse_allocation_output(result.stdout, result.stderr)
            
            # If we got a job ID, the allocation was successful
            if allocation_info.get("job_id"):
                return {
                    "status": "allocated",
                    "message": "Nodes allocated successfully",
                    "allocation_id": allocation_info.get("job_id"),
                    "allocated_nodes": allocation_info.get("nodes", []),
                    "num_nodes": num_nodes,
                    "time_limit": time_limit,
                    "command_used": " ".join(cmd),
                    "raw_output": result.stdout.strip(),
                    "raw_error": result.stderr.strip(),
                    "real_slurm": True
                }
            else:
                # Allocation succeeded but we couldn't parse job ID
                # This can happen with immediate allocations when nodes are allocated but output is minimal
                return {
                    "status": "allocated_no_id",
                    "message": "Nodes may have been allocated but job ID could not be determined",
                    "allocation_id": None,
                    "allocated_nodes": [],
                    "num_nodes": num_nodes,
                    "time_limit": time_limit,
                    "command_used": " ".join(cmd),
                    "raw_output": result.stdout.strip(),
                    "raw_error": result.stderr.strip(),
                    "real_slurm": True
                }
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            
            # Check for common error patterns
            if "partition" in error_msg.lower() and "invalid" in error_msg.lower():
                return {
                    "status": "error",
                    "message": f"Invalid partition specified. Please check partitions first with: sinfo -s. Error: {error_msg}",
                    "allocation_id": None,
                    "command_used": " ".join(cmd),
                    "real_slurm": True
                }
            
            return {
                "status": "error",
                "message": f"Failed to allocate nodes: {error_msg}",
                "allocation_id": None,
                "command_used": " ".join(cmd),
                "real_slurm": True
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": "Node allocation request timed out. This might indicate the nodes are not immediately available.",
            "allocation_id": None,
            "real_slurm": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during node allocation: {str(e)}",
            "allocation_id": None,
            "real_slurm": True
        }


def deallocate_allocation(allocation_id: str) -> dict:
    """
    Deallocate/cancel an existing allocation.
    
    Args:
        allocation_id: The allocation/job ID to cancel
        
    Returns:
        Dictionary with deallocation results
    """
    if not check_slurm_available():
        return {
            "status": "error",
            "message": "Slurm is not available on this system. Please install Slurm.",
            "real_slurm": False
        }
    
    try:
        cmd = ["scancel", allocation_id]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return {
                "allocation_id": allocation_id,
                "status": "deallocated",
                "message": f"Allocation {allocation_id} cancelled successfully",
                "real_slurm": True
            }
        else:
            return {
                "allocation_id": allocation_id,
                "status": "error",
                "message": f"Failed to cancel allocation: {result.stderr.strip()}",
                "real_slurm": True
            }
    except Exception as e:
        return {
            "allocation_id": allocation_id,
            "status": "error",
            "message": str(e),
            "real_slurm": True
        }


def get_allocation_info(allocation_id: str) -> dict:
    """
    Get information about a specific allocation.
    
    Args:
        allocation_id: The allocation/job ID to query
        
    Returns:
        Dictionary with allocation information
    """
    if not check_slurm_available():
        return {
            "status": "error",
            "message": "Slurm is not available on this system. Please install Slurm.",
            "real_slurm": False
        }
    
    try:
        # Use squeue to get allocation information
        cmd = ["squeue", "-j", allocation_id, "--format=%i,%T,%N,%D,%C,%M,%l,%P,%u", "--noheader"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse squeue output
            fields = result.stdout.strip().split(',')
            if len(fields) >= 9:
                return {
                    "allocation_id": fields[0],
                    "status": fields[1],
                    "nodes": fields[2] if fields[2] != "None assigned" else [],
                    "num_nodes": fields[3],
                    "cpus": fields[4],
                    "time_elapsed": fields[5],
                    "time_limit": fields[6],
                    "partition": fields[7],
                    "user": fields[8],
                    "real_slurm": True
                }
            else:
                return {
                    "allocation_id": allocation_id,
                    "status": "unknown",
                    "message": "Could not parse allocation information",
                    "raw_output": result.stdout.strip(),
                    "real_slurm": True
                }
        else:
            return {
                "allocation_id": allocation_id,
                "status": "not_found",
                "message": f"Allocation {allocation_id} not found or completed",
                "real_slurm": True
            }
            
    except Exception as e:
        return {
            "allocation_id": allocation_id,
            "status": "error",
            "message": str(e),
            "real_slurm": True
        }


def _parse_allocation_output(stdout: str, stderr: str = "") -> dict:
    """
    Parse salloc output to extract allocation information.
    
    Args:
        stdout: Standard output from salloc command
        stderr: Standard error from salloc command
        
    Returns:
        Dictionary with parsed allocation info
    """
    info = {}
    
    # Combine stdout and stderr for parsing
    combined_output = stdout + "\n" + stderr
    
    # Look for job ID in various formats
    # Format 1: "Granted job allocation 12345"
    job_id_match = re.search(r'Granted job allocation (\d+)', combined_output)
    if job_id_match:
        info['job_id'] = job_id_match.group(1)
    
    # Format 2: "salloc: Granted job allocation 12345"
    if not info.get('job_id'):
        job_id_match = re.search(r'salloc: Granted job allocation (\d+)', combined_output)
        if job_id_match:
            info['job_id'] = job_id_match.group(1)
    
    # Format 3: Look for job ID in any "12345" pattern after allocation keywords
    if not info.get('job_id'):
        allocation_match = re.search(r'(?:allocation|job)\s+(\d+)', combined_output, re.IGNORECASE)
        if allocation_match:
            info['job_id'] = allocation_match.group(1)
    
    # Look for allocated nodes
    # Format 1: "on node123" or "on node[1-3]"
    nodes_match = re.search(r'on (\S+)', combined_output)
    if nodes_match:
        nodes_str = nodes_match.group(1)
        info['nodes'] = _parse_node_list(nodes_str)
    
    # Format 2: Look for nodelist in other patterns
    if not info.get('nodes'):
        nodelist_match = re.search(r'nodelist[:\s]+(\S+)', combined_output, re.IGNORECASE)
        if nodelist_match:
            info['nodes'] = _parse_node_list(nodelist_match.group(1))
    
    return info


def _parse_node_list(nodes_str: str) -> list:
    """
    Parse a node list string into individual node names.
    
    Args:
        nodes_str: Node list string (e.g., "node[1-3]", "node1,node2")
        
    Returns:
        List of individual node names
    """
    nodes = []
    
    # Handle node ranges like node[1-3]
    if '[' in nodes_str and ']' in nodes_str:
        base = nodes_str.split('[')[0]
        range_part = nodes_str.split('[')[1].split(']')[0]
        
        if '-' in range_part:
            # Handle ranges like "1-3"
            parts = range_part.split('-')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                start, end = int(parts[0]), int(parts[1])
                nodes = [f"{base}{i}" for i in range(start, end + 1)]
        elif ',' in range_part:
            # Handle comma-separated like "1,2,3"
            indices = range_part.split(',')
            nodes = [f"{base}{idx.strip()}" for idx in indices]
        else:
            # Single index
            nodes = [f"{base}{range_part}"]
    else:
        # Simple comma-separated list or single node
        nodes = [node.strip() for node in nodes_str.split(',')]
    
    return nodes
