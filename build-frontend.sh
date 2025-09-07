#!/bin/bash
# Mainza Frontend Build Script

set -e

echo "🚀 Starting Mainza Frontend Build..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/
rm -rf node_modules/
rm -f package-lock.json

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Set environment variables for build
export VITE_API_URL=http://mainza-backend:8000
export VITE_LIVEKIT_URL=ws://mainza-livekit:7880

# Build the application
echo "🔨 Building application..."
npm run build

# Check if build was successful
if [ -d "dist" ] && [ -f "dist/index.html" ]; then
    echo "✅ Build successful!"
    echo "📁 Build output:"
    ls -la dist/
    echo ""
    echo "📄 index.html content:"
    head -20 dist/index.html
else
    echo "❌ Build failed!"
    exit 1
fi

echo "🎉 Frontend build completed successfully!"
