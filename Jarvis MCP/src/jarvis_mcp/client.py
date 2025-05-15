import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Optional
import argparse

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters

from google import genai
from google.genai import types

from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client with API key
client = genai.Client(api_key=GEMINI_API_KEY)


class MCPClient:
    """Handles connection and communication with an MCP server."""

    def __init__(self):
        """Initialize MCPClient with an exit stack and placeholder for session."""
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect(self, server_script: str = "src/server.py"):
        """
        Connect to the MCP server using SSE or stdio transport.

        If MCP_TRANSPORT="sse" is set, connects using SSE with MCP_SSE_HOST and MCP_SSE_PORT.
        Otherwise, uses stdio transport and launches the given server script.

        Args:
            server_script (str): Path to the server script (used for stdio transport).
        """
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()

        if transport == "sse":
            # Use Server-Sent Events transport
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = os.getenv("MCP_SSE_PORT", "3001")
            url = f"http://{host}:{port}/sse"
            print(f"Connecting via SSE to {url}")
            reader, writer = await self.exit_stack.enter_async_context(
                sse_client(url=url)
            )
        else:
            # Use stdio transport: launch the server script as a subprocess
            print(f"Starting server with stdio: {server_script}")
            command = sys.executable  # Path to Python executable
            args = [server_script]
            params = StdioServerParameters(command=command, args=args, env=os.environ)
            reader, writer = await self.exit_stack.enter_async_context(
                stdio_client(params)
            )

        # Initialize the MCP client session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(reader, writer)
        )
        await self.session.initialize()

        # List available tools after connection
        tools = await self.session.list_tools()
        print("Connected. Tools available:")
        for t in tools.tools:
            print(f" - {t.name}: {t.description}")

    async def process_query(self, query: str) -> dict:
        """
        Process a user query using the Gemini model and call tools if needed.

        Args:
            query (str): Natural language input from the user.

        Returns:
            dict: A dictionary containing the response text and token usage.
        """
        # Get available tools from the MCP server
        resp_tools = await self.session.list_tools()
        tool_descs = []

        # Build function descriptions from tools for Gemini tool-calling
        for t in resp_tools.tools:
            tool_descs.append({
                "name": t.name,
                "description": t.description,
                "parameters": {
                    "type": t.inputSchema.get("type", "object"),
                    "properties": {
                        k: {"type": v.get("type", "string"), "description": v.get("description", "")}
                        for k, v in t.inputSchema.get("properties", {}).items()
                    },
                    "required": t.inputSchema.get("required", [])
                }
            })

        # Configure Gemini to be aware of these tools
        tools_schema = types.Tool(function_declarations=tool_descs)
        config = types.GenerateContentConfig(tools=[tools_schema])

        # Send query to Gemini with tool support
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[query],
            config=config,
        )

        # Collect usage metadata
        um = response.usage_metadata
        prompt_tokens = um.prompt_token_count
        completion_tokens = um.candidates_token_count

        final_parts = []

        # Parse each candidate response from Gemini
        for cand in response.candidates:
            parts = getattr(cand.content, 'parts', None)
            if parts:
                for part in parts:
                    if getattr(part, 'function_call', None):
                        # If Gemini requests a function call, extract details
                        name = part.function_call.name
                        raw = part.function_call.args
                        args = json.loads(raw) if isinstance(raw, str) else raw
                        print(f"[Calling tool {name} with args {args}]")

                        # Call the tool via MCP and capture the result
                        tr = await self.session.call_tool(name, args)
                        raw_txt = tr.content[0].text
                        final_parts.append(f"[Called {name}: {raw_txt}]")
                    elif getattr(part, 'text', None):
                        # Plain text response part
                        final_parts.append(part.text)
            else:
                # Legacy-style single text response
                txt = getattr(cand.content, 'text', '')
                if txt:
                    final_parts.append(txt)

        return {
            "text": "\n".join(final_parts).strip(),
            "usage_metadata": {
                "prompt_token_count": prompt_tokens,
                "response_token_count": completion_tokens
            }
        }

    async def chat_loop(self):
        """
        Run an interactive chat loop with the user until they quit.
        """
        print("MCP Client Started! (type 'quit' to exit)")
        while True:
            q = input("\nQuery: ").strip()
            if q.lower() in ('quit', 'exit'):
                break
            out = await self.process_query(q)
            um = out["usage_metadata"]
            total = um["prompt_token_count"] + um["response_token_count"]
            print(f"\n{out['text']}")
            print(f"[Tokens: {total} (prompt {um['prompt_token_count']}, response {um['response_token_count']})]")

    async def cleanup(self):
        """
        Clean up and close all active resources and connections.
        """
        await self.exit_stack.aclose()


async def async_main(server_script: str):
    """
    Main async entry point to connect and begin the client chat loop.

    Args:
        server_script (str): Path to the server script for stdio transport.
    """
    client = MCPClient()
    try:
        await client.connect(server_script)
        await client.chat_loop()
    finally:
        await client.cleanup()


def main():
    """
    Parse command-line arguments and run the async client application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server-script",
        default=os.getenv("MCP_SERVER_SCRIPT", "src/server.py"),
        help="Path to the MCP server script for stdio transport"
    )
    args = parser.parse_args()
    asyncio.run(async_main(args.server_script))


if __name__ == "__main__":
    main()
