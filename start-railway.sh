#!/bin/bash
echo "🚀 Starting Team Welly API on Railway..."
echo "📁 Current directory: $(pwd)"
echo "📄 Directory structure:"
ls -la

echo "🔧 Checking Python path..."
which python
python --version

echo "🔧 Checking if backend module exists..."
python -c "import backend.main; print('✅ Backend module found')" || echo "❌ Backend module not found"

echo "🌐 Starting server..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT