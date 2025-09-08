#!/bin/bash

# Mainza Consciousness System - Development Build Script
# This script builds the application for development with no cache to ensure changes are reflected

set -e  # Exit on any error

echo "🚀 Starting Mainza Development Build Process..."
echo "=================================================="

# Get current timestamp and git commit for cache busting
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
CACHE_BUST=$(date +%s)

echo "📅 Build Date: $BUILD_DATE"
echo "🔗 Git Commit: $GIT_COMMIT"
echo "🔄 Cache Bust: $CACHE_BUST"
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
docker-compose down 2>/dev/null || true
docker system prune -f

# Remove old images to force rebuild
echo "🗑️  Removing old images..."
docker rmi mainza-consciousness-frontend:latest 2>/dev/null || true
docker rmi mainza-consciousness-backend:latest 2>/dev/null || true

# Build with no cache and cache busting arguments
echo "🔨 Building frontend with no cache..."
docker-compose build --no-cache \
  --build-arg CACHE_BUST=$CACHE_BUST \
  --build-arg BUILD_DATE="$BUILD_DATE" \
  --build-arg GIT_COMMIT="$GIT_COMMIT" \
  frontend

echo "🔨 Building backend with no cache..."
docker-compose build --no-cache \
  --build-arg CACHE_BUST=$CACHE_BUST \
  --build-arg BUILD_DATE="$BUILD_DATE" \
  --build-arg GIT_COMMIT="$GIT_COMMIT" \
  backend

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Health check
echo "🏥 Performing health checks..."
echo "Frontend health:"
curl -f http://localhost/health 2>/dev/null && echo "✅ Frontend healthy" || echo "❌ Frontend unhealthy"

echo "Backend health:"
curl -f http://localhost:8000/health 2>/dev/null && echo "✅ Backend healthy" || echo "❌ Backend unhealthy"

echo ""
echo "✅ Development build completed successfully!"
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend: http://localhost:8000"
echo "📊 Neo4j: http://localhost:7474"
echo ""
echo "📝 To view logs:"
echo "   Frontend: docker logs mainza-frontend -f"
echo "   Backend:  docker logs mainza-backend -f"
echo "   All:      docker-compose logs -f"
