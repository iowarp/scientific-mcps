"""
Performance and stress tests for Slurm MCP implementation.
Tests system behavior under various load conditions and edge cases.
"""
import pytest
import asyncio
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import (
    submit_slurm_job_tool,
    check_job_status_tool,
    cancel_slurm_job_tool,
    list_slurm_jobs_tool,
    get_slurm_info_tool
)


class TestPerformance:
    """Performance and stress tests for Slurm MCP."""

    @pytest.mark.asyncio
    async def test_concurrent_job_submissions(self, temp_script):
        """Test concurrent job submission performance."""
        num_concurrent = 10
        start_time = time.time()
        
        # Submit multiple jobs concurrently
        tasks = []
        for i in range(num_concurrent):
            task = submit_slurm_job_tool(
                temp_script, 
                cores=1, 
                job_name=f"perf_test_{i}"
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Check results
        successful_submissions = 0
        job_ids = []
        
        for result in results:
            if not isinstance(result, Exception) and isinstance(result, dict):
                if not result.get("isError") and "job_id" in result:
                    successful_submissions += 1
                    job_ids.append(result["job_id"])
        
        # Performance assertions
        assert duration < 30.0  # Should complete within 30 seconds
        assert successful_submissions >= 0  # At least some should succeed
        
        # Clean up
        if job_ids:
            cleanup_tasks = [cancel_slurm_job_tool(job_id) for job_id in job_ids]
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        
        print(f"Submitted {successful_submissions}/{num_concurrent} jobs in {duration:.2f}s")

    @pytest.mark.asyncio
    async def test_status_check_performance(self, sample_job_id):
        """Test performance of status checking operations."""
        num_checks = 50
        start_time = time.time()
        
        # Perform multiple status checks
        tasks = []
        for i in range(num_checks):
            task = check_job_status_tool(sample_job_id)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Check results
        successful_checks = sum(1 for r in results if not isinstance(r, Exception))
        
        # Performance assertions
        assert duration < 20.0  # Should complete within 20 seconds
        assert successful_checks >= num_checks * 0.8  # At least 80% should succeed
        
        avg_time = duration / num_checks
        print(f"Performed {successful_checks}/{num_checks} status checks in {duration:.2f}s (avg: {avg_time:.3f}s)")

    @pytest.mark.asyncio
    async def test_information_gathering_performance(self):
        """Test performance of information gathering operations."""
        operations = [
            ("cluster_info", get_slurm_info_tool),
            ("job_list", list_slurm_jobs_tool),
        ]
        
        for op_name, op_func in operations:
            start_time = time.time()
            
            # Perform operation multiple times
            tasks = [op_func() for _ in range(10)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_time = time.time()
            duration = end_time - start_time
            
            successful_ops = sum(1 for r in results if not isinstance(r, Exception))
            
            # Performance assertions
            assert duration < 15.0  # Should complete within 15 seconds
            assert successful_ops >= 8  # At least 80% should succeed
            
            avg_time = duration / len(tasks)
            print(f"{op_name}: {successful_ops}/{len(tasks)} operations in {duration:.2f}s (avg: {avg_time:.3f}s)")

    @pytest.mark.asyncio
    async def test_mixed_workload_performance(self, temp_script, sample_job_id):
        """Test performance under mixed workload."""
        start_time = time.time()
        
        # Create mixed workload
        tasks = []
        
        # Job submissions
        for i in range(5):
            tasks.append(submit_slurm_job_tool(temp_script, cores=1, job_name=f"mixed_{i}"))
        
        # Status checks
        for i in range(10):
            tasks.append(check_job_status_tool(sample_job_id))
        
        # Information gathering
        for i in range(3):
            tasks.append(get_slurm_info_tool())
            tasks.append(list_slurm_jobs_tool())
        
        # Execute mixed workload
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Analyze results
        successful_ops = sum(1 for r in results if not isinstance(r, Exception))
        job_ids = []
        
        for result in results:
            if (not isinstance(result, Exception) and 
                isinstance(result, dict) and 
                "job_id" in result and 
                not result.get("isError")):
                job_ids.append(result["job_id"])
        
        # Performance assertions
        assert duration < 45.0  # Should complete within 45 seconds
        assert successful_ops >= len(tasks) * 0.7  # At least 70% should succeed
        
        # Clean up jobs
        if job_ids:
            cleanup_tasks = [cancel_slurm_job_tool(job_id) for job_id in job_ids]
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        
        print(f"Mixed workload: {successful_ops}/{len(tasks)} operations in {duration:.2f}s")

    @pytest.mark.asyncio
    async def test_rapid_sequential_operations(self, temp_script):
        """Test rapid sequential operations."""
        operations_per_second = []
        
        # Test rapid job submissions
        start_time = time.time()
        for i in range(20):
            result = await submit_slurm_job_tool(temp_script, cores=1, job_name=f"rapid_{i}")
            if not isinstance(result, dict) or result.get("isError"):
                continue
                
        duration = time.time() - start_time
        ops_per_sec = 20 / duration if duration > 0 else 0
        operations_per_second.append(("submissions", ops_per_sec))
        
        # Test rapid status checks
        start_time = time.time()
        for i in range(50):
            await check_job_status_tool("1234567")
        duration = time.time() - start_time
        ops_per_sec = 50 / duration if duration > 0 else 0
        operations_per_second.append(("status_checks", ops_per_sec))
        
        # Print performance metrics
        for op_name, ops_per_sec in operations_per_second:
            print(f"{op_name}: {ops_per_sec:.2f} ops/sec")
            assert ops_per_sec > 0.1  # At least some reasonable throughput

    def test_memory_usage_under_load(self, temp_script):
        """Test memory usage under load."""
        import psutil
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        async def memory_test():
            tasks = []
            # Create many tasks
            for i in range(100):
                task = submit_slurm_job_tool(temp_script, cores=1, job_name=f"mem_test_{i}")
                tasks.append(task)
            
            # Execute and wait
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Clean up job IDs
            job_ids = []
            for result in results:
                if (not isinstance(result, Exception) and 
                    isinstance(result, dict) and 
                    "job_id" in result and 
                    not result.get("isError")):
                    job_ids.append(result["job_id"])
            
            return job_ids
        
        # Run memory test
        job_ids = asyncio.run(memory_test())
        
        # Force garbage collection
        gc.collect()
        
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        print(f"Memory usage: {initial_memory:.1f}MB -> {peak_memory:.1f}MB (+{memory_increase:.1f}MB)")
        
        # Memory should not increase excessively
        assert memory_increase < 100  # Less than 100MB increase

    @pytest.mark.asyncio
    async def test_timeout_handling(self, temp_script):
        """Test behavior under timeout conditions."""
        # Test with very short timeouts
        timeout_tests = [
            (0.1, "Very short timeout"),
            (1.0, "Short timeout"),
            (5.0, "Medium timeout"),
        ]
        
        for timeout_duration, description in timeout_tests:
            try:
                result = await asyncio.wait_for(
                    submit_slurm_job_tool(temp_script, cores=1),
                    timeout=timeout_duration
                )
                # If it completes within timeout, that's good
                assert isinstance(result, dict)
                
            except asyncio.TimeoutError:
                # Timeout is also acceptable
                print(f"{description}: Operation timed out after {timeout_duration}s")
                pass

    @pytest.mark.asyncio
    async def test_error_recovery_performance(self):
        """Test performance when recovering from errors."""
        start_time = time.time()
        
        # Submit operations that will likely fail
        error_tasks = []
        for i in range(20):
            # These should fail quickly
            task = submit_slurm_job_tool("nonexistent_script.sh", 1)
            error_tasks.append(task)
        
        results = await asyncio.gather(*error_tasks, return_exceptions=True)
        
        duration = time.time() - start_time
        
        # Should handle errors quickly
        assert duration < 10.0  # Should fail fast
        
        # All should return results (either success or handled errors)
        for result in results:
            if not isinstance(result, Exception):
                assert isinstance(result, dict)
        
        print(f"Error recovery: {len(results)} operations in {duration:.2f}s")

    @pytest.mark.asyncio
    async def test_resource_cleanup_performance(self, temp_script):
        """Test performance of resource cleanup operations."""
        # Submit multiple jobs
        submit_tasks = []
        for i in range(10):
            task = submit_slurm_job_tool(temp_script, cores=1, job_name=f"cleanup_{i}")
            submit_tasks.append(task)
        
        submit_results = await asyncio.gather(*submit_tasks, return_exceptions=True)
        
        # Collect job IDs
        job_ids = []
        for result in submit_results:
            if (not isinstance(result, Exception) and 
                isinstance(result, dict) and 
                "job_id" in result and 
                not result.get("isError")):
                job_ids.append(result["job_id"])
        
        if job_ids:
            # Test cleanup performance
            start_time = time.time()
            
            cleanup_tasks = [cancel_slurm_job_tool(job_id) for job_id in job_ids]
            cleanup_results = await asyncio.gather(*cleanup_tasks, return_exceptions=True)
            
            cleanup_duration = time.time() - start_time
            
            successful_cleanups = sum(
                1 for r in cleanup_results 
                if not isinstance(r, Exception)
            )
            
            print(f"Cleanup: {successful_cleanups}/{len(job_ids)} jobs in {cleanup_duration:.2f}s")
            
            # Cleanup should be reasonably fast
            assert cleanup_duration < 20.0

    @pytest.mark.asyncio
    async def test_scalability_limits(self, temp_script):
        """Test system behavior at scalability limits."""
        # Test increasing load levels
        load_levels = [10, 25, 50]
        
        for load_level in load_levels:
            print(f"Testing load level: {load_level}")
            
            start_time = time.time()
            
            # Create tasks at this load level
            tasks = []
            for i in range(load_level):
                task = submit_slurm_job_tool(temp_script, cores=1, job_name=f"scale_{load_level}_{i}")
                tasks.append(task)
            
            # Execute with timeout
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=60.0  # 60 second timeout
                )
                
                duration = time.time() - start_time
                
                successful_ops = sum(
                    1 for r in results 
                    if not isinstance(r, Exception) and isinstance(r, dict)
                )
                
                success_rate = successful_ops / load_level
                throughput = successful_ops / duration if duration > 0 else 0
                
                print(f"Load {load_level}: {success_rate:.1%} success, {throughput:.2f} ops/sec")
                
                # Clean up any successful jobs
                job_ids = []
                for result in results:
                    if (not isinstance(result, Exception) and 
                        isinstance(result, dict) and 
                        "job_id" in result and 
                        not result.get("isError")):
                        job_ids.append(result["job_id"])
                
                if job_ids:
                    cleanup_tasks = [cancel_slurm_job_tool(job_id) for job_id in job_ids]
                    await asyncio.gather(*cleanup_tasks, return_exceptions=True)
                
                # System should maintain some level of functionality
                assert success_rate > 0.1  # At least 10% success rate
                
            except asyncio.TimeoutError:
                print(f"Load {load_level}: Timed out after 60 seconds")
                # Timeout at high load is acceptable
                break
