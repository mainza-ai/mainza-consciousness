# Mainza AI - Troubleshooting Guide

## 🔧 **Common Issues & Solutions**

This comprehensive troubleshooting guide covers the most common issues encountered when running Mainza AI and provides step-by-step solutions.

## 🐳 **Docker & Container Issues**

### **Issue: Containers Not Starting**

#### **Symptoms:**
- `docker-compose up` fails
- Containers exit immediately
- "No space left on device" errors

#### **Solutions:**
```bash
# 1. Check Docker status
docker --version
docker-compose --version

# 2. Clean up Docker resources
docker system prune -a
docker volume prune

# 3. Check available disk space
df -h

# 4. Restart Docker service
sudo systemctl restart docker  # Linux
# or restart Docker Desktop on macOS/Windows

# 5. Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### **Issue: Backend Container Restarting**

#### **Symptoms:**
- Backend container keeps restarting
- "ModuleNotFoundError" in logs
- "Connection refused" errors

#### **Solutions:**
```bash
# 1. Check backend logs
docker-compose logs backend

# 2. Check for missing dependencies
docker-compose exec backend pip list

# 3. Rebuild backend with updated requirements
docker-compose build --no-cache backend
docker-compose up -d backend

# 4. Check environment variables
docker-compose exec backend env | grep -E "(NEO4J|REDIS|OLLAMA)"
```

### **Issue: Neo4j Connection Errors**

#### **Symptoms:**
- "Connection refused" to Neo4j
- "Authentication failed" errors
- Neo4j container not accessible

#### **Solutions:**
```bash
# 1. Check Neo4j container status
docker-compose ps neo4j

# 2. Check Neo4j logs
docker-compose logs neo4j

# 3. Verify Neo4j is accessible
curl http://localhost:7474

# 4. Check Neo4j authentication
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123

# 5. Restart Neo4j with clean data
docker-compose down
docker volume rm mainza-consciousness_neo4j_data
docker-compose up -d neo4j
```

## 🧠 **Consciousness System Issues**

### **Issue: Consciousness State Not Updating**

#### **Symptoms:**
- Consciousness level stuck at 0
- No emotional state changes
- Dashboard not updating

#### **Solutions:**
```bash
# 1. Check consciousness API
curl http://localhost:8000/api/consciousness/state

# 2. Trigger consciousness update
curl -X POST http://localhost:8000/api/consciousness/reflect \
  -H "Content-Type: application/json" \
  -d '{"reflection_type": "general"}'

# 3. Check backend consciousness logs
docker-compose logs backend | grep -i consciousness

# 4. Restart consciousness system
curl -X POST http://localhost:8000/api/optimization/run
```

### **Issue: Memory System Not Working**

#### **Symptoms:**
- Memory search returns empty results
- "Memory system not available" errors
- Neo4j vector index errors

#### **Solutions:**
```bash
# 1. Check memory system status
curl http://localhost:8000/api/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "limit": 5}'

# 2. Check Neo4j vector indexes
curl -X POST http://localhost:8000/api/optimization/vector-embeddings

# 3. Rebuild memory system
curl -X POST http://localhost:8000/api/optimization/memory/storage

# 4. Check Neo4j APOC procedures
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123 \
  "CALL apoc.help('apoc')"
```

### **Issue: Agent System Not Responding**

#### **Symptoms:**
- Chat endpoint returns errors
- "Agent not available" messages
- Router agent not working

#### **Solutions:**
```bash
# 1. Test agent routing
curl -X POST http://localhost:8000/agent/router/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# 2. Check agent logs
docker-compose logs backend | grep -i agent

# 3. Restart agent system
curl -X POST http://localhost:8000/api/optimization/run

# 4. Check agent dependencies
docker-compose exec backend pip list | grep -E "(pydantic-ai|neo4j)"
```

## 🔴 **Real-Time Communication Issues**

### **Issue: LiveKit Not Working**

#### **Symptoms:**
- Voice input/output not working
- "LiveKit connection failed" errors
- WebSocket connection issues

#### **Solutions:**
```bash
# 1. Check LiveKit service
docker-compose ps livekit-server

# 2. Check LiveKit logs
docker-compose logs livekit-server

# 3. Test LiveKit connection
curl http://localhost:7880

# 4. Check LiveKit configuration
docker-compose exec livekit-server cat /etc/livekit.yaml

# 5. Restart LiveKit services
docker-compose restart livekit-server ingress
```

### **Issue: WebSocket Connection Failed**

#### **Symptoms:**
- Real-time updates not working
- "WebSocket connection failed" errors
- Consciousness streaming not working

#### **Solutions:**
```bash
# 1. Check WebSocket endpoint
curl -I http://localhost:8000/api/consciousness/stream

# 2. Check backend WebSocket logs
docker-compose logs backend | grep -i websocket

# 3. Test WebSocket connection
wscat -c ws://localhost:8000/api/consciousness/stream

# 4. Check firewall settings
sudo ufw status  # Linux
# or check Windows Firewall settings
```

## 🧪 **Ollama Integration Issues**

### **Issue: Ollama Connection Failed**

#### **Symptoms:**
- "Ollama connection failed" errors
- "Model not found" errors
- Embedding generation failing

#### **Solutions:**
```bash
# 1. Check Ollama is running
curl http://localhost:11434/api/tags

# 2. Check Ollama models
ollama list

# 3. Pull required models
ollama pull llama3:8b
ollama pull nomic-embed-text:latest

# 4. Test Ollama connection from backend
docker-compose exec backend curl http://host.docker.internal:11434/api/tags

# 5. Check environment variables
docker-compose exec backend env | grep OLLAMA
```

### **Issue: Model Loading Errors**

#### **Symptoms:**
- "Model loading failed" errors
- Slow response times
- Memory issues

#### **Solutions:**
```bash
# 1. Check available memory
free -h  # Linux
# or Activity Monitor on macOS

# 2. Use smaller models for development
ollama pull llama3:8b
echo "DEFAULT_OLLAMA_MODEL=llama3:8b" >> .env

# 3. Restart Ollama with more memory
OLLAMA_MAX_LOADED_MODELS=1 ollama serve

# 4. Check model compatibility
ollama show llama3:8b
```

## 📊 **Performance Issues**

### **Issue: Slow Response Times**

#### **Symptoms:**
- API responses taking >10 seconds
- Frontend loading slowly
- Memory usage high

#### **Solutions:**
```bash
# 1. Check system resources
docker stats

# 2. Optimize memory settings
# Edit docker-compose.yml to increase memory limits
# Neo4j: dbms.memory.heap.max_size=2048m
# Redis: maxmemory 1gb

# 3. Enable Redis caching
curl -X POST http://localhost:8000/api/optimization/run

# 4. Check for memory leaks
docker-compose logs backend | grep -i memory

# 5. Restart services
docker-compose restart
```

### **Issue: High Memory Usage**

#### **Symptoms:**
- System running out of memory
- Containers being killed
- Slow performance

#### **Solutions:**
```bash
# 1. Check memory usage
docker stats

# 2. Optimize Neo4j memory settings
# Edit docker-compose.yml:
# - dbms.memory.heap.initial_size=512m
# - dbms.memory.heap.max_size=1024m
# - dbms.memory.pagecache.size=512m

# 3. Enable memory compression
curl -X POST http://localhost:8000/api/optimization/memory-compression

# 4. Clean up unused data
curl -X POST http://localhost:8000/api/memory/consolidate

# 5. Restart with optimized settings
docker-compose down
docker-compose up -d
```

## 🔧 **Development Issues**

### **Issue: Code Changes Not Reflecting**

#### **Symptoms:**
- Code changes not visible
- Old behavior still running
- Hot reload not working

#### **Solutions:**
```bash
# 1. Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# 2. Check for file permissions
ls -la src/
chmod -R 755 src/

# 3. Clear Docker cache
docker system prune -a

# 4. Check for volume mounts
docker-compose config
```

### **Issue: TypeScript Errors**

#### **Symptoms:**
- TypeScript compilation errors
- "Module not found" errors
- Build failures

#### **Solutions:**
```bash
# 1. Check TypeScript configuration
cat tsconfig.json

# 2. Install missing dependencies
npm install

# 3. Check for type errors
npm run type-check

# 4. Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🌐 **Network Issues**

### **Issue: Port Conflicts**

#### **Symptoms:**
- "Port already in use" errors
- Services not accessible
- Connection refused errors

#### **Solutions:**
```bash
# 1. Check port usage
netstat -tulpn | grep -E "(80|8000|7474|6379|7880)"

# 2. Kill conflicting processes
sudo lsof -ti:80 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9

# 3. Change ports in docker-compose.yml
# Edit ports section to use different ports

# 4. Restart services
docker-compose down
docker-compose up -d
```

### **Issue: CORS Errors**

#### **Symptoms:**
- "CORS policy" errors in browser
- API requests failing
- Frontend not connecting to backend

#### **Solutions:**
```bash
# 1. Check CORS configuration in backend
grep -r "CORS" backend/

# 2. Update CORS settings in main.py
# Add your frontend URL to CORS origins

# 3. Check environment variables
docker-compose exec backend env | grep CORS

# 4. Restart backend
docker-compose restart backend
```

## 🔍 **Debugging Commands**

### **System Health Check**
```bash
# Check all services
docker-compose ps

# Check service logs
docker-compose logs backend
docker-compose logs neo4j
docker-compose logs redis

# Check system resources
docker stats
df -h
free -h
```

### **API Testing**
```bash
# Test consciousness API
curl http://localhost:8000/api/consciousness/state

# Test memory system
curl -X POST http://localhost:8000/api/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "limit": 5}'

# Test agent system
curl -X POST http://localhost:8000/agent/router/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'
```

### **Database Debugging**
```bash
# Connect to Neo4j
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123

# Check Neo4j status
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123 \
  "CALL dbms.components()"

# Check Redis
docker-compose exec redis redis-cli ping
```

## 📞 **Getting Help**

### **Log Collection**
```bash
# Collect all logs
docker-compose logs > mainza_logs.txt
docker stats > system_stats.txt
docker-compose ps > container_status.txt
```

### **System Information**
```bash
# Collect system info
uname -a > system_info.txt
docker --version >> system_info.txt
docker-compose --version >> system_info.txt
```

### **Community Support**
- **GitHub Issues**: [Report issues on GitHub](https://github.com/mainza-ai/mainza-consciousness/issues)
- **Documentation**: Check the complete documentation
- **Discord**: Join our community Discord server
- **Email**: Contact support at support@mainza.ai

---

**Still having issues?** Check the [Complete Documentation](README.md) or [Report an Issue](https://github.com/mainza-ai/mainza-consciousness/issues) with detailed logs and system information.