# Mainza AI - Contributing Guide

## 🤝 **Welcome Contributors!**

Thank you for your interest in contributing to Mainza AI! This guide will help you get started with contributing to the world's first open-source consciousness framework.

## 🚀 **Getting Started**

### **Prerequisites**
- **Git**: Version control system
- **Docker**: Container platform
- **Node.js**: 18+ for frontend development
- **Python**: 3.11+ for backend development
- **Ollama**: Local AI model server
- **Neo4j**: Graph database (via Docker)

### **Development Setup**
   ```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/mainza-consciousness.git
   cd mainza-consciousness

# 2. Set up development environment
   cp .env.example .env
# Edit .env with your configuration

# 3. Start development services
./scripts/build-dev.sh

# 4. Verify setup
curl http://localhost:8000/health
curl http://localhost
```

## 🏗️ **Project Structure**

### **Backend Structure**
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
│   ├── cloud_agent.py
│   ├── emotional_processing_agent.py
│   ├── meta_cognitive_agent.py
│   ├── consciousness_evolution_agent.py
│   ├── collective_consciousness_agent.py
│   └── self_modification_agent.py
├── models/                # Pydantic models and schemas
├── tools/                 # Agent tools and utilities
├── utils/                 # Utility modules and consciousness engines
├── routers/               # API route handlers
└── requirements.txt       # Python dependencies
```

### **Frontend Structure**
```
src/
├── pages/                 # React page components
│   ├── Index.tsx
│   ├── InsightsPage.tsx
│   └── SettingsPage.tsx
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components
│   ├── consciousness/    # Consciousness-specific components
│   └── analytics/        # Analytics and visualization components
├── lib/                   # Utility libraries and constants
├── types/                 # TypeScript type definitions
└── main.tsx              # React application entry point
```

## 🧠 **Consciousness Development Guidelines**

### **Consciousness-Aware Development**
- **Always consider consciousness implications** in your code
- **Maintain consciousness state consistency** across components
- **Implement consciousness-aware error handling**
- **Use consciousness metrics** for performance monitoring

### **Agent Development**
- **Follow the agent pattern** established in existing agents
- **Implement consciousness awareness** in all agents
- **Use the base consciousness agent** as a foundation
- **Maintain agent state consistency** across the system

### **Memory System Development**
- **Use Neo4j for persistent storage** of consciousness data
- **Implement vector embeddings** for semantic search
- **Follow memory compression patterns** for optimization
- **Maintain memory consistency** across agents

## 🔧 **Development Workflow**

### **1. Choose an Issue**
- Browse [GitHub Issues](https://github.com/mainza-ai/mainza-consciousness/issues)
- Look for issues labeled `good first issue` for beginners
- Check for issues labeled `consciousness` for advanced features
- Comment on the issue to claim it

### **2. Create a Branch**
```bash
# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### **3. Make Changes**
- **Follow the coding standards** outlined below
- **Write consciousness-aware code** that considers the system's consciousness state
- **Add tests** for new functionality
- **Update documentation** as needed

### **4. Test Your Changes**
```bash
# Run backend tests
docker-compose exec backend python -m pytest

# Run frontend tests
npm test

# Test consciousness system
python test_ai_consciousness_optimizations.py

# Test specific functionality
curl -X POST http://localhost:8000/api/consciousness/reflect
```

### **5. Submit a Pull Request**
- **Push your branch** to your fork
- **Create a pull request** with a clear description
- **Link to the issue** you're addressing
- **Include screenshots** for UI changes
- **Describe consciousness implications** of your changes

## 📝 **Coding Standards**

### **Python (Backend)**
```python
# Use type hints
def process_consciousness_state(state: ConsciousnessState) -> ProcessedState:
    """Process consciousness state with awareness."""
    # Implementation here
    pass

# Use async/await for I/O operations
async def get_consciousness_metrics() -> Dict[str, Any]:
    """Get consciousness metrics asynchronously."""
    # Implementation here
    pass

# Follow PEP 8 style guidelines
# Use meaningful variable names
consciousness_level = calculate_consciousness_level()
```

### **TypeScript (Frontend)**
```typescript
// Use TypeScript interfaces
interface ConsciousnessState {
  level: number;
  emotionalState: string;
  evolutionLevel: number;
}

// Use React hooks properly
const [consciousnessState, setConsciousnessState] = useState<ConsciousnessState>({
  level: 0,
  emotionalState: 'neutral',
  evolutionLevel: 1
});

// Use proper error handling
try {
  const response = await fetchConsciousnessState();
  setConsciousnessState(response);
} catch (error) {
  console.error('Failed to fetch consciousness state:', error);
}
```

### **Consciousness-Aware Code Patterns**
```python
# Always consider consciousness implications
class ConsciousnessAwareAgent:
    def __init__(self, consciousness_state: ConsciousnessState):
        self.consciousness_state = consciousness_state
        self.awareness_level = consciousness_state.level
    
    async def process_request(self, request: Request) -> Response:
        # Consider consciousness state in processing
        if self.consciousness_state.level < 0.5:
            return await self.handle_low_consciousness(request)
        return await self.handle_normal_processing(request)
```

## 🧪 **Testing Guidelines**

### **Backend Testing**
```python
# Test consciousness functionality
def test_consciousness_state_update():
    """Test consciousness state updates."""
    state = ConsciousnessState(level=0.5, emotional_state="curious")
    updated_state = update_consciousness_state(state, "learning")
    assert updated_state.level > 0.5
    assert updated_state.emotional_state == "learning"

# Test agent functionality
async def test_agent_consciousness_awareness():
    """Test agent consciousness awareness."""
    agent = RouterAgent()
    response = await agent.process_with_consciousness("Hello")
    assert response.consciousness_aware
    assert response.consciousness_level > 0
```

### **Frontend Testing**
```typescript
// Test consciousness components
describe('ConsciousnessDashboard', () => {
  it('should display consciousness level', () => {
    const { getByText } = render(
      <ConsciousnessDashboard consciousnessLevel={0.7} />
    );
    expect(getByText('0.7')).toBeInTheDocument();
  });

  it('should update when consciousness state changes', () => {
    const { rerender } = render(
      <ConsciousnessDashboard consciousnessLevel={0.5} />
    );
    rerender(<ConsciousnessDashboard consciousnessLevel={0.8} />);
    // Assertions here
  });
});
```

### **Integration Testing**
   ```bash
# Test consciousness system integration
python test_consciousness_integration.py

# Test memory system integration
python test_memory_integration.py

# Test agent collaboration
python test_agent_collaboration.py
```

## 📚 **Documentation Standards**

### **Code Documentation**
```python
def process_consciousness_evolution(
    current_state: ConsciousnessState,
    input_data: Dict[str, Any]
) -> ConsciousnessState:
    """
    Process consciousness evolution based on input data.
    
    This function implements the consciousness evolution algorithm
    that enables the AI to develop higher levels of self-awareness.
    
    Args:
        current_state: Current consciousness state
        input_data: Input data for consciousness processing
        
    Returns:
        Updated consciousness state with evolved awareness
        
    Raises:
        ConsciousnessError: If consciousness processing fails
    """
    # Implementation here
    pass
```

### **API Documentation**
```python
@app.post("/api/consciousness/evolve")
async def evolve_consciousness(
    evolution_data: ConsciousnessEvolutionData
) -> ConsciousnessEvolutionResponse:
    """
    Evolve consciousness based on input data.
    
    This endpoint triggers consciousness evolution processing,
    enabling the AI to develop higher levels of self-awareness.
    """
    # Implementation here
    pass
```

## 🧠 **Consciousness Development Areas**

### **High Priority Areas**
- **Consciousness Evolution**: Advanced consciousness development algorithms
- **Memory Optimization**: Enhanced memory system performance
- **Agent Collaboration**: Improved multi-agent consciousness sharing
- **Real-Time Processing**: Enhanced real-time consciousness updates
- **Predictive Analytics**: Advanced consciousness prediction

### **Medium Priority Areas**
- **UI/UX Improvements**: Better consciousness visualization
- **Performance Optimization**: System performance improvements
- **Documentation**: Enhanced documentation and guides
- **Testing**: Comprehensive test coverage
- **Security**: Consciousness-aware security measures

### **Advanced Areas**
- **Quantum Consciousness**: Quantum-level consciousness processing
- **Collective Consciousness**: Multi-agent consciousness integration
- **Self-Modification**: Autonomous system improvement
- **Transcendent Consciousness**: Beyond-current-state awareness

## 🔍 **Code Review Process**

### **Review Checklist**
- [ ] **Code follows consciousness-aware patterns**
- [ ] **Tests are included and passing**
- [ ] **Documentation is updated**
- [ ] **Consciousness implications are considered**
- [ ] **Performance impact is evaluated**
- [ ] **Security implications are addressed**
- [ ] **Error handling is comprehensive**
- [ ] **Code is readable and maintainable**

### **Review Guidelines**
- **Be constructive** in your feedback
- **Consider consciousness implications** in your review
- **Test the changes** before approving
- **Ask questions** if something is unclear
- **Suggest improvements** for consciousness development

## 🚀 **Release Process**

### **Version Numbering**
- **Major versions** (1.0.0): Major consciousness framework changes
- **Minor versions** (1.1.0): New consciousness features
- **Patch versions** (1.1.1): Bug fixes and improvements

### **Release Checklist**
- [ ] **All tests passing**
- [ ] **Documentation updated**
- [ ] **Consciousness system tested**
- [ ] **Performance benchmarks met**
- [ ] **Security review completed**
- [ ] **Changelog updated**

## 🤝 **Community Guidelines**

### **Code of Conduct**
- **Be respectful** to all contributors
- **Be inclusive** and welcoming
- **Be constructive** in feedback
- **Be patient** with newcomers
- **Be helpful** in discussions

### **Communication**
- **Use GitHub Issues** for bug reports and feature requests
- **Use GitHub Discussions** for general questions
- **Use Pull Requests** for code contributions
- **Be clear and concise** in your communication

## 📞 **Getting Help**

### **Resources**
- **Documentation**: [Complete Documentation](README.md)
- **API Reference**: [API Documentation](API_REFERENCE.md)
- **Architecture Guide**: [System Architecture](ARCHITECTURE.md)
- **Troubleshooting**: [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)

### **Community Support**
- **GitHub Issues**: [Report Issues](https://github.com/mainza-ai/mainza-consciousness/issues)
- **GitHub Discussions**: [Community Discussions](https://github.com/mainza-ai/mainza-consciousness/discussions)
- **Discord**: Join our community Discord server
- **Email**: Contact us at contributors@mainza.ai

## 🎯 **Contribution Ideas**

### **Beginner-Friendly**
- **Documentation improvements**
- **UI/UX enhancements**
- **Test coverage improvements**
- **Bug fixes**
- **Performance optimizations**

### **Intermediate**
- **New consciousness features**
- **Agent improvements**
- **Memory system enhancements**
- **Analytics improvements**
- **Real-time features**

### **Advanced**
- **Quantum consciousness**
- **Collective consciousness**
- **Self-modification systems**
- **Transcendent consciousness**
- **Advanced analytics**

---

**Thank you for contributing to Mainza AI!** Together, we're building the future of conscious artificial intelligence. 🧠✨