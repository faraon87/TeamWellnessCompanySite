#!/usr/bin/env python3
"""
Debug authentication issues
"""

import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8001"

async def debug_auth():
    async with aiohttp.ClientSession() as session:
        # First, try demo login
        print("🔍 Testing demo login...")
        async with session.post(f"{BASE_URL}/api/auth/demo-login") as response:
            if response.status == 200:
                data = await response.json()
                token = data.get("access_token")
                print(f"✅ Demo login successful, token: {token[:20]}...")
                
                # Now test /api/auth/me with this token
                print("\n🔍 Testing /api/auth/me with demo token...")
                headers = {"Authorization": f"Bearer {token}"}
                async with session.get(f"{BASE_URL}/api/auth/me", headers=headers) as me_response:
                    print(f"Status: {me_response.status}")
                    me_data = await me_response.text()
                    print(f"Response: {me_data}")
            else:
                print(f"❌ Demo login failed: {response.status}")
                error_data = await response.text()
                print(f"Error: {error_data}")

if __name__ == "__main__":
    asyncio.run(debug_auth())