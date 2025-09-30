# Mainza Consciousness System - Troubleshooting Guide

## Common Issues & Solutions

### 1. Neo4j Vector Index Errors

#### Error: `WITH is required between FOREACH and MATCH`
**Cause**: Neo4j syntax error in Cypher queries
**Solution**: Add `WITH` clause between `FOREACH` and `MATCH` statements

```cypher
// WRONG
FOREACH (item IN items |
    MATCH (n:Node)
)

// CORRECT
FOREACH (item IN items |
    WITH item
    MATCH (n:Node)
)
```

#### Error: `vector.dimensions must be between 1 and 2048`
**Cause**: Vector dimensions exceed Neo4j limits
**Solution**: Use dimensions ≤ 2048 (recommended: 768)

```python
# WRONG
dimensions=3072

# CORRECT
dimensions=768
```

#### Error: `There is no procedure with the name 'gds.wcc.stream'`
**Cause**: Neo4j Graph Data Science (GDS) plugin not installed
**Solution**: Install GDS plugin or use alternative queries

### 2. Redis Connection Issues

#### Error: `Error 111 connecting to localhost:6379. Connection refused.`
**Cause**: Using localhost instead of Docker service name
**Solution**: Use `redis://redis:6379` in Docker environment

```python
# WRONG
redis_url = "redis://localhost:6379"

# CORRECT
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
```

#### Error: `Redis connection failed`
**Cause**: Redis container not running or network issues
**Solution**: 
1. Check Redis container: `docker-compose ps`
2. Restart Redis: `docker-compose restart redis`
3. Check network: `docker network ls`

### 3. Ollama Integration Issues

#### Error: `ModuleNotFoundError: No module named 'ollama'`
**Cause**: Ollama package not installed in Docker container
**Solution**: Add to `requirements-docker.txt`:
```
ollama>=0.1.0
```

#### Error: `OpenAI API key required`
**Cause**: System trying to use OpenAI instead of Ollama
**Solution**: Use custom OllamaEmbeddings class:
```python
class OllamaEmbeddings:
    def __init__(self, model: str, base_url: str = None):
        self.model = model
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL')
        self.client = ollama.Client(host=self.base_url)
```

### 4. Docker Container Issues

#### Error: `Container keeps restarting`
**Cause**: Application errors preventing startup
**Solution**: 
1. Check logs: `docker-compose logs backend --tail=50`
2. Check environment variables: `docker exec mainza-backend env`
3. Rebuild container: `docker-compose build --no-cache backend`

#### Error: `Port already in use`
**Cause**: Port conflicts with existing services
**Solution**: 
1. Stop conflicting services
2. Change ports in `docker-compose.yml`
3. Use `docker-compose down` then `docker-compose up`

#### Error: `Build failed`
**Cause**: Missing dependencies or syntax errors
**Solution**:
1. Check `requirements-docker.txt` for missing packages
2. Verify Dockerfile syntax
3. Use `docker-compose build --no-cache` for clean build

### 5. Backend Startup Issues

#### Error: `Backend takes too long to start`
**Cause**: Normal behavior - backend needs 4+ minutes to fully initialize
**Solution**: Wait patiently, check logs for progress

#### Error: `Optimization systems not available`
**Cause**: Missing dependencies or initialization errors
**Solution**:
1. Check all required packages installed
2. Verify Redis and Neo4j connections
3. Check environment variables

## Debugging Commands

### Container Management
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs [service_name] --tail=20

# Restart specific service
docker-compose restart [service_name]

# Rebuild and restart
docker-compose build --no-cache [service_name]
docker-compose up -d [service_name]
```

### Environment Verification
```bash
# Check environment variables
docker exec mainza-backend env | grep -E "(REDIS|OLLAMA|NEO4J)"

# Test Redis connection
docker exec mainza-backend python3 -c "import redis; r=redis.from_url('redis://redis:6379'); print(r.ping())"

# Test Ollama connection
docker exec mainza-backend python3 -c "import ollama; print('Ollama available')"

# Test Neo4j connection
docker exec mainza-backend python3 -c "from neo4j import GraphDatabase; print('Neo4j driver available')"
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test optimization endpoints
curl -X POST "http://localhost:8000/api/optimization/status" -H "accept: application/json"
curl -X POST "http://localhost:8000/api/optimization/vector-embeddings" -H "accept: application/json"
```

## Performance Monitoring

### Check System Resources
```bash
# Container resource usage
docker stats

# Disk usage
docker system df

# Memory usage
docker exec mainza-backend free -h
```

### Monitor Logs
```bash
# Follow logs in real-time
docker-compose logs -f backend

# Filter for errors
docker-compose logs backend | grep ERROR

# Filter for warnings
docker-compose logs backend | grep WARNING
```

## Recovery Procedures

### Complete System Reset
```bash
# Stop all containers
docker-compose down

# Remove volumes (WARNING: Data loss)
docker-compose down -v

# Rebuild everything
docker-compose build --no-cache

# Start fresh
docker-compose up -d
```

### Partial Reset (Keep Data)
```bash
# Stop containers
docker-compose down

# Rebuild specific service
docker-compose build --no-cache backend

# Start with data intact
docker-compose up -d
```

### Data Backup
```bash
# Backup Neo4j data
docker exec mainza-neo4j neo4j-admin dump --database=neo4j --to=/tmp/backup.dump
docker cp mainza-neo4j:/tmp/backup.dump ./neo4j-backup.dump

# Backup Redis data
docker exec mainza-redis redis-cli BGSAVE
```

## Prevention Tips

### 1. Environment Setup
- Always use environment variables for configuration
- Never hardcode localhost URLs in Docker environments
- Use service names for inter-container communication

### 2. Dependency Management
- Keep `requirements-docker.txt` updated
- Test new dependencies in development first
- Use version constraints for stability

### 3. Monitoring
- Set up health checks for all services
- Monitor resource usage regularly
- Keep logs for debugging purposes

### 4. Documentation
- Document all configuration changes
- Keep troubleshooting guides updated
- Maintain runbook for common procedures

## Emergency Contacts

### System Administrators
- Primary: [Contact Info]
- Secondary: [Contact Info]

### Service Status
- Neo4j: http://localhost:7474
- Redis: localhost:6379
- Backend API: http://localhost:8000
- Frontend: http://localhost:80

---
*Last Updated: $(date)*
*Version: 1.0*
