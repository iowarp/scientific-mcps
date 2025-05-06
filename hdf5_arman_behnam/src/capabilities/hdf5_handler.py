import os
import pathlib

async def get_hdf5_data(params):
    """Simulate HDF5 file access."""
    path_pattern = params.get("path_pattern", "*.hdf5")
    base_dir = params.get("base_dir", "/data")
    
    # Mock files for simulation
    mock_files = [
        f"{base_dir}/sim_run_123/output_00.hdf5",
        f"{base_dir}/sim_run_123/output_01.hdf5",
        f"{base_dir}/sim_run_124/output_00.hdf5"
    ]
    
    # Filter based on pattern
    matching_files = [f for f in mock_files if pathlib.Path(f).match(path_pattern)]
    
    return {
        "resource_type": "hdf5",
        "files": matching_files,
        "count": len(matching_files),
        "metadata": {
            "base_dir": base_dir,
            "pattern": path_pattern
        }
    }