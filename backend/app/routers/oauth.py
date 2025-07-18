from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uuid
from datetime import datetime, timedelta
import requests
from ..database import get_database, users_collection, user_sessions_collection

router = APIRouter()

# OAuth Models
class OAuthUser(BaseModel):
    email: str
    name: str
    provider: str
    provider_id: str
    avatar_url: Optional[str] = None

class OAuthLoginResponse(BaseModel):
    access_token: str
    user: Dict[str, Any]
    token_type: str = "bearer"
    message: str

# OAuth Configuration
oauth = OAuth()

# Google OAuth Configuration
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Helper functions
def generate_token():
    """Generate a secure session token"""
    return str(uuid.uuid4())

async def create_user_session(user_id: str, session_token: str):
    """Create a new user session"""
    session_data = {
        "user_id": user_id,
        "session_token": session_token,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),
        "active": True
    }
    return await user_sessions_collection.insert_one(session_data)

async def create_or_update_oauth_user(oauth_user: OAuthUser):
    """Create or update OAuth user in database"""
    existing_user = await users_collection.find_one({"email": oauth_user.email})
    
    if existing_user:
        # Update existing user with OAuth info
        await users_collection.update_one(
            {"email": oauth_user.email},
            {
                "$set": {
                    "last_login": datetime.utcnow(),
                    "oauth_provider": oauth_user.provider,
                    "oauth_provider_id": oauth_user.provider_id,
                    "avatar_url": oauth_user.avatar_url
                }
            }
        )
        return existing_user
    else:
        # Create new user
        user_data = {
            "id": str(uuid.uuid4()),
            "email": oauth_user.email,
            "name": oauth_user.name,
            "plan": "basic",
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "oauth_provider": oauth_user.provider,
            "oauth_provider_id": oauth_user.provider_id,
            "avatar_url": oauth_user.avatar_url,
            "is_active": True
        }
        await users_collection.insert_one(user_data)
        return user_data

# Google OAuth Endpoints
@router.get("/auth/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    try:
        # Get the redirect URI for Google OAuth
        redirect_uri = str(request.url_for("google_callback"))
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google OAuth initiation failed: {str(e)}")

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        # Get the access token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = await oauth.google.parse_id_token(request, token)
        
        # Create OAuth user object
        oauth_user = OAuthUser(
            email=user_info.get('email'),
            name=user_info.get('name'),
            provider='google',
            provider_id=user_info.get('sub'),
            avatar_url=user_info.get('picture')
        )
        
        # Create or update user in database
        user = await create_or_update_oauth_user(oauth_user)
        
        # Create session token
        session_token = generate_token()
        await create_user_session(user["id"], session_token)
        
        # Create HTML response that stores the token and redirects
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f2f5;
                }}
                .container {{
                    text-align: center;
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .success {{
                    color: #28a745;
                    font-size: 18px;
                    margin-bottom: 20px;
                }}
                .loading {{
                    color: #007bff;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">✅ Authentication Successful!</div>
                <div class="loading">Redirecting to your dashboard...</div>
            </div>
            <script>
                // Store the authentication token
                localStorage.setItem('oauth_token', '{session_token}');
                localStorage.setItem('user_info', JSON.stringify({{
                    "id": "{user['id']}",
                    "email": "{user['email']}",
                    "name": "{user['name']}",
                    "plan": "{user['plan']}",
                    "avatar_url": "{user.get('avatar_url', '')}",
                    "oauth_provider": "google"
                }}));
                
                // Redirect to main application
                setTimeout(() => {{
                    window.location.href = '/src/BackendIntegratedApp.jsx';
                }}, 1500);
            </script>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_response)
        
    except Exception as e:
        # Return error HTML page
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Error</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f2f5;
                }}
                .container {{
                    text-align: center;
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .error {{
                    color: #dc3545;
                    font-size: 18px;
                    margin-bottom: 20px;
                }}
                .retry {{
                    color: #007bff;
                    font-size: 16px;
                    cursor: pointer;
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error">❌ Authentication Failed</div>
                <div class="retry" onclick="window.location.href='/'">← Back to Home</div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html)

# Apple Sign-In Endpoints (Placeholder Structure)
@router.get("/auth/apple")
async def apple_login(request: Request):
    """Initiate Apple Sign-In (Placeholder)"""
    # TODO: Implement Apple Sign-In when credentials are available
    raise HTTPException(status_code=501, detail="Apple Sign-In not implemented yet. Please provide Apple credentials.")

@router.post("/auth/apple/callback")
async def apple_callback(request: Request):
    """Handle Apple Sign-In callback (Placeholder)"""
    # TODO: Implement Apple Sign-In callback when credentials are available
    raise HTTPException(status_code=501, detail="Apple Sign-In callback not implemented yet. Please provide Apple credentials.")

# Twitter/X OAuth Endpoints (Placeholder Structure)
@router.get("/auth/twitter")
async def twitter_login(request: Request):
    """Initiate Twitter/X OAuth login (Placeholder)"""
    # TODO: Implement Twitter/X OAuth when credentials are available
    raise HTTPException(status_code=501, detail="Twitter/X OAuth not implemented yet. Please provide Twitter credentials.")

@router.get("/auth/twitter/callback")
async def twitter_callback(request: Request):
    """Handle Twitter/X OAuth callback (Placeholder)"""
    # TODO: Implement Twitter/X OAuth callback when credentials are available
    raise HTTPException(status_code=501, detail="Twitter/X OAuth callback not implemented yet. Please provide Twitter credentials.")

# General OAuth endpoints
@router.post("/auth/oauth/logout")
async def oauth_logout(request: Request):
    """Logout OAuth user"""
    try:
        # Get session token from request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="No valid session token provided")
        
        session_token = auth_header.split(' ')[1]
        
        # Deactivate session
        await user_sessions_collection.update_one(
            {"session_token": session_token},
            {"$set": {"active": False}}
        )
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

@router.get("/auth/oauth/me")
async def get_current_oauth_user(request: Request):
    """Get current OAuth user information"""
    try:
        # Get session token from request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="No valid session token provided")
        
        session_token = auth_header.split(' ')[1]
        
        # Find active session
        session = await user_sessions_collection.find_one({
            "session_token": session_token,
            "active": True,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if not session:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        # Get user info - handle both OAuth and regular users
        user = await users_collection.find_one({"_id": session["user_id"]})
        if not user:
            # Try with id field for backward compatibility
            user = await users_collection.find_one({"id": session["user_id"]})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Return user info with safe field access
        return {
            "id": user.get("id"),
            "email": user.get("email"),
            "name": user.get("name"),
            "plan": user.get("plan", "basic"),
            "avatar_url": user.get("avatar_url"),
            "oauth_provider": user.get("oauth_provider"),
            "last_login": user.get("last_login"),
            "created_at": user.get("created_at"),
            "is_active": user.get("is_active", True)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user info: {str(e)}")