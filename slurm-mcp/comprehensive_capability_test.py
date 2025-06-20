#!/usr/bin/env python3
"""
Comprehensive MCP Server Slurm Capabilities Test
================================================
This script tests ALL MCP server Slurm capabilities:
1. Cluster Information
2. Job Submission  
3. Job Listing
4. Job Details
5. Job Output
6. Job Cancellation
7. Node Information (if available)
"""

import sys
import os
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_handlers import (
    get_slurm_info_handler,
    submit_slurm_job_handler,
    list_slurm_jobs_handler,
    get_job_details_handler,
    get_job_output_handler,
    cancel_slurm_job_handler
)

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"🎯 {title}")
    print(f"{'='*70}")

def print_result(title, result):
    """Print formatted result."""
    print(f"\n📋 {title}:")
    print("-" * 60)
    print(json.dumps(result, indent=2))
    print("-" * 60)

def main():
    """Run comprehensive capability tests."""
    print("🚀 MCP SERVER SLURM CAPABILITIES TEST")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test 1: Cluster Information
    print_section("Test 1: Cluster Information Capability")
    try:
        cluster_info = get_slurm_info_handler()
        print_result("Cluster Info", cluster_info)
        results['cluster_info'] = '✅ PASS'
        print("✅ Cluster information capability: WORKING")
    except Exception as e:
        print(f"❌ Cluster information capability: FAILED - {e}")
        results['cluster_info'] = f'❌ FAIL: {e}'
    
    # Test 2: Job Listing
    print_section("Test 2: Job Listing Capability")
    try:
        jobs_list = list_slurm_jobs_handler()
        print_result("Current Jobs", jobs_list)
        results['job_listing'] = '✅ PASS'
        print("✅ Job listing capability: WORKING")
    except Exception as e:
        print(f"❌ Job listing capability: FAILED - {e}")
        results['job_listing'] = f'❌ FAIL: {e}'
    
    # Test 3: Job Submission
    print_section("Test 3: Job Submission Capability")
    
    # Create test job script
    test_script = "comprehensive_test.sh"
    with open(test_script, 'w') as f:
        f.write('''#!/bin/bash
#SBATCH --job-name=comprehensive_test
#SBATCH --output=comprehensive_%j.out
#SBATCH --time=00:01:30

echo "🎯 Comprehensive MCP Capability Test"
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $(hostname)"
echo "User: $USER"
echo "Start Time: $(date)"
echo ""
echo "System Information:"
echo "CPUs: $(nproc)"
echo "Memory: $(free -h | grep Mem)"
echo ""
echo "Slurm Environment:"
echo "SLURM_JOB_ID: $SLURM_JOB_ID"
echo "SLURM_NTASKS: $SLURM_NTASKS"
echo "SLURM_CPUS_ON_NODE: $SLURM_CPUS_ON_NODE"
echo ""
echo "Running comprehensive test computation..."
for i in {1..10}; do
    echo "Processing step $i/10 at $(date)"
    sleep 1
done
echo ""
echo "✅ Comprehensive test completed successfully!"
echo "End Time: $(date)"
''')
    
    os.chmod(test_script, 0o755)
    
    try:
        submission_result = submit_slurm_job_handler(
            script_path=test_script,
            cores=2,
            memory='2GB',
            time_limit='00:02:00',
            job_name='comprehensive_test',
            partition='debug'
        )
        print_result("Job Submission", submission_result)
        test_job_id = submission_result['job_id']
        results['job_submission'] = '✅ PASS'
        print(f"✅ Job submission capability: WORKING (Job ID: {test_job_id})")
    except Exception as e:
        print(f"❌ Job submission capability: FAILED - {e}")
        results['job_submission'] = f'❌ FAIL: {e}'
        test_job_id = None
    
    # Test 4: Job Details (if we have a job ID)
    if test_job_id:
        print_section("Test 4: Job Details Capability")
        try:
            job_details = get_job_details_handler(test_job_id)
            print_result(f"Job {test_job_id} Details", job_details)
            results['job_details'] = '✅ PASS'
            print(f"✅ Job details capability: WORKING")
        except Exception as e:
            print(f"❌ Job details capability: FAILED - {e}")
            results['job_details'] = f'❌ FAIL: {e}'
        
        # Test 5: Wait for job completion and check output
        print_section("Test 5: Job Monitoring and Output")
        print("⏳ Waiting for job completion...")
        
        max_wait = 120  # 2 minutes max wait
        wait_time = 0
        job_completed = False
        
        while wait_time < max_wait:
            try:
                job_details = get_job_details_handler(test_job_id)
                job_state = job_details['details']['jobstate']
                print(f"   Job {test_job_id} state: {job_state} (waited {wait_time}s)")
                
                if job_state in ['COMPLETED', 'FAILED', 'CANCELLED']:
                    job_completed = True
                    break
                    
                time.sleep(5)
                wait_time += 5
                
            except Exception as e:
                print(f"   Error checking job status: {e}")
                break
        
        if job_completed:
            try:
                # Test job output capability
                output_result = get_job_output_handler(test_job_id)
                print_result(f"Job {test_job_id} Output", output_result)
                results['job_output'] = '✅ PASS'
                print("✅ Job output capability: WORKING")
                
                # Also try to read the actual output file
                output_file = f"comprehensive_{test_job_id}.out"
                if os.path.exists(output_file):
                    print(f"\n📄 Actual job output from {output_file}:")
                    print("-" * 60)
                    with open(output_file, 'r') as f:
                        print(f.read())
                    print("-" * 60)
                
            except Exception as e:
                print(f"❌ Job output capability: FAILED - {e}")
                results['job_output'] = f'❌ FAIL: {e}'
        else:
            print("⏰ Job did not complete within timeout period")
            results['job_output'] = '⏰ TIMEOUT'
    
    # Test 6: Job Cancellation (submit a job specifically for cancellation)
    print_section("Test 6: Job Cancellation Capability")
    
    cancel_script = "cancellation_test.sh"
    with open(cancel_script, 'w') as f:
        f.write('''#!/bin/bash
#SBATCH --job-name=cancellation_test
#SBATCH --output=cancel_%j.out
#SBATCH --time=00:10:00

echo "Job for cancellation test - Job ID: $SLURM_JOB_ID"
echo "This job should be cancelled before completion"
for i in {1..600}; do
    echo "Step $i/600 - $(date)"
    sleep 1
done
echo "ERROR: Job completed without being cancelled!"
''')
    
    os.chmod(cancel_script, 0o755)
    
    try:
        cancel_job_result = submit_slurm_job_handler(
            script_path=cancel_script,
            cores=1,
            memory='1GB',
            time_limit='00:10:00',
            job_name='cancellation_test',
            partition='debug'
        )
        
        cancel_job_id = cancel_job_result['job_id']
        print(f"🚀 Submitted job {cancel_job_id} for cancellation test")
        
        # Wait a moment for job to start
        time.sleep(3)
        
        # Cancel the job
        cancel_result = cancel_slurm_job_handler(cancel_job_id)
        print_result(f"Cancellation of Job {cancel_job_id}", cancel_result)
        results['job_cancellation'] = '✅ PASS'
        print("✅ Job cancellation capability: WORKING")
        
    except Exception as e:
        print(f"❌ Job cancellation capability: FAILED - {e}")
        results['job_cancellation'] = f'❌ FAIL: {e}'
    
    # Final Summary
    print_section("FINAL CAPABILITY TEST RESULTS")
    
    print("📊 CAPABILITY TEST SUMMARY:")
    print("=" * 70)
    
    capabilities = [
        ("Cluster Information", results.get('cluster_info', '❓ NOT TESTED')),
        ("Job Listing", results.get('job_listing', '❓ NOT TESTED')),
        ("Job Submission", results.get('job_submission', '❓ NOT TESTED')),
        ("Job Details", results.get('job_details', '❓ NOT TESTED')),
        ("Job Output", results.get('job_output', '❓ NOT TESTED')),
        ("Job Cancellation", results.get('job_cancellation', '❓ NOT TESTED'))
    ]
    
    passed = 0
    total = len(capabilities)
    
    for capability, status in capabilities:
        print(f"{capability:.<25} {status}")
        if status.startswith('✅'):
            passed += 1
    
    print("=" * 70)
    print(f"OVERALL RESULT: {passed}/{total} capabilities working")
    
    if passed == total:
        print("🎉 ALL MCP SLURM CAPABILITIES ARE WORKING!")
        print("The MCP server provides complete Slurm integration.")
    elif passed >= total * 0.8:
        print("✅ MOST capabilities are working - MCP server is functional")
    elif passed >= total * 0.5:
        print("⚠️  SOME capabilities are working - partial functionality")
    else:
        print("❌ MANY capabilities failed - needs investigation")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
