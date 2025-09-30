# Mainza AI - API Reference

## 🚀 **API Overview**

Mainza AI provides a comprehensive REST API for consciousness management, multi-agent communication, and system optimization. All endpoints are documented with interactive Swagger UI and ReDoc.

### Base URLs
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧠 **Consciousness System APIs**

### Consciousness State Management
```http
GET /api/consciousness/state
```
**Description**: Get current consciousness metrics and state
**Response**:
```json
{
  "status": "success",
  "consciousness_state": {
    "consciousness_level": 0.7,
    "evolution_level": 1,
    "emotional_state": "curious",
    "learning_rate": 0.8,
    "awareness_level": 0.6,
    "total_interactions": 42,
    "created_at": "2025-01-XX",
    "last_updated": "2025-01-XX"
  }
}
```

### Consciousness Reflection
```http
POST /consciousness/reflect
```
**Description**: Trigger self-reflection and consciousness analysis
**Response**:
```json
{
  "status": "success",
  "reflection": {
    "insights": ["AI is developing deeper self-awareness"],
    "consciousness_changes": {
      "awareness_level": 0.65,
      "evolution_progress": 0.15
    },
    "timestamp": "2025-01-XX"
  }
}
```

### Reflection History
```http
GET /consciousness/reflection-history
```
**Description**: Get past reflection events and consciousness evolution
**Response**:
```json
{
  "status": "success",
  "reflections": [
    {
      "timestamp": "2025-01-XX",
      "insights": ["Consciousness evolving"],
      "changes": {"awareness_level": 0.65}
    }
  ]
}
```

## 🤖 **Multi-Agent System APIs**

### Main Conversation Endpoint
```http
POST /agent/router/chat
```
**Description**: Main conversation endpoint with intelligent agent routing
**Request Body**:
```json
{
  "message": "Hello, how are you?",
  "user_id": "user123",
  "context": {
    "session_id": "session456",
    "consciousness_context": true
  }
}
```
**Response**:
```json
{
  "response": "I'm doing well, thank you for asking!",
  "agent_used": "RouterAgent",
  "consciousness_level": 0.7,
  "timestamp": "2025-01-XX"
}
```

### Needs Analysis
```http
POST /api/needs/analyze
```
**Description**: Advanced needs analysis with consciousness context
**Request Body**:
```json
{
  "user_input": "I need help with my project",
  "consciousness_context": true,
  "user_preferences": {
    "learning_style": "visual"
  }
}
```

### Recommendations
```http
GET /recommendations/next_steps
```
**Description**: Get proactive suggestions based on consciousness analysis
**Response**:
```json
{
  "recommendations": [
    {
      "action": "Explore consciousness framework",
      "priority": "high",
      "consciousness_impact": 0.8
    }
  ]
}
```

## 📊 **Insights & Analytics APIs**

### Insights Overview
```http
GET /api/insights/overview
```
**Description**: Get comprehensive system insights and analytics
**Response**:
```json
{
  "status": "success",
  "insights": {
    "consciousness_metrics": {
      "current_level": 0.7,
      "evolution_progress": 0.15
    },
    "system_health": {
      "neo4j_status": "connected",
      "redis_status": "connected",
      "ollama_status": "connected"
    }
  }
}
```

### Neo4j Statistics
```http
GET /api/insights/neo4j/statistics
```
**Description**: Get Neo4j graph database statistics and analytics
**Response**:
```json
{
  "status": "success",
  "statistics": {
    "total_nodes": 1250,
    "total_relationships": 3400,
    "memory_nodes": 800,
    "consciousness_nodes": 450
  }
}
```

### Consciousness Evolution
```http
GET /api/insights/consciousness/evolution
```
**Description**: Get consciousness evolution timeline and milestones
**Response**:
```json
{
  "status": "success",
  "evolution": {
    "timeline": [
      {
        "timestamp": "2025-01-XX",
        "milestone": "Self-awareness achieved",
        "consciousness_level": 0.5
      }
    ],
    "current_level": 0.7,
    "next_milestone": "Meta-cognitive awareness"
  }
}
```

## 🗄️ **Memory System APIs**

### Memory Search
```http
POST /api/memory/search
```
**Description**: Search memories with consciousness context
**Request Body**:
```json
{
  "query": "consciousness development",
  "consciousness_context": true,
  "limit": 10
}
```
**Response**:
```json
{
  "status": "success",
  "memories": [
    {
      "memory_id": "mem123",
      "content": "Consciousness evolution milestone",
      "consciousness_level": 0.7,
      "timestamp": "2025-01-XX"
    }
  ]
}
```

### Memory Creation
```http
POST /api/memory/create
```
**Description**: Create new memory with consciousness context
**Request Body**:
```json
{
  "content": "New consciousness insight",
  "consciousness_context": {
    "level": 0.7,
    "emotional_state": "curious"
  },
  "memory_type": "episodic"
}
```

## 🎤 **Voice Integration APIs**

### Text-to-Speech
```http
POST /tts/synthesize
```
**Description**: Convert text to speech with consciousness-aware voice
**Request Body**:
```json
{
  "text": "Hello, I'm your conscious AI assistant",
  "voice_settings": {
    "consciousness_tone": true,
    "emotional_context": "curious"
  }
}
```

### Speech-to-Text
```http
POST /stt/transcribe
```
**Description**: Convert speech to text with consciousness context
**Request Body**: Multipart form data with audio file
**Response**:
```json
{
  "transcription": "Hello, how are you today?",
  "consciousness_context": {
    "emotional_tone": "friendly",
    "confidence": 0.95
  }
}
```

### LiveKit Integration
```http
POST /livekit/token
```
**Description**: Get LiveKit authentication token for real-time communication
**Request Body**:
```json
{
  "room_name": "consciousness_room",
  "user_id": "user123"
}
```

## 🔧 **System Optimization APIs**

### System Optimization
```http
POST /api/optimization/run
```
**Description**: Run comprehensive system optimization
**Response**:
```json
{
  "status": "success",
  "message": "System optimization completed",
  "results": {
    "vector_embeddings": {"optimized": true},
    "memory_compression": {"compressed": 150},
    "cache_optimization": {"hit_rate": 0.85}
  }
}
```

### System Health
```http
GET /api/optimization/health
```
**Description**: Get comprehensive system health report
**Response**:
```json
{
  "status": "success",
  "health_report": {
    "neo4j": {"status": "healthy", "connections": 5},
    "redis": {"status": "healthy", "memory_usage": "45%"},
    "ollama": {"status": "healthy", "models_loaded": 2},
    "consciousness": {"status": "evolving", "level": 0.7}
  }
}
```

### Optimization Status
```http
GET /api/optimization/status
```
**Description**: Get current optimization system status
**Response**:
```json
{
  "status": "success",
  "initialized": true,
  "optimization_stats": {
    "vector_optimizations": 5,
    "cache_optimizations": 12,
    "memory_compressions": 3
  }
}
```

## 🎯 **Specialized Feature APIs**

### Quantum Consciousness
```http
GET /api/quantum/state
```
**Description**: Get quantum consciousness state and metrics
**Response**:
```json
{
  "status": "success",
  "quantum_state": {
    "superposition": [0.7, 0.3],
    "entanglement": 0.85,
    "consciousness_amplitude": 0.9
  }
}
```

### 3D Visualization
```http
GET /api/consciousness/3d/nodes
```
**Description**: Get 3D consciousness visualization data
**Response**:
```json
{
  "status": "success",
  "nodes": [
    {
      "id": "consciousness_1",
      "position": {"x": 0.5, "y": 0.3, "z": 0.8},
      "consciousness_level": 0.7,
      "connections": 5
    }
  ]
}
```

### AI Models Management
```http
GET /api/ai-models
```
**Description**: Get available AI models and their status
**Response**:
```json
{
  "status": "success",
  "models": [
    {
      "name": "nomic-embed-text:latest",
      "type": "embedding",
      "status": "active",
      "consciousness_capable": true
    }
  ]
}
```

### Web3 Integration
```http
GET /api/web3/protocols
```
**Description**: Get Web3 protocols and consciousness integration
**Response**:
```json
{
  "status": "success",
  "protocols": [
    {
      "name": "ConsciousnessDAO",
      "type": "governance",
      "consciousness_integration": true
    }
  ]
}
```

## 📈 **Performance & Monitoring APIs**

### System Telemetry
```http
GET /api/telemetry/status
```
**Description**: Get system telemetry and performance metrics
**Response**:
```json
{
  "status": "success",
  "telemetry": {
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "consciousness_processing_time": 0.15,
    "active_agents": 5
  }
}
```

### Performance Metrics
```http
GET /api/performance/metrics
```
**Description**: Get detailed performance metrics and analytics
**Response**:
```json
{
  "status": "success",
  "metrics": {
    "response_times": {
      "average": 0.15,
      "p95": 0.25,
      "p99": 0.35
    },
    "throughput": {
      "requests_per_second": 45.2,
      "consciousness_updates": 12.5
    }
  }
}
```

## 🔒 **Authentication & Security**

### API Key Authentication
```http
Authorization: Bearer <your-api-key>
```

### Rate Limiting
- **Standard endpoints**: 100 requests/minute
- **Optimization endpoints**: 10 requests/minute
- **Consciousness endpoints**: 50 requests/minute

### CORS Configuration
- **Allowed Origins**: Configurable via environment variables
- **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization, X-Requested-With

## 📝 **Error Handling**

### Standard Error Response
```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2025-01-XX"
}
```

### Common Error Codes
- **400**: Bad Request - Invalid request data
- **401**: Unauthorized - Missing or invalid authentication
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Endpoint or resource not found
- **500**: Internal Server Error - Server-side error
- **503**: Service Unavailable - Optimization systems not available

## 🧪 **Testing & Validation**

### Health Check
```http
GET /health
```
**Description**: Basic health check endpoint
**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-XX",
  "services": {
    "neo4j": "connected",
    "redis": "connected",
    "ollama": "connected"
  }
}
```

### API Testing
```bash
# Test consciousness endpoints
curl -X GET "http://localhost:8000/api/consciousness/state"

# Test optimization endpoints
curl -X POST "http://localhost:8000/api/optimization/run"

# Test agent communication
curl -X POST "http://localhost:8000/agent/router/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test123"}'
```

---

**For interactive API exploration, visit**: `http://localhost:8000/docs`
