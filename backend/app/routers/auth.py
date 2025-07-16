from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
import httpx
import os
from datetime import datetime
from typing import Dict, Any
from ..models import User, UserLogin, UserSignup, GoogleAuthRequest, UserRole, UserPlan
from ..database import users_collection, user_progress_collection
from ..auth import create_access_token, get_current_user
from ..behavior_tracker import BehaviorTracker
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# OAuth Configuration
config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.post("/signup")
async def signup(user_data: UserSignup):
    """Sign up a new user"""
    try:
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user = User(
            email=user_data.email,
            name=user_data.name,
            plan=user_data.plan,
            role=UserRole.CORPORATE if user_data.company_code else UserRole.INDIVIDUAL,
            created_at=datetime.utcnow()
        )
        
        # Insert user into database
        result = await users_collection.insert_one(new_user.dict(exclude={"id"}))
        user_id = str(result.inserted_id)
        
        # Initialize user progress
        await user_progress_collection.insert_one({
            "user_id": user_id,
            "daily_completion": 0.0,
            "weekly_completion": 0.0,
            "monthly_completion": 0.0,
            "welly_points": 0,
            "current_streak": 0,
            "completed_programs": [],
            "bookmarked_programs": [],
            "completed_challenges": [],
            "last_activity": None,
            "updated_at": datetime.utcnow()
        })
        
        # Track signup behavior
        await BehaviorTracker.track_action(
            user_id=user_id,
            action="signup",
            page="auth",
            details={"method": "email", "plan": user_data.plan}
        )
        
        # Create access token
        access_token = await create_access_token(data={"sub": user_id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": new_user.email,
                "name": new_user.name,
                "plan": new_user.plan,
                "role": new_user.role,
                "onboarding_completed": False
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin):
    """Login user (placeholder for email/password auth)"""
    # Note: In a real app, you'd verify password here
    user = await users_collection.find_one({"email": user_data.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(user["_id"])
    
    # Track login behavior
    await BehaviorTracker.track_action(
        user_id=user_id,
        action="login",
        page="auth",
        details={"method": "email"}
    )
    
    # Create access token
    access_token = await create_access_token(data={"sub": user_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": user["email"],
            "name": user["name"],
            "plan": user["plan"],
            "role": user["role"],
            "onboarding_completed": user.get("onboarding_completed", False)
        }
    }

@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    redirect_uri = f"{request.base_url}api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)
        
        # Find or create user
        existing_user = await users_collection.find_one({"email": user_info["email"]})
        
        if existing_user:
            # Update Google ID if not set
            if not existing_user.get("google_id"):
                await users_collection.update_one(
                    {"_id": existing_user["_id"]},
                    {"$set": {"google_id": user_info["sub"]}}
                )
            
            user_id = str(existing_user["_id"])
        else:
            # Create new user
            new_user = User(
                email=user_info["email"],
                name=user_info["name"],
                avatar=user_info.get("picture"),
                google_id=user_info["sub"],
                plan=UserPlan.BASIC,
                role=UserRole.INDIVIDUAL,
                created_at=datetime.utcnow()
            )
            
            result = await users_collection.insert_one(new_user.dict(exclude={"id"}))
            user_id = str(result.inserted_id)
            
            # Initialize user progress
            await user_progress_collection.insert_one({
                "user_id": user_id,
                "daily_completion": 0.0,
                "weekly_completion": 0.0,
                "monthly_completion": 0.0,
                "welly_points": 0,
                "current_streak": 0,
                "completed_programs": [],
                "bookmarked_programs": [],
                "completed_challenges": [],
                "last_activity": None,
                "updated_at": datetime.utcnow()
            })
        
        # Track login behavior
        await BehaviorTracker.track_action(
            user_id=user_id,
            action="login",
            page="auth",
            details={"method": "google"}
        )
        
        # Create access token
        access_token = await create_access_token(data={"sub": user_id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": user_info["email"],
                "name": user_info["name"],
                "avatar": user_info.get("picture"),
                "plan": existing_user.get("plan", "basic") if existing_user else "basic",
                "role": existing_user.get("role", "individual") if existing_user else "individual",
                "onboarding_completed": existing_user.get("onboarding_completed", False) if existing_user else False
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google authentication failed: {str(e)}")

@router.post("/google/mobile")
async def google_mobile_login(auth_request: GoogleAuthRequest):
    """Handle Google OAuth for mobile apps"""
    try:
        # Verify Google access token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={auth_request.access_token}"
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Google access token")
            
            user_info = response.json()
        
        # Find or create user (similar to callback logic)
        existing_user = await users_collection.find_one({"email": user_info["email"]})
        
        if existing_user:
            if not existing_user.get("google_id"):
                await users_collection.update_one(
                    {"_id": existing_user["_id"]},
                    {"$set": {"google_id": user_info["id"]}}
                )
            
            user_id = str(existing_user["_id"])
        else:
            # Create new user
            new_user = User(
                email=user_info["email"],
                name=user_info["name"],
                avatar=user_info.get("picture"),
                google_id=user_info["id"],
                plan=UserPlan.BASIC,
                role=UserRole.INDIVIDUAL,
                created_at=datetime.utcnow()
            )
            
            result = await users_collection.insert_one(new_user.dict(exclude={"id"}))
            user_id = str(result.inserted_id)
            
            # Initialize user progress
            await user_progress_collection.insert_one({
                "user_id": user_id,
                "daily_completion": 0.0,
                "weekly_completion": 0.0,
                "monthly_completion": 0.0,
                "welly_points": 0,
                "current_streak": 0,
                "completed_programs": [],
                "bookmarked_programs": [],
                "completed_challenges": [],
                "last_activity": None,
                "updated_at": datetime.utcnow()
            })
        
        # Track login behavior
        await BehaviorTracker.track_action(
            user_id=user_id,
            action="login",
            page="auth",
            details={"method": "google_mobile"}
        )
        
        # Create access token
        access_token = await create_access_token(data={"sub": user_id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": user_info["email"],
                "name": user_info["name"],
                "avatar": user_info.get("picture"),
                "plan": existing_user.get("plan", "basic") if existing_user else "basic",
                "role": existing_user.get("role", "individual") if existing_user else "individual",
                "onboarding_completed": existing_user.get("onboarding_completed", False) if existing_user else False
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google mobile authentication failed: {str(e)}")

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "avatar": current_user.avatar,
        "plan": current_user.plan,
        "role": current_user.role,
        "onboarding_completed": current_user.onboarding_completed,
        "selected_goals": current_user.selected_goals,
        "created_at": current_user.created_at
    }

@router.post("/complete-onboarding")
async def complete_onboarding(
    onboarding_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Complete user onboarding"""
    try:
        # Update user with onboarding data
        await users_collection.update_one(
            {"_id": current_user.id},
            {
                "$set": {
                    "onboarding_completed": True,
                    "selected_goals": onboarding_data.get("goals", []),
                    "assessment_data": onboarding_data.get("assessment", {}),
                    "device_integrations": onboarding_data.get("devices", []),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Track onboarding completion
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="complete_onboarding",
            page="onboarding",
            details=onboarding_data
        )
        
        return {"message": "Onboarding completed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user"""
    # Track logout behavior
    await BehaviorTracker.track_action(
        user_id=current_user.id,
        action="logout",
        page="auth",
        details={}
    )
    
    return {"message": "Logged out successfully"}