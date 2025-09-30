# Docker Container Debugging Fixes & Lessons Learned

## Overview
This document captures the debugging process and fixes applied to resolve critical issues in the Mainza Consciousness system's Docker containerized environment.

## Issues Resolved

### 1. Neo4j Vector Index Syntax Error

#### Problem
```
ERROR: Neo.ClientError.Statement.SyntaxError: WITH is required between FOREACH and MATCH
```

#### Root Cause
- Neo4j doesn't support parameterized index names in `CREATE VECTOR INDEX` statements
- The `create_vector_index()` function from `neo4j_graphrag` was generating parameterized queries with `$name` and `$dimensions`
- Neo4j requires direct string interpolation for index names

#### Solution Applied
**File**: `backend/utils/optimized_vector_embeddings.py`

**Before**:
```python
create_vector_index(
    self.driver,
    index_name,
    label=label,
    embedding_property=embedding_property,
    dimensions=dimensions,
    similarity_fn=similarity_fn
)
```

**After**:
```python
# Create vector index with direct Cypher query
cypher = f"""
CREATE VECTOR INDEX {index_name} IF NOT EXISTS
FOR (n:{label})
ON (n.{embedding_property})
OPTIONS {{
    indexConfig: {{
        `vector.dimensions`: {dimensions},
        `vector.similarity_function`: '{similarity_fn}'
    }}
}}
"""
```

#### Additional Fix: Vector Dimensions
- **Issue**: Neo4j vector dimensions must be between 1-2048, but we were using 1536 and 3072
- **Solution**: Standardized all vector indexes to 768 dimensions

### 2. Redis Connection Configuration Error

#### Problem
```
ERROR: Error 111 connecting to localhost:6379. Connection refused.
```

#### Root Cause
- `RedisCache` class in `backend/core/performance_optimization.py` had hardcoded `localhost:6379` fallback
- Docker containers need to use service names instead of localhost
- Environment variable `REDIS_URL=redis://redis:6379` was set but not being used

#### Solution Applied
**File**: `backend/core/performance_optimization.py`

**Before**:
```python
def __init__(self, redis_url: str = "redis://localhost:6379", default_ttl: int = 3600):
    self.redis_url = redis_url
```

**After**:
```python
def __init__(self, redis_url: str = None, default_ttl: int = 3600):
    import os
    self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://redis:6379')
```

### 3. Ollama Integration Issues

#### Problem
```
ModuleNotFoundError: No module named 'ollama'
```

#### Root Cause
- `ollama` package was missing from `requirements-docker.txt`
- System was trying to use OpenAI embeddings instead of Ollama

#### Solution Applied
1. **Added to `requirements-docker.txt`**:
   ```
   ollama>=0.1.0
   ```

2. **Created Custom OllamaEmbeddings Class**:
   ```python
   class OllamaEmbeddings:
       def __init__(self, model: str, base_url: str = None):
           self.model = model
           self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
           self.client = ollama.Client(host=self.base_url)
   ```

3. **Updated Vector Embeddings to Use Ollama**:
   ```python
   # Primary model for general embeddings using Ollama
   self.embedding_models["primary"] = OllamaEmbeddings(
       model=default_model,
       base_url=ollama_base_url
   )
   ```

## Key Lessons Learned

### 1. Docker Container Debugging Strategy

#### Always Check Environment Variables
```bash
docker exec container_name env | grep REDIS
```

#### Verify Container Network Connectivity
- Use service names instead of localhost in Docker Compose
- Check `docker-compose.yml` for correct service names
- Verify network configuration

#### Rebuild Strategy
- Use `docker-compose build --no-cache` for clean builds
- Restart containers after code changes
- Check logs with `docker-compose logs service_name --tail=20`

### 2. Neo4j Best Practices

#### Vector Index Creation
- Never use parameterized queries for index names
- Always use direct string interpolation
- Check dimension limits (1-2048 for Neo4j)
- Use `IF NOT EXISTS` to prevent conflicts

#### Cypher Query Debugging
- Test queries in Neo4j Browser first
- Use proper syntax for complex operations
- Include `WITH` clauses between `FOREACH` and `MATCH`

### 3. Redis Configuration in Docker

#### Environment Variable Priority
1. Explicit parameter passed to constructor
2. Environment variable (`REDIS_URL`)
3. Docker service name fallback (`redis:6379`)

#### Connection String Format
```
redis://service_name:port
```

### 4. Dependency Management

#### Requirements Files
- Always update `requirements-docker.txt` for Docker builds
- Include version constraints for stability
- Rebuild containers after dependency changes

#### Package Installation Order
1. System dependencies first
2. Python packages second
3. Test connections after installation

## Debugging Commands Used

### Container Status
```bash
docker-compose ps
docker-compose logs backend --tail=20
```

### Environment Verification
```bash
docker exec mainza-backend env | grep REDIS
docker exec mainza-backend python3 -c "import ollama; print('Ollama available')"
```

### Testing Endpoints
```bash
curl -X POST "http://localhost:8000/api/optimization/vector-embeddings" -H "accept: application/json"
```

### Clean Rebuild Process
```bash
docker-compose build --no-cache backend
docker-compose up -d backend
```

## Prevention Strategies

### 1. Code Review Checklist
- [ ] No hardcoded localhost URLs in Docker environments
- [ ] Environment variables used consistently
- [ ] Neo4j queries use proper syntax
- [ ] Dependencies listed in requirements files

### 2. Testing Protocol
- [ ] Test all endpoints after container rebuild
- [ ] Verify environment variables in running containers
- [ ] Check logs for connection errors
- [ ] Test external service connectivity

### 3. Documentation Updates
- [ ] Update README with Docker setup instructions
- [ ] Document environment variable requirements
- [ ] Include troubleshooting section
- [ ] Maintain debugging command reference

## Files Modified

### Core System Files
- `backend/utils/optimized_vector_embeddings.py` - Fixed Neo4j vector index creation
- `backend/core/performance_optimization.py` - Fixed Redis connection configuration
- `requirements-docker.txt` - Added missing dependencies

### Configuration Files
- `docker-compose.yml` - Already had correct `REDIS_URL=redis://redis:6379`
- `.env` - Contains proper Ollama configuration

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Neo4j Vector Index | ✅ Fixed | Direct Cypher queries, correct dimensions |
| Redis Connection | ✅ Fixed | Uses Docker service name |
| Ollama Integration | ✅ Fixed | Custom embeddings class, proper dependencies |
| Docker Containers | ✅ Working | Clean rebuild completed |
| Backend Startup | ✅ Working | ~4 minute startup time as expected |

## Next Steps

1. **Monitor System Performance**: Watch for any remaining connection issues
2. **Test Full Optimization**: Run complete optimization suite to verify all components
3. **Update Documentation**: Ensure all setup instructions are current
4. **Create Monitoring**: Add health checks for external service dependencies

## Conclusion

The debugging process revealed several critical issues in the Docker containerized environment. The key was systematic investigation of each component (Neo4j, Redis, Ollama) and understanding how they interact in a containerized environment. The fixes ensure proper service communication and eliminate hardcoded localhost references that don't work in Docker networks.

All major issues have been resolved, and the system is now running successfully with proper service-to-service communication.
