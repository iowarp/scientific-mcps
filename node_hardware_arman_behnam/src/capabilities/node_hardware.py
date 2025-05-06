import os
import psutil

async def get_system_info(params):
    """Get system hardware information."""
    return {
        "tool": "node_hardware",
        "cpu_cores": os.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "platform": os.name
    }