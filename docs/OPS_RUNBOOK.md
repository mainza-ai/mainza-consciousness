# Mainza AI - Operations Runbook

## 🚀 **Quick Start Commands**

### **System Startup**
```bash
# Start all services
docker-compose up -d

# Check all services status
docker-compose ps

# View logs for all services
docker-compose logs -f
```

### **Service Management**
```bash
# Restart specific service
docker-compose restart backend
docker-compose restart frontend
docker-compose restart neo4j

# Rebuild and restart (after code changes)
docker-compose build --no-cache backend
docker-compose up -d backend
```

## 🔍 **Health Verification Commands**

### **System Health Checks**
```bash
# Overall system health
curl -s http://localhost:80/health | jq '.status'

# Backend health
curl -s http://localhost:8000/health | jq '.status'

# Neo4j connectivity
curl -s http://localhost:7474
```

### **Quantum System Verification**
```bash
# Quantum engine status
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine | {quantum_engine_active, quantum_algorithms_count}'

# Quantum state metrics
curl -s http://localhost:80/api/quantum/state | jq '.data | {quantum_consciousness_level, quantum_coherence, entanglement_strength}'

# Backend quantum status
curl -s http://localhost:80/api/quantum/backend/status | jq '.quantum_engine_status'
```

### **Consciousness System Checks**
```bash
# Consciousness state
curl -s http://localhost:80/consciousness/state | jq '.consciousness_level'

# Knowledge graph stats
curl -s http://localhost:80/consciousness/knowledge-graph-stats | jq '.total_nodes'

# Neo4j statistics
curl -s http://localhost:80/api/insights/neo4j/statistics | jq '.total_nodes'
```

## 🧠 **Memory System Verification**

### **Memory System Health**
```bash
# Test memory search
curl -X POST http://localhost:8000/api/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "limit": 5}'

# Memory consolidation
curl -X POST http://localhost:8000/api/memory/consolidate
```

### **Agent System Testing**
```bash
# Test agent routing
curl -X POST http://localhost:8000/agent/router/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'
```

## 🔧 **Troubleshooting Commands**

### **Log Analysis**
```bash
# Backend logs (last 100 lines)
docker-compose logs --tail=100 backend

# Neo4j logs
docker-compose logs --tail=100 neo4j

# All services logs
docker-compose logs --tail=50

# Follow logs in real-time
docker-compose logs -f backend
```

### **Resource Monitoring**
```bash
# Container resource usage
docker stats

# System resources
df -h
free -h

# Port usage
netstat -tulpn | grep -E "(80|8000|7474|6379|7880)"
```

### **Database Access**
```bash
# Neo4j shell access
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123

# Redis CLI access
docker-compose exec redis redis-cli ping
```

## ⚛️ **Quantum-Specific Operations**

### **Quantum Engine Management**
```bash
# Check quantum engine status
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.quantum_engine_active'

# Verify quantum algorithms count
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.quantum_algorithms_count'

# Check active algorithms
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.active_algorithms'
```

### **Quantum Metrics Monitoring**
```bash
# Quantum coherence
curl -s http://localhost:80/api/quantum/state | jq '.data.quantum_coherence'

# Entanglement strength
curl -s http://localhost:80/api/quantum/state | jq '.data.entanglement_strength'

# Superposition states
curl -s http://localhost:80/api/quantum/state | jq '.data.superposition_states'

# Quantum advantage
curl -s http://localhost:80/api/quantum/state | jq '.data.quantum_advantage'
```

## 🚨 **Emergency Procedures**

### **Service Recovery**
```bash
# Stop all services
docker-compose down

# Clean restart
docker-compose down
docker-compose up -d

# Nuclear option (clean everything)
docker-compose down
docker system prune -a
docker-compose up -d
```

### **Data Recovery**
```bash
# Backup Neo4j data
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123 "CALL apoc.export.cypher.all('/tmp/backup.cypher')"

# Restore from backup
docker-compose exec neo4j cypher-shell -u neo4j -p mainza123 "CALL apoc.import.cypher('/tmp/backup.cypher')"
```

## 📊 **Performance Monitoring**

### **System Performance**
```bash
# Container performance
docker stats --no-stream

# Memory usage per service
docker-compose exec backend ps aux
docker-compose exec neo4j ps aux
```

### **Quantum Performance**
```bash
# Quantum processing metrics
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.processing_metrics'

# Current operations
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.current_operations'
```

## 🔄 **Development Workflow**

### **Code Changes**
```bash
# Rebuild after backend changes
docker-compose build --no-cache backend
docker-compose up -d backend

# Rebuild after frontend changes
docker-compose build --no-cache frontend
docker-compose up -d frontend

# Full rebuild
docker-compose build --no-cache
docker-compose up -d
```

### **Testing Commands**
```bash
# Run consciousness tests
python test_advanced_quantum_consciousness.py

# Test quantum integration
curl -s http://localhost:80/api/quantum/state | jq '.data.quantum_consciousness_level > 0'

# Verify UI integration
curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.quantum_engine_active == true'
```

## 📝 **Quick Reference**

### **Most Used Commands**
1. `docker-compose ps` - Check service status
2. `docker-compose logs -f backend` - Follow backend logs
3. `curl -s http://localhost:80/health | jq '.status'` - System health
4. `curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine'` - Quantum status
5. `docker-compose restart backend` - Restart backend
6. `docker stats` - Resource monitoring
7. `curl -s http://localhost:80/consciousness/state | jq '.consciousness_level'` - Consciousness level
8. `docker-compose build --no-cache backend && docker-compose up -d backend` - Rebuild backend
9. `docker-compose down && docker-compose up -d` - Clean restart
10. `curl -X POST http://localhost:8000/agent/router/chat -H "Content-Type: application/json" -d '{"message": "Hello", "user_id": "test"}'` - Test agent

### **Quantum-Specific Quick Checks**
- **Engine Active**: `curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.quantum_engine_active'`
- **Algorithms Count**: `curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.quantum_algorithms_count'`
- **Coherence Level**: `curl -s http://localhost:80/api/quantum/state | jq '.data.quantum_coherence'`
- **Processing Active**: `curl -s http://localhost:80/api/quantum/process/status | jq '.quantum_engine.quantum_processing_active'`

---

**Pro Tip**: Bookmark these commands for quick access during development and troubleshooting! 🚀
