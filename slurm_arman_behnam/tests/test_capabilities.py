import pytest
from src.capabilities import hdf5_handler, slurm_handler, node_hardware
@pytest.mark.asyncio
async def test_hdf5_handler():
    """Test HDF5 handler functionality."""
    params = {"path_pattern": "*.hdf5"}
    result = await hdf5_handler.get_hdf5_data(params)
    
    assert "resource_type" in result
    assert result["resource_type"] == "hdf5"
    assert "files" in result
    assert isinstance(result["files"], list)
    
    params = {"path_pattern": "*_00.hdf5"}
    result = await hdf5_handler.get_hdf5_data(params)
    
    assert all("_00.hdf5" in file for file in result["files"])

@pytest.mark.asyncio
async def test_slurm_handler():
    """Test Slurm handler functionality."""
    # Test successful job submission
    params = {
        "script_path": "/path/to/job.sh",
        "cores": 4
    }
    result = await slurm_handler.submit_job(params)
    
    assert "tool" in result
    assert result["tool"] == "slurm"
    assert "job_id" in result
    assert "status" in result
    assert result["status"] == "submitted"
    
    params = {} # Missing required param
    result = await slurm_handler.submit_job(params)
    
    assert "error" in result
    assert "code" in result["error"]
    assert "message" in result["error"]

@pytest.mark.asyncio
async def test_node_hardware():
    """Test Node Hardware functionality."""
    result = await node_hardware.get_system_info({})
    
    assert "tool" in result
    assert result["tool"] == "node_hardware"
    assert "cpu_cores" in result
    assert isinstance(result["cpu_cores"], int)
    assert "memory_gb" in result