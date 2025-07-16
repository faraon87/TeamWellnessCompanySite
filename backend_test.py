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

# Test configuration
BASE_URL = "http://localhost:8001"
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
            f"Status: {status}, Response: {data}"
        )
        
        # Test health endpoint
        success, data, status = await self.make_request("GET", "/health")
        self.log_test(
            "Health endpoint (/health)", 
            success and status == 200,
            f"Status: {status}, Response: {data}"
        )
    
    async def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication Endpoints...")
        
        # Test signup
        success, data, status = await self.make_request("POST", "/api/auth/signup", TEST_USER_DATA)
        if success and status == 200:
            self.access_token = data.get("access_token")
            self.user_id = data.get("user", {}).get("id")
            self.log_test("User signup", True, f"User created with ID: {self.user_id}")
        else:
            self.log_test("User signup", False, f"Status: {status}, Response: {data}")
        
        # Test login (if signup failed, try login)
        if not self.access_token:
            login_data = {"email": TEST_USER_DATA["email"], "password": "testpassword"}
            success, data, status = await self.make_request("POST", "/api/auth/login", login_data)
            if success and status == 200:
                self.access_token = data.get("access_token")
                self.user_id = data.get("user", {}).get("id")
                self.log_test("User login", True, f"Logged in with ID: {self.user_id}")
            else:
                self.log_test("User login", False, f"Status: {status}, Response: {data}")
        
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
        
        # Test logout
        if self.access_token:
            success, data, status = await self.make_request("POST", "/api/auth/logout")
            self.log_test(
                "User logout", 
                success and status == 200,
                f"Logout successful: {success}"
            )
    
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
        """Test payment endpoints"""
        print("\n💳 Testing Payment Endpoints...")
        
        # Test get wellness packages (no auth required)
        success, data, status = await self.make_request("GET", "/api/payments/packages")
        self.log_test(
            "Get wellness packages", 
            success and status == 200,
            f"Packages retrieved: {len(data.get('packages', [])) if success else 'Failed'}"
        )
        
        if not self.access_token:
            self.log_test("Payment tests (authenticated)", False, "No authentication token available")
            return
        
        # Test create checkout session
        payment_data = {
            "package_id": "plus",
            "success_url": "https://teamwelly.com/success",
            "cancel_url": "https://teamwelly.com/cancel",
            "metadata": {"test": "true"}
        }
        success, data, status = await self.make_request("POST", "/api/payments/v1/checkout/session", payment_data)
        self.log_test(
            "Create checkout session", 
            success and status == 200,
            f"Checkout session created: {bool(data.get('session_id')) if success else 'Failed'}"
        )
        
        # Test get payment history
        success, data, status = await self.make_request("GET", "/api/payments/history")
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
                    cors_headers["access-control-allow-origin"] == "*" and
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
        """Run all backend tests"""
        print("🚀 Starting Team Welly Backend API Tests")
        print(f"Testing against: {BASE_URL}")
        print("=" * 60)
        
        try:
            await self.test_health_endpoints()
            await self.test_auth_endpoints()
            await self.test_programs_endpoints()
            await self.test_ai_chat_endpoints()
            await self.test_payment_endpoints()
            await self.test_analytics_endpoints()
            await self.test_cors_configuration()
            
        except Exception as e:
            print(f"❌ Test suite error: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
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
        
        return passed_tests, failed_tests, total_tests

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        passed, failed, total = await tester.run_all_tests()
        
        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())