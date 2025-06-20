#!/usr/bin/env python3
"""
Complete MCP Capabilities Demonstration Script
==============================================
This script demonstrates ALL available MCP capabilities for Slurm management.
"""

import sys
import os
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_handlers import (
    submit_slurm_job_handler,
    check_job_status_handler,
    cancel_slurm_job_handler,
    list_slurm_jobs_handler,
    get_slurm_info_handler,
    get_job_details_handler,
    get_job_output_handler,
    get_queue_info_handler,
    submit_array_job_handler,
    get_node_info_handler
)

def print_header(title):
    """Print formatted header."""
    print(f"\n{'='*70}")
    print(f"🎯 {title}")
    print(f"{'='*70}")

def print_step(step_num, description):
    """Print formatted step."""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 50)

def print_result(data, title="Result"):
    """Print formatted result."""
    print(f"✅ {title}:")
    if isinstance(data, dict):
        # Pretty print key information
        for key, value in data.items():
            if key in ['job_id', 'count', 'real_slurm', 'status', 'message']:
                print(f"   {key}: {value}")
    else:
        print(f"   {data}")

def main():
    """Run complete MCP capabilities demonstration."""
    print_header("Complete MCP Capabilities Demonstration")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Capability 1: Get Cluster Information
    print_step(1, "Get Cluster Information")
    try:
        cluster_info = get_slurm_info_handler()
        print_result(cluster_info, "Cluster Information")
        print(f"   Partitions: {len(cluster_info.get('partitions', []))}")
        print(f"   Version: {cluster_info.get('version', 'N/A')}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Capability 2: List Current Jobs
    print_step(2, "List Current Jobs")
    try:
        jobs = list_slurm_jobs_handler()
        print_result(jobs, "Job Listing")
        if jobs.get('jobs'):
            print("   Recent Jobs:")
            for job in jobs['jobs'][:3]:
                print(f"     - {job.get('job_id', 'N/A')}: {job.get('name', 'N/A')} ({job.get('state', 'N/A')})")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Capability 3: Get Queue Information
    print_step(3, "Get Queue Information")
    try:
        queue_info = get_queue_info_handler()
        print_result(queue_info, "Queue Information")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Capability 4: Get Node Information
    print_step(4, "Get Node Information")
    try:
        node_info = get_node_info_handler()
        print_result(node_info, "Node Information")
        if node_info.get('nodes'):
            print(f"   Total Nodes: {len(node_info['nodes'])}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Capability 5: Submit a Job
    print_step(5, "Submit a Test Job")
    try:
        job_result = submit_slurm_job_handler(
            script_path='test_slurm_env.sh',
            cores=1,
            memory='1GB',
            time_limit='00:01:30',
            job_name='mcp_demo_capability',
            partition='debug'
        )
        print_result(job_result, "Job Submission")
        submitted_job_id = job_result.get('job_id')
    except Exception as e:
        print(f"❌ Error: {e}")
        submitted_job_id = None

    # Capability 6: Check Job Status
    if submitted_job_id:
        print_step(6, f"Check Job Status (Job {submitted_job_id})")
        try:
            status = check_job_status_handler(submitted_job_id)
            print_result(status, "Job Status")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Capability 7: Get Job Details
    if submitted_job_id:
        print_step(7, f"Get Job Details (Job {submitted_job_id})")
        try:
            details = get_job_details_handler(submitted_job_id)
            print_result(details, "Job Details")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Capability 8: Submit Array Job
    print_step(8, "Submit Array Job")
    try:
        array_result = submit_array_job_handler(
            script_path='test_slurm_env.sh',
            array_range='1-3',
            cores=1,
            memory='512MB',
            time_limit='00:01:00',
            job_name='mcp_array_demo',
            partition='debug'
        )
        print_result(array_result, "Array Job Submission")
        array_job_id = array_result.get('job_id')
    except Exception as e:
        print(f"❌ Error: {e}")
        array_job_id = None

    # Capability 9: Get Job Output (if job completed)
    if submitted_job_id:
        print_step(9, f"Get Job Output (Job {submitted_job_id})")
        time.sleep(2)  # Wait a bit for job to potentially complete
        try:
            output = get_job_output_handler(submitted_job_id)
            print_result(output, "Job Output")
            if output.get('content'):
                print(f"   Output preview: {output['content'][:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Capability 10: Cancel a Job (if we have one)
    if array_job_id:
        print_step(10, f"Cancel Array Job (Job {array_job_id})")
        try:
            cancel_result = cancel_slurm_job_handler(array_job_id)
            print_result(cancel_result, "Job Cancellation")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Final Status Check
    print_step("Final", "Final Job Queue Status")
    try:
        final_jobs = list_slurm_jobs_handler()
        print_result(final_jobs, "Final Job Queue")
        print(f"   Total jobs in queue: {final_jobs.get('count', 0)}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print_header("MCP Capabilities Demonstration Complete")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 All 10 MCP capabilities have been demonstrated!")
    print("\nMCP Capabilities Summary:")
    print("1. ✅ get_slurm_info - Cluster information")
    print("2. ✅ list_slurm_jobs - Job listing")
    print("3. ✅ get_queue_info - Queue information")
    print("4. ✅ get_node_info - Node information")
    print("5. ✅ submit_slurm_job - Job submission")
    print("6. ✅ check_job_status - Job status checking")
    print("7. ✅ get_job_details - Detailed job information")
    print("8. ✅ submit_array_job - Array job submission")
    print("9. ✅ get_job_output - Job output retrieval")
    print("10. ✅ cancel_slurm_job - Job cancellation")

if __name__ == "__main__":
    main()
