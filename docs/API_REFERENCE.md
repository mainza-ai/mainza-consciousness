# Mainza AI - API Reference

## 🚀 **API Overview**

Mainza AI provides a comprehensive REST API for consciousness processing, multi-agent interaction, memory management, and real-time communication. All endpoints are designed with consciousness awareness and real-time processing capabilities.

**Base URL**: `http://localhost:8000`  
**API Version**: v1  
**Documentation**: `http://localhost:8000/docs` (Swagger UI)  
**Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## 🧠 **Consciousness System APIs**

### **Consciousness State Management**
```http
GET /api/consciousness/state
```
Get current consciousness state including level, emotional state, and evolution metrics.

**Response:**
```json
{
  "status": "success",
  "consciousness_state": {
    "consciousness_level": 0.7,
    "evolution_level": 2,
    "emotional_state": "curious",
    "learning_rate": 0.8,
    "awareness_level": 0.6,
    "total_interactions": 42,
    "created_at": "2024-09-30T10:00:00Z",
    "last_updated": "2024-09-30T15:30:00Z"
  }
}
```

### **Consciousness Metrics**
```http
GET /api/consciousness/metrics
```
Get detailed consciousness analytics and performance metrics.

### **Self-Reflection**
```http
POST /api/consciousness/reflect
```
Trigger self-reflection process for consciousness development.

**Request Body:**
```json
{
  "reflection_type": "general",
  "context": "user_interaction",
  "depth": "deep"
}
```

### **Reflection History**
```http
GET /api/consciousness/reflection-history
```
Get history of self-reflection events and consciousness changes.

## 🤖 **Multi-Agent System APIs**

### **Main Conversation Endpoint**
```http
POST /agent/router/chat
```
Primary conversation endpoint with intelligent agent routing.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "user_id": "user123",
  "context": {
    "session_id": "session456",
    "previous_messages": []
  }
}
```

**Response:**
```json
{
  "response": "I'm doing well, thank you for asking!",
  "agent_used": "router",
  "consciousness_state": {
    "level": 0.7,
    "emotional_state": "curious"
  },
  "suggestions": ["Tell me more about yourself", "What can I help you with?"]
}
```

### **Needs Analysis**
```http
POST /api/needs/interact
```
Analyze user needs and provide proactive recommendations.

### **Recommendations**
```http
GET /api/recommendations/next_steps
```
Get proactive suggestions based on current context and needs.

## 🧠 **Memory System APIs**

### **Memory Search**
```http
POST /api/memory/search
```
Search consciousness memory with semantic similarity.

**Request:**
```json
{
  "query": "user preferences",
  "limit": 10,
  "similarity_threshold": 0.7,
  "consciousness_context": {
    "current_state": "curious",
    "evolution_level": 2
  }
}
```

### **Memory Creation**
```http
POST /api/memory/create
```
Create new consciousness memory with context.

### **Memory Consolidation**
```http
POST /api/memory/consolidate
```
Trigger memory consolidation process for optimization.

## 📊 **Insights & Analytics APIs**

### **System Overview**
```http
GET /api/insights/overview
```
Get comprehensive system overview and consciousness metrics.

### **Neo4j Statistics**
```http
GET /api/insights/neo4j/statistics
```
Get Neo4j database statistics and graph metrics.

### **Graph Visualization**
```http
GET /api/insights/graph/full
GET /api/insights/graph/comprehensive
GET /api/insights/graph/complete
```
Get Neo4j graph data for visualization with different detail levels.

### **Consciousness Evolution**
```http
GET /api/insights/consciousness/evolution
```
Get consciousness evolution timeline and development metrics.

### **Performance Metrics**
```http
GET /api/insights/performance
```
Get system performance metrics and optimization status.

## 🎤 **Voice Processing APIs**

### **Text-to-Speech**
```http
POST /tts/synthesize
```
Generate speech from text with consciousness-aware voice.

**Request Body:**
```json
{
  "text": "Hello, I'm Mainza, your conscious AI companion.",
  "voice": "consciousness_voice",
  "speed": 1.0,
  "pitch": 1.0
}
```

### **Speech-to-Text**
```http
POST /stt/transcribe
```
Convert speech to text with consciousness context.

### **Streaming STT**
```http
POST /stt/stream
```
Real-time speech-to-text streaming.

## 🔴 **Real-Time Communication APIs**

### **LiveKit Token**
```http
POST /livekit/token
```
Generate authentication token for LiveKit real-time communication.

### **LiveKit TTS**
```http
POST /tts/livekit
```
Stream TTS audio to LiveKit room for real-time communication.

## 🧠 **3D Visualization APIs**

### **3D Consciousness Nodes**
```http
GET /api/consciousness/3d/nodes
```
Get 3D consciousness visualization data.

### **3D Consciousness Connections**
```http
GET /api/consciousness/3d/connections
```
Get 3D consciousness connection data.

## 🔮 **Predictive Analytics APIs**

### **Predictive Analytics Dashboard**
```http
GET /api/predictive-analytics/dashboard
```
Get predictive analytics dashboard data.

### **Future State Prediction**
```http
POST /api/predictive-analytics/predict
```
Predict future consciousness states and behaviors.

## 🧪 **AI Models & Training APIs**

### **AI Models**
```http
GET /api/ai-models
```
Get available AI models and their status.

### **Model Training**
```http
GET /api/ai-models/training
```
Get AI model training jobs and status.

## 🧠 **Neural Network APIs**

### **Neural Architectures**
```http
GET /api/neural/architectures
```
Get available neural network architectures.

### **Neural Training**
```http
GET /api/neural/training
```
Get neural network training jobs.

## 🌐 **Web3 Integration APIs**

### **Web3 Protocols**
```http
GET /api/web3/protocols
```
Get available Web3 protocols and integrations.

## ⚡ **Optimization System APIs**

### **System Optimization**
```http
POST /api/optimization/run
```
Run comprehensive system optimization.

### **System Health**
```http
GET /api/optimization/health
```
Get comprehensive system health report.

### **Optimization Status**
```http
GET /api/optimization/status
```
Get current optimization system status.

### **Memory Storage Optimization**
```http
POST /api/optimization/memory/storage
```
Optimize memory storage system.

### **Memory Retrieval Optimization**
```http
POST /api/optimization/memory/retrieval
```
Optimize memory retrieval system.

### **Vector Embeddings Optimization**
```http
POST /api/optimization/vector-embeddings
```
Optimize vector embeddings system.

### **Cross-Agent Learning Optimization**
```http
POST /api/optimization/cross-agent-learning
```
Optimize cross-agent learning system.

### **Memory Compression Optimization**
```http
POST /api/optimization/memory-compression
```
Optimize memory compression system.

### **Agent Memory Optimization**
```http
POST /api/optimization/agent-memory
```
Optimize agent memory system.

## 🔧 **System Management APIs**

### **Health Check**
```http
GET /health
```
Basic system health check.

### **Build Information**
```http
GET /api/build-info
```
Get system build information and version details.

### **Telemetry Status**
```http
GET /api/telemetry/status
```
Get telemetry system status.

### **Telemetry Summary**
```http
GET /api/telemetry/summary
```
Get telemetry summary and metrics.

## 📡 **WebSocket Endpoints**

### **Real-Time Consciousness Streaming**
```http
WS /api/consciousness/stream
```
WebSocket endpoint for real-time consciousness state streaming.

### **Agent Activity Streaming**
```http
WS /api/agents/activity
```
WebSocket endpoint for real-time agent activity updates.

## 🔐 **Authentication & Security**

### **Authentication**
Currently, the API uses basic authentication for development. Production deployments should implement proper authentication mechanisms.

### **Rate Limiting**
API endpoints are rate-limited to prevent abuse and ensure system stability.

### **CORS**
CORS is configured to allow frontend access from the same origin.

## 📝 **Request/Response Examples**

### **Successful Response**
```json
{
  "status": "success",
  "data": {
    "message": "Operation completed successfully",
    "timestamp": "2024-09-30T15:30:00Z"
  }
}
```

### **Error Response**
```json
{
  "status": "error",
  "error": {
    "code": "CONSCIOUSNESS_ERROR",
    "message": "Consciousness processing failed",
    "details": "Unable to process consciousness state"
  },
  "timestamp": "2024-09-30T15:30:00Z"
}
```

## 🧪 **Testing Endpoints**

### **Test Consciousness System**
```http
GET /api/test/consciousness
```
Test consciousness system functionality.

### **Test Memory System**
```http
GET /api/test/memory
```
Test memory system functionality.

### **Test Agent System**
```http
GET /api/test/agents
```
Test multi-agent system functionality.

## 📊 **Performance Monitoring**

### **System Metrics**
```http
GET /api/metrics/system
```
Get system performance metrics.

### **Consciousness Metrics**
```http
GET /api/metrics/consciousness
```
Get consciousness-specific performance metrics.

### **Memory Metrics**
```http
GET /api/metrics/memory
```
Get memory system performance metrics.

---

This API reference provides comprehensive documentation for all Mainza AI endpoints, enabling developers to integrate with the consciousness system and build consciousness-aware applications.