#!/usr/bin/env python3
"""
Node Allocation Demo Script
Demonstrates the new salloc-based node allocation capabilities for Slurm MCP.

This script showcases:
1. Interactive node allocation using salloc
2. Partition checking and validation
3. Time limit handling (user-specified vs system default)
4. Resource specification (CPUs, memory, generic resources)
5. Exclusive node allocation
6. Allocation info retrieval
7. Proper cleanup and deallocation

Usage: python node_allocation_demo.py
"""

import sys
import os
import time
import json
from typing import Optional, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from capabilities.node_allocation import allocate_nodes, deallocate_allocation, get_allocation_info
from capabilities.queue_info import get_queue_info
from capabilities.utils import check_slurm_available

def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_result(title: str, result: dict):
    """Print formatted result."""
    print(f"\n📋 {title}:")
    print("-" * 40)
    for key, value in result.items():
        if isinstance(value, (dict, list)) and len(str(value)) > 100:
            print(f"  {key}: <complex data structure>")
        else:
            print(f"  {key}: {value}")

def get_available_partition() -> Optional[str]:
    """Get the first available partition, or None if none found."""
    try:
        queue_info = get_queue_info()
        if queue_info.get("real_slurm", False) and "partitions" in queue_info:
            partitions = list(queue_info["partitions"].keys())
            return partitions[0] if partitions else None
        return None
    except Exception as e:
        print(f"⚠️  Could not get partition info: {e}")
        return None

def demo_basic_allocation():
    """Demo 1: Basic node allocation with system default time limit."""
    print_header("Demo 1: Basic Node Allocation (System Default Time)")
    
    print("🚀 Allocating 1 node with system default time limit...")
    print("   Command equivalent: salloc -N 1 --immediate --no-shell")
    
    result = allocate_nodes(
        num_nodes=1,
        immediate=True  # Use immediate to avoid long waits in demo
    )
    
    print_result("Allocation Result", result)
    
    if result["status"] == "allocated":
        allocation_id = result["allocation_id"]
        print(f"✅ Successfully allocated node(s)! Allocation ID: {allocation_id}")
        
        # Clean up
        print("🧹 Cleaning up allocation...")
        cleanup_result = deallocate_allocation(allocation_id)
        print_result("Cleanup Result", cleanup_result)
    else:
        print(f"❌ Allocation failed: {result.get('message', 'Unknown error')}")

def demo_partition_validation():
    """Demo 2: Partition validation and checking."""
    print_header("Demo 2: Partition Validation")
    
    print("🔍 Checking available partitions...")
    partition = get_available_partition()
    
    if partition:
        print(f"✅ Found partition: {partition}")
        print(f"🚀 Allocating node with partition '{partition}'...")
        
        result = allocate_nodes(
            num_nodes=1,
            partition=partition,
            job_name="partition_demo",
            immediate=True
        )
        
        print_result("Partition Allocation Result", result)
        
        if result["status"] == "allocated":
            deallocate_allocation(result["allocation_id"])
            print("✅ Allocation successful and cleaned up")
        
    else:
        print("⚠️  No partitions found. Testing with invalid partition...")
        result = allocate_nodes(
            num_nodes=1,
            partition="nonexistent_partition",
            immediate=True
        )
        print_result("Invalid Partition Result", result)
        
        if "partition" in result.get("message", "").lower():
            print("✅ Correctly detected invalid partition")

def demo_time_limit_handling():
    """Demo 3: Time limit handling (user-specified vs system default)."""
    print_header("Demo 3: Time Limit Handling")
    
    print("🕐 Test 1: User-specified time limit (2 minutes)...")
    result1 = allocate_nodes(
        num_nodes=1,
        time_limit="0:02:00",  # User specified
        job_name="time_demo_user",
        immediate=True
    )
    
    print_result("User Time Limit Result", result1)
    
    if result1["status"] == "allocated":
        print(f"✅ Time limit set to: {result1['time_limit']}")
        deallocate_allocation(result1["allocation_id"])
    
    print("\n🕐 Test 2: System default time limit (no time specified)...")
    result2 = allocate_nodes(
        num_nodes=1,
        job_name="time_demo_default",
        immediate=True
    )
    
    print_result("System Default Time Result", result2)
    
    if result2["status"] == "allocated":
        print("✅ Using system default time limit")
        deallocate_allocation(result2["allocation_id"])

def demo_resource_specification():
    """Demo 4: Resource specification (CPUs, memory, etc.)."""
    print_header("Demo 4: Resource Specification")
    
    partition = get_available_partition()
    
    print("💻 Allocating node with specific resource requirements...")
    print("   - 1 CPU per task")
    print("   - 1GB memory")
    print("   - Exclusive access")
    
    result = allocate_nodes(
        num_nodes=1,
        time_limit="0:01:00",
        partition=partition,
        cpus_per_task=1,
        memory="1G",
        exclusive=True,
        job_name="resource_demo",
        immediate=True
    )
    
    print_result("Resource Allocation Result", result)
    
    if result["status"] == "allocated":
        print("✅ Resource allocation successful!")
        if "command_used" in result:
            print(f"📝 Command used: {result['command_used']}")
        deallocate_allocation(result["allocation_id"])
    else:
        print(f"❌ Resource allocation failed: {result.get('message', 'Unknown error')}")

def demo_allocation_info():
    """Demo 5: Allocation information retrieval."""
    print_header("Demo 5: Allocation Information Retrieval")
    
    print("🚀 Creating a test allocation...")
    result = allocate_nodes(
        num_nodes=1,
        time_limit="0:01:00",
        job_name="info_demo",
        immediate=True
    )
    
    if result["status"] == "allocated":
        allocation_id = result["allocation_id"]
        print(f"✅ Allocation created: {allocation_id}")
        
        print("🔍 Retrieving allocation information...")
        info_result = get_allocation_info(allocation_id)
        print_result("Allocation Info", info_result)
        
        # Clean up
        deallocate_allocation(allocation_id)
        print("✅ Allocation cleaned up")
    else:
        print("❌ Could not create test allocation for info demo")

def demo_error_handling():
    """Demo 6: Error handling and validation."""
    print_header("Demo 6: Error Handling")
    
    print("🧪 Test 1: Invalid time format...")
    result1 = allocate_nodes(
        time_limit="invalid_time",
        immediate=True
    )
    print_result("Invalid Time Format", result1)
    
    print("\n🧪 Test 2: Non-existent node specification...")
    result2 = allocate_nodes(
        specific_nodes=["nonexistent_node_999"],
        immediate=True
    )
    print_result("Non-existent Node", result2)
    
    print("\n🧪 Test 3: Getting info for non-existent allocation...")
    result3 = get_allocation_info("999999")
    print_result("Non-existent Allocation Info", result3)

def main():
    """Main demo function."""
    print_header("Slurm Node Allocation Capabilities Demo")
    print("This demo showcases the new salloc-based node allocation features.")
    
    # Check if Slurm is available
    if not check_slurm_available():
        print("❌ Slurm is not available on this system!")
        print("   Please install Slurm or run this demo on a Slurm-enabled cluster.")
        sys.exit(1)
    
    print("✅ Slurm is available - proceeding with demo...")
    
    try:
        # Run all demos
        demo_basic_allocation()
        demo_partition_validation()
        demo_time_limit_handling()
        demo_resource_specification()
        demo_allocation_info()
        demo_error_handling()
        
        print_header("Demo Complete")
        print("🎉 All node allocation demos completed successfully!")
        print("\n📚 Summary of demonstrated features:")
        print("   ✅ Basic node allocation with salloc")
        print("   ✅ Partition validation and error handling")
        print("   ✅ Time limit handling (user vs system default)")
        print("   ✅ Resource specification (CPU, memory, exclusive)")
        print("   ✅ Allocation information retrieval")
        print("   ✅ Proper error handling and cleanup")
        
        print("\n🚀 Integration with MCP:")
        print("   - All functions are available as MCP tools")
        print("   - Compatible with fastmcp server framework")
        print("   - Full error handling and logging")
        print("   - Real-time allocation status monitoring")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
