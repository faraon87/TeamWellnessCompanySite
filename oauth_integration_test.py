#!/usr/bin/env python3
"""
Team Welly OAuth Integration Testing Suite
Tests the integration between local backend and Railway OAuth backend
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
RAILWAY_BACKEND_URL = "https://teamwellnesscompanysite-production.up.railway.app"
LOCAL_BACKEND_URL = "http://localhost:8001"

class OAuthIntegrationTester:
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
    
    async def make_request(self, method: str, url: str, data: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        try:
            request_headers = {"Content-Type": "application/json"}
            if headers:
                request_headers.update(headers)
            
            async with self.session.request(
                method, 
                url, 
                json=data if data else None,
                headers=request_headers,
                allow_redirects=False  # Don't follow redirects for OAuth testing
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()
                
                return response.status < 400, response_data, response.status
                
        except Exception as e:
            return False, str(e), 0
    
    async def test_railway_backend_health(self):
        """Test Railway backend health and configuration"""
        print("\n🚀 Testing Railway Backend Health...")
        
        # Test root endpoint
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/")
        self.log_test(
            "Railway backend root endpoint", 
            success and status == 200,
            f"Status: {status}, Version: {data.get('version') if success else 'Failed'}"
        )
        
        # Test health endpoint
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/health")
        self.log_test(
            "Railway backend health check", 
            success and status == 200,
            f"Status: {status}, OAuth ready: {data.get('services', {}).get('oauth') if success else 'Failed'}"
        )
        
        # Test API info endpoint
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/api/info")
        self.log_test(
            "Railway backend API info", 
            success and status == 200,
            f"OAuth endpoints available: {bool(data.get('endpoints', {}).get('google_oauth')) if success else 'Failed'}"
        )
        
        # Test debug endpoint for environment variables
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/debug")
        env_check = data.get('environment_check', {}) if success else {}
        self.log_test(
            "Railway backend environment variables", 
            success and env_check.get('client_id_present') == 'YES' and env_check.get('client_secret_present') == 'YES',
            f"Client ID: {env_check.get('client_id_present')}, Client Secret: {env_check.get('client_secret_present')}"
        )
    
    async def test_oauth_endpoints(self):
        """Test OAuth endpoints on Railway backend"""
        print("\n🔐 Testing OAuth Endpoints...")
        
        # Test Google OAuth initiation
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/api/auth/google")
        # Should return redirect info or redirect status codes (302, 307)
        oauth_working = status in [200, 302, 307] or ("google" in str(data).lower() and "oauth" in str(data).lower())
        self.log_test(
            "Google OAuth initiation", 
            oauth_working,
            f"Status: {status}, OAuth flow initiated properly (redirect status expected)"
        )
        
        # Test Google OAuth callback (without code, should handle gracefully)
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/api/auth/google/callback")
        # Should handle missing code parameter gracefully
        callback_working = status in [400, 401] or "code" in str(data).lower() or "error" in str(data).lower()
        self.log_test(
            "Google OAuth callback handling", 
            callback_working,
            f"Status: {status}, Handles missing code parameter appropriately"
        )
    
    async def test_local_backend_health(self):
        """Test local backend health and OAuth integration readiness"""
        print("\n🏠 Testing Local Backend Health...")
        
        # Test if local backend is running
        success, data, status = await self.make_request("GET", f"{LOCAL_BACKEND_URL}/")
        local_running = success and status == 200
        self.log_test(
            "Local backend running", 
            local_running,
            f"Status: {status}, Version: {data.get('version') if success else 'Not running'}"
        )
        
        if not local_running:
            self.log_test(
                "Local backend OAuth integration", 
                False,
                "Local backend not accessible - cannot test OAuth integration"
            )
            return
        
        # Test local backend health
        success, data, status = await self.make_request("GET", f"{LOCAL_BACKEND_URL}/health")
        self.log_test(
            "Local backend health check", 
            success and status == 200,
            f"Status: {status}, Services: {data.get('services') if success else 'Failed'}"
        )
        
        # Test local backend OAuth router availability
        success, data, status = await self.make_request("GET", f"{LOCAL_BACKEND_URL}/api/auth/google")
        oauth_router_available = status != 404
        self.log_test(
            "Local backend OAuth router", 
            oauth_router_available,
            f"Status: {status}, OAuth router {'available' if oauth_router_available else 'not found'}"
        )
    
    async def test_cors_configuration(self):
        """Test CORS configuration for cross-origin communication"""
        print("\n🌐 Testing CORS Configuration...")
        
        # Test CORS on Railway backend
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type,Authorization"
        }
        
        try:
            async with self.session.options(f"{RAILWAY_BACKEND_URL}/api/auth/google", headers=headers) as response:
                cors_headers = {
                    "access-control-allow-origin": response.headers.get("Access-Control-Allow-Origin"),
                    "access-control-allow-methods": response.headers.get("Access-Control-Allow-Methods"),
                    "access-control-allow-credentials": response.headers.get("Access-Control-Allow-Credentials")
                }
                
                cors_working = (
                    cors_headers["access-control-allow-origin"] in ["*", "http://localhost:3000"] and
                    cors_headers["access-control-allow-credentials"] == "true"
                )
                
                self.log_test(
                    "Railway backend CORS configuration", 
                    cors_working,
                    f"Origin: {cors_headers['access-control-allow-origin']}, Credentials: {cors_headers['access-control-allow-credentials']}"
                )
        except Exception as e:
            self.log_test("Railway backend CORS configuration", False, f"Error: {str(e)}")
        
        # Test CORS on local backend (if running)
        try:
            async with self.session.options(f"{LOCAL_BACKEND_URL}/api/auth/signup", headers=headers) as response:
                cors_headers = {
                    "access-control-allow-origin": response.headers.get("Access-Control-Allow-Origin"),
                    "access-control-allow-methods": response.headers.get("Access-Control-Allow-Methods"),
                    "access-control-allow-credentials": response.headers.get("Access-Control-Allow-Credentials")
                }
                
                cors_working = (
                    cors_headers["access-control-allow-origin"] in ["*", "http://localhost:3000"] and
                    "POST" in (cors_headers["access-control-allow-methods"] or "")
                )
                
                self.log_test(
                    "Local backend CORS configuration", 
                    cors_working,
                    f"Origin: {cors_headers['access-control-allow-origin']}, Methods: {cors_headers['access-control-allow-methods']}"
                )
        except Exception as e:
            self.log_test("Local backend CORS configuration", False, f"Error: {str(e)}")
    
    async def test_environment_variable_loading(self):
        """Test that backends are loading environment variables correctly"""
        print("\n⚙️ Testing Environment Variable Loading...")
        
        # Railway backend environment check (already tested in health check)
        success, data, status = await self.make_request("GET", f"{RAILWAY_BACKEND_URL}/debug")
        if success:
            env_check = data.get('environment_check', {})
            oauth_urls = data.get('oauth_urls', {})
            
            self.log_test(
                "Railway backend OAuth credentials loaded", 
                env_check.get('client_id_present') == 'YES' and env_check.get('client_secret_present') == 'YES',
                f"Google Client ID: {env_check.get('client_id_preview')}, OAuth URLs configured: {bool(oauth_urls)}"
            )
        else:
            self.log_test("Railway backend OAuth credentials loaded", False, "Could not access debug endpoint")
        
        # Local backend environment check (check if it can access OAuth endpoints)
        success, data, status = await self.make_request("GET", f"{LOCAL_BACKEND_URL}/api/info")
        if success:
            features = data.get('features', {})
            oauth_feature = features.get('ai_coaching', {})  # Check if features are loaded
            
            self.log_test(
                "Local backend environment variables loaded", 
                bool(features),
                f"Features loaded: {list(features.keys()) if features else 'None'}"
            )
        else:
            self.log_test("Local backend environment variables loaded", False, "Could not access API info endpoint")
    
    async def run_all_tests(self):
        """Run all OAuth integration tests"""
        print("🚀 Starting Team Welly OAuth Integration Tests")
        print(f"Railway Backend: {RAILWAY_BACKEND_URL}")
        print(f"Local Backend: {LOCAL_BACKEND_URL}")
        print("=" * 70)
        
        try:
            await self.test_railway_backend_health()
            await self.test_oauth_endpoints()
            await self.test_local_backend_health()
            await self.test_cors_configuration()
            await self.test_environment_variable_loading()
            
        except Exception as e:
            print(f"❌ Test suite error: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 70)
        print("📋 OAUTH INTEGRATION TEST SUMMARY")
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
        
        return passed_tests, failed_tests, total_tests

async def main():
    """Main test runner"""
    async with OAuthIntegrationTester() as tester:
        passed, failed, total = await tester.run_all_tests()
        
        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())