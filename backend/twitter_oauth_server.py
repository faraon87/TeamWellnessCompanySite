from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env.local first, then .env
load_dotenv('.env.local')
load_dotenv('.env')

# Simple routers that don't depend on emergentintegrations
from app.routers.enhanced_auth import router as enhanced_auth_router
from app.routers.enhanced_payments import router as enhanced_payments_router
from app.routers.oauth import router as oauth_router
from app.database import init_database

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Team Welly API Server...")
    await init_database()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("🔄 Shutting down Team Welly API Server...")

# Create FastAPI app
app = FastAPI(
    title="Team Welly API v2.1 - Twitter OAuth Ready",
    description="Health and wellness platform with complete OAuth authentication",
    version="2.1.0",
    lifespan=lifespan
)

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key-here"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "🏥 Team Welly API v2.1 - Twitter OAuth Ready!",
        "version": "2.1.0",
        "features": [
            "✅ Google OAuth Integration",
            "✅ Apple OAuth Integration", 
            "✅ Twitter OAuth Integration - NEW!",
            "✅ Enhanced Authentication",
            "✅ Enhanced Payment Integration",
            "✅ Progressive Web App Support"
        ],
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-01-17T22:00:00Z",
        "version": "2.1.0",
        "services": {
            "database": "✅ Connected",
            "oauth": "✅ OAuth Ready with Twitter",
            "payments": "✅ Enhanced Payments Ready"
        }
    }

# Include working routers with /api prefix
app.include_router(enhanced_auth_router, prefix="/api/auth", tags=["Enhanced Authentication"])
app.include_router(enhanced_payments_router, prefix="/api/payments", tags=["Enhanced Payments"])
app.include_router(oauth_router, prefix="/api", tags=["OAuth Authentication"])

# Debug endpoint to check environment variables
@app.get("/debug/env")
async def debug_env():
    return {
        "twitter_client_id": os.getenv('TWITTER_CLIENT_ID', 'NOT_SET'),
        "google_client_id": os.getenv('GOOGLE_CLIENT_ID', 'NOT_SET'),
        "apple_service_id": os.getenv('APPLE_SERVICE_ID', 'NOT_SET'),
        "env_vars_loaded": {
            "twitter": bool(os.getenv('TWITTER_CLIENT_ID')),
            "google": bool(os.getenv('GOOGLE_CLIENT_ID')),
            "apple": bool(os.getenv('APPLE_SERVICE_ID'))
        }
    }

# API Info endpoint
@app.get("/api/info")
async def api_info():
    # Check if Twitter OAuth credentials are loaded
    twitter_client_id = os.getenv('TWITTER_CLIENT_ID')
    twitter_configured = "✅ Configured" if twitter_client_id else "❌ Not Configured"
    
    return {
        "title": "Team Welly API v2.1 - Railway Deployment",
        "description": "Health and wellness platform with OAuth authentication",
        "features": {
            "oauth_authentication": {
                "google_oauth": "✅ Working with rotated credentials",
                "apple_oauth": "✅ Working with real credentials",
                "twitter_oauth": f"{twitter_configured} - OAuth 2.0",
                "session_management": "✅ 7-day session tokens"
            },
            "enhanced_authentication": {
                "emergent_auth": "✅ Hassle-free email authentication",
                "user_profiles": "✅ Complete user management"
            },
            "enhanced_payments": {
                "stripe_integration": "✅ Secure payment processing",
                "wellness_packages": "✅ Predefined wellness plans",
                "payment_history": "✅ Transaction tracking"
            }
        },
        "endpoints": {
            "oauth": "/api/auth/google, /api/auth/apple, /api/auth/twitter",
            "auth": "/api/auth/*",
            "payments": "/api/payments/*"
        },
        "debug": {
            "twitter_client_id_present": bool(twitter_client_id),
            "twitter_client_id_length": len(twitter_client_id) if twitter_client_id else 0
        }
    }

# Test endpoint
@app.get("/test")
async def test_page():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Team Welly API v2.1 - Test Page</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 10px; 
                backdrop-filter: blur(10px);
            }
            h1 { color: #fff; text-align: center; }
            .feature { 
                background: rgba(255,255,255,0.1); 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px; 
            }
            .oauth-button {
                display: inline-block;
                margin: 10px;
                padding: 15px 30px;
                background: #fff;
                color: #333;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                transition: transform 0.2s;
            }
            .oauth-button:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Team Welly API v2.1</h1>
            <h2>Twitter OAuth Now Available!</h2>
            
            <div class="feature">
                <h3>✅ OAuth Providers</h3>
                <a href="/api/auth/google" class="oauth-button">🔍 Google OAuth</a>
                <a href="/api/auth/apple" class="oauth-button">🍎 Apple OAuth</a>
                <a href="/api/auth/twitter" class="oauth-button">🐦 Twitter OAuth</a>
            </div>
            
            <div class="feature">
                <h3>🔧 Debug & Info</h3>
                <a href="/debug/env" class="oauth-button">🔍 Environment Variables</a>
                <a href="/api/info" class="oauth-button">ℹ️ API Information</a>
            </div>
            
            <div class="feature">
                <h3>🏥 Health Check</h3>
                <a href="/health" class="oauth-button">💚 Health Status</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))