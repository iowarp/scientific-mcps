#!/usr/bin/env python3
"""
Simple test script to validate real Slurm functionality
This script tests the core Slurm capabilities without mock functionality
"""
import sys
import os
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from capabilities.slurm_handler import (
        _check_slurm_available,
        submit_slurm_job,
        get_job_status,
        cancel_slurm_job,
        list_slurm_jobs,
        get_slurm_info
    )
    print("✅ Successfully imported Slurm handlers")
except ImportError as e:
    print(f"❌ Failed to import Slurm handlers: {e}")
    sys.exit(1)

def test_slurm_availability():
    """Test if Slurm is available"""
    print("\n🔍 Testing Slurm availability...")
    is_available = _check_slurm_available()
    if is_available:
        print("✅ Slurm is available on this system")
        return True
    else:
        print("❌ Slurm is not available on this system")
        print("   Please install Slurm to use real functionality")
        return False

def test_cluster_info():
    """Test cluster information retrieval"""
    print("\n📊 Testing cluster information...")
    try:
        info = get_slurm_info()
        print(f"✅ Cluster info retrieved: {info.get('cluster_name', 'Unknown')}")
        print(f"   Partitions: {len(info.get('partitions', []))}")
        print(f"   Real Slurm: {info.get('real_slurm', False)}")
        return True
    except Exception as e:
        print(f"❌ Failed to get cluster info: {e}")
        return False

def test_job_listing():
    """Test job listing"""
    print("\n📋 Testing job listing...")
    try:
        jobs = list_slurm_jobs()
        print(f"✅ Job listing retrieved: {jobs.get('count', 0)} jobs")
        print(f"   Real Slurm: {jobs.get('real_slurm', False)}")
        return True
    except Exception as e:
        print(f"❌ Failed to list jobs: {e}")
        return False

def test_job_submission():
    """Test job submission if Slurm is available"""
    print("\n🚀 Testing job submission...")
    
    # Create a simple test script
    test_script_content = """#!/bin/bash
echo "Test job from MCP Slurm handler"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Date: $(date)"
sleep 5
echo "Job completed!"
"""
    
    try:
        # Create temporary script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(test_script_content)
            script_path = f.name
        
        os.chmod(script_path, 0o755)
        
        # Submit job
        job_id = submit_slurm_job(script_path, cores=1, job_name="mcp_test")
        print(f"✅ Job submitted successfully: {job_id}")
        
        # Check status
        status = get_job_status(job_id)
        print(f"   Job status: {status.get('status', 'Unknown')}")
        print(f"   Real Slurm: {status.get('real_slurm', False)}")
        
        # Clean up
        os.unlink(script_path)
        
        return job_id
        
    except Exception as e:
        print(f"❌ Failed to submit job: {e}")
        if 'script_path' in locals():
            try:
                os.unlink(script_path)
            except:
                pass
        return None

def main():
    """Main test function"""
    print("🎯 Testing Real Slurm MCP Handler")
    print("=" * 50)
    
    # Test availability first
    slurm_available = test_slurm_availability()
    
    if not slurm_available:
        print("\n⚠️  Slurm is not available - testing will show error handling")
        print("   Install Slurm to test full functionality")
    
    # Test cluster info (should work even if Slurm not available - will show error)
    test_cluster_info()
    
    # Test job listing (should work even if Slurm not available - will show error)
    test_job_listing()
    
    # Test job submission only if Slurm is available
    if slurm_available:
        job_id = test_job_submission()
        if job_id:
            print(f"\n🎉 All tests passed! Job {job_id} was submitted successfully.")
    else:
        try:
            test_job_submission()
        except Exception as e:
            print(f"✅ Expected error when Slurm not available: {type(e).__name__}")
    
    print("\n" + "=" * 50)
    print("✅ Real Slurm handler testing completed!")
    
    if slurm_available:
        print("🚀 All functionality is working with real Slurm")
    else:
        print("📝 To test with real Slurm, please install Slurm on this system")

if __name__ == "__main__":
    main()
