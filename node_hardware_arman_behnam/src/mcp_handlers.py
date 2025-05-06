from .capabilities import hdf5_handler, slurm_handler, node_hardware

async def handle_list_resources(params):
    """Handle mcp/listResources method."""
    resources = [
        {
            "id": "hdf5",
            "name": "HDF5 File Access",
            "description": "Access to HDF5 scientific data files",
            "type": "data_source"
        }
    ]
    return {"resources": resources}

async def handle_list_tools(params):
    tools = [
        {
            "id": "slurm",
            "name": "Slurm Job Scheduler",
            "description": "Submit jobs to HPC cluster via Slurm",
            "parameters": {
                "script_path": {"type": "string", "description": "Path to job script"},
                "cores": {"type": "integer", "description": "Number of CPU cores"}
            }
        },
        {
            "id": "node_hardware",
            "name": "Node Hardware Info",
            "description": "Get system hardware information",
            "parameters": {}
        }
    ]
    return {"tools": tools}


async def handle_call_tool(params):
    tool_id = params.get("tool_id")
    tool_params = params.get("parameters", {})
    
    if tool_id == "slurm":
        return await slurm_handler.submit_job(tool_params)
    elif tool_id == "node_hardware":
        return await node_hardware.get_system_info(tool_params)
    else:
        return {
            "error": {
                "code": -32602,
                "message": f"Unknown tool: {tool_id}"
            }
        }

async def handle_get_resource(params):
    """Handle mcp/getResource method."""
    resource_id = params.get("resource_id")
    resource_params = params.get("parameters", {})
    
    if resource_id == "hdf5":
        return await hdf5_handler.get_hdf5_data(resource_params)
    else:
        return {
            "error": {
                "code": -32602,
                "message": f"Unknown resource: {resource_id}"
            }
        }

MCP_METHODS = {
    "mcp/listResources": handle_list_resources,
    "mcp/callTool": handle_call_tool,
    "mcp/listTools": handle_list_tools,
    "mcp/getResource": handle_get_resource
}

async def handle_mcp_request(request):
    """Handle MCP JSON-RPC 2.0 requests."""
    if not all(k in request for k in ["jsonrpc", "method", "id"]):
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": None
        }
    
    if request["jsonrpc"] != "2.0":
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request: only JSON-RPC 2.0 supported"
            },
            "id": request.get("id")
        }
    
    method = request["method"]
    if method not in MCP_METHODS:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found"
            },
            "id": request["id"]
        }
    
    params = request.get("params", {})
    result = await MCP_METHODS[method](params)
    
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request["id"]
    }