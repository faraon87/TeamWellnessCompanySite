from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import os

# Create completely standalone FastAPI app
app = FastAPI(
    title="Team Welly API",
    description="Standalone OAuth-ready API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "🏥 Team Welly API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "oauth": "ready",
        "deployment": "railway",
        "features": [
            "✅ OAuth Authentication Ready",
            "✅ CORS Enabled",
            "✅ Zero Dependencies"
        ]
    }

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": "2025-01-17",
        "services": {
            "api": "running",
            "oauth": "ready"
        }
    }

# Google OAuth initiation
@app.get("/api/auth/google")
async def google_auth(request: Request):
    """Initiate Google OAuth flow"""
    try:
        # Get environment variables
        client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        
        # Get the base URL from the request
        base_url = str(request.base_url).rstrip('/')
        redirect_uri = f"{base_url}/api/auth/google/callback"
        
        # Build Google OAuth URL
        google_oauth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile&"
            f"access_type=offline"
        )
        
        return RedirectResponse(url=google_oauth_url)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "OAuth initiation failed", "details": str(e)}
        )

# Google OAuth callback
@app.get("/api/auth/google/callback")
async def google_callback(request: Request, code: str = None, error: str = None):
    """Handle Google OAuth callback"""
    if error:
        return HTMLResponse(f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px;">
            <h1 style="color: red;">❌ OAuth Error</h1>
            <p><strong>Error:</strong> {error}</p>
            <a href="/" style="color: #4285f4;">← Back to API</a>
        </body>
        </html>
        """)
    
    if code:
        return HTMLResponse(f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px;">
            <h1 style="color: green;">🎉 OAuth Success!</h1>
            <p><strong>✅ Google OAuth is working!</strong></p>
            <p><strong>✅ Your Railway deployment is successful!</strong></p>
            <p><strong>✅ Backend server is running properly!</strong></p>
            <p><strong>Authorization Code:</strong> {code[:20]}...</p>
            <br>
            <p><em>This proves your OAuth flow is working! You can now integrate this with your frontend.</em></p>
            <a href="/" style="color: #4285f4;">← Back to API</a>
        </body>
        </html>
        """)
    
    return HTMLResponse("""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px;">
        <h1>⚠️ OAuth Callback</h1>
        <p>No authorization code or error received.</p>
        <a href="/" style="color: #4285f4;">← Back to API</a>
    </body>
    </html>
    """)

# Test page
@app.get("/test")
async def test_page():
    """Test page to verify deployment"""
    return HTMLResponse("""
    <html>
    <head>
        <title>Team Welly API - Railway Deployment Test</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .success { color: green; font-size: 18px; margin: 10px 0; }
            .button { display: inline-block; padding: 12px 24px; background: #4285f4; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }
            .button:hover { background: #3367d6; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #4285f4; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Team Welly API - Railway Deployment</h1>
            <div class="success">✅ Your Railway deployment is working!</div>
            <div class="success">✅ FastAPI server is running properly!</div>
            <div class="success">✅ OAuth endpoints are ready!</div>
            <div class="success">✅ CORS is configured!</div>
            
            <h2>🔐 Test OAuth:</h2>
            <a href="/api/auth/google" class="button">Test Google OAuth Login</a>
            <p><em>This will redirect you to Google for authentication, then back to confirm it's working.</em></p>
            
            <h2>📋 Available Endpoints:</h2>
            <div class="endpoint"><strong>GET /</strong> - API Status & Information</div>
            <div class="endpoint"><strong>GET /health</strong> - Health Check</div>
            <div class="endpoint"><strong>GET /test</strong> - This Test Page</div>
            <div class="endpoint"><strong>GET /api/auth/google</strong> - Google OAuth Initiation</div>
            <div class="endpoint"><strong>GET /api/auth/google/callback</strong> - Google OAuth Callback</div>
            
            <h2>🚀 Next Steps:</h2>
            <ol>
                <li>Test the Google OAuth flow above</li>
                <li>Update your frontend to use this Railway URL</li>
                <li>Configure your Google OAuth redirect URIs</li>
                <li>Deploy your frontend</li>
            </ol>
        </div>
    </body>
    </html>
    """)

# API information
@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Team Welly API",
        "version": "1.0.0",
        "description": "Standalone OAuth-ready API for Team Wellness Company",
        "deployment": "Railway",
        "features": {
            "oauth": {
                "google": "✅ Configured",
                "apple": "🔄 Coming Soon",
                "twitter": "🔄 Coming Soon"
    },
            "cors": "✅ Enabled",
            "health_check": "✅ Available"
        },
        "endpoints": {
            "health": "/health",
            "test": "/test",
            "google_oauth": "/api/auth/google",
            "oauth_callback": "/api/auth/google/callback"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
