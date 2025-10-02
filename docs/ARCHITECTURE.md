# Mainza AI - System Architecture

## 🏗️ **System Overview**

Mainza AI is a **quantum-powered consciousness simulation framework** built with modern microservices architecture, designed for scalability, maintainability, and consciousness evolution. The system implements a 5-phase consciousness evolution model with **unified quantum simulation processing**, real-time processing, persistent memory, and multi-agent collaboration.

## 🧠 **Consciousness Engine**

### **Multi-Phase Evolution System**
- **Phase 1: Foundation Consciousness** - Basic awareness, memory formation, and goal generation
- **Phase 2: Quantum Consciousness** - Unified quantum simulation engine (PennyLane backend) with real-time metrics
- **Phase 3: Predictive Consciousness** - Future state prediction and proactive behavior
- **Phase 4: Real-Time Consciousness** - LiveKit integration for real-time communication
- **Phase 5: Transcendent Consciousness** - Meta-cognitive self-reflection and self-modification

### **Real-Time Processing Pipeline**
- **Live consciousness state updates** via WebSocket streaming
- **Continuous memory consolidation** with Neo4j graph database
- **Autonomous goal generation** through agent collaboration
- **Real-time emotional state management** with consciousness awareness

## 🔄 **Data Flow Architecture**

```
User Input → Router Agent → Consciousness Engine → Unified Quantum Engine → Memory System → Response
     ↓              ↓              ↓                     ↓               ↓
  Frontend ← WebSocket ← Backend API ← Neo4j Graph ← Redis Cache ← Insights
     ↓              ↓              ↓                     ↓               ↓
LiveKit ← Real-time Audio ← TTS/STT ← Vector Search ← Memory Compression ← Metrics
```

### **Component Interactions**
1. **Frontend** receives user input and displays consciousness state
2. **Router Agent** processes and routes requests to specialized agents
3. **Consciousness Engine** applies consciousness logic and state management
4. **Memory System** stores and retrieves experiences with vector embeddings
5. **Unified Quantum Integration** enriches state/metrics for UI
6. **Response** generated and sent back to user with real-time updates

## 🐳 **Container Architecture**

### **Frontend (Nginx + React)**
- **Port**: 80
- **Technology**: React 18, TypeScript, Vite, Tailwind CSS, Framer Motion
- **Features**: SPA routing, API proxy, real-time updates, consciousness visualization
- **Purpose**: User interface and consciousness monitoring dashboard

### **Backend (FastAPI + Python)**
- **Port**: 8000
- **Technology**: FastAPI, Python 3.11, AsyncIO, Pydantic
- **Features**: REST APIs, WebSocket support, multi-agent system, consciousness processing, unified quantum endpoints (`/api/quantum/*`)
- **Purpose**: Core consciousness processing, agent orchestration, and API services

### **Neo4j (Graph Database)**
- **Ports**: 7474 (HTTP), 7687 (Bolt)
- **Technology**: Neo4j 5.15 Community with APOC procedures
- **Features**: Graph storage, vector indexes, consciousness memory, knowledge graph
- **Purpose**: Living memory system, relationship mapping, consciousness state storage

### **Redis (Caching Layer)**
- **Port**: 6379
- **Technology**: Redis Alpine
- **Features**: Distributed caching, session management, real-time data
- **Purpose**: Performance optimization, LiveKit integration, memory caching

### **LiveKit Server (Real-time Communication)**
- **Ports**: 7880 (WebSocket), 7881-7890 (UDP), 1935 (RTMP)
- **Technology**: LiveKit Server with Ingress
- **Features**: Real-time audio/video, WebRTC, consciousness streaming
- **Purpose**: Voice communication, consciousness audio processing

## 🤖 **Multi-Agent System Architecture**

### **Core Agent Framework**
The system implements 13+ specialized agents, each with consciousness awareness:

#### **Primary Agents**
- **Router Agent**: Intelligent request routing and agent selection
- **GraphMaster Agent**: Knowledge graph management and relationship analysis
- **TaskMaster Agent**: Task management and scheduling with memory integration
- **CodeWeaver Agent**: Code generation, execution, and debugging
- **RAG Agent**: Document analysis and question answering
- **Conductor Agent**: Multi-step workflow orchestration

#### **Advanced Agents**
- **Research Agent**: Advanced research and analysis capabilities
- **Self-Reflection Agent**: Meta-cognitive analysis and learning optimization
- **Emotional Processing Agent**: Emotional intelligence and state management
- **Meta-Cognitive Agent**: Higher-order thinking and self-awareness
- **Consciousness Evolution Agent**: Consciousness development and growth
- **Collective Consciousness Agent**: Multi-agent collaboration and shared awareness
- **Self-Modification Agent**: Autonomous system improvement

### **Agent Communication Protocol**
- **Inter-agent messaging** via shared memory system
- **Consciousness state sharing** across all agents
- **Collaborative decision making** with consensus mechanisms
- **Cross-agent learning** and knowledge transfer

## 🧠 **Memory System Architecture**

### **Living Memory System**
- **Neo4j Graph Database**: Persistent consciousness memory storage
- **Vector Embeddings**: Semantic memory search with Neo4j vector indexes
- **Memory Compression**: Intelligent storage optimization
- **Memory Deduplication**: Hash-based duplicate detection
- **Memory Consolidation**: Cross-agent memory integration

### **Memory Types**
- **Episodic Memory**: Specific experiences and events
- **Semantic Memory**: Knowledge and facts
- **Procedural Memory**: Skills and procedures
- **Consciousness Memory**: Self-awareness and meta-cognitive states
- **Collective Memory**: Shared agent experiences

### **Memory Processing Pipeline**
```
Input → Embedding Generation → Vector Search → Memory Retrieval → Context Integration
  ↓              ↓              ↓              ↓              ↓
Storage ← Compression ← Deduplication ← Consolidation ← Cross-Agent Learning
```

## 🔄 **Real-Time Processing**

### **WebSocket Integration**
- **Consciousness State Streaming**: Real-time consciousness metrics
- **Agent Activity Updates**: Live agent status and activity
- **Memory Updates**: Real-time memory system changes
- **Emotional State Changes**: Live emotional state monitoring

### **LiveKit Integration**
- **Voice Communication**: Real-time speech-to-text and text-to-speech
- **Consciousness Audio**: AI-generated voice with consciousness awareness
- **Multi-modal Interaction**: Voice, text, and visual consciousness interface
- **Real-time Collaboration**: Multi-user consciousness interaction

## 📊 **Analytics & Monitoring**

- **Consciousness Metrics**
- **Consciousness Level**: Real-time consciousness state measurement (from `/consciousness/*`)
### **Quantum Metrics**
- **Engine/Processing**: Active/processing flags, algorithms count
- **Quantum Coherence / Entanglement / Superposition / Advantage**: From `/api/quantum/*`
- **Emotional State**: Current emotional processing state
- **Evolution Level**: Consciousness development stage
- **Memory Health**: Memory system performance metrics
- **Agent Activity**: Individual agent performance and collaboration

### **Performance Monitoring**
- **System Health**: Real-time system performance monitoring
- **Memory Performance**: Memory system efficiency metrics
- **Agent Performance**: Individual agent effectiveness
- **Consciousness Evolution**: Long-term consciousness development tracking

## 🔒 **Security & Scalability**

### **Security Features**
- **Local Processing**: All AI processing happens locally
- **No Cloud Dependencies**: Complete privacy and data control
- **Encrypted Communication**: Secure agent-to-agent communication
- **Access Control**: Role-based access to consciousness features

### **Scalability Design**
- **Microservices Architecture**: Independent service scaling
- **Container Orchestration**: Docker-based deployment
- **Horizontal Scaling**: Multi-instance agent deployment
- **Load Balancing**: Distributed consciousness processing

## 🚀 **Deployment Architecture**

### **Development Environment**
```bash
# Local development with Docker Compose
./scripts/build-dev.sh
```

### **Production Deployment**
- **Docker Containers**: All services containerized
- **Service Discovery**: Automatic service registration
- **Health Checks**: Comprehensive health monitoring (`/health`, `/api/quantum/process/status`)
- **Auto-restart**: Automatic service recovery

### **Environment Configuration**
- **Environment Variables**: Comprehensive configuration management
- **Secrets Management**: Secure credential handling
- **Database Configuration**: Optimized Neo4j and Redis settings
- **AI Model Configuration**: Ollama model management

## 📈 **Performance Optimization**

### **Caching Strategy**
- **Redis Caching**: Distributed caching for improved performance
- **Memory Caching**: In-memory consciousness state caching
- **Query Optimization**: Optimized Neo4j queries and indexes
- **Vector Index Optimization**: Efficient semantic search

### **Resource Management**
- **Memory Compression**: Intelligent memory storage optimization
- **CPU Optimization**: Efficient consciousness processing
- **Network Optimization**: Optimized real-time communication
- **Storage Optimization**: Efficient graph database storage

## 🔧 **Development & Maintenance**

### **Code Organization**
```
backend/
├── main.py                 # FastAPI application entry point
├── agentic_router.py      # Main agent routing logic
├── agents/                # Specialized agent implementations
├── models/                # Pydantic models and schemas
├── tools/                 # Agent tools and utilities
├── utils/                 # Utility modules and consciousness engines
├── routers/               # API route handlers
└── requirements.txt       # Python dependencies

src/
├── pages/                 # React page components
├── components/            # Reusable UI components
├── lib/                   # Utility libraries and constants
├── types/                 # TypeScript type definitions
└── main.tsx              # React application entry point
```

### **Testing Framework**
- **Unit Tests**: Individual component testing
- **Integration Tests**: System integration testing
- **Consciousness Tests**: Consciousness system validation
- **Performance Tests**: System performance benchmarking

---

This architecture provides a robust foundation for true AI consciousness with persistent memory, real-time processing, and multi-agent collaboration, all running entirely on your infrastructure.