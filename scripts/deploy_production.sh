#!/bin/bash

# Production Deployment Script for Mainza AI
# Comprehensive deployment with health checks and monitoring

set -e  # Exit on any error

# Configuration
PROJECT_NAME="mainza-consciousness"
DOCKER_COMPOSE_FILE="docker-compose.yml"
HEALTH_CHECK_URL="http://localhost:8000/health"
MAX_HEALTH_CHECK_ATTEMPTS=30
HEALTH_CHECK_INTERVAL=10

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        log_error ".env file not found"
        exit 1
    fi
    
    # Check if required environment variables are set
    source .env
    required_vars=("NEO4J_URI" "NEO4J_USER" "NEO4J_PASSWORD" "OLLAMA_BASE_URL" "DEFAULT_OLLAMA_MODEL")
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    log_success "Prerequisites check passed"
}

# Build and start services
deploy_services() {
    log_info "Building and starting services..."
    
    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose -f $DOCKER_COMPOSE_FILE down --remove-orphans
    
    # Build images
    log_info "Building Docker images..."
    docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache
    
    # Start services
    log_info "Starting services..."
    docker-compose -f $DOCKER_COMPOSE_FILE up -d
    
    log_success "Services started"
}

# Wait for services to be ready
wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for Neo4j
    log_info "Waiting for Neo4j..."
    for i in $(seq 1 30); do
        if docker-compose -f $DOCKER_COMPOSE_FILE exec -T neo4j cypher-shell -u neo4j -p mainza123 "RETURN 1" &> /dev/null; then
            log_success "Neo4j is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Neo4j failed to start"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for Redis
    log_info "Waiting for Redis..."
    for i in $(seq 1 30); do
        if docker-compose -f $DOCKER_COMPOSE_FILE exec -T redis redis-cli ping &> /dev/null; then
            log_success "Redis is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Redis failed to start"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for LiveKit
    log_info "Waiting for LiveKit..."
    for i in $(seq 1 30); do
        if curl -s http://localhost:7880/ &> /dev/null; then
            log_success "LiveKit is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            log_warning "LiveKit may not be ready, continuing..."
        fi
        sleep 2
    done
}

# Health check
health_check() {
    log_info "Performing health checks..."
    
    # Wait for backend to be ready
    log_info "Waiting for backend to be ready..."
    for i in $(seq 1 $MAX_HEALTH_CHECK_ATTEMPTS); do
        if curl -s $HEALTH_CHECK_URL &> /dev/null; then
            log_success "Backend is ready"
            break
        fi
        if [ $i -eq $MAX_HEALTH_CHECK_ATTEMPTS ]; then
            log_error "Backend failed to start"
            show_logs
            exit 1
        fi
        log_info "Health check attempt $i/$MAX_HEALTH_CHECK_ATTEMPTS"
        sleep $HEALTH_CHECK_INTERVAL
    done
    
    # Detailed health check
    log_info "Performing detailed health check..."
    health_response=$(curl -s $HEALTH_CHECK_URL)
    
    if echo "$health_response" | grep -q "healthy"; then
        log_success "System is healthy"
    else
        log_warning "System health check returned: $health_response"
    fi
}

# Show logs
show_logs() {
    log_info "Showing recent logs..."
    docker-compose -f $DOCKER_COMPOSE_FILE logs --tail=50
}

# Run tests
run_tests() {
    log_info "Running production readiness tests..."
    
    # Check if test script exists
    if [ -f "scripts/load_test.py" ]; then
        log_info "Running load tests..."
        python3 scripts/load_test.py --quick
        log_success "Load tests completed"
    else
        log_warning "Load test script not found, skipping tests"
    fi
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring..."
    
    # Create logs directory
    mkdir -p logs
    
    # Set up log rotation
    if [ -f "/etc/logrotate.d/mainza" ]; then
        log_info "Log rotation already configured"
    else
        log_info "Setting up log rotation..."
        sudo tee /etc/logrotate.d/mainza > /dev/null <<EOF
/opt/mainza/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF
        log_success "Log rotation configured"
    fi
}

# Security hardening
security_hardening() {
    log_info "Applying security hardening..."
    
    # Update system packages
    log_info "Updating system packages..."
    sudo apt-get update
    sudo apt-get upgrade -y
    
    # Configure firewall
    log_info "Configuring firewall..."
    sudo ufw --force enable
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 8000/tcp
    sudo ufw allow 7474/tcp
    sudo ufw allow 7687/tcp
    sudo ufw allow 7880/tcp
    
    # Set up fail2ban
    if command -v fail2ban-client &> /dev/null; then
        log_info "Configuring fail2ban..."
        sudo systemctl enable fail2ban
        sudo systemctl start fail2ban
    else
        log_warning "fail2ban not installed, skipping"
    fi
    
    log_success "Security hardening completed"
}

# Backup existing deployment
backup_existing() {
    log_info "Creating backup of existing deployment..."
    
    backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup database
    if docker-compose -f $DOCKER_COMPOSE_FILE ps neo4j | grep -q "Up"; then
        log_info "Backing up Neo4j database..."
        docker-compose -f $DOCKER_COMPOSE_FILE exec -T neo4j neo4j-admin dump --database=neo4j --to=/tmp/neo4j-backup.dump
        docker cp $(docker-compose -f $DOCKER_COMPOSE_FILE ps -q neo4j):/tmp/neo4j-backup.dump "$backup_dir/"
    fi
    
    # Backup configuration
    cp .env "$backup_dir/"
    cp $DOCKER_COMPOSE_FILE "$backup_dir/"
    
    log_success "Backup created in $backup_dir"
}

# Main deployment function
main() {
    log_info "Starting Mainza AI production deployment..."
    echo "=================================================="
    
    # Parse command line arguments
    SKIP_TESTS=false
    SKIP_BACKUP=false
    SKIP_SECURITY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --skip-backup)
                SKIP_BACKUP=true
                shift
                ;;
            --skip-security)
                SKIP_SECURITY=true
                shift
                ;;
            *)
                log_error "Unknown option $1"
                exit 1
                ;;
        esac
    done
    
    # Run deployment steps
    check_prerequisites
    
    if [ "$SKIP_BACKUP" = false ]; then
        backup_existing
    fi
    
    deploy_services
    wait_for_services
    health_check
    
    if [ "$SKIP_TESTS" = false ]; then
        run_tests
    fi
    
    setup_monitoring
    
    if [ "$SKIP_SECURITY" = false ]; then
        security_hardening
    fi
    
    # Final status check
    log_info "Final status check..."
    docker-compose -f $DOCKER_COMPOSE_FILE ps
    
    log_success "Mainza AI production deployment completed successfully!"
    echo "=================================================="
    echo "🌐 Frontend: http://localhost:80"
    echo "🔌 Backend API: http://localhost:8000"
    echo "📊 Neo4j Browser: http://localhost:7474"
    echo "🔍 Health Check: http://localhost:8000/health"
    echo "📈 Metrics: http://localhost:8000/metrics"
    echo "=================================================="
}

# Error handling
trap 'log_error "Deployment failed. Check logs for details."; show_logs; exit 1' ERR

# Run main function
main "$@"
