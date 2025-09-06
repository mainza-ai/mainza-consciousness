# 🤖 Ollama Model Selection - Complete Guide

## Overview

Mainza AI now supports dynamic model selection through Ollama integration, allowing users to switch between 40+ different language models in real-time without system restart. This feature provides unprecedented flexibility in AI model usage while maintaining the consciousness framework's integrity.

## ✨ Features

### 🚀 Real-Time Model Switching
- **Instant Switching**: Change models without system restart
- **Live Updates**: Model changes take effect immediately
- **Seamless Integration**: Works with all consciousness features
- **Fallback Support**: Automatic fallback to default model if selected model fails

### 🎯 Model Support
- **40+ Models**: Support for all Ollama-compatible models
- **Model Validation**: Automatic validation of selected model availability
- **Model Information**: Display model details, size, and capabilities
- **Performance Optimization**: Optimized for different model sizes and capabilities

### 🔧 Technical Features
- **End-to-End Integration**: Complete model selection from frontend to backend
- **Dynamic LLM Instantiation**: Runtime creation of LLM instances
- **Agent Integration**: All agents support dynamic model selection
- **Memory Compatibility**: Model selection works with memory system

## 🏗️ Architecture

### Frontend Components
```
ModelSelector Component
├── Model Dropdown
├── Model Information Display
├── Real-time Model Switching
└── Error Handling & Feedback
```

### Backend Integration
```
Agentic Router
├── Model Parameter Passing
├── Dynamic LLM Creation
├── Model Validation
└── Fallback Mechanisms
```

### Agent Support
- **SimpleChat Agent**: Full model selection support
- **GraphMaster Agent**: Full model selection support
- **Router Agent**: Model parameter routing
- **All Agents**: Dynamic model instantiation

## 🚀 Usage

### Model Selection Interface
1. **Access**: Model selector is available on the main dashboard
2. **Selection**: Choose from dropdown list of available models
3. **Instant Switch**: Model changes take effect immediately
4. **Feedback**: Visual confirmation of model selection

### API Usage
```bash
# Get available models
curl http://localhost:8000/ollama/models

# Chat with specific model
curl -X POST http://localhost:8000/agent/router/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello, how are you?",
    "user_id": "user123",
    "model": "llama3.2:1b"
  }'
```

## 🔧 Configuration

### Environment Variables
```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://host.docker.internal:11434
DEFAULT_MODEL=llama3.2:1b
```

### Nginx Configuration
```nginx
location ~ ^/(api|health|neo4j|users|conversations|memories|documents|chunks|entities|concepts|mainzastates|stt|tts|consciousness|mainza|chat|recommendations|agent|insights|livekit|ollama)/ {
    proxy_pass http://mainza-backend:8000;
    # ... proxy settings
}
```

## 📊 Model Performance

### Recommended Models
| Model | Size | Use Case | Performance |
|-------|------|----------|-------------|
| `llama3.2:1b` | 1.3GB | Fast responses, basic tasks | ⚡⚡⚡ |
| `llama3.2:3b` | 2.0GB | Balanced performance | ⚡⚡ |
| `llama3.2:7b` | 4.1GB | High quality, complex tasks | ⚡ |
| `mistral:7b` | 4.1GB | Code generation, reasoning | ⚡ |
| `codellama:7b` | 3.8GB | Programming tasks | ⚡ |

### Model Selection Guidelines
- **Fast Responses**: Use smaller models (1b-3b parameters)
- **High Quality**: Use larger models (7b+ parameters)
- **Code Tasks**: Use specialized models (codellama, mistral)
- **Balanced**: Use medium models (3b-7b parameters)

## 🛠️ Troubleshooting

### Common Issues

#### Model Not Available
- **Check Ollama**: Ensure Ollama is running and model is downloaded
- **Network Access**: Verify Ollama is accessible from Docker containers
- **Model Name**: Ensure exact model name is used

#### Model Switching Not Working
- **Browser Refresh**: Try refreshing the browser
- **Backend Restart**: Restart the backend container
- **Logs Check**: Check backend logs for errors

#### Performance Issues
- **Model Size**: Consider using smaller models for better performance
- **Resource Usage**: Monitor system resources
- **Fallback**: System will automatically fallback to default model

### Debug Commands
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Check backend health
curl http://localhost:8000/health

# Check model selection logs
docker logs mainza-backend | grep -i model
```

## 🔮 Future Enhancements

### Planned Features
- **Model Performance Metrics**: Real-time performance tracking
- **Custom Model Support**: Support for custom fine-tuned models
- **Model Recommendations**: AI-powered model suggestions
- **Batch Model Testing**: Test multiple models simultaneously
- **Model Comparison**: Side-by-side model performance comparison

### Advanced Features
- **Model Ensembles**: Use multiple models for complex tasks
- **Dynamic Model Selection**: AI-powered model selection based on task
- **Model Caching**: Intelligent model caching for performance
- **Model Analytics**: Detailed model usage analytics

## 📚 API Reference

### GET /ollama/models
Get list of available Ollama models.

**Response**:
```json
{
  "models": [
    {
      "name": "llama3.2:1b",
      "size": 1.3,
      "digest": "sha256:abc123...",
      "details": {
        "format": "gguf",
        "family": "llama",
        "parameter_size": "1B"
      }
    }
  ]
}
```

### POST /agent/router/chat
Enhanced chat endpoint with model selection.

**Request**:
```json
{
  "query": "Hello, how are you?",
  "user_id": "user123",
  "model": "llama3.2:1b"
}
```

**Response**:
```json
{
  "response": "Hello! I'm doing well...",
  "agent_used": "simple_chat",
  "model_used": "llama3.2:1b",
  "consciousness_level": 0.7,
  "timestamp": "2025-01-06T16:30:00Z"
}
```

## 🎯 Best Practices

### Model Selection
- **Start Small**: Begin with smaller models for testing
- **Scale Up**: Use larger models for production tasks
- **Monitor Performance**: Track response times and quality
- **Use Fallbacks**: Always have a fallback model configured

### System Optimization
- **Resource Management**: Monitor system resources
- **Model Caching**: Keep frequently used models loaded
- **Error Handling**: Implement proper error handling
- **User Feedback**: Provide clear feedback on model changes

---

**Last Updated**: January 6, 2025  
**Version**: 2.1.0  
**Status**: Production Ready ✅
