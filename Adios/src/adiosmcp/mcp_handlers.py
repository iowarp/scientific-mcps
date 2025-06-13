# mcp_handlers.py
import json
from typing import Any, Dict, Optional
from capabilities import bp5_list, bp5_inspect_variables, bp5_attributes, bp5_read_variable_at_step, bp5_read_all_variables, bp5_minmax, bp5_add

class UnknownToolError(Exception):
    """Raised when an unsupported tool_name is requested."""
    pass

async def list_bp5_files(directory: str = "data") -> Dict[str, Any]:
    """
    List BP5 files in a directory.
    
    Args:
        directory: Path to the directory containing BP5 files
        
    Returns:
        Dict containing list of files and metadata
    """
    try:
        files = bp5_list.list_bp5(directory)
        return files
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "list_bp5", "error": type(e).__name__},
            "isError": True
        }
    
async def inspect_variables_handler(filename: str) -> Dict[str, Any]:
    """
    Async handler for 'inspect_variables' tool.
    """
    try:
        return bp5_inspect_variables.inspect_variables(filename)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "inspect_variables", "error": type(e).__name__},
            "isError": True
        }

async def inspect_attributes_handler(
    filename: str, variable_name: str = None
) -> Dict[str, Any]:
    """
    Async handler for 'inspect_attributes' tool.
    """
    try:
        return bp5_attributes.inspect_attributes(filename, variable_name)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "inspect_attributes", "error": type(e).__name__},
            "isError": True
        }
    
async def read_variable_at_step_handler(
    filename: str, variable_name: str, target_step: int
) -> Dict[str, Any]:
    try:
        value = bp5_read_variable_at_step.read_variable_at_step(filename, variable_name, target_step)
        return {"value": value}
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_variable_at_step", "error": type(e).__name__},
            "isError": True
        }
    
async def read_all_variables_handler(filename: str) -> Dict[str, Any]:
    """
    Async handler for the 'read_bp5' tool.
    Invokes bp5_module.bp5(filename) and returns its result,
    or an error‐formatted dict if an exception occurs.
    """
    try:
        data = bp5_read_all_variables.read_all_variables(filename)
        return data
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_bp5", "error": type(e).__name__},
            "isError": True
        }

async def get_min_max_handler(
    filename: str, variable_name: str, step: Optional[int] = None
) -> Dict[str, Any]:
    try:
        # returns {"min":…, "max":…} or {"step":…, "min":…, "max":…}
        result = bp5_minmax.get_min_max(filename, variable_name, step)
        return result
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "get_min_max", "error": type(e).__name__},
            "isError": True,
        }


async def add_variables_handler(
    filename: str,
    var1: str,
    var2: str,
    step1: Optional[int] = None,
    step2: Optional[int] = None,
) -> Dict[str, Any]:
    try:
        total = bp5_add.add_variables(filename, var1, var2, step1, step2)
        return {"sum": total}
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "add_variables", "error": type(e).__name__},
            "isError": True,
        }
