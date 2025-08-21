#!/usr/bin/env python3
"""
National Data Platform (NDP) MCP Server

This MCP server provides access to the National Data Platform API,
enabling discovery, search, and analysis of datasets including
EarthScope Consortium data and other geospatial datasets.
"""

import asyncio
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse

import aiohttp
import pandas as pd
import geopandas as gpd
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    Prompt,
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
from pydantic import BaseModel, Field
import asyncio_throttle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NDP API Configuration
import os
import argparse
from typing import Optional

# Default configuration values
DEFAULT_NDP_BASE_URL = "http://155.101.6.191:8003"
DEFAULT_SERVER_NAME = "global"
DEFAULT_CHUNK_THRESHOLD = 100

# Get configuration from environment variables or use defaults
NDP_BASE_URL = os.getenv("NDP_BASE_URL", DEFAULT_NDP_BASE_URL)
DEFAULT_SERVER = os.getenv("NDP_DEFAULT_SERVER", DEFAULT_SERVER_NAME)
CHUNK_THRESHOLD = int(os.getenv("NDP_CHUNK_THRESHOLD", str(DEFAULT_CHUNK_THRESHOLD)))  # Number of results before chunking is applied

# Cache for search results
search_cache = {}
chunk_cache = {}

class NDPClient:
    """Client for interacting with the NDP API."""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or NDP_BASE_URL
        self.session = None
        self.throttler = asyncio_throttle.Throttler(rate_limit=10, period=1)  # 10 requests per second
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a throttled request to the NDP API."""
        async with self.throttler:
            url = urljoin(self.base_url, endpoint)
            try:
                async with self.session.get(url, params=params, timeout=30) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"API request failed: {e}")
                raise Exception(f"Failed to fetch data from NDP API: {e}")
    
    async def get_organizations(self) -> List[Dict]:
        """Fetch all organizations from the NDP API."""
        params = {"server": DEFAULT_SERVER}
        data = await self._make_request("/organization", params)
        return data.get("result", [])
    
    async def search_datasets(self, query: str, organization: Optional[str] = None, limit: int = 10) -> Dict:
        """Search for datasets in the NDP catalog."""
        params = {
            "q": query,
            "limit": limit,
            "server": DEFAULT_SERVER
        }
        if organization:
            params["organization"] = organization
        
        data = await self._make_request("/search", params)
        return data
    
    async def get_dataset_details(self, dataset_id: str) -> Dict:
        """Get complete metadata for a specific dataset."""
        params = {"server": DEFAULT_SERVER}
        data = await self._make_request(f"/dataset/{dataset_id}", params)
        return data.get("result", {})
    
    async def download_file(self, url: str) -> bytes:
        """Download a file from a URL."""
        async with self.throttler:
            try:
                async with self.session.get(url, timeout=60) as response:
                    response.raise_for_status()
                    return await response.read()
            except aiohttp.ClientError as e:
                logger.error(f"File download failed: {e}")
                raise Exception(f"Failed to download file from {url}: {e}")

class DatasetResource(BaseModel):
    """Model for dataset resource information."""
    url: str
    format: str
    name: Optional[str] = None
    description: Optional[str] = None

class Dataset(BaseModel):
    """Model for dataset information."""
    id: str
    name: str
    title: str
    owner_org: str
    resources: List[DatasetResource]
    extras: Optional[Dict] = None
    spatial: Optional[Dict] = None

class NDPMCPServer:
    """MCP Server for National Data Platform integration."""
    
    def __init__(self, base_url: Optional[str] = None, server: Optional[str] = None, chunk_threshold: Optional[int] = None):
        self.server = Server("ndp")
        self.ndp_client = None
        self.ndp_base_url = base_url or NDP_BASE_URL
        self.ndp_server = server or DEFAULT_SERVER
        self.chunk_threshold = chunk_threshold or CHUNK_THRESHOLD
        self.setup_server()
    
    def setup_server(self):
        """Setup the MCP server with all resources, tools, and prompts."""
        
        @self.server.list_resources()
        async def list_resources(request: ListResourcesRequest) -> ListResourcesResult:
            """List available NDP resources."""
            try:
                async with NDPClient() as client:
                    # Get organizations
                    organizations = await client.get_organizations()
                    
                    resources = []
                    
                    # Add organizations as resources
                    for org in organizations:
                        resources.append(Resource(
                            uri=f"ndp://organizations/{org.get('id', org.get('name', 'unknown'))}",
                            name=org.get('name', 'Unknown Organization'),
                            description=org.get('description', 'NDP Organization'),
                            mimeType="application/json"
                        ))
                    
                    # Add a general catalog resource
                    resources.append(Resource(
                        uri="ndp://catalog",
                        name="NDP Dataset Catalog",
                        description="Searchable catalog of all NDP datasets",
                        mimeType="application/json"
                    ))
                    
                    return ListResourcesResult(resources=resources)
            except Exception as e:
                logger.error(f"Error listing resources: {e}")
                return ListResourcesResult(resources=[])
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> Union[TextContent, ImageContent, EmbeddedResource]:
            """Read a specific NDP resource."""
            try:
                if uri.startswith("ndp://organizations/"):
                    org_id = uri.split("/")[-1]
                    async with NDPClient() as client:
                        organizations = await client.get_organizations()
                        org = next((o for o in organizations if o.get('id') == org_id or o.get('name') == org_id), None)
                        if org:
                            return TextContent(
                                type="text",
                                text=json.dumps(org, indent=2)
                            )
                
                elif uri == "ndp://catalog":
                    return TextContent(
                        type="text",
                        text=json.dumps({
                            "description": "NDP Dataset Catalog",
                            "search_endpoint": f"{self.ndp_base_url}/search",
                            "organizations_endpoint": f"{self.ndp_base_url}/organization"
                        }, indent=2)
                    )
                
                elif uri.startswith("ndp://datasets/"):
                    dataset_id = uri.split("/")[-1]
                    async with NDPClient() as client:
                        dataset = await client.get_dataset_details(dataset_id)
                        return TextContent(
                            type="text",
                            text=json.dumps(dataset, indent=2)
                        )
                
                raise Exception(f"Unknown resource URI: {uri}")
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return TextContent(
                    type="text",
                    text=f"Error reading resource: {str(e)}"
                )
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available NDP tools."""
            return [
                Tool(
                    name="list_organizations",
                    description="List all available organizations from the NDP API",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="search_datasets",
                    description="Search for datasets across the NDP catalog",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query string"
                            },
                            "organization": {
                                "type": "string",
                                "description": "Optional organization filter"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results (default: 10)"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_dataset_details",
                    description="Retrieve complete metadata for a specific dataset",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dataset_id": {
                                "type": "string",
                                "description": "Dataset ID to retrieve"
                            }
                        },
                        "required": ["dataset_id"]
                    }
                ),
                Tool(
                    name="download_dataset_resources",
                    description="Download dataset files (CSV, GeoJSON, PNG, etc.) from dataset resources",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dataset_id": {
                                "type": "string",
                                "description": "Dataset ID to download resources from"
                            },
                            "resource_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional array of resource types to download (defaults to all)"
                            }
                        },
                        "required": ["dataset_id"]
                    }
                ),
                Tool(
                    name="analyze_geospatial_data",
                    description="Analyze geospatial datasets, specifically designed for EarthScope and similar data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dataset_id": {
                                "type": "string",
                                "description": "Dataset ID to analyze"
                            }
                        },
                        "required": ["dataset_id"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Execute NDP tools."""
            try:
                if name == "list_organizations":
                    return await self._list_organizations()
                elif name == "search_datasets":
                    return await self._search_datasets(**arguments)
                elif name == "get_dataset_details":
                    return await self._get_dataset_details(**arguments)
                elif name == "download_dataset_resources":
                    return await self._download_dataset_resources(**arguments)
                elif name == "analyze_geospatial_data":
                    return await self._analyze_geospatial_data(**arguments)
                else:
                    raise Exception(f"Unknown tool: {name}")
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )
        
        @self.server.list_prompts()
        async def list_prompts(request: ListPromptsRequest) -> ListPromptsResult:
            """List available NDP prompt templates."""
            return ListPromptsResult(
                prompts=[
                    Prompt(
                        name="Find EarthScope Data",
                        description="Template to help users discover EarthScope Consortium datasets",
                        arguments={
                            "type": "object",
                            "properties": {
                                "search_terms": {
                                    "type": "string",
                                    "description": "Specific search terms for EarthScope data"
                                }
                            }
                        }
                    ),
                    Prompt(
                        name="Analyze Geospatial Dataset",
                        description="Template to walk through downloading and analyzing a complete dataset",
                        arguments={
                            "type": "object",
                            "properties": {
                                "dataset_id": {
                                    "type": "string",
                                    "description": "Dataset ID to analyze"
                                }
                            },
                            "required": ["dataset_id"]
                        }
                    ),
                    Prompt(
                        name="Dataset Discovery",
                        description="General purpose dataset search and exploration workflow template",
                        arguments={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query"
                                },
                                "organization": {
                                    "type": "string",
                                    "description": "Optional organization filter"
                                }
                            },
                            "required": ["query"]
                        }
                    )
                ]
            )
        
        @self.server.get_prompt()
        async def get_prompt(name: str) -> Prompt:
            """Get a specific prompt template."""
            prompts = {
                "Find EarthScope Data": Prompt(
                    name="Find EarthScope Data",
                    description="Template to help users discover EarthScope Consortium datasets",
                    arguments={
                        "type": "object",
                        "properties": {
                            "search_terms": {
                                "type": "string",
                                "description": "Specific search terms for EarthScope data"
                            }
                        }
                    },
                    messages=[
                        {
                            "role": "system",
                            "content": "You are helping a user discover EarthScope Consortium datasets. Follow this workflow:\n\n1. First, list all available organizations to find 'earthscope_consortium'\n2. Search for datasets using the provided search terms\n3. Filter results to focus on EarthScope data\n4. Provide step-by-step guidance for dataset selection\n5. Suggest next steps for analysis"
                        },
                        {
                            "role": "user",
                            "content": "I want to find EarthScope data related to: {{search_terms}}\n\nPlease help me discover relevant datasets and guide me through the process."
                        }
                    ]
                ),
                "Analyze Geospatial Dataset": Prompt(
                    name="Analyze Geospatial Dataset",
                    description="Template to walk through downloading and analyzing a complete dataset",
                    arguments={
                        "type": "object",
                        "properties": {
                            "dataset_id": {
                                "type": "string",
                                "description": "Dataset ID to analyze"
                            }
                        },
                        "required": ["dataset_id"]
                    },
                    messages=[
                        {
                            "role": "system",
                            "content": "You are helping a user analyze a geospatial dataset. Follow this workflow:\n\n1. Get detailed metadata for the dataset\n2. Download all available resources (CSV, GeoJSON, PNG)\n3. Parse and analyze the data\n4. Generate summary statistics and insights\n5. Suggest visualizations and further analysis"
                        },
                        {
                            "role": "user",
                            "content": "Please analyze the geospatial dataset with ID: {{dataset_id}}\n\nDownload the data, parse it, and provide comprehensive analysis including statistics and visualization suggestions."
                        }
                    ]
                ),
                "Dataset Discovery": Prompt(
                    name="Dataset Discovery",
                    description="General purpose dataset search and exploration workflow template",
                    arguments={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "organization": {
                                "type": "string",
                                "description": "Optional organization filter"
                            }
                        },
                        "required": ["query"]
                    },
                    messages=[
                        {
                            "role": "system",
                            "content": "You are helping a user discover and explore NDP datasets. Follow this workflow:\n\n1. Search for datasets using the provided query\n2. Present results in an organized manner\n3. Explain how to interpret the results\n4. Guide the user through selecting and accessing datasets\n5. Suggest next steps for data exploration"
                        },
                        {
                            "role": "user",
                            "content": "I want to discover datasets related to: {{query}}\n\n{% if organization %}From organization: {{organization}}{% endif %}\n\nPlease help me explore the available datasets and understand how to work with them."
                        }
                    ]
                )
            }
            
            if name not in prompts:
                raise Exception(f"Unknown prompt: {name}")
            
            return prompts[name]
    
    async def _list_organizations(self) -> CallToolResult:
        """List all available organizations from the NDP API."""
        try:
            async with NDPClient(self.ndp_base_url) as client:
                organizations = await client.get_organizations()
                
                result_text = "Available NDP Organizations:\n\n"
                for org in organizations:
                    result_text += f"- **{org.get('name', 'Unknown')}** (ID: {org.get('id', 'N/A')})\n"
                    if org.get('description'):
                        result_text += f"  Description: {org['description']}\n"
                    result_text += "\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
        except Exception as e:
            logger.error(f"Error listing organizations: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error listing organizations: {str(e)}")]
            )
    
    async def _search_datasets(self, query: str, organization: Optional[str] = None, limit: int = 10) -> CallToolResult:
        """Search for datasets across the NDP catalog with intelligent chunking."""
        try:
            # Check if search exists in cache
            cache_key = f"{query}_{organization}_{limit}"
            if cache_key in search_cache:
                chunk_id = search_cache[cache_key].get('next_chunk', 1)
                return await self._get_chunk(cache_key, chunk_id)
            
            async with NDPClient(self.ndp_base_url) as client:
                search_result = await client.search_datasets(query, organization, limit)
                
                results = search_result.get('result', {}).get('results', [])
                
                if len(results) > self.chunk_threshold:
                    # Implement chunking
                    search_cache[cache_key] = {
                        'results': results,
                        'next_chunk': 1,
                        'total_chunks': (len(results) + 9) // 10  # 10 results per chunk
                    }
                    return await self._get_chunk(cache_key, 1)
                else:
                    return self._format_search_results(results, query, organization)
        
        except Exception as e:
            logger.error(f"Error searching datasets: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error searching datasets: {str(e)}")]
            )
    
    async def _get_chunk(self, cache_key: str, chunk_id: int) -> CallToolResult:
        """Get a specific chunk of search results."""
        if cache_key not in search_cache:
            raise Exception("Search results not found in cache")
        
        cache_data = search_cache[cache_key]
        results = cache_data['results']
        chunk_size = 10
        start_idx = (chunk_id - 1) * chunk_size
        end_idx = start_idx + chunk_size
        
        chunk_results = results[start_idx:end_idx]
        
        result_text = self._format_search_results_text(chunk_results, cache_key, chunk_id, cache_data['total_chunks'])
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    def _format_search_results(self, results: List[Dict], query: str, organization: Optional[str] = None) -> CallToolResult:
        """Format search results for display."""
        result_text = self._format_search_results_text(results, None, 1, 1)
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
    
    def _format_search_results_text(self, results: List[Dict], cache_key: Optional[str], chunk_id: int, total_chunks: int) -> str:
        """Format search results as text."""
        result_text = f"Found {len(results)} datasets"
        if total_chunks > 1:
            result_text += f" (Chunk {chunk_id} of {total_chunks})"
        result_text += ":\n\n"
        
        for i, dataset in enumerate(results, 1):
            result_text += f"{i}. **{dataset.get('title', dataset.get('name', 'Untitled'))}**\n"
            result_text += f"   - ID: `{dataset.get('id', 'N/A')}`\n"
            result_text += f"   - Organization: {dataset.get('owner_org', 'Unknown')}\n"
            if dataset.get('notes'):
                result_text += f"   - Description: {dataset['notes'][:100]}...\n"
            result_text += "\n"
        
        if total_chunks > 1 and chunk_id < total_chunks:
            result_text += f"\nTo get the next chunk, use the search_datasets tool with the same parameters.\n"
        
        return result_text
    
    async def _get_dataset_details(self, dataset_id: str) -> CallToolResult:
        """Retrieve complete metadata for a specific dataset."""
        try:
            async with NDPClient(self.ndp_base_url) as client:
                dataset = await client.get_dataset_details(dataset_id)
                
                if not dataset:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Dataset with ID '{dataset_id}' not found.")]
                    )
                
                result_text = f"**Dataset Details: {dataset.get('title', dataset.get('name', 'Untitled'))}**\n\n"
                result_text += f"- **ID**: `{dataset.get('id', 'N/A')}`\n"
                result_text += f"- **Name**: {dataset.get('name', 'N/A')}\n"
                result_text += f"- **Organization**: {dataset.get('owner_org', 'N/A')}\n"
                result_text += f"- **Created**: {dataset.get('metadata_created', 'N/A')}\n"
                result_text += f"- **Modified**: {dataset.get('metadata_modified', 'N/A')}\n"
                
                if dataset.get('notes'):
                    result_text += f"- **Description**: {dataset['notes']}\n"
                
                if dataset.get('tags'):
                    result_text += f"- **Tags**: {', '.join([tag['name'] for tag in dataset['tags']])}\n"
                
                # Resources
                resources = dataset.get('resources', [])
                if resources:
                    result_text += f"\n**Resources ({len(resources)}):**\n"
                    for i, resource in enumerate(resources, 1):
                        result_text += f"{i}. **{resource.get('name', 'Unnamed Resource')}**\n"
                        result_text += f"   - Format: {resource.get('format', 'Unknown')}\n"
                        result_text += f"   - URL: {resource.get('url', 'N/A')}\n"
                        if resource.get('description'):
                            result_text += f"   - Description: {resource['description']}\n"
                        result_text += "\n"
                
                # Extras
                extras = dataset.get('extras', [])
                if extras:
                    result_text += "**Additional Metadata:**\n"
                    for extra in extras:
                        result_text += f"- {extra.get('key', 'Unknown')}: {extra.get('value', 'N/A')}\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
        
        except Exception as e:
            logger.error(f"Error getting dataset details: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting dataset details: {str(e)}")]
            )
    
    async def _download_dataset_resources(self, dataset_id: str, resource_types: Optional[List[str]] = None) -> CallToolResult:
        """Download dataset files from dataset resources."""
        try:
            async with NDPClient(self.ndp_base_url) as client:
                # Get dataset details first
                dataset = await client.get_dataset_details(dataset_id)
                if not dataset:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Dataset with ID '{dataset_id}' not found.")]
                    )
                
                resources = dataset.get('resources', [])
                if not resources:
                    return CallToolResult(
                        content=[TextContent(type="text", text="No resources found for this dataset.")]
                    )
                
                # Filter resources by type if specified
                if resource_types:
                    resources = [r for r in resources if r.get('format', '').upper() in [rt.upper() for rt in resource_types]]
                
                result_text = f"**Downloading Resources for Dataset: {dataset.get('title', dataset.get('name', 'Untitled'))}**\n\n"
                
                downloaded_files = []
                
                for i, resource in enumerate(resources, 1):
                    try:
                        result_text += f"{i}. Downloading: {resource.get('name', 'Unnamed Resource')} ({resource.get('format', 'Unknown')})\n"
                        
                        # Download the file
                        file_content = await client.download_file(resource['url'])
                        
                        # Save to temporary file
                        file_ext = self._get_file_extension(resource.get('format', ''))
                        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                            temp_file.write(file_content)
                            temp_file_path = temp_file.name
                        
                        downloaded_files.append({
                            'name': resource.get('name', f'resource_{i}'),
                            'format': resource.get('format', 'Unknown'),
                            'path': temp_file_path,
                            'size': len(file_content)
                        })
                        
                        result_text += f"   ✅ Downloaded: {temp_file_path} ({len(file_content)} bytes)\n"
                        
                    except Exception as e:
                        result_text += f"   ❌ Failed to download: {str(e)}\n"
                    
                    result_text += "\n"
                
                result_text += f"**Summary**: Downloaded {len(downloaded_files)} files successfully.\n"
                result_text += "Files are saved in temporary locations and can be accessed for analysis.\n"
                
                # Add file paths to result
                if downloaded_files:
                    result_text += "\n**Downloaded Files:**\n"
                    for file_info in downloaded_files:
                        result_text += f"- {file_info['name']} ({file_info['format']}): {file_info['path']}\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
        
        except Exception as e:
            logger.error(f"Error downloading dataset resources: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error downloading dataset resources: {str(e)}")]
            )
    
    def _get_file_extension(self, format_type: str) -> str:
        """Get file extension based on format type."""
        format_map = {
            'CSV': '.csv',
            'GEOJSON': '.geojson',
            'JSON': '.json',
            'PNG': '.png',
            'JPG': '.jpg',
            'JPEG': '.jpeg',
            'PDF': '.pdf',
            'XML': '.xml',
            'ZIP': '.zip'
        }
        return format_map.get(format_type.upper(), '.txt')
    
    async def _analyze_geospatial_data(self, dataset_id: str) -> CallToolResult:
        """Analyze geospatial datasets, specifically designed for EarthScope and similar data."""
        try:
            async with NDPClient(self.ndp_base_url) as client:
                # Get dataset details
                dataset = await client.get_dataset_details(dataset_id)
                if not dataset:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Dataset with ID '{dataset_id}' not found.")]
                    )
                
                result_text = f"**Geospatial Analysis: {dataset.get('title', dataset.get('name', 'Untitled'))}**\n\n"
                
                # Download and analyze resources
                resources = dataset.get('resources', [])
                csv_data = None
                geojson_data = None
                
                for resource in resources:
                    format_type = resource.get('format', '').upper()
                    
                    if format_type == 'CSV':
                        try:
                            file_content = await client.download_file(resource['url'])
                            csv_data = pd.read_csv(pd.io.common.BytesIO(file_content))
                            result_text += f"✅ Downloaded CSV data: {len(csv_data)} rows, {len(csv_data.columns)} columns\n"
                        except Exception as e:
                            result_text += f"❌ Failed to download CSV: {str(e)}\n"
                    
                    elif format_type == 'GEOJSON':
                        try:
                            file_content = await client.download_file(resource['url'])
                            geojson_data = gpd.read_file(pd.io.common.BytesIO(file_content))
                            result_text += f"✅ Downloaded GeoJSON data: {len(geojson_data)} features\n"
                        except Exception as e:
                            result_text += f"❌ Failed to download GeoJSON: {str(e)}\n"
                
                result_text += "\n**Data Analysis Summary:**\n\n"
                
                # Analyze CSV data
                if csv_data is not None:
                    result_text += "**CSV Data Analysis:**\n"
                    result_text += f"- Shape: {csv_data.shape}\n"
                    result_text += f"- Columns: {list(csv_data.columns)}\n"
                    result_text += f"- Data types:\n"
                    for col, dtype in csv_data.dtypes.items():
                        result_text += f"  - {col}: {dtype}\n"
                    
                    # Basic statistics for numerical columns
                    numeric_cols = csv_data.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        result_text += f"\n- Numerical columns: {list(numeric_cols)}\n"
                        result_text += "- Basic statistics:\n"
                        stats = csv_data[numeric_cols].describe()
                        result_text += stats.to_string()
                        result_text += "\n"
                    
                    # Check for time series data
                    date_cols = []
                    for col in csv_data.columns:
                        if csv_data[col].dtype == 'object':
                            try:
                                pd.to_datetime(csv_data[col])
                                date_cols.append(col)
                            except:
                                pass
                    
                    if date_cols:
                        result_text += f"- Time series columns detected: {date_cols}\n"
                
                # Analyze GeoJSON data
                if geojson_data is not None:
                    result_text += "\n**GeoJSON Data Analysis:**\n"
                    result_text += f"- Geometry type: {geojson_data.geometry.geom_type.unique()}\n"
                    result_text += f"- Coordinate reference system: {geojson_data.crs}\n"
                    result_text += f"- Bounding box: {geojson_data.total_bounds}\n"
                    
                    # Spatial statistics
                    if len(geojson_data) > 0:
                        result_text += f"- Spatial extent:\n"
                        bounds = geojson_data.total_bounds
                        result_text += f"  - Min X: {bounds[0]:.6f}, Min Y: {bounds[1]:.6f}\n"
                        result_text += f"  - Max X: {bounds[2]:.6f}, Max Y: {bounds[3]:.6f}\n"
                
                # Generate insights
                result_text += "\n**Insights and Recommendations:**\n"
                
                if csv_data is not None and geojson_data is not None:
                    result_text += "- This dataset contains both tabular and spatial data\n"
                    result_text += "- Consider creating maps combining the spatial and attribute data\n"
                    result_text += "- Time series analysis may be possible if temporal columns are present\n"
                
                elif csv_data is not None:
                    result_text += "- This is primarily a tabular dataset\n"
                    result_text += "- Consider statistical analysis and visualization of numerical columns\n"
                    if len(numeric_cols) > 0:
                        result_text += "- Time series analysis recommended for temporal data\n"
                
                elif geojson_data is not None:
                    result_text += "- This is a spatial dataset\n"
                    result_text += "- Consider creating maps and spatial analysis\n"
                    result_text += "- Attribute analysis can be performed on non-geometry columns\n"
                
                result_text += "\n**Next Steps:**\n"
                result_text += "1. Use visualization tools to create plots and maps\n"
                result_text += "2. Perform statistical analysis on numerical data\n"
                result_text += "3. Generate time series plots if temporal data is present\n"
                result_text += "4. Create spatial visualizations for geographic data\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
        
        except Exception as e:
            logger.error(f"Error analyzing geospatial data: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error analyzing geospatial data: {str(e)}")]
            )

async def main():
    """Main entry point for the NDP MCP server."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="NDP MCP Server")
    parser.add_argument("--base-url", 
                       default=DEFAULT_NDP_BASE_URL,
                       help=f"NDP API base URL (default: {DEFAULT_NDP_BASE_URL})")
    parser.add_argument("--server", 
                       default=DEFAULT_SERVER_NAME,
                       help=f"NDP server parameter (default: {DEFAULT_SERVER_NAME})")
    parser.add_argument("--chunk-threshold", 
                       type=int,
                       default=DEFAULT_CHUNK_THRESHOLD,
                       help=f"Chunk threshold for large results (default: {DEFAULT_CHUNK_THRESHOLD})")
    
    args = parser.parse_args()
    
    # Create server instance with configuration
    server = NDPMCPServer()
    
    # Update server configuration
    server.ndp_base_url = args.base_url
    server.ndp_server = args.server
    server.chunk_threshold = args.chunk_threshold
    
    # Run as stdio server
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ndp",
                server_version="1.0.0",
                capabilities=server.server.get_capabilities(
                    notification_options=NotificationOptions(
                        tools_changed=False,
                        resources_changed=False,
                        prompts_changed=False,
                    ),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
