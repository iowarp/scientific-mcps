#!/usr/bin/env python3
"""
Step 3: Node Deallocation Test
==============================
"""
import sys
import os
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def get_allocation_id():
    """Get allocation ID from command line argument or saved file."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    # Try to read from saved file
    if os.path.exists('.allocation_id'):
        with open('.allocation_id', 'r') as f:
            allocation_id = f.read().strip()
            print(f"📖 Using saved allocation ID: {allocation_id}")
            return allocation_id
    
    return None

def main():
    print("🧹 STEP 3: Node Deallocation Function")
    print("=" * 50)
    print()
    
    # Get allocation ID
    allocation_id = get_allocation_id()
    
    if not allocation_id:
        print("❌ No allocation ID provided!")
        print("Usage: python step3_deallocate_node.py <allocation_id>")
        print("   or: Run step1_allocate_node.py first to save allocation ID")
        return 1
    
    try:
        # Import the deallocation function
        from capabilities.node_allocation import deallocate_allocation
        
        print(f"Executing: deallocate_allocation('{allocation_id}')")
        result = deallocate_allocation(allocation_id)
        
        print("\nResult:")
        print(json.dumps(result, indent=2))
        
        print(f"\n📋 Deallocation Summary:")
        print(f"   Status: {result.get('status')}")
        print(f"   Allocation ID: {result.get('allocation_id')}")
        print(f"   Message: {result.get('message')}")
        
        print(f"\n🔍 STEP 4: Manual Verification Instructions")
        print("=" * 50)
        print("Run the following commands to verify the deallocation:")
        print(f"   squeue -j {allocation_id}")
        print(f"   scontrol show job {allocation_id}")
        print()
        # Clean up the saved allocation ID file
        if os.path.exists('.allocation_id'):
            os.remove('.allocation_id')
            print("\n🧹 Cleaned up saved allocation ID file")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running from the Slurm directory with 'src' folder available")
    except Exception as e:
        print(f"❌ Error during deallocation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
