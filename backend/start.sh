#!/bin/bash
# Railway startup script for Team Welly API

echo "🚀 Starting Team Welly API on Railway..."
echo "📁 Current directory: $(pwd)"
echo "📄 Python files available:"
ls -la *.py

# Check if environment variables are loaded
echo "🔧 Checking environment variables..."
echo "TWITTER_CLIENT_ID present: $(if [ -n "$TWITTER_CLIENT_ID" ]; then echo "✅ Yes"; else echo "❌ No"; fi)"
echo "GOOGLE_CLIENT_ID present: $(if [ -n "$GOOGLE_CLIENT_ID" ]; then echo "✅ Yes"; else echo "❌ No"; fi)"

# Start the server
echo "🌐 Starting server with server_minimal.py..."
python -m uvicorn server_minimal:app --host 0.0.0.0 --port $PORT