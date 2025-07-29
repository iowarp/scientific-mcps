---
id: mcp-chronolog
title: Chronolog MCP
sidebar_label: Chronolog
description: ChronoLog MCP server implementation using Model Context Protocol
keywords: ['distributed logging', 'chronolog', 'event logging', 'session management', 'context sharing', 'real-time', 'model context protocol', 'scientific data', 'conversational ai', 'high-performance', 'shared log', 'multi-client', 'historical retrieval', 'enterprise logging']
tags: ['distributed logging', 'chronolog', 'event logging', 'session management', 'context sharing', 'real-time', 'model context protocol', 'scientific data', 'conversational ai', 'high-performance', 'shared log', 'multi-client', 'historical retrieval', 'enterprise logging']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Chronolog MCP

## Overview
ChronoLog MCP server implementation using Model Context Protocol

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Distributed Logging • Chronolog • Event Logging • Session Management • Context Sharing • Real Time • Model Context Protocol • Scientific Data • Conversational Ai • High Performance • Shared Log • Multi Client • Historical Retrieval • Enterprise Logging
- **Actions**: 4
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.11 or higher
- [py_chronolog_client](https://github.com/grc-iit/ChronoLog) Python package
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- ChronoLog deployment (see [setup guide](https://github.com/iowarp/scientific-mcps/blob/main/Chronolog/docs/Chronolog_setup.md))

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "chronolog-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "chronolog"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

```json
"mcp": {
  "servers": {
    "chronolog-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "chronolog"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add chronolog-mcp -- uvx iowarp-mcps chronolog
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "chronolog-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "chronolog"]
    }
  }
}
```

</details>

<details>
<summary><b>Manual Setup</b></summary>

**Linux/macOS:**
```bash
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Chronolog run chronolog-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Chronolog run chronolog-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Chronolog run chronolog-mcp --help
```

</details>

## Available Actions

### `start_chronolog`

**Description**: Connects to ChronoLog, creates a chronicle, and acquires a story handle for logging interactions.

**Parameters**: chronicle_name: Name of the chronicle to create or connect to. Defaults to config.DEFAULT_CHRONICLE., story_name: Name of the story to acquire. Defaults to config.DEFAULT_STORY.

### `record_interaction`

**Description**: Logs user messages and LLM responses to the active story with structured event formatting.

**Parameters**: user_message: The user message content to record., assistant_message: The assistant (LLM) response to record.

### `stop_chronolog`

**Description**: Releases the story handle and cleanly disconnects from ChronoLog system.

**Parameters**: No parameters

### `retrieve_interaction`

**Description**: Extracts logged records from specified chronicle and story, generates timestamped output files with filtering options.

**Parameters**: chronicle_name: Name of the chronicle to retrieve from. Defaults to config.DEFAULT_CHRONICLE., story_name: Name of the story to retrieve from. Defaults to config.DEFAULT_STORY., start_time: Start time for filtering records (YYYY-MM-DD HH:MM:SS or similar)., end_time: End time for filtering records (YYYY-MM-DD HH:MM:SS or similar).



## Examples

### Session Logging and Analysis

```
Start logging our conversation, then after we discuss machine learning concepts, retrieve the interaction history for analysis.
```

**Tools used:**
- **start_chronolog**: Initialize logging session
- **record_interaction**: Log conversation events
- **retrieve_interaction**: Generate interaction history

### Multi-Session Context Sharing

```
Connect to the research chronicle and retrieve yesterday's discussion about neural networks to continue our conversation.
```

**Tools used:**
- **start_chronolog**: Connect to existing chronicle
- **retrieve_interaction**: Fetch historical interactions

### Structured Event Documentation

```
Begin recording our software design discussion, ensuring all architectural decisions and code examples are captured for future reference.
```

**Tools used:**
- **start_chronolog**: Begin structured logging
- **record_interaction**: Capture design decisions
- **stop_chronolog**: Complete session

