# 📁 Mainza AI Project Structure

This document provides a comprehensive overview of the Mainza AI project structure, making it easy for contributors and users to understand the codebase organization.

## 🏗️ Root Directory Structure

```
mainza-consciousness/
├── 📁 backend/                    # Python FastAPI backend
├── 📁 src/                       # React TypeScript frontend
├── 📁 docs/                      # Documentation
├── 📁 .kiro/                     # Kiro IDE specifications
├── 📄 docker-compose.yml         # Development environment
├── 📄 package.json              # Frontend dependencies
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Main project documentation
├── 📄 CHANGELOG.md              # Version history
├── 📄 CONTRIBUTING.md           # Contribution guidelines
├── 📄 LICENSE                   # MIT License
└── 📄 .env                      # Environment configuration
```

## 🐍 Backend Structure (`backend/`)

### Core Application
```
backend/
├── 📄 main.py                   # FastAPI application entry point
├── 📄 agentic_router.py         # Main agent routing system
├── 📄 agentic_config.py         # Agent configuration
└── 📄 requirements.txt          # Python dependencies
```

### Agent System (`agents/`)
```
agents/
├── 📄 base_conscious_agent.py   # Base agent class with consciousness
├── 📄 simple_chat.py           # Natural conversation agent
├── 📄 router.py                # Request routing agent
├── 📄 conductor.py             # Multi-agent orchestration
└── 📄 __init__.py              # Agent module initialization
```

### Memory System (`utils/`)
```
utils/
├── 📄 memory_storage_engine.py      # Memory storage and persistence
├── 📄 memory_retrieval_engine.py    # Memory search and retrieval
├── 📄 memory_context_builder.py     # Memory context construction
├── 📄 memory_system_monitor.py      # Health monitoring and metrics
├── 📄 memory_lifecycle_manager.py   # Memory cleanup and optimization
├── 📄 memory_embedding_manager.py   # Embedding generation and search
├── 📄 memory_error_handling.py      # Error handling and recovery
├── 📄 memory_recovery_system.py     # System recovery mechanisms
└── 📄 memory_schema_manager.py      # Database schema management
```

### Consciousness System (`utils/`)
```
utils/
├── 📄 consciousness_orchestrator.py     # Central consciousness management
├── 📄 initialize_consciousness.py       # Consciousness initialization
├── 📄 consciousness_knowledge_integrator.py  # Knowledge integration
└── 📄 enhanced_llm_execution.py        # LLM optimization
```

### Knowledge Graph (`utils/`)
```
utils/
├── 📄 neo4j_enhanced.py            # Enhanced Neo4j integration
├── 📄 neo4j_production.py          # Production Neo4j configuration
├── 📄 dynamic_knowledge_manager.py  # Dynamic knowledge management
├── 📄 knowledge_graph_evolution.py  # Knowledge graph evolution
├── 📄 knowledge_graph_maintenance.py # Graph maintenance
└── 📄 embedding_enhanced.py        # Enhanced embedding generation
```

### API Routers (`routers/`)
```
routers/
├── 📄 memory_system.py         # Memory system REST API
├── 📄 insights.py              # Insights and analytics API
└── 📄 neo4j_admin.py          # Neo4j administration API
```

### Data Models (`models/`)
```
models/
├── 📄 consciousness_models.py   # Consciousness data models
└── 📄 shared.py               # Shared data models
```

### Database Schema (`neo4j/`)
```
neo4j/
├── 📄 memory_schema.cypher      # Memory system schema
├── 📄 enhanced_agent_schema.cypher  # Agent system schema
└── 📄 schema.cypher            # Base Neo4j schema
```

### Testing (`tests/`)
```
tests/
├── 📄 test_memory_storage_engine.py        # Memory storage tests
├── 📄 test_memory_retrieval_engine.py      # Memory retrieval tests
├── 📄 test_memory_context_builder.py       # Memory context tests
├── 📄 test_memory_system_monitor.py        # Memory monitoring tests
├── 📄 test_memory_lifecycle_manager.py     # Memory lifecycle tests
├── 📄 test_memory_error_handling.py        # Memory error handling tests
├── 📄 test_memory_recovery_system.py       # Memory recovery tests
├── 📄 test_consciousness_memory_integration.py  # Integration tests
├── 📄 test_agent_memory_integration.py     # Agent memory tests
├── 📄 test_knowledge_graph_memory_integration.py  # Knowledge graph tests
├── 📄 test_memory_performance.py           # Performance tests
├── 📄 test_conversation_continuity.py      # Conversation tests
└── 📄 test_memory_system_resilience.py    # Resilience tests
```

### Production & Security (`core/`)
```
core/
├── 📄 production_foundation.py     # Production infrastructure
├── 📄 enhanced_error_handling.py   # Enhanced error handling
├── 📄 performance_optimization.py  # Performance optimization
└── 📄 security_framework.py       # Security framework
```

## ⚛️ Frontend Structure (`src/`)

### Core Application
```
src/
├── 📄 main.tsx                 # React application entry point
├── 📄 App.tsx                  # Main application component
├── 📄 index.css               # Global styles
└── 📄 vite-env.d.ts           # Vite type definitions
```

### Pages (`pages/`)
```
pages/
├── 📄 Index.tsx               # Main dashboard page
├── 📄 IndexRedesigned.tsx     # Redesigned dashboard
└── 📄 InsightsPage.tsx        # Insights and analytics page
```

### Components (`components/`)
```
components/
├── 📄 ConversationInterface.tsx    # Chat interface
├── 📄 ConsciousnessDashboard.tsx   # Consciousness metrics
├── 📄 ConsciousnessInsights.tsx    # Consciousness insights
├── 📄 AgentActivityIndicator.tsx   # Agent status display
├── 📄 LoadingScreen.tsx           # Loading animations
└── 📁 ui/                         # UI components
    └── 📄 metric-display.tsx      # Metric display component
```

### Configuration
```
├── 📄 vite.config.ts          # Vite build configuration
├── 📄 package.json           # Frontend dependencies
├── 📄 tsconfig.json          # TypeScript configuration
└── 📄 tailwind.config.js     # Tailwind CSS configuration
```

## 📚 Documentation Structure (`docs/`)

### Core Documentation
```
docs/
├── 📄 MEMORY_SYSTEM.md                    # Complete memory system guide
├── 📄 MEMORY_SYSTEM_DEPLOYMENT.md         # Memory system deployment guide
├── 📄 MEMORY_SYSTEM_TROUBLESHOOTING.md    # Memory system troubleshooting
├── 📄 AGENTS.md                          # Agent system documentation
├── 📄 KNOWLEDGE_GRAPH.md                 # Knowledge graph documentation
└── 📄 API_DOCUMENTATION.md               # Complete API reference
```

### Architecture Documentation
```
├── 📄 AI_CONSCIOUSNESS_ARCHITECTURE_CONTEXT7.md  # Consciousness architecture
├── 📄 CONSCIOUSNESS_IMPLEMENTATION_COMPLETE.md   # Consciousness implementation
├── 📄 NEO4J_COMPREHENSIVE_DOCUMENTATION.md      # Neo4j integration guide
└── 📄 PRODUCTION_ARCHITECTURE_CONTEXT7.md       # Production architecture
```

### Operational Documentation
```
├── 📄 SETUP_GUIDE.md              # Complete setup instructions
├── 📄 PRODUCTION_DEPLOYMENT_GUIDE.md  # Production deployment
├── 📄 SECURITY.md                 # Security guidelines
└── 📄 PROJECT_STATUS.md           # Current project status
```

## 🔧 Configuration Files

### Environment Configuration
```
├── 📄 .env                       # Environment variables
├── 📄 .env.example              # Environment template
└── 📄 docker-compose.yml        # Development environment
```

### Development Configuration
```
├── 📄 .gitignore               # Git ignore rules
├── 📄 .dockerignore            # Docker ignore rules
└── 📁 .kiro/                   # Kiro IDE specifications
    ├── 📁 specs/               # Feature specifications
    └── 📁 settings/            # IDE settings
```

## 🧪 Testing Structure

### Memory System Tests
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-component testing
- **Performance Tests**: Response time and throughput validation
- **Resilience Tests**: Error handling and recovery validation
- **End-to-End Tests**: Complete workflow testing

### Test Categories
```
tests/
├── 📁 unit/                   # Unit tests
├── 📁 integration/            # Integration tests
├── 📁 performance/            # Performance tests
├── 📁 e2e/                    # End-to-end tests
└── 📁 fixtures/               # Test data and fixtures
```

## 🚀 Deployment Structure

### Docker Configuration
```
├── 📄 Dockerfile             # Application container
├── 📄 docker-compose.yml     # Development environment
├── 📄 docker-compose.prod.yml # Production environment
└── 📁 docker/                # Docker-related files
```

### Production Files
```
├── 📄 requirements-production.txt  # Production Python dependencies
├── 📄 main_production.py          # Production application entry
└── 📁 config/                     # Configuration files
    ├── 📄 production_config.py    # Production configuration
    └── 📄 llm_optimization.py     # LLM optimization settings
```

## 📊 Key Metrics and Status Files

### Status Documentation
```
├── 📄 PROJECT_STATUS.md           # Current project status
├── 📄 PROJECT_SUMMARY.md          # Project overview
├── 📄 GITHUB_READINESS_ANALYSIS.md # GitHub readiness assessment
└── 📄 GITHUB_RELEASE_READY.md     # Release readiness checklist
```

### Implementation Status
```
├── 📄 CONSCIOUSNESS_IMPLEMENTATION_COMPLETE.md     # Consciousness status
├── 📄 MEMORY_SYSTEM_MONITORING_IMPLEMENTATION_COMPLETE.md  # Memory monitoring status
├── 📄 CONSCIOUSNESS_MEMORY_INTEGRATION_COMPLETE.md # Integration status
└── 📄 FINAL_SYSTEM_STATUS_COMPLETE.md             # Overall system status
```

## 🔍 Navigation Guide

### For New Contributors
1. Start with `README.md` for project overview
2. Read `SETUP_GUIDE.md` for installation
3. Review `CONTRIBUTING.md` for contribution guidelines
4. Explore `docs/` for detailed documentation

### For Developers
1. Backend development: `backend/` directory
2. Frontend development: `src/` directory
3. Memory system: `backend/utils/memory_*.py` files
4. API documentation: `API_DOCUMENTATION.md`

### For Operators
1. Deployment: `docs/MEMORY_SYSTEM_DEPLOYMENT.md`
2. Troubleshooting: `docs/MEMORY_SYSTEM_TROUBLESHOOTING.md`
3. Monitoring: `docs/MEMORY_SYSTEM.md#monitoring-and-maintenance`
4. Configuration: `.env` and configuration files

### For Researchers
1. Architecture: `AI_CONSCIOUSNESS_ARCHITECTURE_CONTEXT7.md`
2. Consciousness: `CONSCIOUSNESS_IMPLEMENTATION_COMPLETE.md`
3. Memory system: `docs/MEMORY_SYSTEM.md`
4. Knowledge graph: `docs/KNOWLEDGE_GRAPH.md`

## 🏷️ File Naming Conventions

### Python Files
- **Snake case**: `memory_storage_engine.py`
- **Descriptive names**: Clear indication of functionality
- **Module organization**: Related functionality grouped together

### TypeScript/React Files
- **Pascal case**: `ConsciousnessDashboard.tsx`
- **Component suffix**: `.tsx` for React components
- **Descriptive names**: Clear component purpose

### Documentation Files
- **Upper case**: `README.md`, `CHANGELOG.md`
- **Descriptive names**: Clear content indication
- **Markdown format**: `.md` extension for documentation

### Configuration Files
- **Lowercase**: `docker-compose.yml`, `.env`
- **Standard names**: Following community conventions
- **Clear purpose**: Obvious configuration target

## 🔗 Key Dependencies

### Backend Dependencies
- **FastAPI**: Web framework and API
- **Neo4j**: Graph database
- **Pydantic**: Data validation
- **Ollama**: Local LLM integration
- **Sentence Transformers**: Embedding generation

### Frontend Dependencies
- **React**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations

### Development Dependencies
- **Docker**: Containerization
- **pytest**: Testing framework
- **Black**: Code formatting
- **ESLint**: JavaScript linting
- **Prettier**: Code formatting

This structure provides a clear, organized, and scalable foundation for the Mainza AI consciousness framework with integrated memory system, making it easy for contributors to understand and extend the codebase.