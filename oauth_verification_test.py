#!/usr/bin/env python3
"""
OAuth Verification Test for Railway Deployment
Focused testing of OAuth endpoints after redeployment
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Railway backend URL
BASE_URL = "https://teamwellnesscompanysite-production.up.railway.app"

class OAuthVerificationTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
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
    
    async def make_request(self, method: str, endpoint: str, allow_redirects: bool = False) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            
            async with self.session.request(
                method, 
                url,
                allow_redirects=allow_redirects
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()
                
                return response.status < 400, response_data, response.status
                
        except Exception as e:
            return False, str(e), 0
    
    async def test_environment_check(self):
        """Test environment variables are loaded"""
        print("\n🔍 Testing Environment Configuration...")
        
        success, data, status = await self.make_request("GET", "/debug/env")
        
        if success and status == 200:
            env_vars = data.get("env_vars_loaded", {})
            google_loaded = env_vars.get("google", False)
            apple_loaded = env_vars.get("apple", False) 
            twitter_loaded = env_vars.get("twitter", False)
            
            self.log_test(
                "Environment variables check (/debug/env)",
                True,
                f"Google: {google_loaded}, Apple: {apple_loaded}, Twitter: {twitter_loaded}"
            )
            
            # Check specific credentials
            google_client_id = data.get("google_client_id", "NOT_SET")
            apple_service_id = data.get("apple_service_id", "NOT_SET")
            twitter_client_id = data.get("twitter_client_id", "NOT_SET")
            
            print(f"   Google Client ID: {google_client_id[:20]}..." if google_client_id != "NOT_SET" else "   Google Client ID: NOT_SET")
            print(f"   Apple Service ID: {apple_service_id}")
            print(f"   Twitter Client ID: {twitter_client_id[:20]}..." if twitter_client_id != "NOT_SET" else "   Twitter Client ID: NOT_SET")
            
        else:
            self.log_test(
                "Environment variables check (/debug/env)",
                False,
                f"Status: {status}, Response: {data}"
            )
    
    async def test_google_oauth_fix(self):
        """Test Google OAuth fix - should return 302 redirect, not 405"""
        print("\n🔍 Testing Google OAuth Fix...")
        
        success, data, status = await self.make_request("GET", "/api/auth/google")
        
        # Check if the 405 error is fixed
        if status == 405:
            self.log_test(
                "Google OAuth initiation (/api/auth/google)",
                False,
                f"❌ STILL RETURNING 405 ERROR - Router configuration issue not fixed"
            )
        elif status == 302:
            self.log_test(
                "Google OAuth initiation (/api/auth/google)",
                True,
                f"✅ FIXED - Now returns 302 redirect as expected"
            )
        elif status == 307:
            self.log_test(
                "Google OAuth initiation (/api/auth/google)",
                True,
                f"✅ FIXED - Returns 307 temporary redirect to Google OAuth"
            )
        elif status == 200 and "google" in str(data).lower():
            self.log_test(
                "Google OAuth initiation (/api/auth/google)",
                True,
                f"✅ WORKING - Returns Google OAuth redirect information"
            )
        else:
            self.log_test(
                "Google OAuth initiation (/api/auth/google)",
                False,
                f"Status: {status}, Response: {data}"
            )
    
    async def test_apple_oauth_verification(self):
        """Verify Apple OAuth still works"""
        print("\n🍎 Testing Apple OAuth Verification...")
        
        success, data, status = await self.make_request("GET", "/api/auth/apple")
        
        if status in [302, 307]:
            self.log_test(
                "Apple OAuth initiation (/api/auth/apple)",
                True,
                f"✅ WORKING - Returns {status} redirect to Apple Sign-In"
            )
        elif status == 200 and "apple" in str(data).lower():
            self.log_test(
                "Apple OAuth initiation (/api/auth/apple)",
                True,
                f"✅ WORKING - Returns Apple OAuth redirect information"
            )
        else:
            self.log_test(
                "Apple OAuth initiation (/api/auth/apple)",
                False,
                f"Status: {status}, Response: {data}"
            )
    
    async def test_twitter_oauth_verification(self):
        """Verify Twitter OAuth still works"""
        print("\n🐦 Testing Twitter OAuth Verification...")
        
        success, data, status = await self.make_request("GET", "/api/auth/twitter")
        
        if status in [302, 307]:
            self.log_test(
                "Twitter OAuth initiation (/api/auth/twitter)",
                True,
                f"✅ WORKING - Returns {status} redirect to Twitter OAuth"
            )
        elif status == 200 and "twitter" in str(data).lower():
            self.log_test(
                "Twitter OAuth initiation (/api/auth/twitter)",
                True,
                f"✅ WORKING - Returns Twitter OAuth redirect information"
            )
        else:
            self.log_test(
                "Twitter OAuth initiation (/api/auth/twitter)",
                False,
                f"Status: {status}, Response: {data}"
            )
    
    async def run_oauth_verification(self):
        """Run focused OAuth verification tests"""
        print("🚀 Starting OAuth Verification Tests for Railway Deployment")
        print(f"Testing against: {BASE_URL}")
        print("=" * 70)
        
        try:
            await self.test_environment_check()
            await self.test_google_oauth_fix()
            await self.test_apple_oauth_verification()
            await self.test_twitter_oauth_verification()
            
        except Exception as e:
            print(f"❌ Test suite error: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 70)
        print("📋 OAUTH VERIFICATION SUMMARY")
        print("=" * 70)
        
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
        
        # Specific findings
        print("\n🎯 KEY FINDINGS:")
        google_test = next((r for r in self.test_results if "Google OAuth initiation" in r["test"]), None)
        if google_test:
            if google_test["success"]:
                print("✅ Google OAuth fix SUCCESSFUL - No more 405 errors")
            else:
                print("❌ Google OAuth fix FAILED - Still returning 405 errors")
        
        apple_test = next((r for r in self.test_results if "Apple OAuth initiation" in r["test"]), None)
        twitter_test = next((r for r in self.test_results if "Twitter OAuth initiation" in r["test"]), None)
        
        if apple_test and apple_test["success"] and twitter_test and twitter_test["success"]:
            print("✅ No regression on other OAuth providers")
        else:
            print("⚠️ Potential regression on other OAuth providers")
        
        return passed_tests, failed_tests, total_tests

async def main():
    """Main test runner"""
    async with OAuthVerificationTester() as tester:
        passed, failed, total = await tester.run_oauth_verification()
        
        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())