#!/bin/bash

# Mainza Consciousness System - Change Verification Script
# This script verifies that changes are reflected in the running containers

set -e  # Exit on any error

echo "🔍 Verifying Changes in Running Containers..."
echo "============================================="

# Check if containers are running
echo "📋 Checking container status..."
docker-compose ps

echo ""

# Verify frontend changes
echo "🌐 Verifying frontend changes..."
echo "Checking for development status badges..."
if curl -s http://localhost | grep -q "Coming Soon\|Mock Data\|Partial Data\|In Dev"; then
    echo "✅ Development status badges found in frontend"
else
    echo "❌ Development status badges not found in frontend"
fi

echo "Checking for polling optimizations..."
if curl -s http://localhost/assets/index-*.js | grep -q "3600000"; then
    echo "✅ 1-hour polling intervals found in frontend"
else
    echo "❌ 1-hour polling intervals not found in frontend"
fi

echo ""

# Verify backend changes
echo "🔧 Verifying backend changes..."
echo "Checking for cache TTL optimizations..."
if docker exec mainza-backend grep -q "background_cache_ttl" /app/backend/utils/llm_request_manager.py 2>/dev/null; then
    echo "✅ Background cache TTL optimizations found in backend"
else
    echo "❌ Background cache TTL optimizations not found in backend"
fi

echo ""

# Check build information
echo "📊 Build Information:"
echo "Frontend image:"
docker inspect mainza-consciousness-frontend:latest | grep -A 3 -B 3 "Created" | head -5

echo "Backend image:"
docker inspect mainza-consciousness-backend:latest | grep -A 3 -B 3 "Created" | head -5

echo ""

# Check build information via API
echo "📊 Build Information via API:"
echo "Backend build info:"
curl -s http://localhost:8000/build/info 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "❌ Could not fetch build info"

echo "Frontend build info:"
curl -s http://localhost/build-info.js 2>/dev/null | head -1 || echo "❌ Could not fetch frontend build info"

echo ""

# Check container logs for build information
echo "📝 Build logs from containers:"
echo "Frontend build info:"
docker logs mainza-frontend 2>&1 | grep -E "(Cache bust|Build date|Git commit)" | tail -3

echo "Backend build info:"
docker logs mainza-backend 2>&1 | grep -E "(Cache bust|Build date|Git commit)" | tail -3

echo ""
echo "✅ Change verification completed!"
