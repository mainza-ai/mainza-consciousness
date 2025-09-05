# Memory System Troubleshooting Guide

## Overview

This guide provides comprehensive troubleshooting procedures for the Mainza AI Memory System, covering common issues, diagnostic procedures, and resolution steps.

## Quick Diagnostic Commands

### System Health Check
```bash
# Basic health check
curl http://localhost:8000/health

# Memory system specific health
curl http://localhost:8000/api/memory-system/health

# Detailed diagnostics
curl http://localhost:8000/api/memory-system/diagnostics
```

### Performance Metrics
```bash
# Get performance metrics
curl http://localhost:8000/api/memory-system/metrics

# Get usage statistics
curl http://localhost:8000/api/memory-system/usage

# Check monitoring status
curl http://localhost:8000/api/memory-system/monitoring/status
```

### Component Status
```bash
# Check lifecycle management
curl http://localhost:8000/api/memory-system/lifecycle/status

# Validate memory integrity
curl -X POST http://localhost:8000/api/memory-system/admin/validate

# Get system statistics
curl http://localhost:8000/api/memory-system/statistics/overview
```

## Common Issues and Solutions

### 1. Memory System Not Starting

**Symptoms:**
- Application starts but memory system is disabled
- Error messages about memory system initialization
- Health check shows memory system as unavailable

**Diagnostic Steps:**
```bash
# Check environment configuration
grep MEMORY_ .env

# Test configuration validation
conda run -n mainza python test_memory_config.py

# Check Neo4j connectivity
conda run -n mainza python -c "
from backend.utils.neo4j_enhanced import neo4j_manager
print('Neo4j connection test:', neo4j_manager.test_connection())
"
```

**Common Causes and Solutions:**

1. **Missing Environment Variables**
   ```bash
   # Add missing variables to .env
   echo "MEMORY_SYSTEM_ENABLED=true" >> .env
   echo "NEO4J_PASSWORD=your_password" >> .env
   ```

2. **Neo4j Connection Issues**
   ```bash
   # Check Neo4j status
   systemctl status neo4j
   
   # Test connection manually
   cypher-shell -u neo4j -p your_password "RETURN 1"
   
   # Restart Neo4j if needed
   sudo systemctl restart neo4j
   ```

3. **Schema Not Initialized**
   ```bash
   # Apply memory schema
   cypher-shell -u neo4j -p your_password -f backend/neo4j/memory_schema.cypher
   ```

### 2. Poor Memory Search Performance

**Symptoms:**
- Slow response times for memory searches
- Timeouts on memory retrieval operations
- High CPU usage during memory operations

**Diagnostic Steps:**
```bash
# Check performance metrics
curl http://localhost:8000/api/memory-system/metrics

# Run performance diagnostics
curl http://localhost:8000/api/memory-system/diagnostics

# Check Neo4j query performance
cypher-shell -u neo4j -p password "
CALL db.stats.retrieve('GRAPH COUNTS') YIELD data
RETURN data
"
```

**Solutions:**

1. **Optimize Similarity Threshold**
   ```bash
   # Increase threshold for more precise results
   # Edit .env file
   MEMORY_SIMILARITY_THRESHOLD=0.5  # Increase from 0.3
   ```

2. **Reduce Retrieval Limit**
   ```bash
   # Limit number of results
   MEMORY_RETRIEVAL_LIMIT=5  # Reduce from 10
   ```

3. **Neo4j Performance Tuning**
   ```bash
   # Edit /etc/neo4j/neo4j.conf
   dbms.memory.heap.max_size=4g
   dbms.memory.pagecache.size=2g
   
   # Restart Neo4j
   sudo systemctl restart neo4j
   ```

4. **Create Missing Indexes**
   ```cypher
   // Create indexes for better performance
   CREATE INDEX memory_user_idx FOR (m:Memory) ON (m.user_id);
   CREATE INDEX memory_type_idx FOR (m:Memory) ON (m.memory_type);
   CREATE INDEX memory_created_idx FOR (m:Memory) ON (m.created_at);
   ```

### 3. Memory Storage Failures

**Symptoms:**
- Errors when creating new memories
- "Memory storage failed" in logs
- Inconsistent memory creation

**Diagnostic Steps:**
```bash
# Check storage engine health
curl http://localhost:8000/api/memory-system/health | jq '.data.components.storage'

# Test memory creation
curl -X POST http://localhost:8000/api/memory-system/memories/create \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Test memory",
    "memory_type": "test",
    "user_id": "test_user",
    "agent_name": "test_agent"
  }'

# Check Neo4j write permissions
cypher-shell -u neo4j -p password "
CREATE (test:TestNode {id: 'test'})
DELETE test
RETURN 'Write test successful'
"
```

**Solutions:**

1. **Check Disk Space**
   ```bash
   # Check available disk space
   df -h
   
   # Check Neo4j data directory
   du -sh /var/lib/neo4j/data/
   ```

2. **Verify Neo4j Permissions**
   ```bash
   # Check Neo4j user permissions
   ls -la /var/lib/neo4j/data/
   
   # Fix permissions if needed
   sudo chown -R neo4j:neo4j /var/lib/neo4j/
   ```

3. **Check Memory System Configuration**
   ```bash
   # Verify batch size isn't too large
   grep MEMORY_STORAGE_BATCH_SIZE .env
   
   # Reduce if necessary
   MEMORY_STORAGE_BATCH_SIZE=50
   ```

### 4. Embedding Generation Issues

**Symptoms:**
- Memories created without embeddings
- Search results are poor or empty
- Embedding-related errors in logs

**Diagnostic Steps:**
```bash
# Check embedding statistics
curl http://localhost:8000/api/memory-system/admin/validate | jq '.data.memories_without_embeddings'

# Test embedding generation
conda run -n mainza python -c "
from backend.utils.embedding_enhanced import embedding_manager
result = embedding_manager.generate_embedding('test text')
print('Embedding test:', 'SUCCESS' if result else 'FAILED')
"
```

**Solutions:**

1. **Check Ollama Service**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if needed
   ollama serve &
   ```

2. **Verify Embedding Model**
   ```bash
   # Check if embedding model is available
   ollama list | grep embed
   
   # Pull embedding model if missing
   ollama pull nomic-embed-text:latest
   ```

3. **Regenerate Missing Embeddings**
   ```bash
   # Reindex all memories
   curl -X POST http://localhost:8000/api/memory-system/admin/reindex
   ```

### 5. Memory Cleanup Issues

**Symptoms:**
- Memory storage growing without bounds
- Cleanup operations failing
- Old memories not being removed

**Diagnostic Steps:**
```bash
# Check lifecycle management status
curl http://localhost:8000/api/memory-system/lifecycle/status

# Check usage statistics
curl http://localhost:8000/api/memory-system/usage

# Check cleanup configuration
grep CLEANUP .env
```

**Solutions:**

1. **Enable Automatic Cleanup**
   ```bash
   # Enable in .env file
   MEMORY_AUTO_CLEANUP_ENABLED=true
   MEMORY_CLEANUP_INTERVAL_HOURS=24
   ```

2. **Manual Cleanup**
   ```bash
   # Run manual cleanup
   curl -X POST http://localhost:8000/api/memory-system/lifecycle/cleanup
   
   # Run maintenance tasks
   curl -X POST http://localhost:8000/api/memory-system/lifecycle/maintenance
   ```

3. **Adjust Cleanup Thresholds**
   ```bash
   # Configure lifecycle management
   curl -X PUT http://localhost:8000/api/memory-system/lifecycle/configure \
     -H "Content-Type: application/json" \
     -d '{
       "min_importance_threshold": 0.2,
       "max_memory_age_days": 180
     }'
   ```

### 6. Consciousness Integration Issues

**Symptoms:**
- Memories not reflecting consciousness state
- Consciousness-aware search not working
- Missing consciousness context in memories

**Diagnostic Steps:**
```bash
# Check consciousness system status
curl http://localhost:8000/health | jq '.components.consciousness'

# Check memory consciousness levels
curl http://localhost:8000/api/memory-system/statistics/overview | jq '.data.consciousness_levels'
```

**Solutions:**

1. **Verify Consciousness System**
   ```bash
   # Check consciousness orchestrator
   conda run -n mainza python -c "
   from backend.utils.consciousness_orchestrator import consciousness_orchestrator
   print('Consciousness active:', consciousness_orchestrator.is_running if consciousness_orchestrator else False)
   "
   ```

2. **Update Memory Creation**
   ```bash
   # Ensure consciousness context is passed
   # Check agent implementations for proper context passing
   grep -r "consciousness_context" backend/agents/
   ```

### 7. API Endpoint Issues

**Symptoms:**
- 500 errors on memory system endpoints
- Endpoints returning empty results
- Authentication or permission errors

**Diagnostic Steps:**
```bash
# Test each endpoint category
curl http://localhost:8000/api/memory-system/health
curl http://localhost:8000/api/memory-system/metrics
curl http://localhost:8000/api/memory-system/usage

# Check application logs
tail -f backend/uvicorn.log | grep "memory-system"
```

**Solutions:**

1. **Check Router Registration**
   ```bash
   # Verify memory system router is included
   grep -n "memory_system_router" backend/main.py
   ```

2. **Verify Dependencies**
   ```bash
   # Test component imports
   conda run -n mainza python test_memory_api_endpoints.py
   ```

3. **Check Permissions**
   ```bash
   # Ensure proper file permissions
   ls -la backend/routers/memory_system.py
   ls -la backend/utils/memory_*.py
   ```

## Performance Optimization

### Memory System Tuning

1. **Adjust Similarity Thresholds**
   ```bash
   # For more precise results (fewer but more relevant)
   MEMORY_SIMILARITY_THRESHOLD=0.5
   
   # For broader results (more but less precise)
   MEMORY_SIMILARITY_THRESHOLD=0.2
   ```

2. **Optimize Batch Sizes**
   ```bash
   # For high-throughput systems
   MEMORY_STORAGE_BATCH_SIZE=200
   
   # For memory-constrained systems
   MEMORY_STORAGE_BATCH_SIZE=50
   ```

3. **Configure Monitoring Frequency**
   ```bash
   # For production systems (less frequent monitoring)
   MEMORY_HEALTH_CHECK_INTERVAL_MINUTES=10
   
   # For development (more frequent monitoring)
   MEMORY_HEALTH_CHECK_INTERVAL_MINUTES=2
   ```

### Neo4j Optimization

1. **Memory Configuration**
   ```bash
   # Edit /etc/neo4j/neo4j.conf
   dbms.memory.heap.initial_size=2g
   dbms.memory.heap.max_size=4g
   dbms.memory.pagecache.size=2g
   ```

2. **Query Optimization**
   ```cypher
   // Create compound indexes for common queries
   CREATE INDEX memory_user_type_idx FOR (m:Memory) ON (m.user_id, m.memory_type);
   CREATE INDEX memory_importance_created_idx FOR (m:Memory) ON (m.importance_score, m.created_at);
   ```

## Log Analysis

### Key Log Patterns

1. **Successful Operations**
   ```bash
   grep "Memory system.*initialized\|Memory.*stored\|Memory.*retrieved" backend/uvicorn.log
   ```

2. **Error Patterns**
   ```bash
   grep -i "memory.*error\|memory.*failed\|memory.*exception" backend/uvicorn.log
   ```

3. **Performance Issues**
   ```bash
   grep "Memory.*slow\|Memory.*timeout\|Memory.*performance" backend/uvicorn.log
   ```

4. **Health Check Results**
   ```bash
   grep "Memory system health check\|Memory.*health.*" backend/uvicorn.log
   ```

### Log Rotation Setup

```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/mainza-memory << 'EOF'
/path/to/mainza/backend/uvicorn.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 user group
    postrotate
        pkill -USR1 -f "uvicorn.*main:app"
    endscript
}
EOF
```

## Emergency Procedures

### Memory System Recovery

1. **Complete System Reset**
   ```bash
   # Stop all services
   pkill -f "python backend/main.py"
   sudo systemctl stop neo4j
   
   # Clear memory system data (CAUTION: This deletes all memories)
   cypher-shell -u neo4j -p password "MATCH (m:Memory) DETACH DELETE m"
   
   # Restart services
   sudo systemctl start neo4j
   conda run -n mainza python backend/main.py &
   ```

2. **Partial Recovery (Preserve Data)**
   ```bash
   # Stop memory system components only
   curl -X POST http://localhost:8000/api/memory-system/monitoring/stop
   curl -X POST http://localhost:8000/api/memory-system/lifecycle/stop
   
   # Restart components
   curl -X POST http://localhost:8000/api/memory-system/monitoring/start
   curl -X POST http://localhost:8000/api/memory-system/lifecycle/start
   ```

### Data Recovery

1. **Restore from Backup**
   ```bash
   # Stop services
   sudo systemctl stop neo4j
   
   # Restore database
   neo4j-admin restore --from=/backups/memory-system-backup --database=neo4j
   
   # Restart services
   sudo systemctl start neo4j
   ```

2. **Rebuild Indexes**
   ```bash
   # Reindex all memories
   curl -X POST http://localhost:8000/api/memory-system/admin/reindex
   
   # Validate integrity
   curl -X POST http://localhost:8000/api/memory-system/admin/validate
   ```

## Monitoring and Alerting

### Health Check Automation

```bash
# Create health check script
cat > /usr/local/bin/memory-health-check.sh << 'EOF'
#!/bin/bash
HEALTH_URL="http://localhost:8000/api/memory-system/health"
ALERT_EMAIL="admin@example.com"

RESPONSE=$(curl -s $HEALTH_URL)
STATUS=$(echo $RESPONSE | jq -r '.data.overall_status')

if [ "$STATUS" != "healthy" ]; then
    echo "Memory system health check failed: $STATUS" | mail -s "Memory System Alert" $ALERT_EMAIL
    echo "$(date): Memory system unhealthy - $STATUS" >> /var/log/memory-alerts.log
fi
EOF

chmod +x /usr/local/bin/memory-health-check.sh

# Add to crontab for regular checks
echo "*/5 * * * * /usr/local/bin/memory-health-check.sh" | crontab -
```

### Performance Monitoring

```bash
# Create performance monitoring script
cat > /usr/local/bin/memory-performance-check.sh << 'EOF'
#!/bin/bash
METRICS_URL="http://localhost:8000/api/memory-system/metrics"
THRESHOLD_MS=2000

RESPONSE=$(curl -s $METRICS_URL)
AVG_TIME=$(echo $RESPONSE | jq -r '.data.metrics.memory_retrieval.average_response_time')

if (( $(echo "$AVG_TIME > $THRESHOLD_MS" | bc -l) )); then
    echo "Memory system performance degraded: ${AVG_TIME}ms" | mail -s "Memory Performance Alert" $ALERT_EMAIL
fi
EOF
```

## Support Resources

### Documentation References
- Main Memory System Documentation: `docs/MEMORY_SYSTEM.md`
- Deployment Guide: `docs/MEMORY_SYSTEM_DEPLOYMENT.md`
- API Documentation: Available at `/api/memory-system/` endpoints

### Diagnostic Tools
- Configuration Validator: `test_memory_config.py`
- API Endpoint Tester: `test_memory_api_endpoints.py`
- Component Tests: `backend/tests/test_memory_*.py`

### Contact Information
For critical issues that cannot be resolved using this guide:
1. Check the main Mainza AI documentation
2. Review system logs for additional context
3. Contact the development team with specific error messages and diagnostic output

Remember to include the following information when reporting issues:
- System configuration (sanitized .env file)
- Error messages and stack traces
- Output from diagnostic commands
- Steps to reproduce the issue
- System resource usage (CPU, memory, disk)