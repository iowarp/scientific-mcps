import os
import sys
import subprocess
import asyncio

from .base import BaseLLM, LLMReply, ToolDef
from typing import List, Dict
from pathlib import Path

# TODO: Make this user-configurable/generated
OPENCODE_CONFIG_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../confs/custom-opencode-config.json"

class OpenCodeLLM(BaseLLM):
    """Adapter for OpenCode agent wrapper"""
    def __init__(self, model_name: str = "claude-3-haiku-20240307", api_key: str = None, **kwargs):
        if not os.path.exists(OPENCODE_CONFIG_PATH):
            raise FileNotFoundError("Opencode config JSON not found at " + OPENCODE_CONFIG_PATH)
        # TBD: Pass model name to local opencode config during initialization - currently, opencode defaults to model in pre-existing JSON
        self.model_name = model_name
        self.externally_managed_mcps = True
        self.subproc_env = os.environ.copy()
        self.subproc_env["OPENCODE_CONFIG"] = OPENCODE_CONFIG_PATH

        result = subprocess.run(
            ["opencode", "run", "-c", ":ist all tools available to you, along with their descriptions. Group the tools under headers that start with #. Use ' - ' to separate each tool's name from its description. Do not start tool lines wiht '-'"],
            env=self.subproc_env,
            capture_output=True,
            text=True,
            timeout=60
        )

        all_tools = result.stdout

        self.mcp_tools = extract_mcp_tools(all_tools)
        print(f"\nConnected to opencode agent framework with model {self.model_name}. Available tools:\n{self.mcp_tools}")


    async def chat(
        self, messages: List[Dict[str, str]], tools: List[ToolDef]
    ) -> LLMReply:
        system_prompt = "You are a helpful assistant."
        user_messages = [m['content'] for m in messages if m["role"] != "system"]        

        # Continuous opencode session handles remembering previous msgs in interaction
        # Just send the new msg
        result = subprocess.run(
            ["opencode", "run", "-c", user_messages[-1]],
            env=self.subproc_env,
            capture_output=True,
            text=True,
            timeout=60
        )

        agent_stdout = result.stdout
        agent_stderr = result.stderr

        return LLMReply(text=agent_stdout, tool_calls=None)

async def main():
    llm = OpenCodeLLM()
    msg1 = {"send hello world A": "send hello world B"}
    messages=[msg1]
    tools =[]
    chat = await llm.chat(messages=messages, tools=tools)
    print(chat)

    print("done")

if __name__ == "__main__":
    asyncio.run(main())

def extract_mcp_tools(text):
    """
    Extract only MCP-specific tools from opencode tool listing text.

    Removes built-in opencode tools and keeps only tools under novel MCP headers

    Args:
        text (str): The full tool listing text from opencode

    Returns:
        str: Filtered text containing only MCP-specific tools
    """
    lines = text.split('\n')

    # Built-in opencode tool sections to remove
    builtin_sections = {
        "File Operations",
        "Code Execution",
        "Task Management",
        "Web & Research"
    }

    # Built-in tool names to remove
    builtin_tools = {
        "read", "write", "edit", "list", "glob", "grep",
        "bash", "task",
        "todowrite", "todoread",
        "webfetch"
    }

    filtered_lines = []
    current_section = None
    skip_section = False

    for line in lines:
        # Check if this is a section header
        if line.startswith('# '):
            section_name = line.strip()[2:]  # Remove '# ' and spaces
            current_section = section_name
            # TBD - Need more robust detection
            skip_section = (not "arxiv" in line.strip().lower() and not "mcp" in line.strip().lower())

            if skip_section:
                continue

        elif skip_section:
            continue
        elif ' - ' in line.strip():
            # Extract tool name by going from start of line to ' - '
            tool_name = line.strip().split(' - ')[0].strip()
            # If tool name is in builtin tools, continue (skip this line)
            if tool_name in builtin_tools:
                continue
        else:
            # Skip other lines by default (e.g. other semantic LLM output)
            continue

        filtered_lines.append(line)

    return '\n'.join(filtered_lines).strip()
