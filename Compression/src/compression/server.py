#!/usr/bin/env python3
"""
Enhanced Compression MCP Server with comprehensive compression and decompression capabilities.
Provides gzip, zip, zlib, bz2 compression with batch processing, directory compression,
integrity verification, and cross-platform support.
"""
import os
import sys
import json
import argparse
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging
from typing import Optional, List, Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from . import mcp_handlers

# Initialize MCP server
mcp = FastMCP("CompressionMCP")

@mcp.tool(
    name="compress_file",
    description="Compress individual files using advanced compression algorithms with optimization options. Supports gzip, zip, bz2, zlib with configurable compression levels, integrity verification, and comprehensive performance metrics for efficient file storage."
)
async def compress_file_tool(
    file_path: str,
    compression_type: str = "gzip",
    output_path: Optional[str] = None,
    compression_level: int = 6,
    preserve_original: bool = True
) -> dict:
    """
    Compress a single file with advanced compression options and integrity verification.
    
    Args:
        file_path: Absolute path to the file to compress
        compression_type: Compression algorithm (gzip, zip, bz2, zlib)
                         - gzip: Fast compression with good ratios
                         - zip: Universal compatibility with metadata preservation
                         - bz2: High compression ratio, slower processing
                         - zlib: Lightweight compression for streaming data
        output_path: Absolute path for compressed file (None for auto-generated with extension)
        compression_level: Compression level (1-9: 1=fastest, 9=best compression, 6=balanced)
        preserve_original: Whether to keep the original file after compression
    
    Returns:
        Dictionary containing:
        - compression_info: Detailed compression statistics and ratios
        - file_details: Original and compressed file sizes and locations
        - performance_metrics: Compression speed and efficiency measurements
        - integrity_check: Verification of compressed file integrity
    """
    logger.info(f"Compressing file: {file_path} with {compression_type}")
    return mcp_handlers.compress_file_handler(file_path, compression_type, output_path, compression_level, preserve_original)

@mcp.tool(
    name="decompress_file",
    description="Decompress compressed files with automatic format detection and integrity verification. Supports all major compression formats with comprehensive error handling, metadata preservation, and detailed decompression analytics."
)
async def decompress_file_tool(
    file_path: str,
    output_path: Optional[str] = None,
    compression_type: Optional[str] = None,
    preserve_original: bool = True
) -> dict:
    """
    Decompress a compressed file with automatic format detection and verification.
    
    Args:
        file_path: Absolute path to the compressed file
        output_path: Absolute path for decompressed file (None for auto-generated)
        compression_type: Compression format (None for auto-detection from file extension/header)
        preserve_original: Whether to keep the compressed file after decompression
    
    Returns:
        Dictionary containing:
        - decompression_info: Detailed decompression statistics and verification
        - file_details: Original and decompressed file sizes and locations
        - performance_metrics: Decompression speed and efficiency measurements
        - integrity_verification: Comprehensive integrity checks and validation results
    """
    logger.info(f"Decompressing file: {file_path}")
    return mcp_handlers.decompress_file_handler(file_path, output_path, compression_type, preserve_original)

@mcp.tool(
    name="compress_directory",
    description="Compress entire directories into archives with advanced filtering and optimization. Supports zip, tar.gz, tar.bz2 formats with exclude patterns, recursive compression, and comprehensive directory structure preservation."
)
async def compress_directory_tool(
    directory_path: str,
    output_path: Optional[str] = None,
    compression_type: str = "zip",
    compression_level: int = 6,
    exclude_patterns: Optional[List[str]] = None
) -> dict:
    """
    Compress a directory into an archive with advanced filtering and optimization.
    
    Args:
        directory_path: Absolute path to the directory to compress
        output_path: Absolute path for compressed archive (None for auto-generated)
        compression_type: Archive format (zip, tar.gz, tar.bz2)
                         - zip: Universal compatibility with folder structure
                         - tar.gz: Unix standard with gzip compression
                         - tar.bz2: High compression ratio with bzip2
        compression_level: Compression level (1-9: 1=fastest, 9=best compression, 6=balanced)
        exclude_patterns: List of patterns to exclude (e.g., ['*.tmp', '__pycache__/*'])
    
    Returns:
        Dictionary containing:
        - archive_info: Detailed archive statistics and file counts
        - compression_metrics: Space savings and compression ratios
        - file_structure: Preserved directory structure and metadata
        - performance_stats: Compression speed and efficiency measurements
    """
    logger.info(f"Compressing directory: {directory_path}")
    return mcp_handlers.compress_directory_handler(directory_path, output_path, compression_type, compression_level, exclude_patterns)

@mcp.tool(
    name="extract_archive",
    description="Extract files from compressed archives with comprehensive format support and security features. Handles zip, tar.gz, tar.bz2 with password protection, selective extraction, and detailed extraction verification."
)
async def extract_archive_tool(
    archive_path: str,
    output_directory: Optional[str] = None,
    password: Optional[str] = None
) -> dict:
    """
    Extract files from an archive with comprehensive format support and security.
    
    Args:
        archive_path: Absolute path to the archive file
        output_directory: Absolute path to extract files to (None for current directory)
        password: Password for encrypted archives (zip encryption support)
    
    Returns:
        Dictionary containing:
        - extraction_info: Detailed extraction statistics and file counts
        - file_list: Complete list of extracted files with metadata
        - security_check: Archive integrity and security validation results
        - performance_metrics: Extraction speed and efficiency measurements
    """
    logger.info(f"Extracting archive: {archive_path}")
    return mcp_handlers.extract_archive_handler(archive_path, output_directory, password)

@mcp.tool(
    name="list_archive_contents",
    description="List and analyze archive contents without extraction with comprehensive metadata inspection. Provides detailed file information, directory structure analysis, and archive integrity verification for all supported formats."
)
async def list_archive_contents_tool(
    archive_path: str,
    password: Optional[str] = None
) -> dict:
    """
    List and analyze archive contents with comprehensive metadata inspection.
    
    Args:
        archive_path: Absolute path to the archive file
        password: Password for encrypted archives (if applicable)
    
    Returns:
        Dictionary containing:
        - file_list: Complete directory structure with file details
        - archive_metadata: Archive format, compression ratios, and statistics
        - content_analysis: File type distribution and size analysis
        - integrity_status: Archive integrity and corruption checks
    """
    logger.info(f"Listing archive contents: {archive_path}")
    return mcp_handlers.list_archive_contents_handler(archive_path, password)

@mcp.tool(
    name="batch_compress",
    description="Compress multiple files in batch operations with progress tracking and parallel processing. Supports bulk compression with comprehensive error handling, optimization strategies, and detailed progress reporting for large-scale operations."
)
async def batch_compress_tool(
    file_paths: List[str],
    compression_type: str = "gzip",
    output_directory: Optional[str] = None,
    compression_level: int = 6,
    preserve_original: bool = True
) -> dict:
    """
    Compress multiple files in batch with advanced processing and tracking.
    
    Args:
        file_paths: List of absolute paths to files to compress
        compression_type: Compression algorithm (gzip, zip, bz2, zlib)
        output_directory: Absolute path to save compressed files (None for same directory)
        compression_level: Compression level (1-9: 1=fastest, 9=best compression)
        preserve_original: Whether to keep original files after compression
    
    Returns:
        Dictionary containing:
        - batch_summary: Overall batch processing statistics and results
        - individual_results: Detailed results for each file processed
        - performance_metrics: Total processing time and throughput rates
        - error_handling: Any errors encountered with recovery suggestions
    """
    logger.info(f"Batch compressing {len(file_paths)} files with {compression_type}")
    return mcp_handlers.batch_compress_handler(file_paths, compression_type, output_directory, compression_level, preserve_original)

@mcp.tool(
    name="verify_integrity",
    description="Verify the integrity of compressed files using advanced checksum algorithms and comprehensive validation. Provides detailed integrity checking with multiple hash algorithms and corruption detection capabilities."
)
async def verify_integrity_tool(
    file_path: str,
    expected_checksum: Optional[str] = None,
    checksum_algorithm: str = "md5"
) -> dict:
    """
    Verify the integrity of a compressed file with comprehensive validation.
    
    Args:
        file_path: Absolute path to the file to verify
        expected_checksum: Expected checksum value (None to calculate and return checksum)
        checksum_algorithm: Checksum algorithm (md5, sha1, sha256, sha512)
    
    Returns:
        Dictionary containing:
        - integrity_status: Overall integrity verification result
        - checksum_info: Calculated checksums and comparison results
        - file_analysis: File corruption analysis and health assessment
        - security_validation: Security-focused integrity and authenticity checks
    """
    logger.info(f"Verifying integrity of: {file_path}")
    return mcp_handlers.verify_integrity_handler(file_path, expected_checksum, checksum_algorithm)

@mcp.tool(
    name="get_compression_stats",
    description="Get comprehensive compression statistics and performance analysis with detailed metrics and optimization recommendations. Provides in-depth analysis of compression efficiency, file characteristics, and algorithm performance."
)
async def get_compression_stats_tool(
    file_path: str
) -> dict:
    """
    Get comprehensive compression statistics and performance analysis.
    
    Args:
        file_path: Absolute path to the file to analyze
    
    Returns:
        Dictionary containing:
        - compression_metrics: Detailed compression ratios and space savings
        - performance_analysis: Speed and efficiency measurements
        - optimization_recommendations: Suggestions for optimal compression settings
        - file_characteristics: Analysis of file properties affecting compression
    """
    logger.info(f"Getting compression stats for: {file_path}")
    return mcp_handlers.get_compression_stats_handler(file_path)

@mcp.tool(
    name="create_password_protected_archive",
    description="Create secure password-protected archives with advanced encryption and compression capabilities. Supports ZIP format with AES encryption, password strength validation, and comprehensive security features for sensitive data protection."
)
async def create_password_protected_archive_tool(
    file_paths: List[str],
    archive_path: str,
    password: str,
    compression_type: str = "zip"
) -> dict:
    """
    Create a password-protected archive.
    
    Args:
        file_paths: List of file paths to include in archive
        archive_path: Path for the output archive
        password: Password to protect the archive
        compression_type: Type of archive (zip)
    
    Returns:
        Dictionary with archive creation results
    """
    logger.info(f"Creating password-protected archive: {archive_path}")
    return mcp_handlers.create_password_protected_archive_handler(file_paths, archive_path, password, compression_type)

@mcp.tool(
    name="stream_compress",
    description="Memory-efficient streaming compression for large files with chunked processing and progress tracking. Optimizes memory usage through buffer management, supports configurable chunk sizes, and provides real-time compression statistics for optimal performance."
)
async def stream_compress_tool(
    input_path: str,
    output_path: str,
    compression_type: str = "gzip",
    chunk_size: int = 8192,
    compression_level: int = 6
) -> dict:
    """
    Compress a file using streaming for memory efficiency.
    
    Args:
        input_path: Path to the input file
        output_path: Path for the compressed output
        compression_type: Type of compression (gzip, bz2, zlib)
        chunk_size: Size of chunks to process (bytes)
        compression_level: Compression level (1-9, default 6)
    
    Returns:
        Dictionary with streaming compression results
    """
    logger.info(f"Stream compressing: {input_path} -> {output_path}")
    return mcp_handlers.stream_compress_handler(input_path, output_path, compression_type, chunk_size, compression_level)

@mcp.tool(
    name="detect_compression_format",
    description="Intelligent compression format detection through file header analysis and magic number identification. Automatically identifies compression types (gzip, bz2, zip, zlib, tar) with detailed format information, compression ratios, and compatibility analysis."
)
async def detect_compression_format_tool(
    file_path: str
) -> dict:
    """
    Detect the compression format of a file.
    
    Args:
        file_path: Path to the file to analyze
    
    Returns:
        Dictionary with detected format and file information
    """
    logger.info(f"Detecting compression format for: {file_path}")
    return mcp_handlers.detect_compression_format_handler(file_path)

def main():
    """
    Main entry point for the Compression MCP server.
    Supports both stdio and SSE transports based on environment variables or command line arguments.
    """
    parser = argparse.ArgumentParser(description="Compression MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default=None,
        help="Transport protocol (stdio or sse)"
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host for SSE transport (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("Starting Compression MCP Server")
        
        # Use command-line args or environment variables
        transport = args.transport or os.getenv("MCP_TRANSPORT", "stdio").lower()
        
        if transport == "sse":
            # SSE transport for web-based clients
            host = args.host or os.getenv("MCP_SSE_HOST", "localhost")
            port = args.port or int(os.getenv("MCP_SSE_PORT", "8000"))
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
