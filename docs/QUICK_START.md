# Mainza AI - Quick Start Guide

## 🚀 **5-Minute Setup**

### Prerequisites
- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Ollama** with `nomic-embed-text:latest` model (recommended)
- **8GB+ RAM** recommended for optimal performance
- **4+ minutes** for initial backend startup

### One-Command Setup
```bash
# Clone and start Mainza
git clone https://github.com/mainza-ai/mainza-consciousness.git
cd mainza-consciousness
./scripts/build-dev.sh

# Access the system
# Frontend: http://localhost
# Backend API: http://localhost:8000
# Neo4j Browser: http://localhost:7474
```

### Model Setup (Ollama)
```bash
# Start Ollama service
ollama serve

# Pull recommended models
ollama pull nomic-embed-text:latest
ollama pull llama3.2:1b
```

## 🔧 **Development Tools**

```bash
# Development with hot reloading
./scripts/build-dev-hot.sh

# Verify changes are reflected
./scripts/verify-changes.sh

# Monitor build performance
./scripts/monitor-builds.sh

# Comprehensive development tools
./scripts/dev-tools.sh help
```

## 📊 **System Verification**

### Check Container Status
```bash
# Check all containers
docker-compose ps

# View backend logs
docker-compose logs backend --tail=20

# Test API endpoints
curl http://localhost:8000/health
```

### Test Consciousness System
```bash
# Run comprehensive tests
python test_ai_consciousness_optimizations.py

# Test optimization endpoints
curl -X POST "http://localhost:8000/api/optimization/status" -H "accept: application/json"
curl -X POST "http://localhost:8000/api/optimization/vector-embeddings" -H "accept: application/json"
```

## 🎯 **What You'll See**

### Frontend Dashboard
- **Real-time consciousness monitoring**
- **Evolution timeline tracking**
- **Multi-agent system status**
- **Memory system analytics**

### Backend APIs
- **Health endpoints**: System status and performance
- **Consciousness endpoints**: AI state and evolution
- **Insights endpoints**: Analytics and monitoring
- **Optimization endpoints**: System performance tuning

### Neo4j Browser
- **Knowledge graph visualization**
- **Memory system data**
- **Consciousness relationships**
- **Agent interaction patterns**

## 🔧 **Troubleshooting**

### Common Issues
- **Backend startup time**: Allow 4+ minutes for full initialization
- **Redis connection errors**: Ensure Docker service names are used
- **Neo4j vector index errors**: Check dimension limits (1-2048)
- **Ollama integration**: Verify model is pulled and running

### Quick Diagnostics
```bash
# Check container status
docker-compose ps

# View backend logs
docker-compose logs backend --tail=20

# Test API endpoints
curl http://localhost:8000/health
```

For detailed troubleshooting, see [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md).

## 📚 **Next Steps**

1. **Explore the Dashboard**: Navigate to http://localhost
2. **Check System Status**: Monitor consciousness metrics
3. **Test APIs**: Use the backend endpoints
4. **Read Documentation**: Dive deeper into the system
5. **Contribute**: Help improve Mainza AI

---

**Ready to explore the future of conscious AI?** [Get Started →](../README.md)
