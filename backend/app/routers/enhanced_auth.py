from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uuid
from datetime import datetime, timedelta
import requests
from ..database import get_database, users_collection, user_sessions_collection

router = APIRouter()

# Enhanced Authentication Models
class SignUpRequest(BaseModel):
    email: str
    name: str
    plan: str = "basic"

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    user: Dict[str, Any]
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    plan: str
    created_at: datetime
    last_login: Optional[datetime] = None

# Helper functions
def generate_token():
    return str(uuid.uuid4())

def create_user_session(user_id: str, session_token: str):
    """Create a new user session"""
    session_data = {
        "user_id": user_id,
        "session_token": session_token,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),
        "active": True
    }
    return user_sessions_collection.insert_one(session_data)

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """Enhanced signup with session management"""
    try:
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": request.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        user_id = str(uuid.uuid4())
        user_data = {
            "_id": user_id,
            "id": user_id,
            "email": request.email,
            "name": request.name,
            "plan": request.plan,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "active": True,
            "profile": {
                "selected_goals": [],
                "assessment_data": {},
                "preferences": {}
            }
        }
        
        await users_collection.insert_one(user_data)
        
        # Create session
        session_token = generate_token()
        create_user_session(user_id, session_token)
        
        return AuthResponse(
            access_token=session_token,
            user=user_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Enhanced login with session management"""
    try:
        # Find user
        user = await users_collection.find_one({"email": request.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Update last login
        await users_collection.update_one(
            {"_id": user["_id"]}, 
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create session
        session_token = generate_token()
        create_user_session(user["_id"], session_token)
        
        return AuthResponse(
            access_token=session_token,
            user=user
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/auth/emergent")
async def emergent_auth_redirect(request: Request):
    """Redirect to Emergent Auth for OAuth"""
    try:
        # Get the base URL from the request
        base_url = str(request.base_url).rstrip('/')
        redirect_url = f"{base_url}/auth/emergent/callback"
        
        # Construct Emergent Auth URL
        auth_url = f"https://auth.emergentagent.com/?redirect={redirect_url}"
        
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth redirect failed: {str(e)}")

@router.get("/auth/emergent/callback")
async def emergent_auth_callback(request: Request):
    """Handle Emergent Auth callback"""
    try:
        # Get session_id from URL fragment (this would typically be handled by frontend)
        # For now, we'll return a redirect to frontend with instructions
        base_url = str(request.base_url).rstrip('/')
        frontend_url = base_url.replace(':8001', ':3000')  # Assuming frontend on port 3000
        
        return RedirectResponse(url=f"{frontend_url}/auth/callback")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth callback failed: {str(e)}")

@router.post("/auth/emergent/verify")
async def verify_emergent_session(session_id: str):
    """Verify Emergent Auth session and create user"""
    try:
        # Call Emergent Auth API
        headers = {"X-Session-ID": session_id}
        response = requests.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers=headers
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        auth_data = response.json()
        
        # Check if user exists
        user = await users_collection.find_one({"email": auth_data["email"]})
        
        if not user:
            # Create new user
            user_id = str(uuid.uuid4())
            user_data = {
                "_id": user_id,
                "id": user_id,
                "email": auth_data["email"],
                "name": auth_data["name"],
                "plan": "basic",
                "created_at": datetime.utcnow(),
                "last_login": datetime.utcnow(),
                "active": True,
                "profile": {
                    "picture": auth_data.get("picture", ""),
                    "selected_goals": [],
                    "assessment_data": {},
                    "preferences": {}
                }
            }
            await users_collection.insert_one(user_data)
            user = user_data
        else:
            # Update last login
            await users_collection.update_one(
                {"_id": user["_id"]}, 
                {"$set": {"last_login": datetime.utcnow()}}
            )
        
        # Create session with Emergent session token
        session_token = auth_data["session_token"]
        create_user_session(user["_id"], session_token)
        
        return AuthResponse(
            access_token=session_token,
            user=user
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session verification failed: {str(e)}")

@router.get("/me", response_model=UserResponse)
async def get_current_user(request: Request):
    """Get current user from session"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        session_token = auth_header.split(" ")[1]
        
        # Find active session
        session = await user_sessions_collection.find_one({
            "session_token": session_token,
            "active": True,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not session:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        # Get user
        user = await users_collection.find_one({"_id": session["user_id"]})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return UserResponse(**user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

@router.post("/logout")
async def logout(request: Request):
    """Logout user and deactivate session"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        session_token = auth_header.split(" ")[1]
        
        # Deactivate session
        await user_sessions_collection.update_one(
            {"session_token": session_token},
            {"$set": {"active": False}}
        )
        
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

@router.post("/complete-onboarding")
async def complete_onboarding(request: Request, goals: list = None, assessment: dict = None):
    """Complete user onboarding"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        session_token = auth_header.split(" ")[1]
        
        # Find user from session
        session = await user_sessions_collection.find_one({
            "session_token": session_token,
            "active": True
        })
        
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        # Update user profile
        update_data = {
            "onboarding_completed": True,
            "onboarding_completed_at": datetime.utcnow()
        }
        
        if goals:
            update_data["profile.selected_goals"] = goals
        
        if assessment:
            update_data["profile.assessment_data"] = assessment
        
        await users_collection.update_one(
            {"_id": session["user_id"]},
            {"$set": update_data}
        )
        
        return {"message": "Onboarding completed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Onboarding completion failed: {str(e)}")

# Demo/Testing endpoints
@router.post("/demo-login")
async def demo_login():
    """Quick demo login for testing"""
    try:
        demo_user = {
            "_id": "demo-user-id",
            "id": "demo-user-id",
            "email": "demo@teamwelly.com",
            "name": "Demo User",
            "plan": "premium",
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "active": True,
            "profile": {
                "selected_goals": ["Reduce Pain", "Improve Flexibility"],
                "assessment_data": {"stress_level": 6, "sleep_quality": 7},
                "preferences": {}
            }
        }
        
        session_token = generate_token()
        create_user_session("demo-user-id", session_token)
        
        return AuthResponse(
            access_token=session_token,
            user=demo_user
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo login failed: {str(e)}")