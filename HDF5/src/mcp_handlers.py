import json
from typing import Dict, List, Any, Optional
from implementation import hdf5_list, inspect_hdf5, preview_hdf5, read_all_hdf5

class UnknownToolError(Exception):
    """Raised when an unsupported tool_name is requested."""
    pass

async def list_hdf5_files(directory: str = "data") -> Dict[str, Any]:
    """
    List HDF5 files in a directory.
    
    Args:
        directory: Path to the directory containing HDF5 files
        
    Returns:
        Dict containing list of files and metadata
    """
    try:
        files = hdf5_list.list_hdf5(directory)
        return files
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "list_hdf5", "error": type(e).__name__},
            "isError": True
        }

async def inspect_hdf5_handler(filename: str) -> Dict[str, Any]:
    try:
        lines = inspect_hdf5.inspect_hdf5_file(filename)
        text = "\n".join(lines)
        return text
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "inspect_hdf5", "error": type(e).__name__},
            "isError": True
        }

async def preview_hdf5_handler(filename: str, count: int = 10) -> Dict[str, Any]:
    try:
        data = preview_hdf5.preview_hdf5_datasets(filename, count)
        return data
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "preview_hdf5", "error": type(e).__name__},
            "isError": True
        }

async def read_all_hdf5_handler(filename: str) -> Dict[str, Any]:
    try:
        data = read_all_hdf5.read_all_hdf5_datasets(filename)
        return data
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_all_hdf5", "error": type(e).__name__},
            "isError": True
        }

def list_resources() -> Dict[str, Any]:
    """List available MCP resources."""
    return {
        "_meta": {"count": 3},
        "resources": [
            {"name": "list_hdf5", "description": "List HDF5 files in directory"},
            {"name": "inspect_hdf5", "description": "Inspect HDF5 file structure"},
            {"name": "preview_hdf5", "description": "Preview HDF5 datasets"}
        ]
    }

async def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call a specific tool with given arguments."""
    if tool_name == "list_hdf5":
        directory = arguments.get("directory", "data")
        return await list_hdf5_files(directory)
    elif tool_name == "inspect_hdf5":
        file_path = arguments.get("file_path", "")
        return await inspect_hdf5_handler(file_path)
    elif tool_name == "preview_hdf5":
        file_path = arguments.get("file_path", "")
        count = arguments.get("count", 10)
        return await preview_hdf5_handler(file_path, count)
    elif tool_name == "read_all_hdf5":
        file_path = arguments.get("file_path", "")
        return await read_all_hdf5_handler(file_path)
    else:
        raise UnknownToolError(f"Unknown tool: {tool_name}")