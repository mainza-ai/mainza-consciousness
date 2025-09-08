#!/bin/bash

# Mainza Consciousness System - Development Tools
# Comprehensive development utilities for build verification and management

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS") echo -e "${GREEN}✅ $message${NC}" ;;
        "ERROR") echo -e "${RED}❌ $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "INFO") echo -e "${BLUE}ℹ️  $message${NC}" ;;
    esac
}

# Function to show help
show_help() {
    echo "🚀 Mainza Development Tools"
    echo "=========================="
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build-dev          Build for development (no cache)"
    echo "  build-prod         Build for production (with cache)"
    echo "  build-hot          Build with hot reloading"
    echo "  verify             Verify changes are reflected"
    echo "  monitor            Monitor build performance"
    echo "  clean              Clean Docker resources"
    echo "  status             Show container status"
    echo "  logs               Show container logs"
    echo "  restart            Restart containers"
    echo "  health             Check system health"
    echo "  test               Run build verification tests"
    echo "  help               Show this help message"
    echo ""
    echo "Options:"
    echo "  --frontend         Only build/check frontend"
    echo "  --backend          Only build/check backend"
    echo "  --no-cache         Force rebuild without cache"
    echo "  --follow           Follow logs in real-time"
    echo ""
    echo "Examples:"
    echo "  $0 build-dev --no-cache"
    echo "  $0 verify --frontend"
    echo "  $0 logs --follow"
    echo "  $0 monitor"
}

# Function to build development
build_dev() {
    local no_cache=$1
    print_status "INFO" "Starting development build..."
    
    if [ "$no_cache" = "true" ]; then
        ./scripts/build-dev.sh
    else
        ./scripts/build-prod.sh
    fi
    
    print_status "SUCCESS" "Development build completed!"
}

# Function to build with hot reloading
build_hot() {
    print_status "INFO" "Starting development build with hot reloading..."
    ./scripts/build-dev-hot.sh
    print_status "SUCCESS" "Hot reloading build completed!"
}

# Function to verify changes
verify_changes() {
    local service=$1
    print_status "INFO" "Verifying changes..."
    
    if [ "$service" = "frontend" ]; then
        print_status "INFO" "Checking frontend changes..."
        curl -s http://localhost | grep -q "Coming Soon\|Mock Data" && \
            print_status "SUCCESS" "Frontend changes verified" || \
            print_status "ERROR" "Frontend changes not found"
    elif [ "$service" = "backend" ]; then
        print_status "INFO" "Checking backend changes..."
        curl -s http://localhost:8000/build/info >/dev/null && \
            print_status "SUCCESS" "Backend changes verified" || \
            print_status "ERROR" "Backend changes not found"
    else
        ./scripts/verify-changes.sh
    fi
}

# Function to monitor builds
monitor_builds() {
    print_status "INFO" "Starting build monitoring..."
    ./scripts/monitor-builds.sh
}

# Function to clean Docker resources
clean_docker() {
    print_status "INFO" "Cleaning Docker resources..."
    docker-compose down 2>/dev/null || true
    docker system prune -f
    print_status "SUCCESS" "Docker resources cleaned!"
}

# Function to show container status
show_status() {
    print_status "INFO" "Container Status:"
    echo ""
    docker-compose ps
    echo ""
    
    print_status "INFO" "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" | grep mainza || echo "No containers running"
}

# Function to show logs
show_logs() {
    local follow=$1
    local service=$2
    
    if [ "$follow" = "true" ]; then
        if [ -n "$service" ]; then
            print_status "INFO" "Following logs for $service..."
            docker logs -f "mainza-$service" 2>/dev/null || print_status "ERROR" "Container mainza-$service not found"
        else
            print_status "INFO" "Following all logs..."
            docker-compose logs -f
        fi
    else
        if [ -n "$service" ]; then
            print_status "INFO" "Showing logs for $service..."
            docker logs --tail 50 "mainza-$service" 2>/dev/null || print_status "ERROR" "Container mainza-$service not found"
        else
            print_status "INFO" "Showing recent logs..."
            docker-compose logs --tail 50
        fi
    fi
}

# Function to restart containers
restart_containers() {
    print_status "INFO" "Restarting containers..."
    docker-compose restart
    print_status "SUCCESS" "Containers restarted!"
}

# Function to check system health
check_health() {
    print_status "INFO" "Checking system health..."
    echo ""
    
    # Check Docker
    if docker --version >/dev/null 2>&1; then
        print_status "SUCCESS" "Docker is available"
    else
        print_status "ERROR" "Docker is not available"
        return 1
    fi
    
    # Check containers
    if docker-compose ps | grep -q "Up"; then
        print_status "SUCCESS" "Containers are running"
    else
        print_status "WARNING" "Some containers are not running"
    fi
    
    # Check API endpoints
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        print_status "SUCCESS" "Backend API is healthy"
    else
        print_status "ERROR" "Backend API is unhealthy"
    fi
    
    if curl -s http://localhost >/dev/null 2>&1; then
        print_status "SUCCESS" "Frontend is healthy"
    else
        print_status "ERROR" "Frontend is unhealthy"
    fi
}

# Function to run build verification tests
run_tests() {
    print_status "INFO" "Running build verification tests..."
    echo ""
    
    # Test 1: Check if changes are reflected
    print_status "INFO" "Test 1: Checking if changes are reflected..."
    verify_changes
    echo ""
    
    # Test 2: Check build info API
    print_status "INFO" "Test 2: Checking build info API..."
    if curl -s http://localhost:8000/build/info | grep -q "build_date"; then
        print_status "SUCCESS" "Build info API working"
    else
        print_status "ERROR" "Build info API not working"
    fi
    echo ""
    
    # Test 3: Check frontend build info
    print_status "INFO" "Test 3: Checking frontend build info..."
    if curl -s http://localhost/build-info.js | grep -q "BUILD_INFO"; then
        print_status "SUCCESS" "Frontend build info working"
    else
        print_status "ERROR" "Frontend build info not working"
    fi
    echo ""
    
    # Test 4: Check container health
    print_status "INFO" "Test 4: Checking container health..."
    check_health
    echo ""
    
    print_status "SUCCESS" "All tests completed!"
}

# Main function
main() {
    local command=$1
    shift
    
    case $command in
        "build-dev")
            local no_cache="false"
            for arg in "$@"; do
                case $arg in
                    --no-cache) no_cache="true" ;;
                esac
            done
            build_dev $no_cache
            ;;
        "build-prod")
            build_dev "false"
            ;;
        "build-hot")
            build_hot
            ;;
        "verify")
            local service=""
            for arg in "$@"; do
                case $arg in
                    --frontend) service="frontend" ;;
                    --backend) service="backend" ;;
                esac
            done
            verify_changes $service
            ;;
        "monitor")
            monitor_builds
            ;;
        "clean")
            clean_docker
            ;;
        "status")
            show_status
            ;;
        "logs")
            local follow="false"
            local service=""
            for arg in "$@"; do
                case $arg in
                    --follow) follow="true" ;;
                    --frontend) service="frontend" ;;
                    --backend) service="backend" ;;
                esac
            done
            show_logs $follow $service
            ;;
        "restart")
            restart_containers
            ;;
        "health")
            check_health
            ;;
        "test")
            run_tests
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            print_status "ERROR" "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
