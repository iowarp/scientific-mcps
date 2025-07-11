1. go to parquet,pandas,Node_hardware or Slurm or HDF5 or plot or Adios folder and read folder structure and files.
2. now go to compression folder and explore folder. remove existing files and folder. just create new folder structure just like above mentioned mcp also implement similar server code just like plot or parquet.
3. just like node haardware,Slurm or HDF5 or plot  implement compression mcp where:

capability:
# gzip compress/decompress single files and streams
# zip archive creation and extraction
# zlib raw data compression for memory efficiency
# bz2 high-ratio compression for storage optimization
# Batch file compression with progress tracking
# Directory compression (recursive into archives)
# List archive contents without extracting
# Compression level control (speed vs size balance)
# Integrity verification with checksum validation
# Memory-efficient streaming for large files
# Password-protected archives for security
# Auto-format detection of file types
# Command-line tool integration via subprocess
# Compression statistics (ratio, speed, time metrics)
# Error handling for corrupted files and permissions
# Cross-platform compatibility (Windows/Linux/Mac)
# Preserves original files (creates compressed copies, doesn't replace) and also implement any features that i skip here if you think.

4. after that run server , run test using pytest and capabilities using uv also server can be run by using name called compression-mcp. dont use other option then uv.
5. update readme.md just like parquet or plot or slurm or adios readme
