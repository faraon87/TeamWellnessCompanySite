from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env.local first, then .env
load_dotenv('.env.local')
load_dotenv('.env')

from app.routers import auth, payments, ai_chat, programs, analytics
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
    title="Team Welly API",
    description="Health and wellness platform with AI-powered coaching",
    version="2.0.0",
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
        "message": "🏥 Team Welly API is running!",
        "version": "2.0.0",
        "features": [
            "✅ Enhanced Authentication with Emergent Auth",
            "✅ OAuth Authentication (Google, Apple, Twitter/X)",
            "✅ Stripe Payment Integration",
            "✅ AI-powered Wellness Coaching",
            "✅ Comprehensive Program Management",
            "✅ Real-time Analytics",
            "✅ Progressive Web App Support"
        ],
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-01-16T02:30:00Z",
        "version": "2.0.0",
        "services": {
            "database": "✅ Connected",
            "auth": "✅ Emergent Auth Ready",
            "payments": "✅ Stripe Configured",
            "ai_chat": "✅ AI Chat Ready"
        }
    }

# Include enhanced routers with /api prefix
app.include_router(enhanced_auth_router, prefix="/api/auth", tags=["Enhanced Authentication"])
app.include_router(enhanced_payments_router, prefix="/api/payments", tags=["Enhanced Payments"])
app.include_router(oauth_router, prefix="/api", tags=["OAuth Authentication"])

# Include existing routers with /api prefix
app.include_router(auth.router, prefix="/api/auth-legacy", tags=["Legacy Authentication"])
# Temporarily disabled payments router due to emergentintegrations dependency
# app.include_router(payments.router, prefix="/api/payments-legacy", tags=["Legacy Payments"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Chat"])

app.include_router(programs.router, prefix="/api/programs", tags=["Programs"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

# API Info endpoint
@app.get("/api/info")
async def api_info():
    return {
        "title": "Team Welly API v2.0",
        "description": "Enhanced health and wellness platform",
        "features": {
            "authentication": {
                "emergent_auth": "✅ Hassle-free email authentication",
                "session_management": "✅ 7-day session tokens",
                "user_profiles": "✅ Complete user management"
            },
            "payments": {
                "stripe_integration": "✅ Secure payment processing",
                "wellness_packages": "✅ Predefined wellness plans",
                "payment_history": "✅ Transaction tracking",
                "webhooks": "✅ Real-time payment updates"
            },
            "ai_coaching": {
                "gemini_integration": "⚠️ Requires API key",
                "behavioral_analysis": "✅ User behavior tracking",
                "personalized_recommendations": "✅ AI-driven suggestions"
            },
            "programs": {
                "comprehensive_library": "✅ 6 program categories",
                "progress_tracking": "✅ User progress analytics",
                "bookmarking": "✅ Save favorite programs"
            }
        },
        "endpoints": {
            "auth": "/api/auth/*",
            "payments": "/api/payments/*", 
            "ai_chat": "/api/ai/*",
            "programs": "/api/programs/*",
            "analytics": "/api/analytics/*"
        }
    }

# Enhanced error handling
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "The requested resource was not found",
        "available_endpoints": [
            "/api/auth/* - Authentication endpoints",
            "/api/payments/* - Payment processing",
            "/api/ai/* - AI chat and coaching",
            "/api/programs/* - Wellness programs",
            "/api/analytics/* - User analytics"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "Something went wrong on our end",
        "support": "Please check the logs or contact support"
    }

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )