"""
Test cases for node allocation capabilities.
Tests the new salloc-based node allocation functionality.
Requires real Slurm environment - skips if not available.
"""
import pytest
from capabilities.node_allocation import allocate_nodes, deallocate_allocation, get_allocation_info
from capabilities.queue_info import get_queue_info
from capabilities.utils import check_slurm_available


class TestNodeAllocation:
    """Test cases for node allocation functionality."""
    
    @pytest.fixture(autouse=True)
    def check_slurm_required(self):
        """Skip all tests if Slurm is not available."""
        if not check_slurm_available():
            pytest.skip("Slurm is not available - node allocation tests require real Slurm")
    
    def get_available_partitions(self):
        """Get list of available partitions, or return None if none found."""
        try:
            queue_info = get_queue_info()
            if queue_info.get("real_slurm", False) and "partitions" in queue_info:
                partitions = list(queue_info["partitions"].keys())
                return partitions[0] if partitions else None
            return None
        except Exception:
            return None
    
    def test_allocate_nodes_basic(self):
        """Test basic node allocation with system default time limit."""
        result = allocate_nodes(num_nodes=1)  # No time limit - use system default
        
        assert "status" in result
        assert "allocation_id" in result
        assert result.get("real_slurm", False) == True
        
        # Real Slurm should either allocate or give a clear error
        if result["status"] == "allocated":
            assert result["allocation_id"] is not None
            assert "allocated_nodes" in result
        elif result["status"] == "timeout":
            # Timeout is acceptable for immediate allocation requests
            assert "timeout" in result["message"].lower() or "timed out" in result["message"].lower()
        else:
            # Should be an error with explanation
            assert result["status"] == "error"
            assert "message" in result
    
    def test_allocate_nodes_with_partition_check(self):
        """Test node allocation with partition validation."""
        partition = self.get_available_partitions()
        
        if partition is None:
            pytest.skip("No partitions found - please check partitions first with: sinfo -s")
        
        result = allocate_nodes(
            num_nodes=1,
            job_name="test_allocation",
            partition=partition,
            immediate=True  # Use immediate to avoid long waits
        )
        
        assert "status" in result
        assert result.get("real_slurm", False) == True
        
        if result["status"] == "allocated":
            assert result["allocation_id"] is not None
            # Clean up immediately
            cleanup_result = deallocate_allocation(result["allocation_id"])
            assert cleanup_result["status"] in ["deallocated", "error"]
        else:
            # Error or timeout is acceptable for testing
            assert result["status"] in ["error", "timeout"]
    
    def test_allocate_with_user_specified_time(self):
        """Test allocation with user-specified time limit."""
        result = allocate_nodes(
            num_nodes=1,
            time_limit="0:02:00",  # User specified 2 minutes
            immediate=True
        )
        
        assert "status" in result
        assert result.get("real_slurm", False) == True
        
        if result["status"] == "allocated":
            assert result["time_limit"] == "0:02:00"
            # Clean up
            deallocate_allocation(result["allocation_id"])
    
    def test_allocate_without_time_limit(self):
        """Test allocation without time limit (use system default)."""
        result = allocate_nodes(
            num_nodes=1,
            immediate=True
        )
        
        assert "status" in result
        # Should either work with system default or fail clearly
        assert result["status"] in ["allocated", "error", "timeout"]
    
    def test_deallocate_allocation(self):
        """Test allocation deallocation with real job ID."""
        # First try to allocate a short job
        alloc_result = allocate_nodes(
            num_nodes=1,
            time_limit="0:01:00",
            immediate=True
        )
        
        if alloc_result["status"] == "allocated":
            job_id = alloc_result["allocation_id"]
            
            # Now test deallocation
            result = deallocate_allocation(job_id)
            
            assert "status" in result
            assert "allocation_id" in result
            assert result["allocation_id"] == job_id
            assert result["status"] in ["deallocated", "error"]  # May already be completed
        else:
            pytest.skip("Could not allocate test job for deallocation test")
    
    def test_get_allocation_info_real(self):
        """Test getting allocation information for real allocation."""
        # Try to allocate first
        alloc_result = allocate_nodes(
            num_nodes=1,
            time_limit="0:01:00",
            immediate=True
        )
        
        if alloc_result["status"] == "allocated":
            job_id = alloc_result["allocation_id"]
            
            # Get info about the allocation
            result = get_allocation_info(job_id)
            
            assert "allocation_id" in result
            assert result["allocation_id"] == job_id
            assert "status" in result
            
            # Clean up
            deallocate_allocation(job_id)
        else:
            # Test with non-existent job ID
            result = get_allocation_info("999999")
            assert result["status"] in ["not_found", "error"]
    
    def test_allocation_workflow_integration(self):
        """Test complete allocation workflow with real Slurm."""
        partition = self.get_available_partitions()
        
        # Try to allocate with immediate flag and short time
        allocation_result = allocate_nodes(
            num_nodes=1,
            time_limit="0:01:00",
            job_name="test_workflow",
            partition=partition,
            immediate=True
        )
        
        assert "status" in allocation_result
        
        if allocation_result["status"] == "allocated":
            allocation_id = allocation_result["allocation_id"]
            
            # Get allocation info
            info_result = get_allocation_info(allocation_id)
            assert info_result["allocation_id"] == allocation_id
            
            # Clean up - deallocate
            dealloc_result = deallocate_allocation(allocation_id)
            assert dealloc_result["allocation_id"] == allocation_id
        else:
            # If allocation failed, that's also a valid test result
            assert allocation_result["status"] in ["error", "timeout"]
            if "partition" in allocation_result.get("message", "").lower():
                pytest.fail("Unknown partition - please check partitions first with: sinfo -s")
    
    def test_partition_validation(self):
        """Test partition validation and error handling."""
        # Test with an invalid partition
        result = allocate_nodes(
            num_nodes=1,
            partition="nonexistent_partition",
            immediate=True
        )
        
        assert result["status"] == "error"
        assert "partition" in result.get("message", "").lower() or "invalid" in result.get("message", "").lower()
    
    def test_exclusive_allocation_real(self):
        """Test exclusive node allocation with real Slurm."""
        partition = self.get_available_partitions()
        
        result = allocate_nodes(
            num_nodes=1,
            time_limit="0:01:00",
            partition=partition,
            exclusive=True,
            immediate=True
        )
        
        assert "status" in result
        if result["status"] == "allocated":
            # Check that exclusive flag was used
            assert "--exclusive" in result.get("command_used", "")
            # Clean up
            deallocate_allocation(result["allocation_id"])
        else:
            # Error or timeout is acceptable
            assert result["status"] in ["error", "timeout"]
    
    def test_resource_specifications_real(self):
        """Test allocation with specific resource requirements."""
        partition = self.get_available_partitions()
        
        result = allocate_nodes(
            num_nodes=1,
            time_limit="0:01:00",
            partition=partition,
            cpus_per_task=1,  # Conservative request
            memory="1G",      # Conservative request
            immediate=True
        )
        
        assert "status" in result
        if result["status"] == "allocated":
            command = result.get("command_used", "")
            assert "-c 1" in command  # CPUs per task
            assert "--mem 1G" in command  # Memory
            # Clean up
            deallocate_allocation(result["allocation_id"])
        else:
            assert result["status"] in ["error", "timeout"]


class TestNodeAllocationMCP:
    """Test MCP handler integration for node allocation."""
    
    @pytest.fixture(autouse=True)
    def check_slurm_required(self):
        """Skip all tests if Slurm is not available."""
        if not check_slurm_available():
            pytest.skip("Slurm is not available - MCP handler tests require real Slurm")
    
    def test_mcp_handlers_import(self):
        """Test that MCP handlers can be imported."""
        try:
            from mcp_handlers import (
                allocate_nodes_handler,
                deallocate_allocation_handler,
                get_allocation_info_handler
            )
            assert callable(allocate_nodes_handler)
            assert callable(deallocate_allocation_handler)
            assert callable(get_allocation_info_handler)
        except ImportError as e:
            pytest.fail(f"Failed to import MCP handlers: {e}")
    
    def test_allocate_nodes_handler_real(self):
        """Test the MCP handler for node allocation with real Slurm."""
        from mcp_handlers import allocate_nodes_handler
        
        result = allocate_nodes_handler(
            num_nodes=1,
            time_limit="0:01:00",
            immediate=True
        )
        
        assert isinstance(result, dict)
        assert "status" in result
        
        if result["status"] == "allocated":
            # Clean up
            from mcp_handlers import deallocate_allocation_handler
            deallocate_allocation_handler(result["allocation_id"])
    
    def test_deallocate_allocation_handler_real(self):
        """Test the MCP handler for allocation deallocation."""
        from mcp_handlers import deallocate_allocation_handler
        
        # Test with non-existent job ID
        result = deallocate_allocation_handler("999999")
        
        assert isinstance(result, dict)
        assert "allocation_id" in result
        assert result["allocation_id"] == "999999"
        # Slurm scancel may succeed even for non-existent jobs
        assert result["status"] in ["error", "deallocated"]
    
    def test_get_allocation_info_handler_real(self):
        """Test the MCP handler for allocation info."""
        from mcp_handlers import get_allocation_info_handler
        
        # Test with non-existent job ID
        result = get_allocation_info_handler("999999")
        
        assert isinstance(result, dict)
        assert "allocation_id" in result
        assert result["allocation_id"] == "999999"
        assert result["status"] in ["not_found", "error"]
    
    def test_node_list_parsing_real(self):
        """Test parsing of comma-separated node lists with real validation."""
        from mcp_handlers import allocate_nodes_handler
        
        # Use real node names if available, otherwise expect error
        result = allocate_nodes_handler(
            specific_nodes="node001,node002,node003",  # These may not exist
            immediate=True
        )
        
        assert isinstance(result, dict)
        # Should either work or fail with node-related error
        if result["status"] == "error":
            assert "node" in result.get("message", "").lower() or "invalid" in result.get("message", "").lower()
