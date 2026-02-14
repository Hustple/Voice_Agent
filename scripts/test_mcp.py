#!/usr/bin/env python3
"""
Test pfMCP connection
"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_mcp_connection():
    """Test connection to pfMCP server"""
    base_url = os.getenv("PFMCP_BASE_URL", "http://localhost:8000")
    
    print(f"Testing connection to: {base_url}")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{base_url}/health")
            
            if response.status_code == 200:
                print("✅ pfMCP server is running!")
                print(f"Response: {response.json()}")
            else:
                print(f"⚠️  Server returned status: {response.status_code}")
                
    except httpx.ConnectError:
        print("❌ Cannot connect to pfMCP server")
        print(f"Make sure the server is running at: {base_url}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
