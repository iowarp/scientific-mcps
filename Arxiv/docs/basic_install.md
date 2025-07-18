# ArXiv MCP Server - Installation Guide

## Overview

The ArXiv MCP Server provides comprehensive access to ArXiv research papers through the Model Context Protocol (MCP). It offers advanced search capabilities, paper analysis, and citation management tools.

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Internet connection for ArXiv API access

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/iowarp/scientific-mcps.git
cd scientific-mcps/Arxiv
```

### 2. Install Dependencies

Using uv (recommended):
```bash
uv sync
```

### 3. Test Installation

Run the demo to verify everything works:
```bash
uv run python demo.py
```

## Usage

### Start the Server

```bash
# Using uv
uv run arxiv-mcp

# Direct execution
uv run python src/server.py
```

### Configuration

The server supports environment variables for configuration:

- `MCP_TRANSPORT`: Transport type (`stdio` or `sse`)
- `MCP_SSE_HOST`: Host for SSE transport (default: `0.0.0.0`)
- `MCP_SSE_PORT`: Port for SSE transport (default: `8000`)

### Available Tools

#### Search & Discovery Tools
1. **search_arxiv** - Search by category or topic
2. **get_recent_papers** - Get recent papers from specific category
3. **search_papers_by_author** - Search by author name
4. **search_by_title** - Search by title keywords
5. **search_by_abstract** - Search by abstract keywords
6. **search_by_subject** - Search by subject classification
7. **search_date_range** - Search by date range

#### Paper Analysis Tools
8. **get_paper_details** - Get detailed paper information by ID
9. **find_similar_papers** - Find papers similar to reference paper

#### Export & Citation Tools
10. **export_to_bibtex** - Export search results to BibTeX format

#### PDF Download Tools
11. **download_paper_pdf** - Download PDF of a paper from ArXiv
12. **get_pdf_url** - Get direct PDF URL without downloading
13. **download_multiple_pdfs** - Download multiple PDFs concurrently

## Common ArXiv Categories

- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.CV` - Computer Vision and Pattern Recognition
- `cs.CL` - Computation and Language
- `physics.astro-ph` - Astrophysics
- `math.CO` - Combinatorics
- `q-bio.QM` - Quantitative Methods in Biology

## Troubleshooting

### Import Errors
Make sure all dependencies are installed:
```bash
uv sync
```

### Network Issues
Ensure you have internet access for ArXiv API calls.

### Timeout Issues
The server has a 30-second timeout for ArXiv API calls. For slow connections, this might need adjustment.

## Integration with MCP Clients

### Claude Desktop
Add to your Claude Desktop configuration:
```json
{
  "arxiv-mcp": {
    "command": "uv",
    "args": [
      "--directory", "/path/to/scientific-mcps/Arxiv",
      "run", "arxiv-mcp"
    ]
  }
}
```

### Other MCP Clients
The server uses stdio transport by default and is compatible with any MCP client supporting the protocol.