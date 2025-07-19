#!/usr/bin/env python3
"""
Team Welly Backend API Testing Suite
Tests all backend endpoints for functionality and integration
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Test configuration - Use production backend for testing
BASE_URL = "https://teamwellnesscompanysite-production.up.railway.app"
TEST_USER_DATA = {
    "email": "sarah.wellness@teamwelly.com",
    "name": "Sarah Wellness",
    "plan": "plus"
}

class BackendTester:
    def __init__(self):
        self.session = None
        self.access_token = None
        self.user_id = None
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
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        try:
            url = f"{BASE_URL}{endpoint}"
            request_headers = {"Content-Type": "application/json"}
            
            if headers:
                request_headers.update(headers)
            
            if self.access_token and "Authorization" not in request_headers:
                request_headers["Authorization"] = f"Bearer {self.access_token}"
            
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
    
    async def test_health_endpoints(self):
        """Test basic health and status endpoints"""
        print("\n🔍 Testing Health Endpoints...")
        
        # Test root endpoint
        success, data, status = await self.make_request("GET", "/")
        self.log_test(
            "Root endpoint (/)", 
            success and status == 200,
            f"Status: {status}, Version: {data.get('version') if success else 'Failed'}"
        )
        
        # Test health endpoint
        success, data, status = await self.make_request("GET", "/health")
        self.log_test(
            "Health endpoint (/health)", 
            success and status == 200,
            f"Status: {status}, Services: {data.get('services') if success else 'Failed'}"
        )
        
        # Test API info endpoint
        success, data, status = await self.make_request("GET", "/api/info")
        self.log_test(
            "API info endpoint (/api/info)", 
            success and status == 200,
            f"API info retrieved: {bool(data.get('features')) if success else 'Failed'}"
        )
    
    async def test_auth_endpoints(self):
        """Test enhanced authentication endpoints"""
        print("\n🔐 Testing Enhanced Authentication Endpoints...")
        
        # Test enhanced signup
        success, data, status = await self.make_request("POST", "/api/auth/signup", TEST_USER_DATA)
        if success and status == 200:
            self.access_token = data.get("access_token")
            self.user_id = data.get("user", {}).get("id")
            self.log_test("Enhanced signup", True, f"User created with ID: {self.user_id}")
        else:
            self.log_test("Enhanced signup", False, f"Status: {status}, Response: {data}")
        
        # Test enhanced login (if signup failed, try login)
        if not self.access_token:
            login_data = {"email": TEST_USER_DATA["email"], "password": "testpassword"}
            success, data, status = await self.make_request("POST", "/api/auth/login", login_data)
            if success and status == 200:
                self.access_token = data.get("access_token")
                self.user_id = data.get("user", {}).get("id")
                self.log_test("Enhanced login", True, f"Logged in with ID: {self.user_id}")
            else:
                self.log_test("Enhanced login", False, f"Status: {status}, Response: {data}")
        
        # Test demo login endpoint
        success, data, status = await self.make_request("POST", "/api/auth/demo-login")
        demo_token = None
        if success and status == 200:
            demo_token = data.get("access_token")
            self.log_test("Demo login", True, f"Demo user logged in successfully")
        else:
            self.log_test("Demo login", False, f"Status: {status}, Response: {data}")
        
        # Test get current user (requires auth)
        if self.access_token:
            success, data, status = await self.make_request("GET", "/api/auth/me")
            self.log_test(
                "Get current user (/api/auth/me)", 
                success and status == 200,
                f"User data retrieved: {data.get('name') if success else 'Failed'}"
            )
        
        # Test complete onboarding
        if self.access_token:
            onboarding_data = {
                "goals": ["Reduce Pain", "Improve Flexibility", "Boost Mental Health"],
                "assessment": {
                    "stressLevel": "medium",
                    "sleepQuality": "good",
                    "painAreas": ["lower_back", "neck"],
                    "movementHabits": "sedentary"
                },
                "devices": ["fitbit"]
            }
            success, data, status = await self.make_request("POST", "/api/auth/complete-onboarding", onboarding_data)
            self.log_test(
                "Complete onboarding", 
                success and status == 200,
                f"Onboarding completed: {success}"
            )
        
        # Test logout (skip for now to keep token for OAuth tests)
        # if self.access_token:
        #     success, data, status = await self.make_request("POST", "/api/auth/logout")
        #     self.log_test(
        #         "Enhanced logout", 
        #         success and status == 200,
        #         f"Logout successful: {success}"
        #     )
    
    async def test_programs_endpoints(self):
        """Test programs endpoints"""
        print("\n📚 Testing Programs Endpoints...")
        
        if not self.access_token:
            self.log_test("Programs tests", False, "No authentication token available")
            return
        
        # Test get all programs
        success, data, status = await self.make_request("GET", "/api/programs/")
        self.log_test(
            "Get all programs", 
            success and status == 200,
            f"Retrieved {len(data) if isinstance(data, list) else 'unknown'} programs"
        )
        
        # Test get programs by category
        success, data, status = await self.make_request("GET", "/api/programs/?category=stretch_mobility")
        self.log_test(
            "Get programs by category", 
            success and status == 200,
            f"Retrieved {len(data) if isinstance(data, list) else 'unknown'} stretch programs"
        )
        
        # Test get specific program
        success, data, status = await self.make_request("GET", "/api/programs/stretch_mobility_1")
        self.log_test(
            "Get specific program", 
            success and status == 200,
            f"Program details: {data.get('title') if success else 'Failed'}"
        )
        
        # Test start program
        success, data, status = await self.make_request("POST", "/api/programs/stretch_mobility_1/start")
        self.log_test(
            "Start program", 
            success and status == 200,
            f"Program started: {success}"
        )
        
        # Test bookmark program
        success, data, status = await self.make_request("POST", "/api/programs/breath_stress_1/bookmark")
        self.log_test(
            "Bookmark program", 
            success and status == 200,
            f"Program bookmarked: {success}"
        )
        
        # Test complete program
        completion_data = {"rating": 5, "notes": "Great program, felt much better!"}
        success, data, status = await self.make_request("POST", "/api/programs/stretch_mobility_1/complete", completion_data)
        self.log_test(
            "Complete program", 
            success and status == 200,
            f"Program completed: {success}"
        )
        
        # Test get category stats
        success, data, status = await self.make_request("GET", "/api/programs/categories/stats")
        self.log_test(
            "Get category stats", 
            success and status == 200,
            f"Category stats retrieved: {success}"
        )
        
        # Test get recommendations
        success, data, status = await self.make_request("GET", "/api/programs/recommendations")
        self.log_test(
            "Get program recommendations", 
            success and status == 200,
            f"Recommendations retrieved: {success}"
        )
    
    async def test_ai_chat_endpoints(self):
        """Test AI chat endpoints"""
        print("\n🤖 Testing AI Chat Endpoints...")
        
        if not self.access_token:
            self.log_test("AI Chat tests", False, "No authentication token available")
            return
        
        # Test chat with AI
        chat_data = {
            "user_id": self.user_id,
            "message": "I'm feeling stressed and have lower back pain. What wellness activities would you recommend?",
            "session_id": "test-session-123"
        }
        success, data, status = await self.make_request("POST", "/api/ai/chat", chat_data)
        self.log_test(
            "Chat with AI", 
            success and status == 200,
            f"AI response received: {bool(data.get('response')) if success else 'Failed'}"
        )
        
        # Test get user insights
        success, data, status = await self.make_request("GET", "/api/ai/insights")
        self.log_test(
            "Get user insights", 
            success and status == 200,
            f"Insights generated: {bool(data.get('user_insights')) if success else 'Failed'}"
        )
        
        # Test get chat history
        success, data, status = await self.make_request("GET", "/api/ai/chat/history?session_id=test-session-123")
        self.log_test(
            "Get chat history", 
            success and status == 200,
            f"Chat history retrieved: {success}"
        )
        
        # Test get wellness tips
        success, data, status = await self.make_request("GET", "/api/ai/wellness-tips")
        self.log_test(
            "Get wellness tips", 
            success and status == 200,
            f"Wellness tips generated: {bool(data.get('wellness_tips')) if success else 'Failed'}"
        )
        
        # Test get motivation
        success, data, status = await self.make_request("GET", "/api/ai/motivation")
        self.log_test(
            "Get motivation", 
            success and status == 200,
            f"Motivation message generated: {bool(data.get('motivation')) if success else 'Failed'}"
        )
        
        # Test provide feedback
        feedback_data = {"rating": 5, "helpful": True, "comment": "Great advice!"}
        success, data, status = await self.make_request("POST", "/api/ai/feedback", feedback_data)
        self.log_test(
            "Provide AI feedback", 
            success and status == 200,
            f"Feedback recorded: {success}"
        )
    
    async def test_payment_endpoints(self):
        """Test enhanced payment endpoints"""
        print("\n💳 Testing Enhanced Payment Endpoints...")
        
        # Test get wellness packages (no auth required)
        success, data, status = await self.make_request("GET", "/api/payments/packages")
        self.log_test(
            "Get wellness packages", 
            success and status == 200,
            f"Packages retrieved: {len(data.get('packages', [])) if success else 'Failed'}"
        )
        
        # Test demo packages info
        success, data, status = await self.make_request("GET", "/api/payments/demo/packages")
        self.log_test(
            "Demo packages info", 
            success and status == 200,
            f"Demo packages info retrieved: {success}"
        )
        
        # Test demo payment success
        success, data, status = await self.make_request("POST", "/api/payments/demo/success")
        self.log_test(
            "Demo payment success", 
            success and status == 200,
            f"Demo payment success: {success}"
        )
        
        if not self.access_token:
            self.log_test("Payment tests (authenticated)", False, "No authentication token available")
            return
        
        # Test create checkout session for wellness package
        payment_data = {
            "package_id": "plus",
            "origin_url": "http://localhost:3000",
            "user_id": self.user_id
        }
        success, data, status = await self.make_request("POST", "/api/payments/checkout/session", payment_data)
        session_id = None
        if success and status == 200:
            session_id = data.get("session_id")
            self.log_test(
                "Create checkout session", 
                True,
                f"Checkout session created: {session_id}"
            )
        else:
            self.log_test(
                "Create checkout session", 
                False,
                f"Status: {status}, Response: {data}"
            )
        
        # Test custom checkout session
        custom_payment_data = {
            "amount": 29.99,
            "currency": "usd",
            "origin_url": "http://localhost:3000",
            "user_id": self.user_id,
            "metadata": {"test": "custom_payment"}
        }
        success, data, status = await self.make_request("POST", "/api/payments/checkout/custom", custom_payment_data)
        self.log_test(
            "Create custom checkout session", 
            success and status == 200,
            f"Custom checkout session created: {bool(data.get('session_id')) if success else 'Failed'}"
        )
        
        # Test checkout status (if we have a session_id)
        if session_id:
            success, data, status = await self.make_request("GET", f"/api/payments/checkout/status/{session_id}")
            self.log_test(
                "Get checkout status", 
                success and status == 200,
                f"Checkout status retrieved: {success}"
            )
        
        # Test get payment history
        success, data, status = await self.make_request("GET", f"/api/payments/history?user_id={self.user_id}")
        self.log_test(
            "Get payment history", 
            success and status == 200,
            f"Payment history retrieved: {success}"
        )
    
    async def test_analytics_endpoints(self):
        """Test analytics endpoints"""
        print("\n📊 Testing Analytics Endpoints...")
        
        if not self.access_token:
            self.log_test("Analytics tests", False, "No authentication token available")
            return
        
        # Test get user analytics
        success, data, status = await self.make_request("GET", "/api/analytics/user")
        self.log_test(
            "Get user analytics", 
            success and status == 200,
            f"User analytics retrieved: {success}"
        )
        
        # Test get behavior analytics
        success, data, status = await self.make_request("GET", "/api/analytics/behavior?days=7")
        self.log_test(
            "Get behavior analytics", 
            success and status == 200,
            f"Behavior analytics retrieved: {success}"
        )
        
        # Test get progress analytics
        success, data, status = await self.make_request("GET", "/api/analytics/progress")
        self.log_test(
            "Get progress analytics", 
            success and status == 200,
            f"Progress analytics retrieved: {success}"
        )
        
        # Test get wellness score
        success, data, status = await self.make_request("GET", "/api/analytics/wellness-score")
        self.log_test(
            "Get wellness score", 
            success and status == 200,
            f"Wellness score calculated: {data.get('overall_score') if success else 'Failed'}"
        )
    
    async def test_oauth_endpoints(self):
        """Test OAuth authentication endpoints - Focus on initiation and credential loading"""
        print("\n🔐 Testing OAuth Endpoints...")
        
        # First, test environment variables are loaded
        success, data, status = await self.make_request("GET", "/debug/env")
        if success and status == 200:
            env_vars = data.get("env_vars_loaded", {})
            self.log_test(
                "OAuth credentials loaded from environment", 
                env_vars.get("google", False) and env_vars.get("twitter", False) and env_vars.get("apple", False),
                f"Google: {env_vars.get('google')}, Apple: {env_vars.get('apple')}, Twitter: {env_vars.get('twitter')}"
            )
        else:
            self.log_test("OAuth credentials check", False, f"Could not verify environment variables: {status}")
        
        # Test Google OAuth initiation (should redirect to Google OAuth)
        success, data, status = await self.make_request("GET", "/api/auth/google", headers={"User-Agent": "Mozilla/5.0"})
        # Google OAuth should redirect (302/307) or return redirect info
        google_working = status in [302, 307] or (status == 200 and "google" in str(data).lower())
        redirect_url = ""
        if hasattr(data, 'get') and data.get('redirect_url'):
            redirect_url = data.get('redirect_url')
        elif status in [302, 307]:
            redirect_url = "Redirect response received"
        
        self.log_test(
            "Google OAuth initiation (/api/auth/google)", 
            google_working,
            f"Status: {status}, Redirect: {redirect_url}, Should redirect to Google OAuth"
        )
        
        # Test Apple OAuth initiation (should redirect to Apple Sign-In)
        success, data, status = await self.make_request("GET", "/api/auth/apple", headers={"User-Agent": "Mozilla/5.0"})
        # Apple OAuth should redirect (302/307) or return redirect info
        apple_working = status in [302, 307] or (status == 200 and "apple" in str(data).lower())
        apple_redirect_url = ""
        if hasattr(data, 'get') and data.get('redirect_url'):
            apple_redirect_url = data.get('redirect_url')
        elif status in [302, 307]:
            apple_redirect_url = "Redirect response received"
        
        self.log_test(
            "Apple OAuth initiation (/api/auth/apple)", 
            apple_working,
            f"Status: {status}, Redirect: {apple_redirect_url}, Should redirect to Apple Sign-In"
        )
        
        # Test Twitter/X OAuth initiation (should redirect to Twitter OAuth 2.0)
        success, data, status = await self.make_request("GET", "/api/auth/twitter", headers={"User-Agent": "Mozilla/5.0"})
        # Twitter OAuth should redirect (302/307) or return redirect info
        twitter_working = status in [302, 307] or (status == 200 and "twitter" in str(data).lower())
        twitter_redirect_url = ""
        if hasattr(data, 'get') and data.get('redirect_url'):
            twitter_redirect_url = data.get('redirect_url')
        elif status in [302, 307]:
            twitter_redirect_url = "Redirect response received"
        
        self.log_test(
            "Twitter/X OAuth initiation (/api/auth/twitter)", 
            twitter_working,
            f"Status: {status}, Redirect: {twitter_redirect_url}, Should redirect to Twitter OAuth 2.0"
        )
        
        # Test redirect URI construction by checking if base URL is used correctly
        print("\n🔍 Testing Redirect URI Construction...")
        
        # Verify that all OAuth endpoints are accessible (no 404 errors)
        endpoints_to_test = [
            ("/api/auth/google/callback", "Google OAuth callback"),
            ("/api/auth/apple/callback", "Apple OAuth callback"), 
            ("/api/auth/twitter/callback", "Twitter OAuth callback")
        ]
        
        for endpoint, description in endpoints_to_test:
            success, data, status = await self.make_request("GET", endpoint)
            # Callback endpoints should exist (not 404) but may return errors without proper OAuth flow
            endpoint_exists = status != 404
            self.log_test(
                f"{description} endpoint exists", 
                endpoint_exists,
                f"Status: {status}, Endpoint accessible (expected to fail without OAuth flow)"
            )
        
        # Test OAuth session management endpoints
        print("\n🔐 Testing OAuth Session Management...")
        
        # Test OAuth logout (without token, should fail appropriately)
        success, data, status = await self.make_request("POST", "/api/auth/oauth/logout")
        logout_working = status == 401 or "token" in str(data).lower() or "unauthorized" in str(data).lower()
        self.log_test(
            "OAuth logout without token", 
            logout_working,
            f"Status: {status}, Properly requires authentication"
        )
        
        # Test OAuth me endpoint (without token, should fail appropriately)
        success, data, status = await self.make_request("GET", "/api/auth/oauth/me")
        me_working = status == 401 or "token" in str(data).lower() or "unauthorized" in str(data).lower()
        self.log_test(
            "OAuth get current user without token", 
            me_working,
            f"Status: {status}, Properly requires authentication"
        )
        
        # Test OAuth endpoints with valid token (if we have one from regular auth)
        if self.access_token:
            print("\n🔑 Testing OAuth with Valid Token...")
            
            # Test OAuth me endpoint with valid token
            success, data, status = await self.make_request("GET", "/api/auth/oauth/me")
            oauth_me_working = success and status == 200 and (data.get("email") or data.get("user"))
            self.log_test(
                "OAuth get current user with token", 
                oauth_me_working,
                f"Status: {status}, User info retrieved: {bool(data.get('email') or data.get('user')) if success else 'Failed'}"
            )
            
            # Test OAuth logout with valid token
            success, data, status = await self.make_request("POST", "/api/auth/oauth/logout")
            oauth_logout_working = success and status == 200
            self.log_test(
                "OAuth logout with token", 
                oauth_logout_working,
                f"Status: {status}, Logout successful: {success}"
            )

    async def test_cors_configuration(self):
        """Test CORS configuration"""
        print("\n🌐 Testing CORS Configuration...")
        
        # Test preflight request
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type,Authorization"
        }
        
        try:
            async with self.session.options(f"{BASE_URL}/api/auth/signup", headers=headers) as response:
                cors_headers = {
                    "access-control-allow-origin": response.headers.get("Access-Control-Allow-Origin"),
                    "access-control-allow-methods": response.headers.get("Access-Control-Allow-Methods"),
                    "access-control-allow-headers": response.headers.get("Access-Control-Allow-Headers")
                }
                
                cors_working = (
                    cors_headers["access-control-allow-origin"] in ["*", "http://localhost:3000"] and
                    "POST" in (cors_headers["access-control-allow-methods"] or "") and
                    "Content-Type" in (cors_headers["access-control-allow-headers"] or "")
                )
                
                self.log_test(
                    "CORS preflight request", 
                    cors_working,
                    f"CORS headers: {cors_headers}"
                )
        except Exception as e:
            self.log_test("CORS preflight request", False, f"Error: {str(e)}")
    
    async def run_all_tests(self):
        """Run all backend tests with focus on OAuth functionality"""
        print("🚀 Starting Team Welly Backend API Tests - OAuth Focus")
        print(f"Testing against: {BASE_URL}")
        print("=" * 60)
        
        try:
            # Run health checks first to ensure backend is accessible
            await self.test_health_endpoints()
            
            # Run authentication to get token for OAuth session tests
            await self.test_auth_endpoints()
            
            # PRIMARY FOCUS: OAuth functionality testing
            await self.test_oauth_endpoints()
            
            # Test CORS for OAuth requests
            await self.test_cors_configuration()
            
            # Optional: Run other tests if time permits (but OAuth is priority)
            print("\n📝 Note: Focusing on OAuth testing as requested. Other endpoint tests available but not priority.")
            
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
        
        # Separate OAuth-specific results
        oauth_tests = [result for result in self.test_results if "oauth" in result["test"].lower() or "google" in result["test"].lower() or "apple" in result["test"].lower() or "twitter" in result["test"].lower()]
        oauth_passed = sum(1 for result in oauth_tests if result["success"])
        oauth_total = len(oauth_tests)
        
        if oauth_total > 0:
            print(f"\n🔐 OAuth-Specific Results:")
            print(f"OAuth Tests: {oauth_total}")
            print(f"✅ OAuth Passed: {oauth_passed}")
            print(f"❌ OAuth Failed: {oauth_total - oauth_passed}")
            print(f"OAuth Success Rate: {(oauth_passed/oauth_total*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        return passed_tests, failed_tests, total_tests

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        passed, failed, total = await tester.run_all_tests()
        
        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())