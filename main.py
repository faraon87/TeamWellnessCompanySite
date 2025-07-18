#!/usr/bin/env python3
"""
Railway-specific server file for Team Welly API with Twitter OAuth
"""
import sys
import os
sys.path.append('/app')
sys.path.append('/app/backend')

# Import the app from backend
from backend.twitter_oauth_server import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)