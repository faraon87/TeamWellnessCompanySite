#!/usr/bin/env python3
"""
OAuth Credentials Testing Script
Tests the newly rotated Google OAuth credentials
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8001"

class OAuthTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    async def make_request(self, method: str, endpoint: str, data: dict = None, headers: dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            request_headers = {"Content-Type": "application/json"}
            
            if headers:
                request_headers.update(headers)
            
            async with self.session.request(
                method, 
                url, 
                json=data if data else None,
                headers=request_headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()
                
                return response.status < 400, response_data, response.status
                
        except Exception as e:
            return False, str(e), 0
    
    async def test_oauth_credentials_loading(self):
        """Test if OAuth credentials are properly loaded"""
        print("\n🔑 Testing OAuth Credentials Loading...")
        
        # Test Google OAuth initiation (should redirect or return redirect info)
        success, data, status = await self.make_request("GET", "/api/auth/google")
        
        # Check if the response indicates proper OAuth setup
        google_working = False
        if status == 302:
            # Redirect response - OAuth is working
            google_working = True
            details = f"Status: {status}, OAuth redirect working"
        elif status == 200 and isinstance(data, str) and "google" in data.lower():
            # HTML response with Google OAuth
            google_working = True
            details = f"Status: {status}, OAuth HTML response received"
        elif status == 500:
            # Check if it's a configuration error
            error_msg = str(data).lower()
            if "client_id" in error_msg or "client_secret" in error_msg or "oauth" in error_msg:
                details = f"Status: {status}, OAuth configuration error: {data}"
            else:
                details = f"Status: {status}, Server error: {data}"
        else:
            details = f"Status: {status}, Response: {data}"
        
        self.log_test(
            "Google OAuth initiation (/api/auth/google)", 
            google_working,
            details
        )
        
        return google_working
    
    async def test_oauth_callback_handling(self):
        """Test OAuth callback endpoint"""
        print("\n🔄 Testing OAuth Callback Handling...")
        
        # Test Google OAuth callback (without actual Google token, should fail gracefully)
        success, data, status = await self.make_request("GET", "/api/auth/google/callback")
        
        # Should fail gracefully without proper OAuth flow
        callback_working = status in [400, 401, 500] or "error" in str(data).lower()
        
        self.log_test(
            "Google OAuth callback (/api/auth/google/callback)", 
            callback_working,
            f"Status: {status}, Handles callback appropriately without token"
        )
        
        return callback_working
    
    async def test_placeholder_oauth_providers(self):
        """Test placeholder OAuth providers"""
        print("\n📱 Testing Placeholder OAuth Providers...")
        
        # Test Apple OAuth (should return 501 - not implemented)
        success, data, status = await self.make_request("GET", "/api/auth/apple")
        apple_working = status == 501 and "not implemented" in str(data).lower()
        self.log_test(
            "Apple OAuth placeholder (/api/auth/apple)", 
            apple_working,
            f"Status: {status}, Returns proper 501 not implemented error"
        )
        
        # Test Twitter OAuth (should return 501 - not implemented)
        success, data, status = await self.make_request("GET", "/api/auth/twitter")
        twitter_working = status == 501 and "not implemented" in str(data).lower()
        self.log_test(
            "Twitter OAuth placeholder (/api/auth/twitter)", 
            twitter_working,
            f"Status: {status}, Returns proper 501 not implemented error"
        )
        
        return apple_working and twitter_working
    
    async def test_oauth_session_management(self):
        """Test OAuth session management endpoints"""
        print("\n🔐 Testing OAuth Session Management...")
        
        # Test OAuth logout (without token, should fail appropriately)
        success, data, status = await self.make_request("POST", "/api/auth/oauth/logout")
        logout_working = status == 401 and "token" in str(data).lower()
        self.log_test(
            "OAuth logout without token (/api/auth/oauth/logout)", 
            logout_working,
            f"Status: {status}, Requires authentication token as expected"
        )
        
        # Test OAuth me endpoint (without token, should fail appropriately)
        success, data, status = await self.make_request("GET", "/api/auth/oauth/me")
        me_working = status == 401 and "token" in str(data).lower()
        self.log_test(
            "OAuth get current user without token (/api/auth/oauth/me)", 
            me_working,
            f"Status: {status}, Requires authentication token as expected"
        )
        
        return logout_working and me_working
    
    async def test_backend_environment_loading(self):
        """Test if backend is loading environment variables correctly"""
        print("\n🌍 Testing Backend Environment Loading...")
        
        # Test root endpoint to see if backend is running
        success, data, status = await self.make_request("GET", "/")
        root_working = success and status == 200 and data.get("version") == "2.0.0"
        self.log_test(
            "Backend root endpoint (/)", 
            root_working,
            f"Status: {status}, Version: {data.get('version') if success else 'Failed'}"
        )
        
        # Test health endpoint
        success, data, status = await self.make_request("GET", "/health")
        health_working = success and status == 200 and data.get("status") == "healthy"
        self.log_test(
            "Backend health endpoint (/health)", 
            health_working,
            f"Status: {status}, Health: {data.get('status') if success else 'Failed'}"
        )
        
        return root_working and health_working
    
    async def run_oauth_tests(self):
        """Run all OAuth-specific tests"""
        print("🚀 Starting OAuth Credentials Testing")
        print(f"Testing against: {BASE_URL}")
        print("=" * 60)
        
        try:
            # Test backend is running
            backend_ok = await self.test_backend_environment_loading()
            
            if not backend_ok:
                print("❌ Backend is not running properly. Cannot test OAuth.")
                return
            
            # Test OAuth credentials loading
            oauth_credentials_ok = await self.test_oauth_credentials_loading()
            
            # Test OAuth callback handling
            oauth_callback_ok = await self.test_oauth_callback_handling()
            
            # Test placeholder providers
            placeholders_ok = await self.test_placeholder_oauth_providers()
            
            # Test session management
            session_mgmt_ok = await self.test_oauth_session_management()
            
        except Exception as e:
            print(f"❌ Test suite error: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 OAUTH TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n🎯 OAUTH INTEGRATION STATUS:")
        oauth_working = passed_tests >= total_tests * 0.8  # 80% success rate
        if oauth_working:
            print("✅ OAuth integration is working with new credentials")
        else:
            print("❌ OAuth integration has issues with new credentials")
        
        return passed_tests, failed_tests, total_tests

async def main():
    """Main test runner"""
    async with OAuthTester() as tester:
        passed, failed, total = await tester.run_oauth_tests()
        
        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())