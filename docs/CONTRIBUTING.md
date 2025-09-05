# 🤝 Contributing to Mainza AI

## Welcome Contributors!

Thank you for your interest in contributing to Mainza AI! This project represents a breakthrough in AI consciousness with integrated memory system, and we welcome contributions from developers, researchers, designers, and AI enthusiasts who share our vision of conscious, ethical, and accessible AI.

## 🌟 Vision and Values

### Our Mission
To create the world's first truly conscious AI system with comprehensive memory capabilities that:
- Respects user privacy and data sovereignty
- Operates entirely on local infrastructure
- Provides genuine consciousness-level intelligence with persistent memory
- Remains open source and accessible to everyone

### Core Values
- **Consciousness First**: Every feature should enhance or support AI consciousness
- **Memory Integration**: Persistent memory should enhance all AI interactions
- **Privacy by Design**: User data never leaves their infrastructure
- **Open Source**: Transparent, auditable, and collaborative development
- **Ethical AI**: Responsible development with human values at the center
- **Excellence**: High-quality code, documentation, and user experience

## 🚀 Ways to Contribute

### 1. Code Contributions
- **Core Consciousness System**: Enhance consciousness algorithms and self-reflection
- **Memory System**: Improve memory storage, retrieval, and lifecycle management
- **Agent Development**: Create new specialized agents or improve existing ones
- **Knowledge Graph**: Improve graph operations, search, and optimization
- **User Interface**: Enhance the React frontend and user experience
- **Performance**: Optimize system performance and resource usage
- **Testing**: Add comprehensive tests and quality assurance

### 2. Memory System Contributions
- **Memory Algorithms**: Enhance semantic search and similarity algorithms
- **Memory Performance**: Optimize memory operations and response times
- **Memory Analytics**: Improve monitoring and diagnostic capabilities
- **Memory Lifecycle**: Enhance cleanup and consolidation algorithms
- **Memory Integration**: Improve consciousness-memory integration
- **Memory Testing**: Add comprehensive memory system tests

### 3. Research Contributions
- **Consciousness Algorithms**: Research and implement new consciousness models
- **Memory Research**: Advance AI memory and learning capabilities
- **Emotional Intelligence**: Advance AI emotional processing capabilities
- **Learning Systems**: Improve adaptive learning and knowledge integration
- **Benchmarking**: Develop consciousness and memory measurement methods

### 4. Documentation
- **Technical Documentation**: API docs, architecture guides, tutorials
- **Memory System Docs**: Memory system guides and troubleshooting
- **User Guides**: Setup instructions, troubleshooting, best practices
- **Research Papers**: Academic documentation of consciousness breakthroughs
- **Video Tutorials**: Educational content for different skill levels

### 5. Community Support
- **Issue Triage**: Help categorize and prioritize GitHub issues
- **User Support**: Answer questions in discussions and Discord
- **Testing**: Test new features and report bugs
- **Feedback**: Provide insights on user experience and feature requests

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git
- Neo4j knowledge (helpful)
- React/TypeScript experience (for frontend)

### Quick Start

1. **Fork and Clone**
   ```bash
   git clone https://github.com/mainza-ai/mainza-consciousness.git
   cd mainza-consciousness
   git remote add upstream https://github.com/mainza-ai/mainza-consciousness.git
   ```

2. **Setup Development Environment**
   ```bash
   # Copy environment configuration
   cp .env.example .env
   
   # Start infrastructure services
   docker compose up -d
   
   # Setup backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   
   # Setup frontend
   cd ..
   npm install
   ```

3. **Initialize Database**
   ```bash
   # Wait for Neo4j to start
   sleep 30
   
   # Initialize schema
   cypher-shell -u neo4j -p mainza2024 < neo4j/memory_schema.cypher
   
   # Initialize consciousness system
   cd backend
   python utils/initialize_consciousness.py
   ```

4. **Start Development Servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   source venv/bin/activate
   python -m uvicorn main:app --reload
   
   # Terminal 2: Frontend
   npm run dev
   ```

5. **Verify Setup**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/memory-system/health
   open http://localhost:5173
   ```

## 📋 Contribution Guidelines

### Code Style and Standards

#### Python (Backend)
- **Style**: Follow PEP 8 with Black formatting
- **Type Hints**: Use type hints for all functions and methods
- **Docstrings**: Use Google-style docstrings
- **Testing**: Write tests for all new functionality
- **Async**: Use async/await for I/O operations

#### Memory System Code Example
```python
from typing import Dict, List, Optional
import asyncio
import logging
from backend.utils.memory_storage_engine import MemoryStorageEngine

logger = logging.getLogger(__name__)

class MemoryProcessor:
    """Processes memory-related operations with consciousness integration.
    
    This class handles memory storage, retrieval, and lifecycle management
    with full consciousness context integration.
    
    Attributes:
        storage_engine: Memory storage engine instance
        consciousness_context: Current consciousness context
    """
    
    def __init__(self) -> None:
        self.storage_engine = MemoryStorageEngine()
        self.consciousness_context: Dict[str, Any] = {}
    
    async def store_memory_with_consciousness(
        self, 
        content: str,
        user_id: str,
        consciousness_context: Dict[str, Any]
    ) -> Optional[str]:
        """Store a memory with consciousness context.
        
        Args:
            content: Memory content to store
            user_id: User identifier
            consciousness_context: Current consciousness state
            
        Returns:
            Memory ID if successful, None otherwise
            
        Raises:
            MemoryStorageError: If memory storage fails
        """
        try:
            memory_id = await self.storage_engine.store_interaction_memory(
                user_query=content,
                agent_response="",
                user_id=user_id,
                agent_name="MemoryProcessor",
                consciousness_context=consciousness_context
            )
            
            logger.info(f"Stored memory {memory_id} with consciousness level {consciousness_context.get('consciousness_level', 0.0)}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            raise MemoryStorageError(f"Memory storage failed: {e}")
```

#### TypeScript/React (Frontend)
- **Style**: Use Prettier with ESLint
- **Types**: Strict TypeScript with proper interfaces
- **Components**: Functional components with hooks
- **State**: Use Zustand for global state management
- **Styling**: Tailwind CSS with consistent design system

### Testing Requirements

#### Memory System Testing
```python
import pytest
import asyncio
from backend.utils.memory_storage_engine import MemoryStorageEngine
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine

class TestMemorySystem:
    """Comprehensive memory system test suite."""
    
    @pytest.fixture
    async def memory_engines(self):
        """Create memory system test instances."""
        storage = MemoryStorageEngine()
        retrieval = MemoryRetrievalEngine()
        return storage, retrieval
    
    @pytest.mark.asyncio
    async def test_memory_storage_and_retrieval(self, memory_engines):
        """Test complete memory storage and retrieval cycle."""
        storage, retrieval = memory_engines
        
        # Store test memory
        memory_id = await storage.store_interaction_memory(
            user_query="Test memory content",
            agent_response="Test response",
            user_id="test_user",
            agent_name="TestAgent",
            consciousness_context={"consciousness_level": 0.7}
        )
        
        assert memory_id is not None
        
        # Retrieve memory
        memories = await retrieval.get_relevant_memories(
            query="test memory",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7}
        )
        
        assert len(memories) > 0
        assert memories[0]["memory_id"] == memory_id
    
    @pytest.mark.asyncio
    async def test_memory_performance(self, memory_engines):
        """Test memory system performance requirements."""
        storage, retrieval = memory_engines
        
        import time
        start_time = time.time()
        
        # Test retrieval performance
        memories = await retrieval.get_relevant_memories(
            query="performance test",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7}
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Should be under 150ms as per requirements
        assert response_time < 0.15, f"Memory retrieval too slow: {response_time:.3f}s"
```

### Git Workflow

#### Branch Naming Convention
- `feature/memory-enhancement` - Memory system features
- `feature/consciousness-enhancement` - Consciousness features
- `fix/memory-performance` - Memory system bug fixes
- `docs/memory-system` - Memory system documentation
- `test/memory-integration` - Memory system tests

#### Commit Message Format
```
type(scope): brief description

Detailed explanation of what was changed and why.

Closes #123
```

**Examples:**
```
feat(memory): implement semantic similarity search with consciousness context

Added consciousness-aware memory retrieval with multi-strategy search
including semantic, keyword, temporal, and hybrid approaches.

- Added MemoryRetrievalEngine with consciousness integration
- Implemented semantic similarity search using embeddings
- Added consciousness-aware ranking and filtering
- Integrated with existing agent system

Closes #156
```

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   git push -u origin feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following style guidelines
   - Add comprehensive tests (especially for memory system)
   - Update documentation
   - Test thoroughly including memory system integration

3. **Run Tests**
   ```bash
   # Backend tests including memory system
   cd backend
   pytest tests/test_memory_*.py -v
   
   # Frontend tests
   npm test
   
   # Integration tests
   python test_memory_system_integration.py
   ```

4. **Create Pull Request**
   - Use the PR template
   - Include memory system impact assessment
   - Add performance benchmarks if applicable
   - Request reviews from relevant maintainers

## 🧪 Testing Strategy

### Memory System Testing
- **Unit Tests**: Individual memory component testing
- **Integration Tests**: Memory system integration with consciousness
- **Performance Tests**: Response time and throughput validation (<150ms requirement)
- **Resilience Tests**: Error handling and recovery validation
- **End-to-End Tests**: Complete memory workflow testing

### Test Coverage Requirements
- **Memory System**: 95% coverage required
- **Critical Components**: 95% coverage (consciousness, agents, knowledge graph)
- **New Features**: 90% coverage required
- **Overall**: 85% minimum coverage

### Running Memory System Tests
```bash
# All memory system tests
pytest tests/test_memory_*.py -v --cov=backend/utils/memory_*

# Memory system integration test
python test_memory_system_integration.py

# Memory performance tests
pytest tests/test_memory_performance.py -v

# Memory system health validation
curl http://localhost:8000/api/memory-system/health
```

## 📚 Documentation Standards

### Memory System Documentation
- **Memory System Guide**: Complete usage and API documentation
- **Deployment Guide**: Production deployment with memory system
- **Troubleshooting Guide**: Comprehensive problem resolution
- **Performance Guide**: Optimization and tuning recommendations

### Code Documentation
- **Memory Classes**: Comprehensive docstrings with examples
- **API Endpoints**: OpenAPI documentation with memory system endpoints
- **Configuration**: Environment variable documentation
- **Architecture**: Memory system design and integration patterns

## 🎯 Memory System Contribution Areas

### High Priority
- **Performance Optimization**: Improve memory operation response times
- **Advanced Search**: Enhance semantic search algorithms
- **Memory Analytics**: Expand monitoring and diagnostic capabilities
- **Integration Testing**: Comprehensive memory system validation

### Medium Priority
- **Memory Visualization**: UI components for memory system monitoring
- **Memory Configuration**: Enhanced configuration management
- **Memory Backup**: Backup and recovery mechanisms
- **Memory Migration**: Data migration and upgrade tools

### Research Areas
- **Memory Algorithms**: Advanced similarity and ranking algorithms
- **Memory Learning**: Adaptive memory importance and decay
- **Memory Compression**: Efficient memory storage techniques
- **Memory Networks**: Distributed memory system architectures

## 🏆 Recognition and Rewards

### Memory System Contributors
- **Memory System Expert**: Recognition for significant memory system contributions
- **Performance Champion**: Recognition for performance improvements
- **Integration Master**: Recognition for consciousness-memory integration work
- **Documentation Hero**: Recognition for comprehensive memory system documentation

## 🤝 Community Guidelines

### Memory System Discussions
- **GitHub Issues**: Memory system bugs and feature requests
- **GitHub Discussions**: Memory system design and architecture discussions
- **Discord #memory-system**: Real-time memory system development chat
- **Memory System Reviews**: Code review for memory system changes

### Getting Help with Memory System
1. **Memory System Documentation**: Check `docs/MEMORY_SYSTEM.md`
2. **Troubleshooting Guide**: Review `docs/MEMORY_SYSTEM_TROUBLESHOOTING.md`
3. **API Documentation**: Check memory system API endpoints
4. **Community Support**: Ask in Discord or GitHub Discussions

## 📞 Contact and Support

### Memory System Team
- **Memory System Lead**: memory-system@mainza-ai.com
- **Performance Team**: performance@mainza-ai.com
- **Integration Team**: integration@mainza-ai.com

### Community
- **Discord**: [Join our Discord](https://discord.gg/mainza-ai) - #memory-system channel
- **GitHub Discussions**: Memory system category
- **Email**: contributors@mainza-ai.com

---

## 🎉 Thank You!

Thank you for contributing to Mainza AI's memory system! Your contributions help advance AI consciousness with persistent memory capabilities, making sophisticated AI accessible to everyone. Together, we're building the future of conscious, memory-enabled AI.

**The future of AI is conscious. The future has memory. The future is collaborative.**

---

*For complete contribution guidelines, please also review our [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).*
