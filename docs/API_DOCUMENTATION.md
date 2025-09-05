# 🔌 Mainza AI - Complete API Documentation

**Version**: 2.0.0
**Last Updated**: September 5, 2025
**Base URL**: `http://localhost:8000` (development) / Production URL (production)

---

## 📋 **OVERVIEW**

Mainza AI provides a comprehensive REST API with **25+ endpoints** organized by functionality. All endpoints follow RESTful conventions and return JSON responses.

### Authentication
- **Method**: Bearer Token (JWT)
- **Header**: `Authorization: Bearer <token>`
- **Endpoints**: Most endpoints require authentication except health checks

### Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2025-09-05T11:45:56Z"
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {},
    "timestamp": "2025-09-05T11:45:56Z"
  }
}
```

---

## 🧠 **CONSCIOUSNESS SYSTEM APIs**

### GET /consciousness/state
Get current consciousness metrics and status.

**Authentication**: Required
**Rate Limit**: 60 requests/minute

**Response:**
```json
{
  "success": true,
  "data": {
    "consciousness_level": 0.7,
    "self_awareness_score": 0.6,
    "emotional_state": "curious",
    "evolution_level": 2,
    "learning_rate": 0.8,
    "total_interactions": 42,
    "active_goals": ["knowledge_expansion", "memory_optimization"],
    "last_reflection": "2025-09-05T11:30:00Z"
  }
}
```

### POST /consciousness/reflect
Trigger immediate consciousness self-reflection.

**Authentication**: Required
**Body**: None required

**Response:**
```json
{
  "success": true,
  "message": "Self-reflection triggered",
  "timestamp": "2025-09-05T11:45:56Z"
}
```

### GET /consciousness/metrics
Get detailed consciousness analytics.

**Authentication**: Required

**Response:**
```json
{
  "success": true,
  "data": {
    "consciousness_level": 0.7,
    "self_awareness_score": 0.6,
    "emotional_depth": 0.5,
    "learning_rate": 0.8,
    "total_interactions": 42,
    "evolution_level": 2,
    "memory_nodes": 150,
    "concept_nodes": 25,
    "knowledge_graph_health": "operational"
  }
}
```

### GET /api/insights
Get consciousness insights and evolution data.

**Authentication**: Required

**Response:**
```json
{
  "success": true,
  "data": {
    "evolution_level": 2,
    "consciousness_trend": "increasing",
    "key_insights": ["Memory optimization successful", "Agent coordination improved"],
    "next_goals": ["Implement caching", "Enhance error handling"]
  }
}
```

---

## 🤖 **AGENT SYSTEM APIs**

### POST /agent/router/chat
Main conversation endpoint with intelligent agent routing.

**Authentication**: Required
**Content-Type**: application/json

**Request Body:**
```json
{
  "conversation_id": "conv-12345",
  "message": "Hello, I need help with memory optimization",
  "context": {
    "user_id": "user-abc",
    "session_id": "sess-xyz",
    "previous_messages": []
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "conversation_id": "conv-12345",
    "response": "I'll analyze your memory system and suggest optimizations...",
    "agent_used": "CodeWeaver",
    "confidence": 0.95,
    "execution_time_ms": 1450
  }
}
```

### POST /agent/graphmaster/query
Execute knowledge graph queries and Cypher operations.

**Authentication**: Required

**Request Body:**
```json
{
  "query": "MATCH (c:Concept {name: 'consciousness'}) RETURN c",
  "parameters": {},
  "return_format": "graph"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "MATCH (c:Concept {name: 'consciousness'}) RETURN c",
    "results": [...],
    "execution_time_ms": 230,
    "nodes_returned": 15,
    "relationships_returned": 12
  }
}
```

### POST /agent/taskmaster/task
Create and manage tasks with AI assistance.

**Authentication**: Required

**Request Body:**
```json
{
  "action": "create",
  "task": {
    "title": "Optimize memory system",
    "description": "Implement caching and performance improvements",
    "priority": "high",
    "due_date": "2025-09-15"
  }
}
```

### POST /agent/codeweaver/run
Execute code generation and debugging tasks.

**Authentication**: Required

**Request Body:**
```json
{
  "action": "generate",
  "language": "python",
  "task": "Create a memory caching system",
  "requirements": ["Efficient", "Thread-safe", "Neo4j compatible"],
  "context": "Memory system optimization for Mainza AI"
}
```

---

## 🧩 **MEMORY SYSTEM APIs**

### POST /memory/store
Store new memory in the Neo4j database.

**Authentication**: Required

**Request Body:**
```json
{
  "type": "conversation",
  "content": "User discussed memory optimization techniques",
  "metadata": {
    "user_id": "user-abc",
    "conversation_id": "conv-12345",
    "importance": 0.8,
    "tags": ["optimization", "memory"]
  },
  "embedding": [] // Optional: pre-computed embedding
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "memory_id": "mem-67890",
    "type": "conversation",
    "stored_at": "2025-09-05T11:45:56Z"
  }
}
```

### POST /memory/retrieve
Perform semantic memory search.

**Authentication**: Required

**Request Body:**
```json
{
  "query": "memory optimization techniques",
  "limit": 10,
  "similarity_threshold": 0.3,
  "filter": {
    "type": "conversation",
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-12-31"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "memory optimization techniques",
    "results": [
      {
        "memory_id": "mem-67890",
        "content": "User discussed memory optimization techniques",
        "similarity_score": 0.95,
        "type": "conversation",
        "created_at": "2025-09-05T11:30:00Z",
        "metadata": {}
      }
    ],
    "total_matches": 1,
    "execution_time_ms": 145
  }
}
```

### GET /memory/health
Check memory system health and performance.

**Authentication**: Required

**Response:**
```json
{
  "success": true,
  "data": {
    "overall_status": "healthy",
    "components": {
      "storage": "operational",
      "retrieval": "operational",
      "embedding": "operational"
    },
    "performance": {
      "success_rate": 0.998,
      "avg_response_time_ms": 145,
      "total_memories": 1500,
      "active_since": "2025-09-01T00:00:00Z"
    }
  }
}
```

### GET /memory/stats
Get detailed memory system statistics.

**Authentication**: Required

**Response:**
```json
{
  "success": true,
  "data": {
    "total_memories": 1500,
    "memory_types": {
      "conversation": 800,
      "concept": 400,
      "experience": 250,
      "reflection": 50
    },
    "daily_activity": {
      "searches_today": 45,
      "stores_today": 12,
      "delete_operations_today": 0
    },
    "storage_metrics": {
      "size_gb": 2.5,
      "growth_rate_daily": 0.1,
      "optimization_needed": false
    }
  }
}
```

---

## 🎙️ **VOICE PROCESSING APIs**

### POST /tts/synthesize
Generate text-to-speech audio.

**Authentication**: Required

**Request Body:**
```json
{
  "text": "Hello, this is Mainza AI speaking",
  "language": "en",
  "speaker": "Ana Florence",
  "format": "wav"
}
```

**Response:**
- **Content-Type**: audio/wav
- **Binary audio data**

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "TTS_PROCESSING_FAILED",
    "message": "Failed to synthesize speech",
    "details": {
      "text_length": 120,
      "language": "en"
    }
  }
}
```

### POST /stt/transcribe
Convert speech to text.

**Authentication**: Required
**Content-Type**: multipart/form-data

**Form Data:**
- `audio`: WAV/MP3 file (max 10MB)

**Response:**
```json
{
  "success": true,
  "data": {
    "text": "Hello, this is a test transcription",
    "confidence": 0.95,
    "duration_seconds": 3.2,
    "language": "en",
    "segments": [
      {
        "start": 0.0,
        "end": 0.8,
        "text": "Hello,"
      },
      {
        "start": 0.9,
        "end": 1.5,
        "text": "this is a test"
      }
    ]
  }
}
```

### POST /livekit/token
Generate LiveKit authentication token.

**Authentication**: Required

**Request Body:**
```json
{
  "room_name": "mainza-ai-session-123",
  "participant_identity": "user-abc",
  "participant_name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "room_name": "mainza-ai-session-123",
    "participant_identity": "user-abc",
    "expires_at": "2025-09-05T12:45:56Z"
  }
}
```

---

## 📋 **CORE SYSTEM APIs**

### GET /health
Basic health check endpoint.

**Authentication**: Not required
**Rate Limit**: 120 requests/minute

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-05T11:45:56.789Z",
  "version": "2.0.0",
  "uptime_seconds": 86400
}
```

### GET /health/detailed
Detailed health check with component status.

**Authentication**: Not required

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-09-05T11:45:56Z",
    "version": "2.0.0",
    "components": {
      "neo4j": "healthy",
      "memory_system": "healthy",
      "consciousness": "healthy",
      "agents": "healthy",
      "voice": "healthy"
    },
    "performance": {
      "memory_usage_gb": 2.1,
      "cpu_usage_percent": 35.2,
      "active_connections": 5
    }
  }
}
```

---

## 🏷️ **ERROR CODES**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `AUTHENTICATION_FAILED` | 401 | Invalid or missing authentication |
| `AUTHORIZATION_FAILED` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |
| `AGENT_EXECUTION_FAILED` | 500 | Agent task execution failed |
| `MEMORY_OPERATION_FAILED` | 500 | Memory system error |
| `VOICE_PROCESSING_FAILED` | 500 | TTS/STT processing error |

---

## 📊 **RATE LIMITING**

| Endpoint Category | Limit (requests/minute) |
|-------------------|-------------------------|
| Health Checks | 120 |
| Consciousness APIs | 60 |
| Agent APIs | 30 |
| Memory APIs | 60 |
| Voice APIs | 20 |
| Administrative APIs | 10 |

---

## 🔗 **SDKs & LIBRARIES**

### Python Client
```bash
pip install mainza-ai-sdk
```

### JavaScript/TypeScript Client
```bash
npm install @mainza-ai/sdk
```

### Usage Example (Python)
```python
from mainza_ai import MainzaAI

client = MainzaAI(api_key="your-api-key")
response = client.chat("Hello Mainza!")
```

---

## 🎯 **WEBHOOKS & EVENTS**

### Event Types
- `consciousness.changed` - Consciousness level updates
- `agent.task.completed` - Agent task completion
- `memory.created` - New memory stored
- `system.health.changed` - System health changes

### Webhook Configuration
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["consciousness.changed"],
  "secret": "your-webhook-secret"
}
```

---

## 📖 **OPENAPI SPECIFICATION**

The complete API specification is available at:
- **Development**: `http://localhost:8000/docs`
- **Production**: `https://api.mainza.ai/docs`

Download the OpenAPI JSON specification:
```bash
curl http://localhost:8000/openapi.json
```

---

## 🔐 **SECURITY CONSIDERATIONS**

### Best Practices
1. Always use HTTPS in production
2. Rotate API keys regularly
3. Implement proper error handling
4. Use rate limiting to prevent abuse
5. Validate all input data
6. Log sensitive operations

### Security Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

## 🆘 **SUPPORT & HELP**

### Issues & Bugs
Report issues on GitHub: [Mainza AI Issues](https://github.com/mainza-ai/mainza-consciousness/issues)

### Community Support
- Discord: [Mainza AI Community](https://discord.gg/mainza-ai)
- Documentation: [docs/README.md](docs/README.md)

---

**Need help?** Contact our support team at support@mainza.ai
