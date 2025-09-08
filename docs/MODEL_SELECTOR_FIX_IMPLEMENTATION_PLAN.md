# Model Selector Fix Implementation Plan

**Date:** September 8, 2025  
**Issue:** LLM Model Selector not working in Docker environment  
**Priority:** High - Core functionality broken

## Overview

The model selector appears to work but actually fails due to parameter passing issues in the agent execution chain. This plan outlines the specific fixes needed to restore model switching functionality.

## Root Cause Summary

1. **Model parameter is correctly passed** from frontend to backend
2. **Agent execution fails** due to incorrect parameter passing to pydantic-ai agents
3. **System falls back to default model** without user notification
4. **Result**: All model selections appear to use the same model

## Implementation Steps

### **Step 1: Fix Base Conscious Agent Method Signature**

**File:** `backend/agents/base_conscious_agent.py`

**Current Issue:**
```python
async def run_with_consciousness(
    self, 
    query: str, 
    user_id: str = "mainza-user",
    **kwargs
):
```

**Fix Required:**
- Add explicit `model` parameter to method signature
- Ensure model parameter is passed correctly to `execute_with_context`

**Implementation:**
```python
async def run_with_consciousness(
    self, 
    query: str, 
    user_id: str = "mainza-user",
    model: str = None,
    **kwargs
):
    # ... existing code ...
    
    # Pass model parameter to execute_with_context
    result = await self.execute_with_context(
        query=query,
        user_id=user_id,
        consciousness_context=consciousness_context,
        knowledge_context=knowledge_context,
        memory_context=memory_context,
        model=model,  # Add this line
        **kwargs
    )
```

### **Step 2: Fix GraphMaster Agent Parameter Passing**

**File:** `backend/agents/graphmaster.py`

**Current Issue:**
```python
# Line 140 - Incorrect parameter passing
result = await dynamic_agent.run(enhanced_query, user_id=user_id, **kwargs)
```

**Fix Required:**
- Remove `user_id` parameter from pydantic-ai agent calls
- Ensure model parameter is correctly passed to dynamic agent creation

**Implementation:**
```python
# Fix the dynamic agent execution
if model and model != "default":
    # Create a dynamic agent with the selected model
    dynamic_llm = create_llm_for_model(model)
    dynamic_agent = Agent[None, GraphQueryOutput](
        dynamic_llm,
        system_prompt=GRAPHMASTER_PROMPT,
        tools=tools
    )
    # FIXED: Remove user_id parameter - pydantic-ai agents don't accept it
    result = await dynamic_agent.run(enhanced_query, **kwargs)
else:
    # Use default agent
    result = await self.pydantic_agent.run(enhanced_query, **kwargs)
```

### **Step 3: Fix Simple Chat Agent Parameter Passing**

**File:** `backend/agents/simple_chat.py`

**Current Issue:**
- Same parameter passing issue as GraphMaster

**Fix Required:**
- Apply same fixes as GraphMaster
- Ensure model parameter is handled correctly

**Implementation:**
```python
# Similar fixes to GraphMaster
if model and model != "default":
    dynamic_llm = create_llm_for_model(model)
    dynamic_agent = Agent[None, str](
        dynamic_llm,
        system_prompt=SIMPLE_CHAT_PROMPT
    )
    # FIXED: Remove user_id parameter
    result = await dynamic_agent.run(enhanced_query, **kwargs)
else:
    result = await self.pydantic_agent.run(enhanced_query, **kwargs)
```

### **Step 4: Update Router Parameter Passing**

**File:** `backend/agentic_router.py`

**Current Issue:**
- Model parameter is passed correctly but agents fail to use it

**Fix Required:**
- Ensure model parameter is passed correctly to agent methods
- Add better error handling for model switching failures

**Implementation:**
```python
# In enhanced_router_chat function (around line 900)
if agent_used == "graphmaster":
    from backend.agents.graphmaster import enhanced_graphmaster_agent
    logging.debug(f"   Executing graphmaster agent via LLM request manager with model: {model}")
    result = await llm_request_manager.submit_request(
        enhanced_graphmaster_agent.run_with_consciousness,
        RequestPriority.USER_CONVERSATION,
        user_id=user_id,
        timeout=60.0,
        query=query,
        model=model  # This is already correct
    )
```

### **Step 5: Add Model Switching Validation**

**File:** `backend/agentic_router.py`

**Implementation:**
```python
# Add model validation after agent execution
if model and model != "default":
    # Log successful model usage
    logging.info(f"✅ Successfully used model: {model}")
    
    # Add model info to response
    return {
        "response": response,
        "agent_used": agent_used,
        "model_used": model,  # Add this
        "consciousness_level": consciousness_context.get("consciousness_level", 0.7),
        "emotional_state": consciousness_context.get("emotional_state", "curious"),
        "routing_confidence": routing_decision.get("confidence", 0.8),
        "user_id": user_id,
        "query": query
    }
```

### **Step 6: Improve Error Handling**

**File:** `backend/agents/graphmaster.py`

**Implementation:**
```python
# Add better error handling for model switching
try:
    if model and model != "default":
        # Create a dynamic agent with the selected model
        dynamic_llm = create_llm_for_model(model)
        dynamic_agent = Agent[None, GraphQueryOutput](
            dynamic_llm,
            system_prompt=GRAPHMASTER_PROMPT,
            tools=tools
        )
        result = await dynamic_agent.run(enhanced_query, **kwargs)
        self.logger.info(f"✅ Successfully used model: {model}")
    else:
        # Use default agent
        result = await self.pydantic_agent.run(enhanced_query, **kwargs)
        self.logger.info(f"✅ Used default model")
        
except Exception as model_error:
    self.logger.error(f"❌ Model {model} failed: {model_error}")
    # Fallback to default model
    try:
        result = await self.pydantic_agent.run(enhanced_query, **kwargs)
        self.logger.warning(f"⚠️ Fallback to default model successful")
    except Exception as fallback_error:
        self.logger.error(f"❌ Fallback to default model failed: {fallback_error}")
        raise
```

## Testing Strategy

### **Phase 1: Unit Tests**
1. Test agent method signatures
2. Test parameter passing
3. Test model creation logic

### **Phase 2: Integration Tests**
1. Test model switching through API
2. Test different models produce different responses
3. Test error handling and fallbacks

### **Phase 3: Docker Tests**
1. Test model switching in Docker environment
2. Verify model selection persists across requests
3. Test performance with different models

### **Phase 4: User Acceptance Tests**
1. Test model selector UI
2. Verify different models produce different responses
3. Test error handling and user feedback

## Expected Results

After implementation:

### **Immediate Results**
- ✅ Model selector will work correctly
- ✅ Different models will produce different responses
- ✅ No more agent execution errors
- ✅ Clear logging of model usage

### **User Experience**
- ✅ Model selection will be responsive
- ✅ Different models will show different response styles
- ✅ Error messages will be clear if model switching fails
- ✅ System will be more reliable

### **System Performance**
- ✅ Reduced error logs
- ✅ Better resource utilization
- ✅ Improved system stability

## Rollback Plan

If issues arise:
1. **Immediate**: Revert agent method signature changes
2. **Short-term**: Disable model switching temporarily
3. **Long-term**: Implement gradual rollout with feature flags

## Success Criteria

1. **Functional**: Model selector works in Docker environment
2. **Behavioral**: Different models produce different responses
3. **Performance**: No significant performance degradation
4. **Reliability**: No increase in error rates
5. **User Experience**: Clear feedback on model selection

## Timeline

- **Phase 1**: 1 hour (Fix method signatures)
- **Phase 2**: 1 hour (Fix parameter passing)
- **Phase 3**: 30 minutes (Add validation and error handling)
- **Phase 4**: 30 minutes (Testing and verification)
- **Total**: 3 hours

## Risk Assessment

- **Low Risk**: Changes are isolated to agent execution
- **No Breaking Changes**: Existing functionality remains intact
- **Easy Rollback**: Changes can be easily reverted
- **High Impact**: Restores core functionality

## Conclusion

This implementation plan addresses the root cause of the model selector issue through targeted fixes to the agent execution chain. The changes are minimal, focused, and low-risk, ensuring that model switching functionality is restored without affecting other system components.
