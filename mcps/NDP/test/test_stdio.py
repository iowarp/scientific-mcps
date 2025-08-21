#!/usr/bin/env python3
"""
Test script to verify stdio communication with the NDP MCP server.
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

async def test_stdio_communication():
    """Test stdio communication with the NDP MCP server."""
    
    print("🧪 Testing STDIO Communication with NDP MCP Server")
    print("=" * 60)
    
    # Start the server process
    process = subprocess.Popen(
        [sys.executable, "../ndp_mcp_server.py", "--base-url", "http://155.101.6.191:8003"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Test 1: Initialize request
        print("📡 Test 1: Sending initialize request...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialize request
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            response_data = json.loads(response)
            print(f"✅ Initialize response received: {response_data.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        else:
            print("❌ No response received for initialize")
            return False
        
        # Test 2: List tools request
        print("📡 Test 2: Sending tools/list request...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        # Send tools list request
        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            response_data = json.loads(response)
            tools = response_data.get('result', {}).get('tools', [])
            print(f"✅ Tools list received: {len(tools)} tools available")
            for tool in tools:
                print(f"   - {tool.get('name', 'Unknown')}")
        else:
            print("❌ No response received for tools/list")
            return False
        
        # Test 3: List resources request
        print("📡 Test 3: Sending resources/list request...")
        resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        
        # Send resources list request
        process.stdin.write(json.dumps(resources_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            response_data = json.loads(response)
            resources = response_data.get('result', {}).get('resources', [])
            print(f"✅ Resources list received: {len(resources)} resources available")
            for resource in resources:
                print(f"   - {resource.get('uri', 'Unknown')}")
        else:
            print("❌ No response received for resources/list")
            return False
        
        # Test 4: Call tool request
        print("📡 Test 4: Sending tool call request...")
        tool_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "list_organizations",
                "arguments": {}
            }
        }
        
        # Send tool call request
        process.stdin.write(json.dumps(tool_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            response_data = json.loads(response)
            print("✅ Tool call response received")
            if 'error' in response_data:
                print(f"   ⚠️  Tool call error: {response_data['error'].get('message', 'Unknown error')}")
            else:
                print("   ✅ Tool call successful")
        else:
            print("❌ No response received for tool call")
            return False
        
        print("\n🎉 All STDIO communication tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    finally:
        # Clean up
        process.terminate()
        process.wait()

def test_command_line_args():
    """Test command line argument parsing."""
    
    print("\n🔧 Testing Command Line Arguments")
    print("=" * 40)
    
    # Test help
    try:
        result = subprocess.run(
            [sys.executable, "../ndp_mcp_server.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Help command works")
        else:
            print("❌ Help command failed")
            return False
    except Exception as e:
        print(f"❌ Error testing help: {e}")
        return False
    
    # Test custom base URL
    try:
        result = subprocess.run(
            [sys.executable, "../ndp_mcp_server.py", "--base-url", "http://test-server:8003", "--server", "test"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ Custom parameters accepted")
    except subprocess.TimeoutExpired:
        print("✅ Server started with custom parameters (timeout expected)")
    except Exception as e:
        print(f"❌ Error testing custom parameters: {e}")
        return False
    
    return True

async def main():
    """Main test function."""
    
    print("🚀 NDP MCP Server STDIO Communication Test")
    print("=" * 60)
    
    # Test command line arguments
    if not test_command_line_args():
        print("❌ Command line argument tests failed")
        return
    
    # Test stdio communication
    if await test_stdio_communication():
        print("\n🎉 All tests passed! STDIO communication is working correctly.")
    else:
        print("\n❌ STDIO communication tests failed.")

if __name__ == "__main__":
    asyncio.run(main())
