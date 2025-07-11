"""
Test suite for Compression MCP handlers
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compression.mcp_handlers import (
    compress_file_handler,
    decompress_file_handler,
    compress_directory_handler,
    extract_archive_handler,
    list_archive_contents_handler,
    batch_compress_handler,
    verify_integrity_handler,
    get_compression_stats_handler,
    create_password_protected_archive_handler,
    stream_compress_handler,
    detect_compression_format_handler
)

class TestCompressionHandlers:
    """Test class for compression handlers"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_file(self, temp_dir):
        """Create a sample file for testing"""
        file_path = os.path.join(temp_dir, "sample.txt")
        with open(file_path, 'w') as f:
            f.write("This is a sample file for compression testing.\n" * 100)
        return file_path
    
    @pytest.fixture
    def sample_directory(self, temp_dir):
        """Create a sample directory with files for testing"""
        dir_path = os.path.join(temp_dir, "sample_dir")
        os.makedirs(dir_path)
        
        # Create some files
        for i in range(3):
            file_path = os.path.join(dir_path, f"file_{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"Content of file {i}\n" * 50)
        
        return dir_path
    
    def test_compress_file_gzip(self, sample_file, temp_dir):
        """Test gzip compression of a single file"""
        output_path = os.path.join(temp_dir, "compressed.gz")
        
        result = compress_file_handler(
            sample_file,
            compression_type="gzip",
            output_path=output_path
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["compression_type"] == "gzip"
        assert result["compressed_size"] < result["original_size"]
        assert result["compression_ratio"] > 0
    
    def test_compress_file_bz2(self, sample_file, temp_dir):
        """Test bz2 compression of a single file"""
        output_path = os.path.join(temp_dir, "compressed.bz2")
        
        result = compress_file_handler(
            sample_file,
            compression_type="bz2",
            output_path=output_path
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["compression_type"] == "bz2"
    
    def test_compress_file_zip(self, sample_file, temp_dir):
        """Test zip compression of a single file"""
        output_path = os.path.join(temp_dir, "compressed.zip")
        
        result = compress_file_handler(
            sample_file,
            compression_type="zip",
            output_path=output_path
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["compression_type"] == "zip"
    
    def test_compress_file_zlib(self, sample_file, temp_dir):
        """Test zlib compression of a single file"""
        output_path = os.path.join(temp_dir, "compressed.zlib")
        
        result = compress_file_handler(
            sample_file,
            compression_type="zlib",
            output_path=output_path
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["compression_type"] == "zlib"
    
    def test_decompress_file_gzip(self, sample_file, temp_dir):
        """Test gzip decompression"""
        # First compress
        compressed_path = os.path.join(temp_dir, "compressed.gz")
        compress_result = compress_file_handler(
            sample_file,
            compression_type="gzip",
            output_path=compressed_path
        )
        assert compress_result["success"] is True
        
        # Then decompress
        decompressed_path = os.path.join(temp_dir, "decompressed.txt")
        decompress_result = decompress_file_handler(
            compressed_path,
            output_path=decompressed_path
        )
        
        assert decompress_result["success"] is True
        assert os.path.exists(decompressed_path)
        
        # Verify content
        with open(sample_file, 'r') as f1, open(decompressed_path, 'r') as f2:
            assert f1.read() == f2.read()
    
    def test_compress_directory_zip(self, sample_directory, temp_dir):
        """Test directory compression to zip"""
        output_path = os.path.join(temp_dir, "directory.zip")
        
        result = compress_directory_handler(
            sample_directory,
            output_path=output_path,
            compression_type="zip"
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["files_processed"] == 3
    
    def test_compress_directory_tar_gz(self, sample_directory, temp_dir):
        """Test directory compression to tar.gz"""
        output_path = os.path.join(temp_dir, "directory.tar.gz")
        
        result = compress_directory_handler(
            sample_directory,
            output_path=output_path,
            compression_type="tar.gz"
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["files_processed"] == 3
    
    def test_extract_archive_zip(self, sample_directory, temp_dir):
        """Test zip archive extraction"""
        # First create archive
        archive_path = os.path.join(temp_dir, "test.zip")
        compress_result = compress_directory_handler(
            sample_directory,
            output_path=archive_path,
            compression_type="zip"
        )
        assert compress_result["success"] is True
        
        # Extract
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir)
        
        extract_result = extract_archive_handler(
            archive_path,
            output_directory=extract_dir
        )
        
        assert extract_result["success"] is True
        assert extract_result["files_extracted"] == 3
    
    def test_list_archive_contents_zip(self, sample_directory, temp_dir):
        """Test listing zip archive contents"""
        # First create archive
        archive_path = os.path.join(temp_dir, "test.zip")
        compress_result = compress_directory_handler(
            sample_directory,
            output_path=archive_path,
            compression_type="zip"
        )
        assert compress_result["success"] is True
        
        # List contents
        list_result = list_archive_contents_handler(archive_path)
        
        assert list_result["success"] is True
        assert list_result["total_files"] == 3
        assert len(list_result["contents"]) == 3
    
    def test_batch_compress(self, temp_dir):
        """Test batch compression of multiple files"""
        # Create multiple files
        file_paths = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"file_{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"Content of file {i}\n" * 20)
            file_paths.append(file_path)
        
        result = batch_compress_handler(
            file_paths,
            compression_type="gzip",
            output_directory=temp_dir
        )
        
        assert result["success"] is True
        assert result["summary"]["total_files"] == 3
        assert result["summary"]["successful_compressions"] == 3
        assert result["summary"]["failed_compressions"] == 0
    
    def test_verify_integrity(self, sample_file):
        """Test file integrity verification"""
        result = verify_integrity_handler(sample_file)
        
        assert result["success"] is True
        assert "calculated_checksum" in result
        assert result["checksum_algorithm"] == "md5"
        assert result["file_size"] > 0
    
    def test_get_compression_stats(self, sample_file):
        """Test getting compression statistics"""
        result = get_compression_stats_handler(sample_file)
        
        assert result["success"] is True
        assert "compression_stats" in result
        assert "recommendations" in result
        assert result["file_size"] > 0
    
    def test_stream_compress(self, sample_file, temp_dir):
        """Test streaming compression"""
        output_path = os.path.join(temp_dir, "stream_compressed.gz")
        
        result = stream_compress_handler(
            sample_file,
            output_path,
            compression_type="gzip",
            chunk_size=1024
        )
        
        assert result["success"] is True
        assert os.path.exists(output_path)
        assert result["streaming"] is True
    
    def test_detect_compression_format(self, sample_file, temp_dir):
        """Test compression format detection"""
        # Create a gzip file
        compressed_path = os.path.join(temp_dir, "test.gz")
        compress_result = compress_file_handler(
            sample_file,
            compression_type="gzip",
            output_path=compressed_path
        )
        assert compress_result["success"] is True
        
        # Detect format
        detect_result = detect_compression_format_handler(compressed_path)
        
        assert detect_result["success"] is True
        assert detect_result["format"] == "gzip"
        assert detect_result["confidence"] == "high"
    
    def test_create_password_protected_archive(self, sample_file, temp_dir):
        """Test creating password-protected archive"""
        archive_path = os.path.join(temp_dir, "protected.zip")
        
        result = create_password_protected_archive_handler(
            [sample_file],
            archive_path,
            password="test123"
        )
        
        assert result["success"] is True
        assert os.path.exists(archive_path)
        assert result["password_protected"] is True
    
    def test_error_handling_nonexistent_file(self, temp_dir):
        """Test error handling for nonexistent files"""
        nonexistent_file = os.path.join(temp_dir, "nonexistent.txt")
        
        result = compress_file_handler(nonexistent_file)
        
        assert result["success"] is False
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_error_handling_invalid_compression_type(self, sample_file):
        """Test error handling for invalid compression type"""
        result = compress_file_handler(
            sample_file,
            compression_type="invalid_type"
        )
        
        assert result["success"] is False
        assert "error" in result
    
    def test_compression_levels(self, sample_file, temp_dir):
        """Test different compression levels"""
        results = []
        
        for level in [1, 6, 9]:
            output_path = os.path.join(temp_dir, f"compressed_level_{level}.gz")
            result = compress_file_handler(
                sample_file,
                compression_type="gzip",
                output_path=output_path,
                compression_level=level
            )
            
            assert result["success"] is True
            results.append(result)
        
        # Level 9 should have better compression than level 1
        assert results[2]["compression_ratio"] >= results[0]["compression_ratio"]
    
    def test_preserve_original_false(self, sample_file, temp_dir):
        """Test compression without preserving original file"""
        # Create a copy to test with
        test_file = os.path.join(temp_dir, "test_copy.txt")
        shutil.copy2(sample_file, test_file)
        
        result = compress_file_handler(
            test_file,
            compression_type="gzip",
            preserve_original=False
        )
        
        assert result["success"] is True
        assert not os.path.exists(test_file)  # Original should be removed
        assert result["original_preserved"] is False

if __name__ == "__main__":
    pytest.main([__file__])
