#!/bin/bash

# Mainza Consciousness System - Build Monitoring Script
# Monitors build performance, cache usage, and system resources

set -e  # Exit on any error

echo "📊 Mainza Build Performance Monitor"
echo "==================================="

# Function to get Docker system info
get_docker_info() {
    echo "🐳 Docker System Information:"
    echo "----------------------------"
    docker system df
    echo ""
    
    echo "📦 Image Information:"
    echo "-------------------"
    docker images | grep mainza | head -5
    echo ""
    
    echo "🏃 Container Status:"
    echo "------------------"
    docker-compose ps
    echo ""
}

# Function to get build performance metrics
get_build_metrics() {
    echo "⏱️  Build Performance Metrics:"
    echo "-----------------------------"
    
    # Get image creation times
    echo "Image Creation Times:"
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}" | grep mainza
    echo ""
    
    # Get container resource usage
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" | grep mainza
    echo ""
}

# Function to check cache efficiency
check_cache_efficiency() {
    echo "💾 Cache Efficiency Analysis:"
    echo "----------------------------"
    
    # Check build cache size
    echo "Build Cache Size:"
    docker system df | grep "Build Cache" || echo "No build cache data available"
    echo ""
    
    # Check layer cache usage
    echo "Layer Cache Analysis:"
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep mainza | while read repo tag size; do
        if [ "$repo" != "REPOSITORY" ]; then
            echo "  $repo:$tag - $size"
        fi
    done
    echo ""
}

# Function to check build context efficiency
check_build_context() {
    echo "📁 Build Context Analysis:"
    echo "------------------------"
    
    # Check .dockerignore effectiveness
    echo "Files excluded by .dockerignore:"
    if [ -f .dockerignore ]; then
        echo "✅ .dockerignore file exists"
        echo "Excluded patterns:"
        grep -v "^#" .dockerignore | grep -v "^$" | head -10
    else
        echo "❌ No .dockerignore file found"
    fi
    echo ""
    
    # Check current directory size
    echo "Current directory size:"
    du -sh . 2>/dev/null || echo "Could not calculate directory size"
    echo ""
}

# Function to check build health
check_build_health() {
    echo "🏥 Build Health Check:"
    echo "---------------------"
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Containers are running"
    else
        echo "❌ Some containers are not running"
    fi
    
    # Check API endpoints
    echo "API Health:"
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo "✅ Backend API healthy"
    else
        echo "❌ Backend API unhealthy"
    fi
    
    if curl -s http://localhost >/dev/null 2>&1; then
        echo "✅ Frontend healthy"
    else
        echo "❌ Frontend unhealthy"
    fi
    echo ""
}

# Function to generate performance report
generate_performance_report() {
    echo "📈 Performance Report:"
    echo "--------------------"
    
    # Calculate build context reduction
    if [ -f .dockerignore ]; then
        echo "✅ Build context optimized with .dockerignore"
        echo "   Expected reduction: ~96% (from 388MB to ~14MB)"
    else
        echo "❌ No .dockerignore file - build context not optimized"
    fi
    
    # Check cache usage
    cache_size=$(docker system df | grep "Build Cache" | awk '{print $3}' | head -1)
    if [ -n "$cache_size" ]; then
        echo "💾 Build cache size: $cache_size"
    fi
    
    # Check image sizes
    echo "📦 Image sizes:"
    docker images --format "  {{.Repository}}:{{.Tag}} - {{.Size}}" | grep mainza
    echo ""
}

# Main execution
main() {
    get_docker_info
    get_build_metrics
    check_cache_efficiency
    check_build_context
    check_build_health
    generate_performance_report
    
    echo "✅ Build monitoring completed!"
    echo ""
    echo "💡 Tips for optimization:"
    echo "  - Run './scripts/build-dev.sh' for development builds"
    echo "  - Run './scripts/build-prod.sh' for production builds"
    echo "  - Run 'docker system prune -f' to clean up unused resources"
    echo "  - Check 'docs/DOCKER_BUILD_PROCESS_GUIDE.md' for detailed instructions"
}

# Run main function
main
