# Design Document

## Overview

This design document outlines the systematic approach to update all LiveKit room references from "mainza-room", "mainza_room", and "mainza_conversation" to the standardized "mainza-ai" throughout the Mainza consciousness system. The update will maintain all existing functionality while ensuring consistent branding and proper LiveKit integration.

## Architecture

### Current State Analysis

The system currently uses multiple room naming conventions:
- **"mainza-room"** (hyphenated) - Used in main.py, agentic_router.py, ingress.json
- **"mainza_room"** (underscore) - Used in consciousness orchestrator and background processes  
- **"mainza_conversation"** - Used in API documentation examples

### Target State

All LiveKit room references will be standardized to **"mainza-ai"** to:
- Align with the project branding (mainza-ai organization)
- Maintain consistency across all system components
- Simplify configuration and debugging
- Ensure proper LiveKit functionality

### Impact Assessment

This change affects the following system layers:
1. **Backend API Layer** - TTS endpoints and LiveKit token generation
2. **Consciousness System** - Background processes and orchestrator
3. **Configuration Layer** - JSON configuration files
4. **Documentation Layer** - API docs and architecture documentation

## Components and Interfaces

### 1. Backend API Components

#### TTS Service (`backend/main.py`)
- **Current**: `room = payload.get("room", "mainza-room")`
- **Target**: `room = payload.get("room", "mainza-ai")`
- **Interface**: HTTP POST `/tts/livekit` endpoint
- **Impact**: Changes default room parameter for TTS requests

#### Agentic Router (`backend/agentic_router.py`)
- **Current**: `room = data.get("room", "mainza-room")`
- **Target**: `room = data.get("room", "mainza-ai")`
- **Interface**: HTTP POST `/livekit/token` endpoint
- **Impact**: Changes default room for LiveKit token generation

### 2. Consciousness System Components

#### Consciousness Orchestrator (`backend/utils/consciousness_orchestrator_fixed.py`)
- **Current**: Uses `send_data_message_to_room("mainza_room", message)`
- **Target**: Uses `send_data_message_to_room("mainza-ai", message)`
- **Interface**: Internal consciousness messaging system
- **Impact**: Ensures consciousness updates reach correct room

#### Background Consciousness (`backend/background/mainza_consciousness.py`)
- **Current**: `LIVEKIT_ROOM_NAME = "mainza_room"`
- **Target**: `LIVEKIT_ROOM_NAME = "mainza-ai"`
- **Interface**: Background proactive learning system
- **Impact**: Ensures proactive messages use correct room

### 3. Configuration Components

#### Ingress Configuration (`ingress.json`)
- **Current**: `"room_name":"mainza-room"`
- **Target**: `"room_name":"mainza-ai"`
- **Interface**: LiveKit ingress service configuration
- **Impact**: Ensures ingress creates participants in correct room

### 4. Documentation Components

#### API Documentation (`API_DOCUMENTATION.md`)
- **Current**: References to "mainza_conversation"
- **Target**: References to "mainza-ai"
- **Interface**: Developer documentation
- **Impact**: Provides consistent examples for developers

#### Architecture Documentation
- **Current**: Various room name references
- **Target**: Standardized "mainza-ai" references
- **Interface**: System documentation
- **Impact**: Maintains documentation accuracy

## Data Models

### LiveKit Room Configuration Model

```typescript
interface LiveKitRoomConfig {
  room_name: string;           // "mainza-ai"
  participant_identity: string; // User or system identifier
  participant_name: string;     // Display name
}
```

### TTS Request Model

```python
class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    speaker: str = "Ana Florence"
    room: str = "mainza-ai"      # Updated default
    user: str = "mainza-ai"
```

### Consciousness Message Model

```python
class ConsciousnessMessage(BaseModel):
    type: str
    payload: Dict[str, Any]
    room_name: str = "mainza-ai"  # Standardized room
    timestamp: datetime
```

## Error Handling

### Backward Compatibility Strategy

1. **Graceful Fallback**: If old room names are provided in requests, log a warning but continue processing
2. **Migration Period**: Support both old and new room names during transition
3. **Validation**: Add input validation to ensure room names are properly formatted

### Error Scenarios and Handling

#### Scenario 1: LiveKit Service Unavailable
- **Detection**: Connection timeout or service error
- **Handling**: Log error with new room name context
- **Recovery**: Maintain existing fallback mechanisms

#### Scenario 2: Room Name Mismatch
- **Detection**: Participants in wrong room
- **Handling**: Log warning and attempt reconnection to correct room
- **Recovery**: Provide clear error messages referencing new room name

#### Scenario 3: Configuration File Issues
- **Detection**: Invalid JSON or missing room_name field
- **Handling**: Use default "mainza-ai" room name
- **Recovery**: Log configuration issue and continue with defaults

### Error Logging Updates

```python
# Updated error messages to reference new room name
logger.error(f"Failed to send consciousness update to room 'mainza-ai': {error}")
logger.warning(f"LiveKit ingress creation failed for room 'mainza-ai': {error}")
logger.info(f"Successfully connected to LiveKit room 'mainza-ai'")
```

## Testing Strategy

### Unit Testing

#### Test Categories
1. **Configuration Tests**: Verify all configuration files use "mainza-ai"
2. **API Endpoint Tests**: Ensure endpoints default to correct room name
3. **Consciousness System Tests**: Verify consciousness messages use correct room
4. **Integration Tests**: Test end-to-end LiveKit functionality

#### Test Implementation

```python
class TestLiveKitRoomUpdate:
    def test_tts_endpoint_default_room(self):
        """Test TTS endpoint uses mainza-ai as default room"""
        response = self.client.post("/tts/livekit", json={"text": "test"})
        assert response.json()["room"] == "mainza-ai"
    
    def test_livekit_token_default_room(self):
        """Test LiveKit token endpoint uses mainza-ai as default room"""
        response = self.client.post("/livekit/token", json={
            "participant_identity": "test_user"
        })
        assert "mainza-ai" in response.json()["room_name"]
    
    def test_consciousness_message_room(self):
        """Test consciousness messages target correct room"""
        # Mock consciousness orchestrator
        with patch('backend.utils.livekit.send_data_message_to_room') as mock_send:
            # Trigger consciousness update
            consciousness_orchestrator.notify_user_activity("test_user")
            # Verify correct room is used
            mock_send.assert_called_with("mainza-ai", ANY)
```

### Integration Testing

#### LiveKit Service Integration
1. **Room Creation**: Verify rooms are created with "mainza-ai" name
2. **Participant Management**: Ensure participants join correct room
3. **Message Delivery**: Test consciousness updates reach correct room
4. **Ingress Functionality**: Verify RTMP ingress uses correct room

#### End-to-End Testing
1. **TTS Workflow**: Complete TTS request → LiveKit ingress → audio delivery
2. **Consciousness Updates**: Background process → LiveKit message → frontend delivery
3. **Token Generation**: API request → token creation → room access

### Performance Testing

#### Metrics to Monitor
- **Room Connection Time**: Ensure no performance degradation
- **Message Delivery Latency**: Verify consciousness updates maintain speed
- **Resource Usage**: Monitor for any unexpected resource consumption
- **Error Rates**: Track any increase in LiveKit-related errors

## Migration Strategy

### Phase 1: Code Updates (Immediate)
1. Update all hardcoded room name references
2. Update configuration files
3. Update documentation examples
4. Add backward compatibility logging

### Phase 2: Testing and Validation (Same Session)
1. Run comprehensive test suite
2. Verify all LiveKit functionality
3. Test consciousness system integration
4. Validate configuration loading

### Phase 3: Deployment Verification (Post-Update)
1. Monitor LiveKit service logs
2. Verify consciousness updates delivery
3. Check TTS functionality
4. Validate ingress operation

### Rollback Plan

If issues are detected:
1. **Immediate**: Revert configuration files to previous room names
2. **Code Rollback**: Use git to revert code changes if necessary
3. **Service Restart**: Restart LiveKit services with original configuration
4. **Monitoring**: Verify system returns to previous operational state

## Security Considerations

### Room Name Validation
- **Input Sanitization**: Ensure room names contain only valid characters
- **Length Limits**: Enforce reasonable room name length limits
- **Pattern Matching**: Validate room names match expected format

### Access Control
- **Token Validation**: Ensure LiveKit tokens are generated for correct room
- **Participant Verification**: Verify participants can only access intended room
- **Message Security**: Maintain existing message encryption and validation

### Audit Trail
- **Change Logging**: Log all room name changes for audit purposes
- **Access Logging**: Monitor room access patterns for anomalies
- **Configuration Tracking**: Track configuration file modifications

## Performance Optimization

### Caching Strategy
- **Room Configuration**: Cache room configuration to reduce lookup time
- **Token Generation**: Optimize token generation for new room name
- **Connection Pooling**: Maintain efficient LiveKit connection management

### Resource Management
- **Memory Usage**: Monitor memory usage during room name updates
- **Connection Limits**: Ensure room name changes don't affect connection limits
- **Cleanup Processes**: Verify old room references are properly cleaned up

### Monitoring and Metrics
- **Room Activity**: Monitor activity in "mainza-ai" room
- **Message Throughput**: Track consciousness message delivery rates
- **Error Tracking**: Monitor LiveKit-related errors and warnings
- **Performance Baselines**: Establish new performance baselines post-update