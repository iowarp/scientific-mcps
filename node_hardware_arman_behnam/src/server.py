from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

# Change absolute import to relative import
from .mcp_handlers import handle_mcp_request

app = FastAPI()

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Endpoint for MCP JSON-RPC 2.0 requests."""
    try:
        data = await request.json()
        response = await handle_mcp_request(data)
        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                "id": None
            },
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="127.0.0.1", port=8000, reload=True)