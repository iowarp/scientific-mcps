# mcp_handlers.py
import json
from typing import Any, Dict
from capabilities import bp5 as bp5_module

class UnknownToolError(Exception):
    """Raised when an unsupported tool_name is requested."""
    pass

async def read_bp5_handler(filename: str) -> Dict[str, Any]:
    """
    Async handler for the 'read_bp5' tool.
    Invokes bp5_module.bp5(filename) and returns its result,
    or an error‐formatted dict if an exception occurs.
    """
    try:
        data = bp5_module.bp5(filename)
        return data
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "read_bp5", "error": type(e).__name__},
            "isError": True
        }
