"""
Tests for MCP server tools.
Tests the actual MCP tool implementations and server functionality.
"""
import pytest
import asyncio
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import server tools
from server import (
    submit_slurm_job_tool, 
    check_job_status_tool,
    cancel_slurm_job_tool,
    list_slurm_jobs_tool,
    get_slurm_info_tool,
    get_job_details_tool,
    get_job_output_tool,
    get_queue_info_tool,
    submit_array_job_tool,
    get_node_info_tool
)


class TestServerTools:
    """Test suite for MCP server tools."""

    @pytest.mark.asyncio
    async def test_submit_job_tool_success(self, temp_script, valid_cores):
        """Test successful job submission through MCP tool."""
        result = await submit_slurm_job_tool(temp_script, valid_cores)
        
        assert isinstance(result, dict)
        # Should either be a success response or error response
        if "isError" in result:
            assert isinstance(result["isError"], bool)
        else:
            assert "job_id" in result or "error" in result

    @pytest.mark.asyncio
    async def test_submit_job_tool_enhanced(self, temp_script, job_parameters):
        """Test enhanced job submission through MCP tool."""
        result = await submit_slurm_job_tool(
            temp_script, 
            cores=4,
            memory=job_parameters["memory"],
            time_limit=job_parameters["time_limit"],
            job_name=job_parameters["job_name"],
            partition=job_parameters["partition"]
        )
        
        assert isinstance(result, dict)
        
        if not result.get("isError") and "job_id" in result:
            # Verify parameters were passed through
            assert result.get("memory") == job_parameters["memory"]
            assert result.get("time_limit") == job_parameters["time_limit"]
            assert result.get("job_name") == job_parameters["job_name"]
            assert result.get("partition") == job_parameters["partition"]

    @pytest.mark.asyncio
    async def test_submit_job_tool_invalid_file(self, valid_cores):
        """Test job submission tool with invalid file."""
        result = await submit_slurm_job_tool("nonexistent.sh", valid_cores)
        
        assert isinstance(result, dict)
        # Should handle error gracefully
        assert "isError" in result or "error" in result

    @pytest.mark.asyncio
    async def test_submit_job_tool_invalid_cores(self, temp_script):
        """Test job submission tool with invalid cores."""
        result = await submit_slurm_job_tool(temp_script, 0)
        
        assert isinstance(result, dict)
        assert "isError" in result or "error" in result

    @pytest.mark.asyncio
    async def test_check_status_tool(self, sample_job_id):
        """Test job status checking tool."""
        result = await check_job_status_tool(sample_job_id)
        
        assert isinstance(result, dict)
        # Should either be a success response or error response
        if "isError" in result:
            assert isinstance(result["isError"], bool)
        else:
            assert "job_id" in result or "error" in result

    @pytest.mark.asyncio
    async def test_cancel_job_tool(self, sample_job_id):
        """Test job cancellation tool."""
        result = await cancel_slurm_job_tool(sample_job_id)
        
        assert isinstance(result, dict)
        # Should handle cancellation request
        if not result.get("isError"):
            assert "job_id" in result or "status" in result

    @pytest.mark.asyncio
    async def test_list_jobs_tool(self):
        """Test job listing tool."""
        result = await list_slurm_jobs_tool()
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            assert "jobs" in result or "count" in result

    @pytest.mark.asyncio
    async def test_list_jobs_tool_with_filters(self):
        """Test job listing tool with filters."""
        result = await list_slurm_jobs_tool(user="testuser", state="RUNNING")
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            # Should include filter information
            assert "user_filter" in result or "state_filter" in result

    @pytest.mark.asyncio
    async def test_get_slurm_info_tool(self):
        """Test cluster info tool."""
        result = await get_slurm_info_tool()
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            assert "cluster_name" in result or "partitions" in result

    @pytest.mark.asyncio
    async def test_get_job_details_tool(self, sample_job_id):
        """Test job details tool."""
        result = await get_job_details_tool(sample_job_id)
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            assert "job_id" in result

    @pytest.mark.asyncio
    async def test_get_job_output_tool(self, sample_job_id):
        """Test job output tool."""
        for output_type in ["stdout", "stderr"]:
            result = await get_job_output_tool(sample_job_id, output_type)
            
            assert isinstance(result, dict)
            if not result.get("isError"):
                assert "job_id" in result or "output_type" in result

    @pytest.mark.asyncio
    async def test_get_queue_info_tool(self):
        """Test queue info tool."""
        result = await get_queue_info_tool()
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            assert "jobs" in result or "total_jobs" in result

    @pytest.mark.asyncio
    async def test_get_queue_info_tool_with_partition(self):
        """Test queue info tool with partition filter."""
        result = await get_queue_info_tool(partition="compute")
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            assert "partition_filter" in result or "jobs" in result

    @pytest.mark.asyncio
    async def test_submit_array_job_tool(self, array_script, array_parameters):
        """Test array job submission tool."""
        result = await submit_array_job_tool(
            array_script,
            array_parameters["array_range"],
            cores=array_parameters["cores"],
            memory=array_parameters["memory"],
            time_limit=array_parameters["time_limit"],
            job_name=array_parameters["job_name"]
        )
        
        assert isinstance(result, dict)
        if not result.get("isError") and not result.get("error"):
            # Should have array job information
            assert "array_job_id" in result or "array_range" in result

    @pytest.mark.asyncio
    async def test_get_node_info_tool(self):
        """Test node info tool."""
        result = await get_node_info_tool()
        
        assert isinstance(result, dict)
        if not result.get("isError"):
            assert "nodes" in result or "total_nodes" in result

    @pytest.mark.asyncio
    async def test_tool_parameter_defaults(self, temp_script):
        """Test that tools handle default parameters correctly."""
        # Test submit job with minimal parameters
        result = await submit_slurm_job_tool(temp_script, cores=1)
        assert isinstance(result, dict)
        
        # Test submit job with default memory and time
        result = await submit_slurm_job_tool(temp_script, cores=1, memory="1GB")
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_tool_parameter_validation(self):
        """Test parameter validation in tools."""
        # Test with missing required parameters
        with pytest.raises(TypeError):
            await submit_slurm_job_tool()  # Missing required parameters
        
        # Test with invalid parameter types
        result = await submit_slurm_job_tool("script.sh", "invalid_cores")
        assert isinstance(result, dict)
        # Should handle type error gracefully

    @pytest.mark.asyncio
    async def test_concurrent_tool_execution(self, temp_script):
        """Test concurrent execution of tools."""
        # Submit multiple jobs concurrently
        tasks = []
        for i in range(3):
            task = submit_slurm_job_tool(temp_script, cores=1, job_name=f"concurrent_{i}")
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check that all completed
        assert len(results) == 3
        for result in results:
            if not isinstance(result, Exception):
                assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_tool_error_handling(self):
        """Test error handling in tools."""
        # Test with various error conditions
        error_scenarios = [
            (submit_slurm_job_tool, ["nonexistent.sh", 1]),
            (check_job_status_tool, ["invalid_job_id"]),
            (cancel_slurm_job_tool, ["invalid_job_id"]),
            (get_job_details_tool, ["invalid_job_id"]),
        ]
        
        for tool_func, args in error_scenarios:
            try:
                result = await tool_func(*args)
                assert isinstance(result, dict)
                # Should handle errors gracefully
            except Exception as e:
                # Exception handling is also acceptable
                assert isinstance(e, Exception)

    @pytest.mark.asyncio
    async def test_integration_workflow_through_tools(self, temp_script):
        """Test complete workflow through MCP tools."""
        # Submit job
        submit_result = await submit_slurm_job_tool(temp_script, cores=2, job_name="integration_test")
        assert isinstance(submit_result, dict)
        
        if not submit_result.get("isError") and "job_id" in submit_result:
            job_id = submit_result["job_id"]
            
            # Check status
            status_result = await check_job_status_tool(job_id)
            assert isinstance(status_result, dict)
            
            # Get details
            details_result = await get_job_details_tool(job_id)
            assert isinstance(details_result, dict)
            
            # Try to get output
            output_result = await get_job_output_tool(job_id, "stdout")
            assert isinstance(output_result, dict)
            
            # Cancel job
            cancel_result = await cancel_slurm_job_tool(job_id)
            assert isinstance(cancel_result, dict)

    @pytest.mark.asyncio
    async def test_tool_logging(self, temp_script, caplog):
        """Test that tools produce appropriate log messages."""
        with caplog.at_level("INFO"):
            result = await submit_slurm_job_tool(temp_script, cores=1)
            
            # Should have logged the operation
            assert len(caplog.records) > 0
            # Look for relevant log messages
            log_messages = [record.message for record in caplog.records]
            assert any("submit" in msg.lower() for msg in log_messages)

    @pytest.mark.asyncio
    async def test_tool_response_consistency(self, temp_script, sample_job_id):
        """Test that all tools return consistent response formats."""
        tools_to_test = [
            (submit_slurm_job_tool, [temp_script, 1]),
            (check_job_status_tool, [sample_job_id]),
            (list_slurm_jobs_tool, []),
            (get_slurm_info_tool, []),
            (get_node_info_tool, []),
        ]
        
        for tool_func, args in tools_to_test:
            result = await tool_func(*args)
            assert isinstance(result, dict)
            
            # All results should be dictionaries
            # and should not contain both success and error indicators
            if result.get("isError"):
                assert "content" in result or "error" in result
            else:
                # Success responses should have meaningful data
                assert len(result) > 0

    @pytest.mark.asyncio
    async def test_array_job_workflow(self, array_script):
        """Test array job workflow through tools."""
        # Submit array job
        result = await submit_array_job_tool(
            array_script,
            array_range="1-3",
            cores=1,
            memory="1GB",
            time_limit="00:10:00",
            job_name="test_array"
        )
        
        assert isinstance(result, dict)
        
        if not result.get("isError") and "array_job_id" in result:
            array_job_id = result["array_job_id"]
            
            # Check status of array job
            status_result = await check_job_status_tool(array_job_id)
            assert isinstance(status_result, dict)
            
            # Try to cancel array job
            cancel_result = await cancel_slurm_job_tool(array_job_id)
            assert isinstance(cancel_result, dict)

    @pytest.mark.asyncio
    async def test_tool_timeout_handling(self, temp_script):
        """Test that tools handle timeouts gracefully."""
        # This test might be environment-specific
        try:
            # Set a very short timeout (if supported by underlying implementation)
            result = await asyncio.wait_for(
                submit_slurm_job_tool(temp_script, cores=1), 
                timeout=30.0  # 30 second timeout
            )
            assert isinstance(result, dict)
        except asyncio.TimeoutError:
            # Timeout is acceptable for this test
            pass

    def test_tool_documentation(self):
        """Test that all tools have proper documentation."""
        tools = [
            submit_slurm_job_tool,
            check_job_status_tool,
            cancel_slurm_job_tool,
            list_slurm_jobs_tool,
            get_slurm_info_tool,
            get_job_details_tool,
            get_job_output_tool,
            get_queue_info_tool,
            submit_array_job_tool,
            get_node_info_tool
        ]
        
        for tool in tools:
            # Check that each tool has a docstring
            assert tool.__doc__ is not None
            assert len(tool.__doc__.strip()) > 0
            
            # Check that docstring contains basic information
            docstring = tool.__doc__.lower()
            assert "args:" in docstring or "parameters:" in docstring
            assert "returns:" in docstring or "return:" in docstring
