# Memory System Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Mainza AI Memory System in production environments.

## Prerequisites

### System Requirements

- **Neo4j Database**: Version 4.4+ with APOC plugin
- **Python**: Version 3.8+ with conda environment
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: Minimum 10GB free space for memory data
- **Network**: Stable connection to Neo4j database

### Dependencies

Ensure the following Python packages are installed in your conda environment:

```bash
conda activate mainza
pip install neo4j sentence-transformers numpy fastapi uvicorn python-dotenv
```

## Pre-Deployment Checklist

### 1. Database Setup

Verify Neo4j is properly configured:

```bash
# Check Neo4j status
systemctl status neo4j

# Verify connection
cypher-shell -u neo4j -p your_password "RETURN 1"
```

### 2. Schema Initialization

Run the memory schema setup:

```bash
# Apply memory schema
cypher-shell -u neo4j -p your_password -f backend/neo4j/memory_schema.cypher
```

### 3. Environment Configuration

Create or update your `.env` file with memory system configuration:

```bash
# Copy example configuration
cp .env.example .env

# Edit memory system settings
nano .env
```

Required memory system variables:
```bash
MEMORY_SYSTEM_ENABLED=true
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_secure_password
MEMORY_STORAGE_BATCH_SIZE=100
MEMORY_RETRIEVAL_LIMIT=10
MEMORY_SIMILARITY_THRESHOLD=0.3
MEMORY_IMPORTANCE_DECAY_RATE=0.95
MEMORY_CLEANUP_INTERVAL_HOURS=24
MEMORY_MAX_STORAGE_SIZE_GB=10
MEMORY_HEALTH_CHECK_INTERVAL_MINUTES=5
MEMORY_PERFORMANCE_TRACKING_ENABLED=true
MEMORY_AUTO_CLEANUP_ENABLED=true
```

### 4. Validation Tests

Run pre-deployment validation:

```bash
# Test memory system configuration
conda run -n mainza python test_memory_config.py

# Test API endpoints
conda run -n mainza python test_memory_api_endpoints.py

# Run memory system tests
conda run -n mainza python -m pytest backend/tests/test_memory_*.py -v
```

## Deployment Steps

### Step 1: Backup Existing Data

Before deploying, backup your existing Neo4j database:

```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Create backup
neo4j-admin backup --backup-dir=/path/to/backup --name=pre-memory-deployment

# Restart Neo4j
sudo systemctl start neo4j
```

### Step 2: Deploy Application Code

```bash
# Pull latest code
git pull origin main

# Activate conda environment
conda activate mainza

# Install/update dependencies
pip install -r backend/requirements.txt
```

### Step 3: Initialize Memory System

```bash
# Run memory system initialization
conda run -n mainza python -c "
import asyncio
import sys
sys.path.append('backend')
from backend.utils.memory_system_monitor import memory_monitor
from backend.utils.memory_lifecycle_manager import memory_lifecycle_manager

async def init_memory_system():
    print('Initializing memory system...')
    
    # Initialize monitor
    monitor_init = await memory_monitor.initialize()
    print(f'Memory monitor initialized: {monitor_init}')
    
    # Initialize lifecycle manager
    lifecycle_init = await memory_lifecycle_manager.initialize()
    print(f'Memory lifecycle manager initialized: {lifecycle_init}')
    
    # Perform health check
    health = await memory_monitor.perform_health_check()
    print(f'Initial health status: {health.overall_status.value}')
    
    return monitor_init and lifecycle_init

success = asyncio.run(init_memory_system())
print(f'Memory system initialization: {\"SUCCESS\" if success else \"FAILED\"}')
"
```

### Step 4: Start Application Services

```bash
# Start the main application
conda run -n mainza python backend/main.py &

# Or use uvicorn directly
conda run -n mainza uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
```

### Step 5: Verify Deployment

```bash
# Check application health
curl http://localhost:8000/health

# Check memory system health
curl http://localhost:8000/api/memory-system/health

# Run diagnostics
curl http://localhost:8000/api/memory-system/diagnostics
```

## Post-Deployment Configuration

### 1. Monitoring Setup

Configure monitoring and alerting:

```bash
# Start memory system monitoring
curl -X POST http://localhost:8000/api/memory-system/monitoring/start

# Configure monitoring parameters
curl -X POST "http://localhost:8000/api/memory-system/monitoring/configure" \
  -H "Content-Type: application/json" \
  -d '{
    "health_check_interval": 300,
    "max_response_time": 2.0,
    "min_success_rate": 95.0,
    "max_storage_size_gb": 10.0
  }'
```

### 2. Lifecycle Management

Start automatic lifecycle management:

```bash
# Start lifecycle management
curl -X POST http://localhost:8000/api/memory-system/lifecycle/start

# Configure lifecycle parameters
curl -X PUT "http://localhost:8000/api/memory-system/lifecycle/configure" \
  -H "Content-Type: application/json" \
  -d '{
    "base_decay_rate": 0.95,
    "min_importance_threshold": 0.1,
    "max_memory_age_days": 365,
    "similarity_threshold": 0.8,
    "cleanup_batch_size": 100
  }'
```

### 3. Performance Tuning

Optimize performance based on your workload:

```bash
# Get current performance metrics
curl http://localhost:8000/api/memory-system/metrics

# Adjust configuration based on metrics
# Edit .env file and restart application if needed
```

## Production Considerations

### Security Configuration

1. **Database Security**
   ```bash
   # Secure Neo4j configuration
   # Edit /etc/neo4j/neo4j.conf
   dbms.security.auth_enabled=true
   dbms.connector.bolt.listen_address=127.0.0.1:7687
   dbms.connector.http.listen_address=127.0.0.1:7474
   ```

2. **API Security**
   - Configure authentication for memory system endpoints
   - Restrict admin endpoints to authorized users
   - Use HTTPS in production

3. **Data Privacy**
   - Configure memory retention policies
   - Implement data anonymization if required
   - Set up secure backup procedures

### Performance Optimization

1. **Neo4j Tuning**
   ```bash
   # Edit /etc/neo4j/neo4j.conf
   dbms.memory.heap.initial_size=2g
   dbms.memory.heap.max_size=4g
   dbms.memory.pagecache.size=2g
   ```

2. **Memory System Tuning**
   ```bash
   # Adjust based on usage patterns
   MEMORY_STORAGE_BATCH_SIZE=200
   MEMORY_RETRIEVAL_LIMIT=20
   MEMORY_SIMILARITY_THRESHOLD=0.4
   ```

3. **Monitoring Configuration**
   ```bash
   # Reduce monitoring frequency for high-load systems
   MEMORY_HEALTH_CHECK_INTERVAL_MINUTES=10
   ```

### Backup and Recovery

1. **Automated Backups**
   ```bash
   # Create backup script
   cat > /usr/local/bin/backup-memory-system.sh << 'EOF'
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="/backups/memory-system"
   
   # Create backup directory
   mkdir -p $BACKUP_DIR
   
   # Backup Neo4j database
   neo4j-admin backup --backup-dir=$BACKUP_DIR --name=memory-system-$DATE
   
   # Backup configuration
   cp /path/to/mainza/.env $BACKUP_DIR/env-$DATE
   
   # Cleanup old backups (keep last 7 days)
   find $BACKUP_DIR -name "memory-system-*" -mtime +7 -delete
   EOF
   
   chmod +x /usr/local/bin/backup-memory-system.sh
   
   # Add to crontab for daily backups
   echo "0 2 * * * /usr/local/bin/backup-memory-system.sh" | crontab -
   ```

2. **Recovery Procedures**
   ```bash
   # Stop services
   sudo systemctl stop neo4j
   pkill -f "python backend/main.py"
   
   # Restore from backup
   neo4j-admin restore --from=/backups/memory-system/memory-system-YYYYMMDD_HHMMSS --database=neo4j
   
   # Restart services
   sudo systemctl start neo4j
   conda run -n mainza python backend/main.py &
   ```

### Scaling Considerations

1. **Horizontal Scaling**
   - Use Neo4j clustering for database scaling
   - Deploy multiple application instances behind load balancer
   - Implement distributed memory caching if needed

2. **Vertical Scaling**
   - Increase memory allocation for Neo4j
   - Optimize batch sizes for memory operations
   - Use SSD storage for better I/O performance

## Troubleshooting

### Common Deployment Issues

1. **Memory System Not Starting**
   ```bash
   # Check logs
   tail -f backend/uvicorn.log | grep MEMORY
   
   # Verify Neo4j connection
   conda run -n mainza python -c "
   from backend.utils.neo4j_enhanced import neo4j_manager
   print('Neo4j connection:', neo4j_manager.test_connection())
   "
   ```

2. **Poor Performance**
   ```bash
   # Check memory system metrics
   curl http://localhost:8000/api/memory-system/metrics
   
   # Run diagnostics
   curl http://localhost:8000/api/memory-system/diagnostics
   
   # Check Neo4j performance
   cypher-shell -u neo4j -p password "CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Page cache')"
   ```

3. **Memory Storage Issues**
   ```bash
   # Check disk space
   df -h
   
   # Check Neo4j logs
   tail -f /var/log/neo4j/neo4j.log
   
   # Validate memory integrity
   curl -X POST http://localhost:8000/api/memory-system/admin/validate
   ```

### Health Check Commands

```bash
# Application health
curl http://localhost:8000/health

# Memory system health
curl http://localhost:8000/api/memory-system/health

# Detailed diagnostics
curl http://localhost:8000/api/memory-system/diagnostics

# Performance metrics
curl http://localhost:8000/api/memory-system/metrics

# Usage statistics
curl http://localhost:8000/api/memory-system/usage
```

### Log Analysis

Key log patterns to monitor:

```bash
# Memory system initialization
grep "Memory system.*initialized" backend/uvicorn.log

# Health check results
grep "Memory system health check" backend/uvicorn.log

# Performance issues
grep "Memory operation.*slow" backend/uvicorn.log

# Error patterns
grep "Memory.*failed\|Memory.*error" backend/uvicorn.log
```

## Rollback Procedures

If deployment issues occur:

1. **Stop New Services**
   ```bash
   pkill -f "python backend/main.py"
   ```

2. **Restore Previous Configuration**
   ```bash
   git checkout previous-commit
   cp backup/.env .env
   ```

3. **Restore Database if Needed**
   ```bash
   sudo systemctl stop neo4j
   neo4j-admin restore --from=/backups/pre-memory-deployment --database=neo4j
   sudo systemctl start neo4j
   ```

4. **Restart Previous Version**
   ```bash
   conda run -n mainza python backend/main.py &
   ```

## Maintenance Schedule

### Daily Tasks
- Monitor system health and performance
- Check error logs for issues
- Verify backup completion

### Weekly Tasks
- Review memory usage statistics
- Analyze performance trends
- Update configuration if needed

### Monthly Tasks
- Review and optimize cleanup policies
- Analyze memory system effectiveness
- Plan capacity upgrades if needed

### Quarterly Tasks
- Full system backup and recovery test
- Security audit and updates
- Performance optimization review

## Support and Documentation

For additional support:

- Review main documentation: `docs/MEMORY_SYSTEM.md`
- Check API documentation: `/api/memory-system/` endpoints
- Monitor system logs: `backend/uvicorn.log`
- Contact development team for critical issues

Remember to keep this deployment guide updated as the memory system evolves.