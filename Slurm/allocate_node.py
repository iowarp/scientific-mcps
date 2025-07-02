#!/usr/bin/env python3
"""
Step 1: Node Allocation Test
============================
"""

import sys
import os
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🚀 STEP 1: Node Allocation Function")
    print("=" * 50)
    print()
    
    try:
        # Import the node allocation function
        from capabilities.node_allocation import allocate_nodes
        
        # Allocate nodes with specified parameters
        print("Executing: allocate_nodes(num_nodes=1, time_limit='0:02:00', job_name='test_allocation')")
        result = allocate_nodes(num_nodes=1, time_limit='0:02:00', job_name='test_allocation')
        
        print("\nResult:")
        print(json.dumps(result, indent=2))
        
        # Extract allocation ID for user reference
        allocation_id = result.get('allocation_id')
        
        print(f"\n📋 Allocation Summary:")
        print(f"   Status: {result.get('status')}")
        print(f"   Allocation ID: {allocation_id}")
        print(f"   Nodes: {result.get('allocated_nodes')}")
        print(f"   Command Used: {result.get('command_used')}")
        
        if allocation_id:
            print(f"\n🔍 STEP 2: Manual Verification Instructions")
            print("=" * 50)
            print("Run the following commands to verify the allocation:")
            print(f"   squeue -j {allocation_id}")
            print(f"   scontrol show job {allocation_id}")
            print()
            print("⚠️  Remember to run step3_deallocate_node.py to clean up!")
            
            # Save allocation ID for the deallocation script
            with open('.allocation_id', 'w') as f:
                f.write(allocation_id)
            print(f"✅ Allocation ID saved for deallocation script")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running from the Slurm directory with 'src' folder available")
    except Exception as e:
        print(f"❌ Error during allocation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
