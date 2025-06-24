#!/usr/bin/env python3
"""
Node Allocation Capabilities Demo
Demonstrates the new salloc-based node allocation functionality.

This script showcases:
1. Basic node allocation with system default time
2. Node allocation with user-specified parameters  
3. Partition validation and error handling
4. Node deallocation
5. Getting allocation information
6. Resource specification (CPU, memory, etc.)
7. Exclusive node allocation
8. Immediate allocation attempts

Usage:
    python node_allocation_demo.py
"""

import sys
import os
import time
import json
import logging
from typing import Dict, Any

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from capabilities.node_allocation import allocate_nodes, deallocate_allocation, get_allocation_info
from capabilities.queue_info import get_queue_info
from capabilities.utils import check_slurm_available

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print('='*60)

def print_result(result: Dict[str, Any], title: str = "Result"):
    """Print formatted results."""
    print(f"\n📋 {title}:")
    print("-" * 40)
    for key, value in result.items():
        if isinstance(value, list) and len(value) > 3:
            print(f"  {key}: [{', '.join(map(str, value[:3]))}, ... ({len(value)} total)]")
        else:
            print(f"  {key}: {value}")
    print("-" * 40)

def get_available_partitions():
    """Get available partitions from the system."""
    try:
        queue_info = get_queue_info()
        if queue_info.get("real_slurm", False) and "partitions" in queue_info:
            partitions = list(queue_info["partitions"].keys())
            return partitions
        return []
    except Exception as e:
        logger.error(f"Error getting partitions: {e}")
        return []

def demo_basic_allocation():
    """Demo 1: Basic node allocation with system default time limit."""
    print_header("Demo 1: Basic Node Allocation (System Default Time)")
    
    print("🔧 Allocating 1 node with system default time limit...")
    result = allocate_nodes(
        num_nodes=1,
        immediate=True  # Don't wait long for demo
    )
    
    print_result(result, "Basic Allocation Result")
    
    # Clean up if successful
    if result["status"] == "allocated":
        print("\n🧹 Cleaning up allocation...")
        cleanup_result = deallocate_allocation(result["allocation_id"])
        print_result(cleanup_result, "Cleanup Result")
    
    return result

def demo_partition_validation():
    """Demo 2: Partition validation and error handling."""
    print_header("Demo 2: Partition Validation")
    
    # Get available partitions
    partitions = get_available_partitions()
    
    if partitions:
        print(f"📋 Available partitions: {', '.join(partitions)}")
        
        # Try with a valid partition
        print(f"\n🔧 Trying allocation with valid partition: {partitions[0]}")
        result = allocate_nodes(
            num_nodes=1,
            partition=partitions[0],
            time_limit="0:01:00",
            immediate=True
        )
        print_result(result, "Valid Partition Result")
        
        # Clean up if successful
        if result["status"] == "allocated":
            deallocate_allocation(result["allocation_id"])
    else:
        print("⚠️  No partitions found - please check partitions first with: sinfo -s")
    
    # Try with invalid partition
    print("\n🔧 Trying allocation with invalid partition...")
    result = allocate_nodes(
        num_nodes=1,
        partition="nonexistent_partition",
        immediate=True
    )
    print_result(result, "Invalid Partition Result")

def demo_time_limit_variations():
    """Demo 3: Different time limit scenarios."""
    print_header("Demo 3: Time Limit Variations")
    
    # Test 1: No time limit (system default)
    print("🔧 Test 1: No time limit specified (system default)")
    result1 = allocate_nodes(num_nodes=1, immediate=True)
    print_result(result1, "System Default Time")
    if result1["status"] == "allocated":
        deallocate_allocation(result1["allocation_id"])
    
    # Test 2: User-specified time limit
    print("\n🔧 Test 2: User-specified time limit (2 minutes)")
    result2 = allocate_nodes(num_nodes=1, time_limit="0:02:00", immediate=True)
    print_result(result2, "User-Specified Time")
    if result2["status"] == "allocated":
        deallocate_allocation(result2["allocation_id"])

def demo_resource_specification():
    """Demo 4: Resource specification (CPU, memory, etc.)."""
    print_header("Demo 4: Resource Specification")
    
    print("🔧 Allocating with specific resource requirements...")
    result = allocate_nodes(
        num_nodes=1,
        time_limit="0:01:00",
        cpus_per_task=1,  # Conservative request
        memory="1G",      # Conservative memory request
        job_name="resource_demo",
        immediate=True
    )
    
    print_result(result, "Resource Specification Result")
    
    if result["status"] == "allocated":
        print("\n📊 Checking allocation details...")
        info_result = get_allocation_info(result["allocation_id"])
        print_result(info_result, "Allocation Details")
        
        # Clean up
        print("\n🧹 Cleaning up...")
        deallocate_allocation(result["allocation_id"])

def demo_workflow_integration():
    """Demo 5: Complete workflow integration."""
    print_header("Demo 5: Complete Workflow Integration")
    
    print("🔧 Complete allocation workflow...")
    
    # Step 1: Allocate
    print("Step 1: Allocating nodes...")
    alloc_result = allocate_nodes(
        num_nodes=1,
        time_limit="0:01:00",
        job_name="workflow_demo",
        immediate=True
    )
    print_result(alloc_result, "Allocation")
    
    if alloc_result["status"] == "allocated":
        job_id = alloc_result["allocation_id"]
        
        # Step 2: Get allocation info
        print("\nStep 2: Getting allocation information...")
        info_result = get_allocation_info(job_id)
        print_result(info_result, "Allocation Info")
        
        # Step 3: Deallocate
        print("\nStep 3: Deallocating...")
        dealloc_result = deallocate_allocation(job_id)
        print_result(dealloc_result, "Deallocation")
        
        print("\n✅ Complete workflow finished successfully!")
    else:
        print("⚠️  Initial allocation failed, skipping workflow steps")

def main():
    """Main demo function."""
    print_header("Slurm Node Allocation Capabilities Demo")
    
    # Check if Slurm is available
    if not check_slurm_available():
        print("❌ Slurm is not available on this system!")
        print("Please install Slurm to run this demo.")
        return
    
    print("✅ Slurm is available! Starting demo...")
    
    # Run all demos
    demos = [
        demo_basic_allocation,
        demo_partition_validation,
        demo_time_limit_variations,
        demo_resource_specification,
        demo_workflow_integration
    ]
    
    for i, demo in enumerate(demos, 1):
        try:
            demo()
            print(f"\n✅ Demo {i} completed successfully!")
        except Exception as e:
            print(f"\n❌ Demo {i} failed with error: {e}")
            logger.exception(f"Demo {i} error")
        
        if i < len(demos):
            print("\n" + "⏳ Waiting 2 seconds before next demo...")
            time.sleep(2)
    
    print_header("Demo Complete")
    print("🎉 All node allocation demos completed!")
    print("\nNew capabilities added:")
    print("  • ✅ Interactive node allocation with salloc")
    print("  • ✅ Partition validation and error handling") 
    print("  • ✅ Flexible time limit handling (system default or user-specified)")
    print("  • ✅ Resource specification (CPU, memory)")
    print("  • ✅ Allocation status monitoring")
    print("  • ✅ Proper cleanup and deallocation")
    print("  • ✅ Comprehensive error handling")

if __name__ == "__main__":
    main()
