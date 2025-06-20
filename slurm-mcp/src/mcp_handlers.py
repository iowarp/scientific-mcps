"""
MCP handlers for Slurm job management.
These handlers wrap the Slurm capabilities for MCP protocol compliance.
"""
import json
from typing import Optional
from capabilities.job_submission import submit_slurm_job
from capabilities.job_status import get_job_status
from capabilities.job_cancellation import cancel_slurm_job
from capabilities.job_listing import list_slurm_jobs
from capabilities.cluster_info import get_slurm_info
from capabilities.job_details import get_job_details
from capabilities.job_output import get_job_output
from capabilities.queue_info import get_queue_info
from capabilities.array_jobs import submit_array_job
from capabilities.node_info import get_node_info


def submit_slurm_job_handler(script_path: str, cores: int, memory: Optional[str] = None, 
                            time_limit: Optional[str] = None, job_name: Optional[str] = None, 
                            partition: Optional[str] = None) -> dict:
    """
    Handler wrapping the Slurm submission capability for MCP.
    Returns a dict with job_id on success or an error payload on failure.
    
    Args:
        script_path: Path to the job script
        cores: Number of CPU cores to request
        memory: Memory requirement (e.g., "4G", "2048M")
        time_limit: Time limit (e.g., "1:00:00")
        job_name: Name for the job
        partition: Slurm partition to use
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        job_id = submit_slurm_job(script_path, cores, memory, time_limit, job_name, partition)
        return {
            "job_id": job_id,
            "status": "submitted",
            "script_path": script_path,
            "cores": cores,
            "memory": memory,
            "time_limit": time_limit,
            "job_name": job_name,
            "partition": partition,
            "message": f"Job {job_id} submitted successfully"
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "submit_slurm_job", "error": type(e).__name__},
            "isError": True
        }


def check_job_status_handler(job_id: str) -> dict:
    """
    Handler wrapping the job status check capability for MCP.
    Returns job status information or an error payload on failure.
    
    Args:
        job_id: The Slurm job ID to check
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        status_info = get_job_status(job_id)
        return status_info
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "check_job_status", "error": type(e).__name__},
            "isError": True
        }


def cancel_slurm_job_handler(job_id: str) -> dict:
    """
    Handler wrapping the job cancellation capability for MCP.
    Returns cancellation results or an error payload on failure.
    
    Args:
        job_id: The Slurm job ID to cancel
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = cancel_slurm_job(job_id)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "cancel_slurm_job", "error": type(e).__name__},
            "isError": True
        }


def list_slurm_jobs_handler(user: Optional[str] = None, state: Optional[str] = None) -> dict:
    """
    Handler wrapping the job listing capability for MCP.
    Returns list of jobs or an error payload on failure.
    
    Args:
        user: Username to filter by (default: current user)
        state: Job state to filter by (PENDING, RUNNING, COMPLETED, etc.)
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = list_slurm_jobs(user, state)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "list_slurm_jobs", "error": type(e).__name__},
            "isError": True
        }


def get_slurm_info_handler() -> dict:
    """
    Handler wrapping the cluster info capability for MCP.
    Returns cluster information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_slurm_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_slurm_info", "error": type(e).__name__},
            "isError": True
        }


def get_job_details_handler(job_id: str) -> dict:
    """
    Handler wrapping the job details capability for MCP.
    Returns detailed job information or an error payload on failure.
    
    Args:
        job_id: The Slurm job ID
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_job_details(job_id)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_job_details", "error": type(e).__name__},
            "isError": True
        }


def get_job_output_handler(job_id: str, output_type: str = "stdout") -> dict:
    """
    Handler wrapping the job output capability for MCP.
    Returns job output content or an error payload on failure.
    
    Args:
        job_id: The Slurm job ID
        output_type: Type of output ("stdout" or "stderr")
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_job_output(job_id, output_type)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_job_output", "error": type(e).__name__},
            "isError": True
        }


def get_queue_info_handler(partition: Optional[str] = None) -> dict:
    """
    Handler wrapping the queue info capability for MCP.
    Returns queue information or an error payload on failure.
    
    Args:
        partition: Specific partition to query (optional)
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_queue_info(partition)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_queue_info", "error": type(e).__name__},
            "isError": True
        }


def submit_array_job_handler(script_path: str, array_range: str, cores: int = 1,
                            memory: Optional[str] = None, time_limit: Optional[str] = None,
                            job_name: Optional[str] = None, partition: Optional[str] = None) -> dict:
    """
    Handler wrapping the array job submission capability for MCP.
    Returns array job submission results or an error payload on failure.
    
    Args:
        script_path: Path to the job script
        array_range: Array range specification (e.g., "1-10", "1-100:2")
        cores: Number of cores per array task
        memory: Memory per array task
        time_limit: Time limit per array task
        job_name: Base name for the array job
        partition: Slurm partition to use
        
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = submit_array_job(script_path, array_range, cores, memory, time_limit, job_name, partition)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "submit_array_job", "error": type(e).__name__},
            "isError": True
        }


def get_node_info_handler() -> dict:
    """
    Handler wrapping the node info capability for MCP.
    Returns node information or an error payload on failure.
    
    Returns:
        MCP-compliant response dictionary
    """
    try:
        result = get_node_info()
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_node_info", "error": type(e).__name__},
            "isError": True
        }