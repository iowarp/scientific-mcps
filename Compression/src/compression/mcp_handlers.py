"""
Compression MCP Handlers
Comprehensive compression and decompression functionality with multi-format support.
"""
import os
import sys
import gzip
import bz2
import zipfile
import tarfile
import zlib
import hashlib
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging
from tqdm import tqdm
import shutil
import mimetypes
import subprocess

logger = logging.getLogger(__name__)

class CompressionError(Exception):
    """Custom exception for compression-related errors."""
    pass

def compress_file_handler(
    file_path: str,
    compression_type: str = "gzip",
    output_path: Optional[str] = None,
    compression_level: int = 6,
    preserve_original: bool = True
) -> dict:
    """
    Compress a single file using specified compression algorithm.
    """
    try:
        if not os.path.exists(file_path):
            raise CompressionError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise CompressionError(f"Path is not a file: {file_path}")
        
        # Get file info
        original_size = os.path.getsize(file_path)
        start_time = time.time()
        
        # Generate output path if not provided
        if output_path is None:
            base_path = Path(file_path)
            if compression_type == "gzip":
                output_path = str(base_path.with_suffix(base_path.suffix + ".gz"))
            elif compression_type == "bz2":
                output_path = str(base_path.with_suffix(base_path.suffix + ".bz2"))
            elif compression_type == "zip":
                output_path = str(base_path.with_suffix(".zip"))
            elif compression_type == "zlib":
                output_path = str(base_path.with_suffix(base_path.suffix + ".zlib"))
            else:
                raise CompressionError(f"Unsupported compression type: {compression_type}")
        
        # Perform compression
        if compression_type == "gzip":
            with open(file_path, 'rb') as f_in:
                with gzip.open(output_path, 'wb', compresslevel=compression_level) as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        elif compression_type == "bz2":
            with open(file_path, 'rb') as f_in:
                with bz2.open(output_path, 'wb', compresslevel=compression_level) as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        elif compression_type == "zip":
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zf:
                zf.write(file_path, os.path.basename(file_path))
        
        elif compression_type == "zlib":
            with open(file_path, 'rb') as f_in:
                data = f_in.read()
                compressed_data = zlib.compress(data, compression_level)
                with open(output_path, 'wb') as f_out:
                    f_out.write(compressed_data)
        
        # Calculate results
        compressed_size = os.path.getsize(output_path)
        compression_time = time.time() - start_time
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        # Remove original file if not preserving
        if not preserve_original:
            os.remove(file_path)
        
        return {
            "success": True,
            "input_file": file_path,
            "output_file": output_path,
            "compression_type": compression_type,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(compression_ratio, 2),
            "compression_time": round(compression_time, 3),
            "compression_level": compression_level,
            "original_preserved": preserve_original
        }
    
    except Exception as e:
        logger.error(f"Error compressing file {file_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "input_file": file_path
        }

def decompress_file_handler(
    file_path: str,
    output_path: Optional[str] = None,
    compression_type: Optional[str] = None,
    preserve_original: bool = True
) -> dict:
    """
    Decompress a compressed file with auto-detection or manual specification.
    """
    try:
        if not os.path.exists(file_path):
            raise CompressionError(f"File not found: {file_path}")
        
        # Auto-detect compression type if not specified
        if compression_type is None:
            compression_type = detect_compression_format_handler(file_path)["format"]
        
        # Get file info
        compressed_size = os.path.getsize(file_path)
        start_time = time.time()
        
        # Generate output path if not provided
        if output_path is None:
            base_path = Path(file_path)
            if compression_type == "gzip" and str(base_path).endswith('.gz'):
                output_path = str(base_path.with_suffix(''))
            elif compression_type == "bz2" and str(base_path).endswith('.bz2'):
                output_path = str(base_path.with_suffix(''))
            elif compression_type == "zip":
                output_path = str(base_path.parent / base_path.stem)
            elif compression_type == "zlib":
                output_path = str(base_path.with_suffix(''))
            else:
                output_path = str(base_path.with_suffix('.decompressed'))
        
        # Perform decompression
        if compression_type == "gzip":
            with gzip.open(file_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        elif compression_type == "bz2":
            with bz2.open(file_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        elif compression_type == "zip":
            with zipfile.ZipFile(file_path, 'r') as zf:
                zf.extractall(os.path.dirname(output_path))
                # For single file archives, rename to output_path
                extracted_files = zf.namelist()
                if len(extracted_files) == 1:
                    extracted_path = os.path.join(os.path.dirname(output_path), extracted_files[0])
                    if os.path.exists(extracted_path):
                        os.rename(extracted_path, output_path)
        
        elif compression_type == "zlib":
            with open(file_path, 'rb') as f_in:
                compressed_data = f_in.read()
                decompressed_data = zlib.decompress(compressed_data)
                with open(output_path, 'wb') as f_out:
                    f_out.write(decompressed_data)
        
        # Calculate results
        decompressed_size = os.path.getsize(output_path)
        decompression_time = time.time() - start_time
        
        # Remove original file if not preserving
        if not preserve_original:
            os.remove(file_path)
        
        return {
            "success": True,
            "input_file": file_path,
            "output_file": output_path,
            "compression_type": compression_type,
            "compressed_size": compressed_size,
            "decompressed_size": decompressed_size,
            "decompression_time": round(decompression_time, 3),
            "original_preserved": preserve_original
        }
    
    except Exception as e:
        logger.error(f"Error decompressing file {file_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "input_file": file_path
        }

def compress_directory_handler(
    directory_path: str,
    output_path: Optional[str] = None,
    compression_type: str = "zip",
    compression_level: int = 6,
    exclude_patterns: Optional[List[str]] = None
) -> dict:
    """
    Compress an entire directory into an archive.
    """
    try:
        if not os.path.exists(directory_path):
            raise CompressionError(f"Directory not found: {directory_path}")
        
        if not os.path.isdir(directory_path):
            raise CompressionError(f"Path is not a directory: {directory_path}")
        
        # Generate output path if not provided
        if output_path is None:
            base_name = os.path.basename(directory_path.rstrip('/'))
            if compression_type == "zip":
                output_path = f"{directory_path}.zip"
            elif compression_type == "tar.gz":
                output_path = f"{directory_path}.tar.gz"
            elif compression_type == "tar.bz2":
                output_path = f"{directory_path}.tar.bz2"
            else:
                raise CompressionError(f"Unsupported directory compression type: {compression_type}")
        
        start_time = time.time()
        exclude_patterns = exclude_patterns or []
        
        # Count files for progress tracking
        total_files = sum(len(files) for _, _, files in os.walk(directory_path))
        processed_files = 0
        
        if compression_type == "zip":
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zf:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Check exclude patterns
                        if any(pattern in file_path for pattern in exclude_patterns):
                            continue
                        
                        arc_path = os.path.relpath(file_path, directory_path)
                        zf.write(file_path, arc_path)
                        processed_files += 1
        
        elif compression_type in ["tar.gz", "tar.bz2"]:
            mode = "w:gz" if compression_type == "tar.gz" else "w:bz2"
            with tarfile.open(output_path, mode) as tf:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Check exclude patterns
                        if any(pattern in file_path for pattern in exclude_patterns):
                            continue
                        
                        arc_path = os.path.relpath(file_path, directory_path)
                        tf.add(file_path, arc_path)
                        processed_files += 1
        
        # Calculate results
        compressed_size = os.path.getsize(output_path)
        compression_time = time.time() - start_time
        
        # Calculate original directory size
        original_size = sum(
            os.path.getsize(os.path.join(root, file))
            for root, dirs, files in os.walk(directory_path)
            for file in files
        )
        
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        return {
            "success": True,
            "input_directory": directory_path,
            "output_archive": output_path,
            "compression_type": compression_type,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(compression_ratio, 2),
            "compression_time": round(compression_time, 3),
            "files_processed": processed_files,
            "total_files": total_files,
            "excluded_patterns": exclude_patterns
        }
    
    except Exception as e:
        logger.error(f"Error compressing directory {directory_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "input_directory": directory_path
        }

def extract_archive_handler(
    archive_path: str,
    output_directory: Optional[str] = None,
    password: Optional[str] = None
) -> dict:
    """
    Extract files from an archive.
    """
    try:
        if not os.path.exists(archive_path):
            raise CompressionError(f"Archive not found: {archive_path}")
        
        # Auto-detect archive type
        archive_type = detect_compression_format_handler(archive_path)["format"]
        
        # Set output directory
        if output_directory is None:
            output_directory = os.path.dirname(archive_path)
        
        start_time = time.time()
        extracted_files = []
        
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                if password:
                    zf.setpassword(password.encode())
                zf.extractall(output_directory)
                extracted_files = zf.namelist()
        
        elif archive_type == "tar.gz":
            with tarfile.open(archive_path, 'r:gz') as tf:
                tf.extractall(output_directory)
                extracted_files = tf.getnames()
        
        elif archive_type == "tar.bz2":
            with tarfile.open(archive_path, 'r:bz2') as tf:
                tf.extractall(output_directory)
                extracted_files = tf.getnames()
        
        extraction_time = time.time() - start_time
        
        return {
            "success": True,
            "archive_path": archive_path,
            "output_directory": output_directory,
            "archive_type": archive_type,
            "extracted_files": extracted_files,
            "files_extracted": len(extracted_files),
            "extraction_time": round(extraction_time, 3)
        }
    
    except Exception as e:
        logger.error(f"Error extracting archive {archive_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "archive_path": archive_path
        }

def list_archive_contents_handler(
    archive_path: str,
    password: Optional[str] = None
) -> dict:
    """
    List the contents of an archive without extracting.
    """
    try:
        if not os.path.exists(archive_path):
            raise CompressionError(f"Archive not found: {archive_path}")
        
        # Auto-detect archive type
        archive_type = detect_compression_format_handler(archive_path)["format"]
        
        contents = []
        
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                if password:
                    zf.setpassword(password.encode())
                for info in zf.infolist():
                    contents.append({
                        "filename": info.filename,
                        "file_size": info.file_size,
                        "compress_size": info.compress_size,
                        "date_time": info.date_time,
                        "is_dir": info.is_dir()
                    })
        
        elif archive_type in ["tar.gz", "tar.bz2"]:
            with tarfile.open(archive_path, 'r:*') as tf:
                for info in tf.getmembers():
                    contents.append({
                        "filename": info.name,
                        "file_size": info.size,
                        "is_dir": info.isdir(),
                        "is_file": info.isfile(),
                        "mode": info.mode
                    })
        
        return {
            "success": True,
            "archive_path": archive_path,
            "archive_type": archive_type,
            "contents": contents,
            "total_files": len(contents)
        }
    
    except Exception as e:
        logger.error(f"Error listing archive contents {archive_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "archive_path": archive_path
        }

def batch_compress_handler(
    file_paths: List[str],
    compression_type: str = "gzip",
    output_directory: Optional[str] = None,
    compression_level: int = 6,
    preserve_original: bool = True
) -> dict:
    """
    Compress multiple files in batch with progress tracking.
    """
    try:
        results = []
        total_original_size = 0
        total_compressed_size = 0
        successful_compressions = 0
        failed_compressions = 0
        
        start_time = time.time()
        
        for file_path in tqdm(file_paths, desc="Compressing files"):
            if output_directory:
                filename = os.path.basename(file_path)
                if compression_type == "gzip":
                    output_path = os.path.join(output_directory, f"{filename}.gz")
                elif compression_type == "bz2":
                    output_path = os.path.join(output_directory, f"{filename}.bz2")
                elif compression_type == "zip":
                    output_path = os.path.join(output_directory, f"{filename}.zip")
                elif compression_type == "zlib":
                    output_path = os.path.join(output_directory, f"{filename}.zlib")
                else:
                    output_path = None
            else:
                output_path = None
            
            result = compress_file_handler(file_path, compression_type, output_path, compression_level, preserve_original)
            results.append(result)
            
            if result["success"]:
                successful_compressions += 1
                total_original_size += result["original_size"]
                total_compressed_size += result["compressed_size"]
            else:
                failed_compressions += 1
        
        batch_time = time.time() - start_time
        overall_compression_ratio = (1 - total_compressed_size / total_original_size) * 100 if total_original_size > 0 else 0
        
        return {
            "success": True,
            "batch_results": results,
            "summary": {
                "total_files": len(file_paths),
                "successful_compressions": successful_compressions,
                "failed_compressions": failed_compressions,
                "total_original_size": total_original_size,
                "total_compressed_size": total_compressed_size,
                "overall_compression_ratio": round(overall_compression_ratio, 2),
                "batch_time": round(batch_time, 3),
                "compression_type": compression_type
            }
        }
    
    except Exception as e:
        logger.error(f"Error in batch compression: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "file_paths": file_paths
        }

def verify_integrity_handler(
    file_path: str,
    expected_checksum: Optional[str] = None,
    checksum_algorithm: str = "md5"
) -> dict:
    """
    Verify the integrity of a file using checksums.
    """
    try:
        if not os.path.exists(file_path):
            raise CompressionError(f"File not found: {file_path}")
        
        # Calculate checksum
        if checksum_algorithm == "md5":
            hasher = hashlib.md5()
        elif checksum_algorithm == "sha1":
            hasher = hashlib.sha1()
        elif checksum_algorithm == "sha256":
            hasher = hashlib.sha256()
        else:
            raise CompressionError(f"Unsupported checksum algorithm: {checksum_algorithm}")
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        
        calculated_checksum = hasher.hexdigest()
        
        # Verify if expected checksum is provided
        is_valid = None
        if expected_checksum:
            is_valid = calculated_checksum.lower() == expected_checksum.lower()
        
        return {
            "success": True,
            "file_path": file_path,
            "checksum_algorithm": checksum_algorithm,
            "calculated_checksum": calculated_checksum,
            "expected_checksum": expected_checksum,
            "is_valid": is_valid,
            "file_size": os.path.getsize(file_path)
        }
    
    except Exception as e:
        logger.error(f"Error verifying integrity of {file_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }

def get_compression_stats_handler(file_path: str) -> dict:
    """
    Get detailed compression statistics and recommendations for a file.
    """
    try:
        if not os.path.exists(file_path):
            raise CompressionError(f"File not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        file_type = mimetypes.guess_type(file_path)[0] or "unknown"
        
        # Test different compression algorithms
        algorithms = ["gzip", "bz2", "zlib"]
        stats = {}
        
        for algo in algorithms:
            try:
                temp_compressed = f"{file_path}.{algo}_test"
                result = compress_file_handler(file_path, algo, temp_compressed, 6, True)
                
                if result["success"]:
                    stats[algo] = {
                        "compressed_size": result["compressed_size"],
                        "compression_ratio": result["compression_ratio"],
                        "compression_time": result["compression_time"]
                    }
                    # Clean up test file
                    if os.path.exists(temp_compressed):
                        os.remove(temp_compressed)
                else:
                    stats[algo] = {"error": result["error"]}
            except Exception as e:
                stats[algo] = {"error": str(e)}
        
        # Determine best algorithm
        best_ratio = max(stats.items(), key=lambda x: x[1].get("compression_ratio", 0) if "error" not in x[1] else 0)
        best_speed = min(stats.items(), key=lambda x: x[1].get("compression_time", float('inf')) if "error" not in x[1] else float('inf'))
        
        return {
            "success": True,
            "file_path": file_path,
            "file_size": file_size,
            "file_type": file_type,
            "compression_stats": stats,
            "recommendations": {
                "best_compression_ratio": best_ratio[0],
                "fastest_compression": best_speed[0]
            }
        }
    
    except Exception as e:
        logger.error(f"Error getting compression stats for {file_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }

def create_password_protected_archive_handler(
    file_paths: List[str],
    archive_path: str,
    password: str,
    compression_type: str = "zip"
) -> dict:
    """
    Create a password-protected archive.
    """
    try:
        if compression_type != "zip":
            raise CompressionError("Password protection is only supported for ZIP archives")
        
        start_time = time.time()
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.setpassword(password.encode())
            
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    logger.warning(f"File not found: {file_path}")
                    continue
                
                if os.path.isfile(file_path):
                    zf.write(file_path, os.path.basename(file_path))
                elif os.path.isdir(file_path):
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            arc_path = os.path.relpath(full_path, os.path.dirname(file_path))
                            zf.write(full_path, arc_path)
        
        archive_size = os.path.getsize(archive_path)
        creation_time = time.time() - start_time
        
        return {
            "success": True,
            "archive_path": archive_path,
            "file_paths": file_paths,
            "archive_size": archive_size,
            "creation_time": round(creation_time, 3),
            "password_protected": True
        }
    
    except Exception as e:
        logger.error(f"Error creating password-protected archive: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "archive_path": archive_path
        }

def stream_compress_handler(
    input_path: str,
    output_path: str,
    compression_type: str = "gzip",
    chunk_size: int = 8192,
    compression_level: int = 6
) -> dict:
    """
    Compress a file using streaming for memory efficiency.
    """
    try:
        if not os.path.exists(input_path):
            raise CompressionError(f"File not found: {input_path}")
        
        start_time = time.time()
        total_bytes_read = 0
        total_bytes_written = 0
        
        if compression_type == "gzip":
            with open(input_path, 'rb') as f_in:
                with gzip.open(output_path, 'wb', compresslevel=compression_level) as f_out:
                    while True:
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        f_out.write(chunk)
                        total_bytes_read += len(chunk)
                        total_bytes_written += len(chunk)  # Approximate
        
        elif compression_type == "bz2":
            with open(input_path, 'rb') as f_in:
                with bz2.open(output_path, 'wb', compresslevel=compression_level) as f_out:
                    while True:
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        f_out.write(chunk)
                        total_bytes_read += len(chunk)
        
        elif compression_type == "zlib":
            compressor = zlib.compressobj(compression_level)
            with open(input_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    while True:
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        compressed_chunk = compressor.compress(chunk)
                        if compressed_chunk:
                            f_out.write(compressed_chunk)
                        total_bytes_read += len(chunk)
                    
                    # Write final compressed data
                    final_chunk = compressor.flush()
                    if final_chunk:
                        f_out.write(final_chunk)
        
        compressed_size = os.path.getsize(output_path)
        compression_time = time.time() - start_time
        compression_ratio = (1 - compressed_size / total_bytes_read) * 100 if total_bytes_read > 0 else 0
        
        return {
            "success": True,
            "input_path": input_path,
            "output_path": output_path,
            "compression_type": compression_type,
            "original_size": total_bytes_read,
            "compressed_size": compressed_size,
            "compression_ratio": round(compression_ratio, 2),
            "compression_time": round(compression_time, 3),
            "chunk_size": chunk_size,
            "streaming": True
        }
    
    except Exception as e:
        logger.error(f"Error in stream compression: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "input_path": input_path
        }

def detect_compression_format_handler(file_path: str) -> dict:
    """
    Auto-detect the compression format of a file.
    """
    try:
        if not os.path.exists(file_path):
            raise CompressionError(f"File not found: {file_path}")
        
        # Check file extension first
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Check magic bytes
        with open(file_path, 'rb') as f:
            magic_bytes = f.read(10)
        
        format_detected = "unknown"
        confidence = "low"
        
        # Detect based on magic bytes
        if magic_bytes.startswith(b'\x1f\x8b'):
            format_detected = "gzip"
            confidence = "high"
        elif magic_bytes.startswith(b'BZ'):
            format_detected = "bz2"
            confidence = "high"
        elif magic_bytes.startswith(b'PK'):
            format_detected = "zip"
            confidence = "high"
        elif magic_bytes.startswith(b'\x78\x9c') or magic_bytes.startswith(b'\x78\xda'):
            format_detected = "zlib"
            confidence = "high"
        elif file_ext == '.gz':
            format_detected = "gzip"
            confidence = "medium"
        elif file_ext == '.bz2':
            format_detected = "bz2"
            confidence = "medium"
        elif file_ext == '.zip':
            format_detected = "zip"
            confidence = "medium"
        elif file_ext in ['.tar.gz', '.tgz']:
            format_detected = "tar.gz"
            confidence = "medium"
        elif file_ext in ['.tar.bz2', '.tbz2']:
            format_detected = "tar.bz2"
            confidence = "medium"
        
        return {
            "success": True,
            "file_path": file_path,
            "format": format_detected,
            "confidence": confidence,
            "file_extension": file_ext,
            "magic_bytes": magic_bytes.hex()
        }
    
    except Exception as e:
        logger.error(f"Error detecting compression format for {file_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }
