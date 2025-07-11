"""
Compression capabilities and utilities
"""

# Supported compression formats
SUPPORTED_FORMATS = {
    "gzip": {
        "extensions": [".gz"],
        "magic_bytes": b'\x1f\x8b',
        "description": "GNU zip compression",
        "level_range": (1, 9),
        "default_level": 6
    },
    "bz2": {
        "extensions": [".bz2"],
        "magic_bytes": b'BZ',
        "description": "Bzip2 compression",
        "level_range": (1, 9),
        "default_level": 6
    },
    "zip": {
        "extensions": [".zip"],
        "magic_bytes": b'PK',
        "description": "ZIP archive format",
        "level_range": (1, 9),
        "default_level": 6
    },
    "zlib": {
        "extensions": [".zlib"],
        "magic_bytes": b'\x78\x9c',
        "description": "Zlib compression",
        "level_range": (1, 9),
        "default_level": 6
    },
    "tar.gz": {
        "extensions": [".tar.gz", ".tgz"],
        "magic_bytes": b'\x1f\x8b',
        "description": "Gzipped tar archive",
        "level_range": (1, 9),
        "default_level": 6
    },
    "tar.bz2": {
        "extensions": [".tar.bz2", ".tbz2"],
        "magic_bytes": b'BZ',
        "description": "Bzip2 compressed tar archive",
        "level_range": (1, 9),
        "default_level": 6
    }
}

# File size categories for compression recommendations
SIZE_CATEGORIES = {
    "small": {"max_size": 1024 * 1024, "recommended": ["gzip", "zlib"]},  # < 1MB
    "medium": {"max_size": 100 * 1024 * 1024, "recommended": ["gzip", "bz2"]},  # < 100MB
    "large": {"max_size": float('inf'), "recommended": ["bz2", "streaming"]}  # > 100MB
}

# File type specific recommendations
FILE_TYPE_RECOMMENDATIONS = {
    "text": ["gzip", "bz2"],
    "binary": ["zlib", "gzip"],
    "image": ["zip"],
    "video": ["zip"],  # Usually already compressed
    "audio": ["zip"],  # Usually already compressed
    "archive": ["zip"]
}

def get_compression_recommendation(file_path: str, file_size: int, file_type: str = None) -> dict:
    """
    Get compression recommendations based on file characteristics.
    """
    recommendations = {
        "primary": "gzip",
        "alternatives": ["bz2", "zlib"],
        "reason": "Default recommendation"
    }
    
    # Size-based recommendations
    for category, info in SIZE_CATEGORIES.items():
        if file_size <= info["max_size"]:
            recommendations["primary"] = info["recommended"][0]
            recommendations["alternatives"] = info["recommended"][1:]
            recommendations["reason"] = f"Optimized for {category} files"
            break
    
    # File type specific recommendations
    if file_type and file_type in FILE_TYPE_RECOMMENDATIONS:
        type_recommendations = FILE_TYPE_RECOMMENDATIONS[file_type]
        recommendations["primary"] = type_recommendations[0]
        recommendations["alternatives"] = type_recommendations[1:]
        recommendations["reason"] = f"Optimized for {file_type} files"
    
    return recommendations

def get_format_info(format_name: str) -> dict:
    """
    Get detailed information about a compression format.
    """
    return SUPPORTED_FORMATS.get(format_name, {})

def list_supported_formats() -> list:
    """
    List all supported compression formats.
    """
    return list(SUPPORTED_FORMATS.keys())

def validate_compression_level(format_name: str, level: int) -> bool:
    """
    Validate compression level for a specific format.
    """
    format_info = SUPPORTED_FORMATS.get(format_name)
    if not format_info:
        return False
    
    min_level, max_level = format_info["level_range"]
    return min_level <= level <= max_level
