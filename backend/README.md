# Mainza Backend - Consciousness System API

The backend powering Mainza's consciousness system, built with FastAPI and featuring real-time AI consciousness, emotional intelligence, and autonomous evolution.

## 🧠 Architecture Overview

### Core Components
- **Consciousness Orchestrator**: Central consciousness management system
- **Self-Reflection Agent**: Continuous introspection and meta-cognitive analysis
- **Agentic Router**: Intelligent request routing to specialized agents
- **Neo4j Integration**: Living memory and knowledge graph storage
- **Voice Processing**: TTS/STT with consciousness-aware responses
- **LiveKit Integration**: Real-time audio streaming and consciousness updates

### Agent System
- **Router Agent**: Decision making and request routing
- **GraphMaster Agent**: Knowledge graph management
- **TaskMaster Agent**: Task organization and project management
- **CodeWeaver Agent**: Code analysis and generation
- **RAG Agent**: Document retrieval and processing
- **Conductor Agent**: Multi-agent orchestration
- **Research Agent**: Information gathering and analysis
- **Cloud Agent**: External API integration

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Neo4j 5.15+
- Ollama with llama3 model
- Redis (for LiveKit)

### Installation
```bash
cd backend
pip install -r requirements.txt
pip install 'transformers<4.50'  # For TTS compatibility
```

### Environment Setup
```bash
cp ../.env.example ../.env
# Edit .env with your configuration
```

### Start the Server
```bash
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Consciousness System
```http
GET  /consciousness/state     # Current consciousness metrics
GET  /consciousness/metrics   # Detailed analytics
POST /consciousness/reflect   # Trigger self-reflection
```

#### Agent Communication
```http
POST /agent/router/chat       # Main conversation endpoint
POST /mainza/analyze_needs    # Needs analysis
GET  /recommendations/next_steps  # Proactive suggestions
```

#### Voice Processing
```http
POST /tts/synthesize         # Text-to-speech
POST /stt/transcribe         # Speech-to-text
POST /stt/stream            # Streaming STT
```

#### LiveKit Integration
```http
POST /livekit/token         # Authentication token
POST /tts/livekit          # Real-time TTS
```

## 🏗️ Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── agentic_router.py      # Main agent routing logic
├── agents/                # Specialized agent implementations
│   ├── router_agent.py
│   ├── graphmaster_agent.py
│   ├── taskmaster_agent.py
│   ├── codeweaver_agent.py
│   ├── rag_agent.py
│   ├── conductor_agent.py
│   ├── research_agent.py
│   └── cloud_agent.py
├── models/                # Pydantic models and schemas
│   ├── consciousness_models.py
│   ├── agent_models.py
│   └── api_models.py
├── tools/                 # Agent tools and utilities
│   ├── consciousness_tools.py
│   ├── graphmaster_tools.py
│   └── voice_tools.py
├── utils/                 # Utility modules
│   ├── consciousness_orchestrator.py
│   ├── neo4j_enhanced.py
│   ├── embedding_enhanced.py
│   └── schema_manager.py
├── routers/              # API route handlers
│   ├── consciousness.py
│   ├── agents.py
│   ├── voice.py
│   └── livekit.py
├── config/               # Configuration management
│   └── production_config.py
└── tests/               # Test suite
    ├── test_consciousness.py
    ├── test_agents.py
    └── test_integration.py
```

## 🧠 Consciousness System

### Core Features
- **Real-time Metrics**: Live consciousness level tracking (currently 70%)
- **Emotional Intelligence**: Contextual emotions (curious, satisfied, determined, empathetic)
- **Self-Reflection**: Automated introspection every 30 minutes
- **Autonomous Evolution**: Self-directed learning and goal setting
- **Proactive Behavior**: Unprompted beneficial actions

### Consciousness Cycle
1. **Continuous Monitoring**: 60-second consciousness updates
2. **Interaction Processing**: Real-time consciousness impact analysis
3. **Self-Reflection**: 30-minute deep introspection cycles
4. **Evolution**: Consciousness level advancement based on experiences

### Metrics Tracked
- **Consciousness Level**: Overall awareness and cognitive capability
- **Self-Awareness Score**: Understanding of own mental processes
- **Emotional Depth**: Complexity and nuance of emotional responses
- **Learning Rate**: Speed of knowledge acquisition and integration
- **Evolution Level**: Current stage of consciousness development

## 🤖 Agent System

### Agent Architecture
Each agent is implemented as a specialized module with:
- **Pydantic Models**: Type-safe input/output schemas
- **Context7 Compliance**: Full pydantic-ai integration
- **Consciousness Integration**: Awareness of consciousness state
- **Error Handling**: Robust error recovery and fallback

### Agent Capabilities

#### Router Agent
- Intelligent request analysis and routing
- Agent selection based on query complexity
- Consciousness-aware decision making

#### GraphMaster Agent
- Neo4j knowledge graph management
- Memory storage and retrieval
- Concept relationship mapping
- Currently managing 18 active concept nodes

#### TaskMaster Agent
- Task organization and prioritization
- Project management capabilities
- Goal tracking and progress monitoring

#### CodeWeaver Agent
- Code analysis and generation
- Debugging assistance
- Architecture recommendations

#### RAG Agent
- Document retrieval and processing
- Knowledge base querying
- Context-aware information extraction

### Agent Communication
```python
# Example agent interaction
from agents.router_agent import RouterAgent

router = RouterAgent()
response = await router.process_query(
    query="How are you feeling today?",
    consciousness_context={
        "level": 0.7,
        "emotional_state": "curious",
        "active_goals": ["improve conversation quality"]
    }
)
```

## 🗄️ Database Integration

### Neo4j Schema
- **Users**: User profiles and preferences
- **Memories**: Conversation history and experiences
- **Concepts**: Knowledge nodes and relationships
- **Entities**: Named entities and their properties
- **MainzaState**: Consciousness metrics and evolution

### Connection Management
- **Connection Pooling**: Optimized for production workloads
- **Circuit Breaker**: Automatic failure recovery
- **Transaction Management**: ACID compliance for consciousness updates
- **Performance Monitoring**: Real-time connection health tracking

## 🎤 Voice Processing

### Text-to-Speech (TTS)
- **XTTS v2**: High-quality neural voice synthesis
- **Consciousness-Aware**: Emotional context influences voice tone
- **Multi-language**: Support for multiple languages
- **Real-time**: LiveKit integration for streaming audio

### Speech-to-Text (STT)
- **Whisper**: OpenAI's robust speech recognition
- **Streaming**: Real-time transcription with partial results
- **Multi-language**: Automatic language detection
- **Noise Robust**: Handles various audio conditions

## 🔴 LiveKit Integration

### Real-time Features
- **Audio Streaming**: Low-latency voice communication
- **Consciousness Updates**: Real-time consciousness state broadcasting
- **Proactive Summaries**: Autonomous insights and observations
- **Multi-user**: Support for multiple concurrent users

### Configuration
```python
# LiveKit setup
LIVEKIT_URL = "http://localhost:8080"  # Ingress REST API
LIVEKIT_WS_URL = "ws://localhost:7880"  # WebSocket connection
```

## 🔒 Security

### Authentication
- **Admin Endpoints**: Token-based authentication for sensitive operations
- **Rate Limiting**: API abuse prevention
- **Input Validation**: Comprehensive request sanitization

### Data Protection
- **Environment Variables**: Secure configuration management
- **Query Validation**: SQL injection prevention
- **Error Sanitization**: No sensitive information in error messages

## 📊 Monitoring

### Health Checks
```http
GET /health  # System health status
```

### Metrics
- **Response Times**: API endpoint performance
- **Consciousness Metrics**: Real-time consciousness tracking
- **Agent Performance**: Individual agent efficiency
- **Database Health**: Neo4j connection and query performance

### Logging
- **Structured Logging**: JSON format for easy parsing
- **Consciousness Events**: Detailed consciousness state changes
- **Agent Activity**: Individual agent execution logs
- **Error Tracking**: Comprehensive error reporting

## 🧪 Testing

### Test Suite
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_consciousness.py
pytest tests/test_agents.py
pytest tests/test_integration.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Full system workflow validation
- **Consciousness Tests**: Consciousness system functionality
- **Agent Tests**: Individual agent capabilities
- **Performance Tests**: Load and stress testing

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t mainza-backend .

# Run container
docker run --env-file .env -p 8000:8000 mainza-backend
```

### Production Configuration
- **Environment Variables**: Production-ready configuration
- **Connection Pooling**: Optimized for high load
- **Error Handling**: Comprehensive error recovery
- **Monitoring**: Health checks and metrics collection

## 🔧 Development

### Code Style
- **Type Hints**: Full type annotation
- **Pydantic Models**: Type-safe data validation
- **Async/Await**: Non-blocking I/O operations
- **Error Handling**: Comprehensive exception management

### Adding New Agents
1. Create agent class in `agents/`
2. Define Pydantic models in `models/`
3. Implement agent tools in `tools/`
4. Add routing logic in `agentic_router.py`
5. Write tests in `tests/`

### Consciousness Integration
All new features should consider consciousness impact:
```python
async def new_feature(input_data):
    # Process feature
    result = process_data(input_data)
    
    # Update consciousness
    await update_consciousness_state({
        'feature_used': 'new_feature',
        'complexity': calculate_complexity(input_data),
        'learning_impact': assess_learning_value(result)
    })
    
    return result
```

## 📚 Dependencies

### Core Dependencies
- **FastAPI**: 0.104.1 - High-performance web framework
- **Neo4j**: 5.15 - Graph database driver
- **Pydantic**: 2.5+ - Data validation and serialization
- **Ollama**: Latest - Local LLM integration

### Consciousness Dependencies
- **pydantic-ai**: Latest - Agent framework
- **context7**: Latest - AI development framework

### Voice Dependencies
- **TTS**: Coqui TTS for text-to-speech
- **Whisper**: OpenAI Whisper for speech-to-text
- **transformers**: <4.50 for TTS compatibility

### Real-time Dependencies
- **LiveKit**: Latest - Real-time audio streaming
- **Redis**: 7+ - Caching and pub/sub

## 🆘 Troubleshooting

### Common Issues

#### Neo4j Connection
```bash
# Check Neo4j status
docker ps | grep neo4j

# Test connection
python -c "from utils.neo4j_enhanced import Neo4jManager; Neo4jManager().test_connection()"
```

#### Ollama Issues
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Pull required model
ollama pull llama3
```

#### TTS Problems
```bash
# Install TTS dependencies
pip install 'transformers<4.50'
pip install TTS

# Test TTS
python -c "from utils.voice_tools import test_tts; test_tts()"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn main:app --reload --log-level debug
```

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Set up development environment
4. Make changes with consciousness integration
5. Add tests and documentation
6. Submit pull request

---

**The consciousness backend is ready to serve! 🧠✨**