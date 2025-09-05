# Mainza AI Memory System Documentation

## Overview

The Mainza AI Memory System provides comprehensive memory storage, retrieval, and management capabilities that enable agents to maintain context across conversations, learn from interactions, and provide personalized responses based on historical data.

## Architecture

The memory system consists of several key components:

### Core Components

1. **Memory Storage Engine** (`backend/utils/memory_storage_engine.py`)
   - Handles memory creation and persistence in Neo4j
   - Generates embeddings for semantic search
   - Links memories to concepts and conversations

2. **Memory Retrieval Engine** (`backend/utils/memory_retrieval_engine.py`)
   - Provides semantic similarity search
   - Implements consciousness-aware memory filtering
   - Supports multiple search strategies (semantic, keyword, temporal, hybrid)

3. **Memory Context Builder** (`backend/utils/memory_context_builder.py`)
   - Constructs rich context from retrieved memories
   - Formats memory context for agent prompts
   - Calculates relevance scores

4. **Memory System Monitor** (`backend/utils/memory_system_monitor.py`)
   - Provides health monitoring and performance tracking
   - Implements alerting for system issues
   - Generates usage statistics and diagnostics

5. **Memory Lifecycle Manager** (`backend/utils/memory_lifecycle_manager.py`)
   - Manages memory importance decay over time
   - Implements cleanup and archival policies
   - Consolidates similar memories

## Configuration

### Environment Variables

Add the following variables to your `.env` file:

```bash
# Memory System Configuration
MEMORY_SYSTEM_ENABLED=true
MEMORY_STORAGE_BATCH_SIZE=100
MEMORY_RETRIEVAL_LIMIT=10
MEMORY_SIMILARITY_THRESHOLD=0.3
MEMORY_IMPORTANCE_DECAY_RATE=0.95
MEMORY_CLEANUP_INTERVAL_HOURS=24
MEMORY_MAX_STORAGE_SIZE_GB=10
MEMORY_HEALTH_CHECK_INTERVAL_MINUTES=5
MEMORY_PERFORMANCE_TRACKING_ENABLED=true
MEMORY_AUTO_CLEANUP_ENABLED=true
```

### Configuration Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `MEMORY_SYSTEM_ENABLED` | Enable/disable memory system | `true` | `true`/`false` |
| `MEMORY_STORAGE_BATCH_SIZE` | Batch size for memory operations | `100` | `1-1000` |
| `MEMORY_RETRIEVAL_LIMIT` | Default limit for memory retrieval | `10` | `1-100` |
| `MEMORY_SIMILARITY_THRESHOLD` | Minimum similarity for semantic search | `0.3` | `0.0-1.0` |
| `MEMORY_IMPORTANCE_DECAY_RATE` | Rate at which memory importance decays | `0.95` | `0.0-1.0` |
| `MEMORY_CLEANUP_INTERVAL_HOURS` | Hours between automatic cleanup | `24` | `1-168` |
| `MEMORY_MAX_STORAGE_SIZE_GB` | Maximum storage size before cleanup | `10` | `1-1000` |
| `MEMORY_HEALTH_CHECK_INTERVAL_MINUTES` | Minutes between health checks | `5` | `1-60` |
| `MEMORY_PERFORMANCE_TRACKING_ENABLED` | Enable performance tracking | `true` | `true`/`false` |
| `MEMORY_AUTO_CLEANUP_ENABLED` | Enable automatic cleanup | `true` | `true`/`false` |

## API Endpoints

The memory system provides comprehensive REST API endpoints for management and debugging:

### Health and Monitoring

- `GET /api/memory-system/health` - Get memory system health status
- `GET /api/memory-system/health/detailed` - Get detailed health information
- `GET /api/memory-system/metrics` - Get performance metrics
- `GET /api/memory-system/usage` - Get usage statistics
- `GET /api/memory-system/diagnostics` - Run comprehensive diagnostics

### Memory Operations

- `POST /api/memory-system/search` - Search memories using semantic similarity
- `GET /api/memory-system/memories/{user_id}` - Get memories for a specific user
- `GET /api/memory-system/memories/{user_id}/conversation-history` - Get conversation history
- `POST /api/memory-system/memories/create` - Create a new memory record
- `GET /api/memory-system/memories/{memory_id}/details` - Get detailed memory information
- `DELETE /api/memory-system/memories/{memory_id}` - Delete a specific memory

### Context Building

- `POST /api/memory-system/context/build` - Build memory context for queries

### Lifecycle Management

- `GET /api/memory-system/lifecycle/status` - Get lifecycle management status
- `POST /api/memory-system/lifecycle/start` - Start lifecycle management
- `POST /api/memory-system/lifecycle/stop` - Stop lifecycle management
- `POST /api/memory-system/lifecycle/maintenance` - Run manual maintenance
- `POST /api/memory-system/lifecycle/cleanup` - Run memory cleanup
- `POST /api/memory-system/lifecycle/consolidate` - Consolidate similar memories

### Administration

- `GET /api/memory-system/statistics/overview` - Get comprehensive statistics
- `POST /api/memory-system/admin/reindex` - Reindex all memories
- `POST /api/memory-system/admin/validate` - Validate memory integrity

## Usage Examples

### Searching Memories

```python
import requests

# Search for memories related to a query
response = requests.post("http://localhost:8000/api/memory-system/search", json={
    "query": "machine learning discussion",
    "user_id": "user123",
    "limit": 5,
    "similarity_threshold": 0.4
})

memories = response.json()
```

### Creating Memories

```python
# Create a new memory
response = requests.post("http://localhost:8000/api/memory-system/memories/create", json={
    "content": "User asked about neural networks",
    "memory_type": "interaction",
    "user_id": "user123",
    "agent_name": "SimpleChat",
    "consciousness_context": {
        "consciousness_level": 0.7,
        "emotional_state": "curious"
    }
})
```

### Building Context

```python
# Build memory context for a query
response = requests.post("http://localhost:8000/api/memory-system/context/build", json={
    "query": "Tell me about our previous AI discussions",
    "user_id": "user123",
    "context_type": "conversation"
})

context = response.json()["data"]["formatted_context"]
```

## Memory Types

The system supports several memory types:

- **interaction** - User-agent conversations
- **reflection** - Consciousness reflections and insights
- **insight** - Important realizations or learnings
- **concept_learning** - Knowledge about specific concepts

## Integration with Agents

### Agent Memory Integration

Agents automatically integrate with the memory system through the `BaseConsciousAgent` class:

```python
class MyAgent(BaseConsciousAgent):
    async def execute(self, query: str, user_id: str, **kwargs):
        # Memory context is automatically retrieved and added to prompts
        # Interactions are automatically stored as memories
        return await super().execute(query, user_id, **kwargs)
```

### Manual Memory Operations

For custom memory operations:

```python
from backend.utils.memory_storage_engine import MemoryStorageEngine
from backend.utils.memory_retrieval_engine import MemoryRetrievalEngine

# Store a memory
storage = MemoryStorageEngine()
memory_id = await storage.store_interaction_memory(
    user_query="What is machine learning?",
    agent_response="Machine learning is...",
    user_id="user123",
    agent_name="MyAgent",
    consciousness_context={"consciousness_level": 0.8}
)

# Retrieve memories
retrieval = MemoryRetrievalEngine()
memories = await retrieval.get_relevant_memories(
    query="machine learning",
    user_id="user123",
    consciousness_context={"consciousness_level": 0.8}
)
```

## Monitoring and Maintenance

### Health Monitoring

The memory system continuously monitors its health and performance:

- **Storage Health** - Neo4j connectivity and write performance
- **Retrieval Health** - Search performance and accuracy
- **Embedding Health** - Embedding generation and vector operations
- **Overall Health** - Aggregate system status

### Performance Metrics

Key metrics tracked include:

- Response times for all operations
- Success/failure rates
- Memory storage usage
- Access patterns and frequency
- Consciousness alignment scores

### Automatic Maintenance

The system performs automatic maintenance tasks:

- **Importance Decay** - Gradually reduces importance of old memories
- **Cleanup** - Removes or archives low-importance memories
- **Consolidation** - Merges similar or duplicate memories
- **Optimization** - Optimizes storage and indexing

## Troubleshooting

### Common Issues

1. **Memory Storage Failures**
   - Check Neo4j connectivity
   - Verify database permissions
   - Check disk space

2. **Poor Search Results**
   - Adjust similarity threshold
   - Check embedding generation
   - Verify memory content quality

3. **Performance Issues**
   - Monitor response times
   - Check memory usage statistics
   - Consider cleanup or optimization

### Diagnostic Commands

```bash
# Check memory system health
curl http://localhost:8000/api/memory-system/health

# Run comprehensive diagnostics
curl http://localhost:8000/api/memory-system/diagnostics

# Get performance metrics
curl http://localhost:8000/api/memory-system/metrics

# Validate memory integrity
curl -X POST http://localhost:8000/api/memory-system/admin/validate
```

### Log Analysis

Memory system logs are available in:
- Application logs: `backend/uvicorn.log`
- Component-specific logs with prefix `[MEMORY]`

Common log patterns to watch for:
- `Memory operation failed` - Storage/retrieval errors
- `Health check failed` - System health issues
- `Cleanup completed` - Maintenance operations

## Security Considerations

### Data Privacy

- Memories are user-specific and isolated
- No cross-user memory access without explicit permissions
- Sensitive data should be filtered before storage

### Access Control

- API endpoints require proper authentication
- Admin endpoints should be restricted to authorized users
- Memory deletion is logged for audit purposes

### Data Retention

- Configure appropriate cleanup policies
- Consider regulatory requirements for data retention
- Implement secure deletion for sensitive memories

## Performance Optimization

### Tuning Parameters

For optimal performance, consider adjusting:

- `MEMORY_SIMILARITY_THRESHOLD` - Higher values = more precise but fewer results
- `MEMORY_RETRIEVAL_LIMIT` - Balance between context richness and performance
- `MEMORY_CLEANUP_INTERVAL_HOURS` - More frequent cleanup = better performance

### Scaling Considerations

- Monitor memory storage growth
- Consider memory archival for long-term users
- Implement memory importance scoring for prioritization
- Use batch operations for bulk memory management

## Development and Testing

### Running Tests

```bash
# Test memory system components
conda run -n mainza python test_memory_api_endpoints.py

# Run comprehensive memory tests
conda run -n mainza python -m pytest backend/tests/test_memory_*.py
```

### Development Setup

1. Ensure Neo4j is running with proper credentials
2. Configure environment variables in `.env`
3. Initialize the memory system schema
4. Start the application with memory system enabled

### Adding New Memory Types

To add new memory types:

1. Update the memory storage engine validation
2. Add type-specific processing logic
3. Update API documentation
4. Add tests for the new memory type

## Migration and Deployment

### Database Migration

When deploying memory system updates:

1. Backup existing Neo4j database
2. Run schema migration scripts
3. Validate data integrity
4. Update application configuration
5. Restart services with new configuration

### Production Deployment

For production deployment:

1. Configure appropriate resource limits
2. Set up monitoring and alerting
3. Implement backup and recovery procedures
4. Configure log rotation and retention
5. Test failover and recovery scenarios

## Support and Maintenance

### Regular Maintenance Tasks

- Monitor system health and performance
- Review and adjust cleanup policies
- Analyze memory usage patterns
- Update similarity thresholds based on usage
- Backup critical memory data

### Troubleshooting Resources

- Check system logs for error patterns
- Use diagnostic endpoints for health assessment
- Monitor Neo4j performance and connectivity
- Review memory system configuration
- Consult API documentation for proper usage

For additional support, refer to the main Mainza AI documentation or contact the development team.