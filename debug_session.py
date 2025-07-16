#!/usr/bin/env python3
"""
Debug session lookup
"""

import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8001"

async def debug_session():
    async with aiohttp.ClientSession() as session:
        # First, try demo login
        print("🔍 Testing demo login...")
        async with session.post(f"{BASE_URL}/api/auth/demo-login") as response:
            if response.status == 200:
                data = await response.json()
                token = data.get("access_token")
                user_id = data.get("user", {}).get("id")
                print(f"✅ Demo login successful")
                print(f"   Token: {token}")
                print(f"   User ID: {user_id}")
                
                # Test a simple endpoint to see if backend is working
                print("\n🔍 Testing health endpoint...")
                async with session.get(f"{BASE_URL}/health") as health_response:
                    health_data = await health_response.json()
                    print(f"Health status: {health_data}")
                
            else:
                print(f"❌ Demo login failed: {response.status}")
                error_data = await response.text()
                print(f"Error: {error_data}")

if __name__ == "__main__":
    asyncio.run(debug_session())