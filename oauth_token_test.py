#!/usr/bin/env python3
"""
OAuth Token Test - Test OAuth endpoints with valid token
"""

import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8001"

async def test_oauth_with_token():
    async with aiohttp.ClientSession() as session:
        # First, create a user and get a token
        signup_data = {
            "email": "oauth.test@teamwelly.com",
            "name": "OAuth Test User",
            "plan": "plus"
        }
        
        async with session.post(f"{BASE_URL}/api/auth/signup", json=signup_data) as response:
            if response.status == 200:
                auth_data = await response.json()
                token = auth_data.get("access_token")
                user_id = auth_data.get("user", {}).get("id")
                print(f"✅ Created user with token: {token[:20]}...")
                
                # Test OAuth me endpoint with token
                headers = {"Authorization": f"Bearer {token}"}
                async with session.get(f"{BASE_URL}/api/auth/oauth/me", headers=headers) as me_response:
                    if me_response.status == 200:
                        user_data = await me_response.json()
                        print(f"✅ OAuth /me endpoint works: {user_data.get('email')}")
                    else:
                        error_data = await me_response.json()
                        print(f"❌ OAuth /me endpoint failed: {me_response.status} - {error_data}")
                
                # Test OAuth logout with token
                async with session.post(f"{BASE_URL}/api/auth/oauth/logout", headers=headers) as logout_response:
                    if logout_response.status == 200:
                        logout_data = await logout_response.json()
                        print(f"✅ OAuth logout works: {logout_data.get('message')}")
                    else:
                        error_data = await logout_response.json()
                        print(f"❌ OAuth logout failed: {logout_response.status} - {error_data}")
            else:
                error_data = await response.json()
                print(f"❌ Failed to create user: {response.status} - {error_data}")

if __name__ == "__main__":
    asyncio.run(test_oauth_with_token())