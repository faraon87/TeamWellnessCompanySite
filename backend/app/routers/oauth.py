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
import jwt
import json
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
        # Use production HTTPS URL for Railway deployment
        redirect_uri = "https://teamwellnesscompanysite-production.up.railway.app/api/auth/google/callback"
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

# Apple Sign-In Configuration
def generate_apple_client_secret():
    """Generate Apple Client Secret JWT"""
    private_key = os.getenv('APPLE_PRIVATE_KEY')
    # Handle Railway environment variable format (single line with \n escapes)
    if private_key and '\\n' in private_key:
        private_key = private_key.replace('\\n', '\n')
    team_id = os.getenv('APPLE_TEAM_ID')
    key_id = os.getenv('APPLE_KEY_ID')
    service_id = os.getenv('APPLE_SERVICE_ID')
    
    if not all([private_key, team_id, key_id, service_id]):
        raise ValueError("Missing Apple OAuth credentials")
    
    now = datetime.utcnow()
    
    payload = {
        "iss": team_id,
        "aud": "https://appleid.apple.com",
        "sub": service_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=150)).timestamp()),
    }
    
    return jwt.encode(
        payload,
        private_key,
        algorithm="ES256",
        headers={"kid": key_id}
    )

# Apple Sign-In Endpoints
@router.get("/auth/apple")
async def apple_login(request: Request):
    """Initiate Apple Sign-In"""
    try:
        service_id = os.getenv('APPLE_SERVICE_ID')
        if not service_id:
            raise HTTPException(status_code=500, detail="Apple OAuth not configured")
        
        # Build redirect URI with HTTPS
        redirect_uri = "https://teamwellnesscompanysite-production.up.railway.app/api/auth/apple/callback"
        
        # Generate state for CSRF protection
        state = str(uuid.uuid4())
        
        # Store state in session for verification
        request.session['apple_state'] = state
        
        # Build Apple authorization URL
        auth_url = (
            f"https://appleid.apple.com/auth/authorize"
            f"?client_id={service_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=email name"
            f"&response_mode=form_post"
            f"&state={state}"
        )
        
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Apple OAuth initiation failed: {str(e)}")

@router.post("/auth/apple/callback")
async def apple_callback(request: Request):
    """Handle Apple Sign-In callback"""
    try:
        # Get form data from Apple
        form_data = await request.form()
        authorization_code = form_data.get('code')
        state = form_data.get('state')
        user_info = form_data.get('user')
        
        if not authorization_code:
            raise HTTPException(status_code=400, detail="No authorization code received")
        
        # Verify state for CSRF protection
        if state != request.session.get('apple_state'):
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        
        # Generate client secret
        client_secret = generate_apple_client_secret()
        
        # Exchange authorization code for tokens
        token_response = requests.post(
            "https://appleid.apple.com/auth/token",
            data={
                "client_id": os.getenv('APPLE_SERVICE_ID'),
                "client_secret": client_secret,
                "code": authorization_code,
                "grant_type": "authorization_code",
                "redirect_uri": "https://teamwellnesscompanysite-production.up.railway.app/api/auth/apple/callback"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        
        tokens = token_response.json()
        
        # Decode ID token to get user info
        id_token = tokens.get('id_token')
        if not id_token:
            raise HTTPException(status_code=400, detail="No ID token received")
        
        # Decode JWT (without verification for now - in production, verify signature)
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        
        # Parse user info (sent on first login only)
        user_name = "Apple User"
        if user_info:
            user_data = json.loads(user_info)
            name_data = user_data.get('name', {})
            if name_data:
                first_name = name_data.get('firstName', '')
                last_name = name_data.get('lastName', '')
                user_name = f"{first_name} {last_name}".strip() or "Apple User"
        
        # Create OAuth user object
        oauth_user = OAuthUser(
            email=decoded_token.get('email'),
            name=user_name,
            provider='apple',
            provider_id=decoded_token.get('sub'),
            avatar_url=None  # Apple doesn't provide avatar URLs
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
            <title>Apple Sign-In Successful</title>
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
                .apple-logo {{
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="apple-logo">🍎</div>
                <div class="success">✅ Apple Sign-In Successful!</div>
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
                    "avatar_url": null,
                    "oauth_provider": "apple"
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
            <title>Apple Sign-In Error</title>
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
                <div class="error">🍎 ❌ Apple Sign-In Failed</div>
                <div class="retry" onclick="window.location.href='/'">← Back to Home</div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html)

# Twitter/X OAuth 2.0 Configuration
oauth.register(
    name='twitter',
    client_id=os.getenv('TWITTER_CLIENT_ID'),
    client_secret=os.getenv('TWITTER_CLIENT_SECRET'),
    authorize_url='https://twitter.com/i/oauth2/authorize',
    access_token_url='https://api.twitter.com/2/oauth2/token',
    client_kwargs={
        'scope': 'tweet.read users.read offline.access',
        'token_endpoint_auth_method': 'client_secret_basic',
    },
    server_metadata_url='https://api.twitter.com/2/oauth2/token',
)

# Twitter/X OAuth Endpoints
@router.get("/auth/twitter")
async def twitter_login(request: Request):
    """Initiate Twitter/X OAuth 2.0 login"""
    try:
        client_id = os.getenv('TWITTER_CLIENT_ID')
        if not client_id:
            raise HTTPException(status_code=500, detail="Twitter OAuth not configured")
        
        # Build redirect URI using absolute URL
        base_url = str(request.base_url).rstrip('/')
        redirect_uri = f"{base_url}/api/auth/twitter/callback"
        
        # Generate state for CSRF protection
        state = str(uuid.uuid4())
        
        # Store state in session for verification
        request.session['twitter_state'] = state
        
        # Build Twitter OAuth 2.0 authorization URL
        auth_url = (
            f"https://twitter.com/i/oauth2/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=tweet.read users.read"
            f"&state={state}"
            f"&code_challenge=challenge"
            f"&code_challenge_method=plain"
        )
        
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Twitter OAuth initiation failed: {str(e)}")

@router.get("/auth/twitter/callback")
async def twitter_callback(request: Request):
    """Handle Twitter/X OAuth 2.0 callback"""
    try:
        # Get authorization code and state from query params
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        error = request.query_params.get('error')
        
        if error:
            raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
        
        if not code:
            raise HTTPException(status_code=400, detail="No authorization code received")
        
        # Verify state for CSRF protection
        if state != request.session.get('twitter_state'):
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        
        # Exchange authorization code for access token
        token_response = requests.post(
            "https://api.twitter.com/2/oauth2/token",
            auth=(os.getenv('TWITTER_CLIENT_ID'), os.getenv('TWITTER_CLIENT_SECRET')),
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": str(request.url_for("twitter_callback")),
                "code_verifier": "challenge"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        
        tokens = token_response.json()
        access_token = tokens.get('access_token')
        
        # Get user info from Twitter API v2
        user_response = requests.get(
            "https://api.twitter.com/2/users/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            params={"user.fields": "id,name,username,profile_image_url"}
        )
        
        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")
        
        user_data = user_response.json()
        user_info = user_data.get('data', {})
        
        # Create OAuth user object
        oauth_user = OAuthUser(
            email=f"{user_info.get('username')}@twitter.placeholder",  # Twitter doesn't always provide email
            name=user_info.get('name', 'Twitter User'),
            provider='twitter',
            provider_id=user_info.get('id'),
            avatar_url=user_info.get('profile_image_url')
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
            <title>Twitter Sign-In Successful</title>
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
                .twitter-logo {{
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="twitter-logo">🐦</div>
                <div class="success">✅ Twitter Sign-In Successful!</div>
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
                    "oauth_provider": "twitter"
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
            <title>Twitter Sign-In Error</title>
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
                <div class="error">🐦 ❌ Twitter Sign-In Failed</div>
                <div class="retry" onclick="window.location.href='/'">← Back to Home</div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html)

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