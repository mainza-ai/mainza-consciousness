#!/bin/bash

# Neo4j Authentication Reset Script
# Resets Neo4j volume data to fix authentication issues

echo "🔧 Resetting Neo4j authentication..."
echo "==================================="

# Stop all containers
echo "📉 Stopping containers..."
docker-compose down

# Remove Neo4j volumes to clear stale auth data
echo "🗑️  Removing Neo4j volume data..."
docker volume rm mainza-consciousness_neo4j_data || true
docker volume rm mainza-consciousness_neo4j_logs || true

# Start only Neo4j with fresh authentication
echo "🚀 Starting Neo4j with fresh authentication..."
docker-compose up -d neo4j

echo ""
echo "⏳ Waiting for Neo4j to fully initialize..."
sleep 30

echo ""
echo "✅ Neo4j authentication reset complete!"
echo ""
echo "🌐 Login to Neo4j Browser:"
echo "   URL: http://localhost:7474"
echo "   Username: neo4j"
echo "   Password: mainza123"
echo ""
echo "💡 Note: Wait a moment after login if the interface asks you to change the password"
echo ""

# Check Neo4j status
echo "🔍 Neo4j container status:"
docker-compose ps neo4j
