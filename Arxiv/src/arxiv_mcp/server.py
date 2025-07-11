#!/usr/bin/env python3
"""
ArXiv MCP Server implementation using Model Context Protocol.
Provides access to ArXiv research papers through search and retrieval tools.
"""
import os
import sys
import json
from fastmcp import FastMCP
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

import mcp_handlers

# Initialize MCP server
mcp = FastMCP("ArxivMCP")

@mcp.tool(
    name="search_arxiv",
    description="Search ArXiv for research papers by category or topic."
)
async def search_arxiv_tool(query: str = "cs.AI", max_results: int = 5) -> dict:
    """
    Search ArXiv for research papers.
    
    Args:
        query: Search query or category (default: "cs.AI")
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Searching ArXiv for query: {query}")
    return await mcp_handlers.search_arxiv_handler(query, max_results)


@mcp.tool(
    name="get_recent_papers",
    description="Get recent papers from a specific ArXiv category."
)
async def get_recent_papers_tool(category: str = "cs.AI", max_results: int = 5) -> dict:
    """
    Get recent papers from ArXiv category.
    
    Args:
        category: ArXiv category (default: "cs.AI")
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Dictionary with recent papers
    """
    logger.info(f"Getting recent papers from category: {category}")
    return await mcp_handlers.get_recent_papers_handler(category, max_results)


@mcp.tool(
    name="search_papers_by_author",
    description="Search ArXiv papers by author name."
)
async def search_papers_by_author_tool(author: str, max_results: int = 10) -> dict:
    """
    Search ArXiv papers by author.
    
    Args:
        author: Author name to search for
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        Dictionary with author's papers
    """
    logger.info(f"Searching papers by author: {author}")
    return await mcp_handlers.search_papers_by_author_handler(author, max_results)


@mcp.tool(
    name="search_by_title",
    description="Search ArXiv papers by title keywords."
)
async def search_by_title_tool(title_keywords: str, max_results: int = 10) -> dict:
    """
    Search ArXiv papers by title keywords.
    
    Args:
        title_keywords: Keywords to search in paper titles
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Searching papers by title: {title_keywords}")
    return await mcp_handlers.search_by_title_handler(title_keywords, max_results)


@mcp.tool(
    name="search_by_abstract",
    description="Search ArXiv papers by abstract keywords."
)
async def search_by_abstract_tool(abstract_keywords: str, max_results: int = 10) -> dict:
    """
    Search ArXiv papers by abstract keywords.
    
    Args:
        abstract_keywords: Keywords to search in paper abstracts
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Searching papers by abstract: {abstract_keywords}")
    return await mcp_handlers.search_by_abstract_handler(abstract_keywords, max_results)


@mcp.tool(
    name="search_by_subject",
    description="Search ArXiv papers by subject classification."
)
async def search_by_subject_tool(subject: str, max_results: int = 10) -> dict:
    """
    Search ArXiv papers by subject classification.
    
    Args:
        subject: ArXiv subject classification (e.g., 'cs.AI', 'physics.astro-ph')
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Searching papers by subject: {subject}")
    return await mcp_handlers.search_by_subject_handler(subject, max_results)


@mcp.tool(
    name="search_date_range",
    description="Search ArXiv papers within a specific date range."
)
async def search_date_range_tool(start_date: str, end_date: str, category: str = "", max_results: int = 20) -> dict:
    """
    Search ArXiv papers within a date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        category: Optional category filter (e.g., 'cs.AI')
        max_results: Maximum number of results to return (default: 20)
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Searching papers by date range: {start_date} to {end_date}")
    return await mcp_handlers.search_date_range_handler(start_date, end_date, category, max_results)


@mcp.tool(
    name="get_paper_details",
    description="Get detailed information about a specific ArXiv paper by ID."
)
async def get_paper_details_tool(arxiv_id: str) -> dict:
    """
    Get detailed paper information.
    
    Args:
        arxiv_id: ArXiv paper ID (e.g., '2301.12345' or 'cs/0501001')
        
    Returns:
        Dictionary with detailed paper information
    """
    logger.info(f"Getting paper details for: {arxiv_id}")
    return await mcp_handlers.get_paper_details_handler(arxiv_id)


@mcp.tool(
    name="export_to_bibtex",
    description="Export search results to BibTeX format for citation management."
)
async def export_to_bibtex_tool(papers_json: str) -> dict:
    """
    Export papers to BibTeX format.
    
    Args:
        papers_json: JSON string containing list of papers to export
        
    Returns:
        Dictionary with BibTeX citations
    """
    logger.info("Exporting papers to BibTeX format")
    return await mcp_handlers.export_to_bibtex_handler(papers_json)


@mcp.tool(
    name="find_similar_papers",
    description="Find papers similar to a reference paper based on categories and keywords."
)
async def find_similar_papers_tool(reference_paper_id: str, max_results: int = 10) -> dict:
    """
    Find similar papers to a reference paper.
    
    Args:
        reference_paper_id: ArXiv ID of the reference paper
        max_results: Maximum number of similar papers to return (default: 10)
        
    Returns:
        Dictionary with similar papers
    """
    logger.info(f"Finding papers similar to: {reference_paper_id}")
    return await mcp_handlers.find_similar_papers_handler(reference_paper_id, max_results)


def main():
    """
    Main entry point for the ArXiv MCP server.
    Supports both stdio and SSE transports based on environment variables.
    """
    try:
        logger.info("Starting ArXiv MCP Server")
        
        # Determine which transport to use
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport == "sse":
            # SSE transport for web-based clients
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = int(os.getenv("MCP_SSE_PORT", "8000"))
            logger.info(f"Starting SSE transport on {host}:{port}")
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            # Default stdio transport
            logger.info("Starting stdio transport")
            print(json.dumps({"message": "Starting stdio transport"}), file=sys.stderr)
            mcp.run(transport="stdio")

    except Exception as e:
        logger.error(f"Server error: {e}")
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()