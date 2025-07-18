from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')
load_dotenv('.env')

# Only import working routers
from app.routers.enhanced_auth import router as enhanced_auth_router
from app.routers.enhanced_payments import router as enhanced_payments_router
from app.routers.oauth import router as oauth_router
from app.database import init_database

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Team Welly API Server...")
    await init_database()
    print("✅ Database initialized")
    yield
    print("🔄 Shutting down Team Welly API Server...")

# Create FastAPI app
app = FastAPI(
    title="Team Welly API",
    description="Health and wellness platform with OAuth authentication",
    version="2.0.0",
    lifespan=lifespan
)

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key-here"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "🏥 Team Welly API is running!",
        "version": "2.0.0",
        "features": [
            "✅ OAuth Authentication (Google)",
            "✅ Enhanced Authentication",
            "✅ Enhanced Payment Integration"
        ],
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# Include ONLY working routers
app.include_router(enhanced_auth_router, prefix="/api/auth", tags=["Enhanced Authentication"])
app.include_router(enhanced_payments_router, prefix="/api/payments", tags=["Enhanced Payments"])
app.include_router(oauth_router, prefix="/api", tags=["OAuth Authentication"])

# Test page
@app.get("/test")
async def test_page():
    return HTMLResponse("""
    <html><body>
        <h1>🎉 Team Welly API is Running!</h1>
        <p>✅ OAuth endpoints ready</p>
        <a href="/api/auth/google">Test Google OAuth</a>
    </body></html>
    """)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
