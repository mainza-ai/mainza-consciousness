#!/bin/bash

# Mainza Consciousness System - Development Build with Hot Reloading
# This script builds the application for development with hot reloading

set -e  # Exit on any error

echo "🚀 Starting Mainza Development Build with Hot Reloading..."
echo "========================================================="

# Get current timestamp and git commit for cache busting
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
CACHE_BUST=$(date +%s)

echo "📅 Build Date: $BUILD_DATE"
echo "🔗 Git Commit: $GIT_COMMIT"
echo "🔄 Cache Bust: $CACHE_BUST"
echo ""

# Clean previous builds
echo "🧹 Cleaning previous development builds..."
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
docker system prune -f

# Build with development configuration
echo "🔨 Building development containers with hot reloading..."
docker-compose -f docker-compose.dev.yml build \
  --build-arg CACHE_BUST=$CACHE_BUST \
  --build-arg BUILD_DATE="$BUILD_DATE" \
  --build-arg GIT_COMMIT="$GIT_COMMIT"

# Start services
echo "🚀 Starting development services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Health check
echo "🏥 Performing health checks..."
echo "Frontend health (Vite dev server):"
curl -f http://localhost:5173 2>/dev/null && echo "✅ Frontend healthy" || echo "❌ Frontend unhealthy"

echo "Backend health:"
curl -f http://localhost:8000/health 2>/dev/null && echo "✅ Backend healthy" || echo "❌ Backend unhealthy"

echo ""
echo "✅ Development build with hot reloading completed successfully!"
echo "🌐 Frontend (Vite): http://localhost:5173"
echo "🔧 Backend: http://localhost:8000"
echo "📊 Neo4j: http://localhost:7474"
echo ""
echo "🔥 Hot Reloading Enabled:"
echo "   - Frontend: Changes to src/ will auto-reload"
echo "   - Backend: Changes to backend/ will auto-reload"
echo ""
echo "📝 To view logs:"
echo "   Frontend: docker logs mainza-frontend-dev -f"
echo "   Backend:  docker logs mainza-backend-dev -f"
echo "   All:      docker-compose -f docker-compose.dev.yml logs -f"
