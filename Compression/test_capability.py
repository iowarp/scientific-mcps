#!/usr/bin/env python3
"""
Compression MCP Data Demonstration
Shows practical examples of compression operations using data folder files
"""
import os
import tempfile
import shutil
from pathlib import Path
import sys
from tabulate import tabulate

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from compression.mcp_handlers import (
    compress_file_handler,
    decompress_file_handler,
    get_compression_stats_handler,
    batch_compress_handler,
    create_password_protected_archive_handler,
    verify_integrity_handler
)

def demonstrate_compression_with_data():
    """Demonstrate compression capabilities with actual data files"""
    
    print("📊 COMPRESSION MCP DEMONSTRATION")
    print("=" * 60)
    
    # Get data directory
    data_dir = Path(__file__).parent / "data"
    
    # Available files
    files = [
        "data.csv",
        "huge_log.txt",
        "output.log", 
        "small_log.txt",
        "weather_data.parquet"
    ]
    
    # Filter existing files
    existing_files = [f for f in files if (data_dir / f).exists()]
    
    print(f"📁 Data Directory: {data_dir}")
    print(f"📄 Available Files: {len(existing_files)}")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1. File Analysis
        print("\n🔍 FILE ANALYSIS")
        print("-" * 40)
        
        analysis_data = []
        for filename in existing_files:
            file_path = data_dir / filename
            file_size = file_path.stat().st_size
            
            # Get compression stats
            stats = get_compression_stats_handler(str(file_path))
            
            if stats["success"]:
                compression_stats = stats.get("compression_stats", {})
                
                # Get best compression ratios
                gzip_ratio = compression_stats.get("gzip", {}).get("compression_ratio", 0)
                bz2_ratio = compression_stats.get("bz2", {}).get("compression_ratio", 0)
                
                recommendations = stats.get("recommendations", {})
                best_ratio = recommendations.get("best_compression_ratio", "N/A")
                fastest = recommendations.get("fastest_compression", "N/A")
                
                analysis_data.append([
                    filename,
                    f"{file_size:,}",
                    f"{gzip_ratio:.1f}%",
                    f"{bz2_ratio:.1f}%", 
                    best_ratio,
                    fastest
                ])
        
        headers = ["File", "Size", "Gzip", "Bz2", "Best Ratio", "Fastest"]
        print(tabulate(analysis_data, headers=headers, tablefmt="grid"))
        
        # 2. Compression Examples
        print("\n🗜️  COMPRESSION EXAMPLES")
        print("-" * 40)
        
        # Example 1: CSV file compression
        csv_file = data_dir / "data.csv"
        if csv_file.exists():
            print(f"\n📄 Compressing CSV file: {csv_file.name}")
            
            for algo in ["gzip", "bz2", "zip"]:
                result = compress_file_handler(
                    str(csv_file),
                    compression_type=algo,
                    output_path=os.path.join(temp_dir, f"data.{algo}"),
                    preserve_original=True
                )
                
                if result["success"]:
                    print(f"  ✅ {algo.upper():>4}: {result['original_size']:>6,} → {result['compressed_size']:>6,} bytes ({result['compression_ratio']:>5.1f}% reduction)")
                    
                    # Clean up
                    if os.path.exists(result["output_file"]):
                        os.remove(result["output_file"])
        
        # Example 2: Log file compression
        log_file = data_dir / "huge_log.txt"
        if log_file.exists():
            print(f"\n📄 Compressing log file: {log_file.name}")
            
            result = compress_file_handler(
                str(log_file),
                compression_type="gzip",
                compression_level=9,  # Maximum compression
                preserve_original=True
            )
            
            if result["success"]:
                print(f"  ✅ High compression: {result['compression_ratio']:.1f}% reduction")
                print(f"  ✅ Time taken: {result['compression_time']:.3f}s")
                
                # Verify integrity
                integrity = verify_integrity_handler(result["output_file"])
                if integrity["success"]:
                    print(f"  ✅ Integrity verified: {integrity['calculated_checksum'][:16]}...")
                
                # Clean up
                if os.path.exists(result["output_file"]):
                    os.remove(result["output_file"])
        
        # 3. Batch Operations
        print("\n📦 BATCH COMPRESSION")
        print("-" * 40)
        
        # Select files for batch compression
        batch_files = [str(data_dir / f) for f in existing_files[:3]]  # First 3 files
        
        print(f"📋 Batch compressing {len(batch_files)} files...")
        
        result = batch_compress_handler(
            batch_files,
            compression_type="gzip",
            output_directory=temp_dir,
            preserve_original=True
        )
        
        if result["success"]:
            summary = result["summary"]
            print(f"  ✅ Success: {summary['successful_compressions']}/{summary['total_files']} files")
            print(f"  ✅ Total reduction: {summary['overall_compression_ratio']:.1f}%")
            print(f"  ✅ Total time: {summary['batch_time']:.3f}s")
            print(f"  ✅ Original size: {summary['total_original_size']:,} bytes")
            print(f"  ✅ Compressed size: {summary['total_compressed_size']:,} bytes")
        
        # 4. Security Example
        print("\n🔐 SECURITY EXAMPLE")
        print("-" * 40)
        
        # Create password-protected archive
        secure_files = [str(data_dir / f) for f in existing_files[:2]]  # First 2 files
        archive_path = os.path.join(temp_dir, "secure_data.zip")
        
        result = create_password_protected_archive_handler(
            secure_files,
            archive_path,
            password="DataSec2024!"
        )
        
        if result["success"]:
            print(f"  ✅ Protected archive created: {result['archive_size']:,} bytes")
            print(f"  ✅ Files included: {len(result['file_paths'])}")
            print(f"  ✅ Password protection: {'Enabled' if result['password_protected'] else 'Disabled'}")
        
        # 5. Format Detection
        print("\n🔍 FORMAT DETECTION")
        print("-" * 40)
        
        # Test with existing compressed file
        compressed_file = data_dir / "output.log.gz"
        if compressed_file.exists():
            from compression.mcp_handlers import detect_compression_format_handler
            
            result = detect_compression_format_handler(str(compressed_file))
            if result["success"]:
                print(f"  ✅ File: {compressed_file.name}")
                print(f"  ✅ Detected format: {result['format']}")
                print(f"  ✅ Confidence: {result['confidence']}")
                print(f"  ✅ File extension: {result['file_extension']}")
        
        # 6. Practical Use Cases
        print("\n💡 PRACTICAL USE CASES")
        print("-" * 40)
        
        use_cases = [
            ("📊 Data Archives", "CSV and Parquet files compress well with gzip/bz2"),
            ("📝 Log Compression", "Text logs achieve 40-70% compression ratios"),
            ("🔒 Secure Backup", "Password-protected ZIP for sensitive data"),
            ("📦 Batch Processing", "Compress multiple files efficiently"),
            ("🔄 Format Detection", "Auto-detect compression for processing pipelines"),
            ("✅ Integrity Checks", "Verify file integrity with checksums")
        ]
        
        for title, description in use_cases:
            print(f"  {title}: {description}")
        
        print("\n🎯 COMPRESSION RECOMMENDATIONS")
        print("-" * 40)
        
        recommendations = [
            ("Small files (<1KB)", "zlib or gzip for speed"),
            ("Text files", "bz2 for best compression, gzip for speed"),
            ("Binary files", "gzip or zlib for general use"),
            ("Archives", "ZIP for compatibility, tar.gz for Unix"),
            ("Large files", "Stream compression to save memory"),
            ("Secure data", "Password-protected ZIP archives")
        ]
        
        for scenario, recommendation in recommendations:
            print(f"  📌 {scenario}: {recommendation}")
        
        print("\n✨ COMPRESSION MCP READY FOR PRODUCTION!")
        print("=" * 60)
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up temporary files")

if __name__ == "__main__":
    try:
        demonstrate_compression_with_data()
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install tabulate")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
