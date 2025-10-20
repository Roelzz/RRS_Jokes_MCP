#!/usr/bin/env python3
"""
Simple manual test for the Joke MCP Server HTTP endpoint
Use this to quickly verify the server is running and responding
"""

import requests
import json
import sys

SERVER_URL = "http://localhost:8000/mcp"

def test_endpoint():
    """Test if the MCP endpoint is responding"""
    
    print("🧪 Testing Joke MCP Server at", SERVER_URL)
    print("-" * 60)
    
    try:
        # Test 1: Check if server is alive with a simple request
        print("\n1️⃣  Testing server connectivity...")
        
        # For MCP Streamable, we need to send proper JSON-RPC requests
        response = requests.post(
            SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "roots": {
                            "listChanged": False
                        }
                    },
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10
        )
        
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Server is responding!")
            try:
                result = response.json()
                if "result" in result:
                    server_info = result.get("result", {}).get("serverInfo", {})
                    print(f"   Server: {server_info.get('name', 'Unknown')}")
                    print(f"   Version: {server_info.get('version', 'Unknown')}")
                elif "error" in result:
                    print(f"   Error from server: {result['error']}")
            except Exception as e:
                print(f"   Response: {response.text[:200]}")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            
            if response.status_code == 406:
                print("\n💡 TIP: Status 406 usually means:")
                print("   - Server might not be running in HTTP mode")
                print("   - Try restarting: python joke_mcp_server.py")
                print("   - Make sure you're not using --stdio flag")
            
            return False
        
        # Test 2: List tools
        print("\n2️⃣  Listing available tools...")
        response = requests.post(
            SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                tools = result.get("result", {}).get("tools", [])
                print(f"✅ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"   • {tool['name']}")
            else:
                print(f"⚠️  Unexpected response: {result}")
        else:
            print(f"❌ Failed to list tools: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
        
        # Test 3: Call a tool
        print("\n3️⃣  Calling get_random_joke tool...")
        response = requests.post(
            SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "get_random_joke",
                    "arguments": {}
                }
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                content = result.get("result", {}).get("content", [])
                if content and len(content) > 0:
                    joke_text = content[0].get("text", "")
                    print("✅ Got a joke:")
                    print(f"\n{joke_text}\n")
                else:
                    print("⚠️  No content returned")
                    print(f"   Full response: {result}")
            else:
                print(f"⚠️  Unexpected response: {result}")
        else:
            print(f"❌ Failed to call tool: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
        
        print("-" * 60)
        print("🎉 All tests passed! Server is working correctly.")
        print("\nYou can now connect this server to Copilot Studio!")
        print("\nNext steps:")
        print("  1. Upload joke_mcp_schema.yaml to Power Apps")
        print("  2. Create custom connector")
        print("  3. Add to your Copilot agent")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server!")
        print("\n💡 Troubleshooting:")
        print("  1. Make sure the server is running:")
        print("     python joke_mcp_server.py")
        print("\n  2. Check that you see this message:")
        print("     'Starting Joke MCP Server with HTTP transport on http://localhost:8000/mcp'")
        print("\n  3. Make sure you're NOT using the --stdio flag")
        print("\n  4. Try restarting the server")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out!")
        print("   Server might be overloaded or not responding")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON response from server: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("JOKE MCP SERVER - HTTP TEST")
    print("=" * 60)
    
    success = test_endpoint()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS - Server is ready for Copilot Studio!")
    else:
        print("❌ FAILED - Check the error messages above")
        print("\nCommon issues:")
        print("  • Server not running: python joke_mcp_server.py")
        print("  • Wrong port: Check server is on port 8000")
        print("  • STDIO mode: Don't use --stdio flag for HTTP testing")
    print("=" * 60 + "\n")
    
    sys.exit(0 if success else 1)
