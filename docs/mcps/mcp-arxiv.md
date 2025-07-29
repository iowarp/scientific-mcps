---
id: mcp-arxiv
title: Arxiv MCP
sidebar_label: Arxiv
description: ArXiv MCP server implementation using Model Context Protocol
keywords: ['data processing', 'arxiv', 'publications', 'scientific data', 'research', 'papers']
tags: ['data processing', 'arxiv', 'publications', 'scientific data', 'research', 'papers']
last_update:
  date: 2025-07-28
  author: IOWarp Team
---

# Arxiv MCP

## Overview
ArXiv MCP server implementation using Model Context Protocol

## Information
- **Version**: 1.0.0
- **Language**: Python
- **Category**: Data Processing • Arxiv • Publications • Scientific Data • Research • Papers
- **Actions**: 13
- **Last Updated**: 2025-07-28

## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Linux/macOS environment (Windows supported)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "arxiv-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "arxiv"]
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
    "arxiv-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "arxiv"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add arxiv-mcp -- uvx iowarp-mcps arxiv
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "arxiv-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "arxiv"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Arxiv run arxiv-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Arxiv run arxiv-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Arxiv run arxiv-mcp --help
```

</details>

## Available Actions

### `search_arxiv`

**Description**: Search ArXiv for research papers by category or topic with comprehensive filtering and ranking capabilities.

**Parameters**: query: Search query or category (default: "cs.AI"), max_results: Maximum number of results to return (default: 5)

### `get_recent_papers`

**Description**: Get recent papers from a specific ArXiv category with chronological ordering and metadata extraction.

**Parameters**: category: ArXiv category (default: "cs.AI"), max_results: Maximum number of results to return (default: 5)

### `search_papers_by_author`

**Description**: Search ArXiv papers by author name with comprehensive author matching and publication history.

**Parameters**: author: Author name to search for, max_results: Maximum number of results to return (default: 10)

### `search_by_title`

**Description**: Search ArXiv papers by title keywords with intelligent keyword matching and relevance scoring.

**Parameters**: title_keywords: Keywords to search in paper titles, max_results: Maximum number of results to return (default: 10)

### `search_by_abstract`

**Description**: Search ArXiv papers by abstract keywords with semantic content analysis and relevance ranking.

**Parameters**: abstract_keywords: Keywords to search in paper abstracts, max_results: Maximum number of results to return (default: 10)

### `search_by_subject`

**Description**: Search ArXiv papers by subject classification with comprehensive category-based filtering.

**Parameters**: subject: ArXiv subject classification (e.g., 'cs.AI', 'physics.astro-ph'), max_results: Maximum number of results to return (default: 10)

### `search_date_range`

**Description**: Search ArXiv papers within a specific date range with optional category filtering and chronological organization.

**Parameters**: start_date: Start date in YYYY-MM-DD format, end_date: End date in YYYY-MM-DD format, category: Optional category filter (e.g., 'cs.AI'), max_results: Maximum number of results to return (default: 20)

### `get_paper_details`

**Description**: Get detailed information about a specific ArXiv paper by ID with comprehensive metadata extraction.

**Parameters**: arxiv_id: ArXiv paper ID (e.g., '2301.12345' or 'cs/0501001')

### `export_to_bibtex`

**Description**: Export search results to BibTeX format for citation management and bibliography generation.

**Parameters**: papers_json: JSON string containing list of papers to export

### `find_similar_papers`

**Description**: Find papers similar to a reference paper based on categories, keywords, and content analysis.

**Parameters**: reference_paper_id: ArXiv ID of the reference paper, max_results: Maximum number of similar papers to return (default: 10)

### `download_paper_pdf`

**Description**: Download the PDF of a paper from ArXiv with automatic file management and error handling.

**Parameters**: arxiv_id: ArXiv paper ID (e.g., '2301.12345' or 'cs/0501001'), download_path: Optional path to save the PDF

### `get_pdf_url`

**Description**: Get PDF URL for an ArXiv paper.

**Parameters**: arxiv_id: Parameter for arxiv_id

### `download_multiple_pdfs`

**Description**: Download multiple PDFs concurrently.

**Parameters**: arxiv_ids_json: Parameter for arxiv_ids_json, download_path: Parameter for download_path, max_concurrent: Parameter for max_concurrent (default: 3)



## Examples

### Academic Research Discovery

```
I'm researching machine learning applications in computer vision. Can you search for recent papers in this area and provide detailed information about the most relevant ones?
```

**Tools used:**
- **search_arxiv**: Search for machine learning and computer vision papers
- **get_paper_details**: Get detailed information about top papers

### Author-Based Research Analysis

```
Find all papers by Geoffrey Hinton published in the last 3 years, get their details, and export them to BibTeX format for my bibliography.
```

**Tools used:**
- **search_papers_by_author**: Find papers by Geoffrey Hinton
- **search_date_range**: Filter papers from last 3 years
- **get_paper_details**: Get detailed information for each paper
- **export_to_bibtex**: Generate BibTeX citations

### Literature Review Preparation

```
I need to conduct a literature review on transformer architectures. Find papers by searching titles and abstracts, identify similar papers to key references, and download the most important ones.
```

**Tools used:**
- **search_by_title**: Search for transformer-related papers by title
- **search_by_abstract**: Search abstracts for transformer content
- **find_similar_papers**: Find papers similar to key references
- **download_multiple_pdfs**: Download important papers

### Subject-Specific Research Monitoring

```
Monitor recent publications in quantum computing (quant-ph category) and natural language processing (cs.CL), focusing on papers from the last month.
```

**Tools used:**
- **get_recent_papers**: Get recent papers from quantum computing
- **search_by_subject**: Search cs.CL category papers
- **search_date_range**: Filter papers from last month

### Citation Network Analysis

```
Starting with the paper "Attention Is All You Need" (1706.03762), find similar papers and analyze the research landscape around transformer architectures.
```

**Tools used:**
- **get_paper_details**: Get details of the reference paper
- **find_similar_papers**: Find papers similar to the reference
- **search_by_title**: Search for transformer-related papers

### Comprehensive Research Package

```
Create a complete research package on deep reinforcement learning: find key papers, get author information, download PDFs, and prepare citations for academic writing.
```

**Tools used:**
- **search_by_subject**: Search cs.LG and cs.AI categories
- **search_by_title**: Title-based search for reinforcement learning
- **get_paper_details**: Extract comprehensive paper information
- **download_multiple_pdfs**: Download selected papers
- **export_to_bibtex**: Generate citation bibliography

