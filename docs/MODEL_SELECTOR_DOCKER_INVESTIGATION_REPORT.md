# LLM Model Selector Docker Investigation Report

**Date:** September 8, 2025  
**Investigator:** AI Assistant  
**Issue:** Model selector changes not taking effect in Docker environment - system continues using default model

## Executive Summary

After thorough investigation, the **model selector is actually working correctly** in terms of API parameter passing, but there's a **critical execution error** in the Docker environment that prevents the selected model from being used. The system falls back to the default model due to agent execution failures.

## Root Cause Analysis

### **Primary Issue: Agent Execution Error**
The logs reveal the real problem:
```
ERROR:agent.GraphMaster:Enhanced GraphMaster execution failed: AbstractAgent.run() got an unexpected keyword argument 'user_id'
WARNING:agent.GraphMaster:Selected model gpt-oss:20b failed, using default
ERROR:agent.GraphMaster:Enhanced GraphMaster execution failed: AbstractAgent.run() got an unexpected keyword argument 'user_id'  
WARNING:agent.GraphMaster:Selected model llama3.2:1b failed, using default
```

### **Technical Details**

1. **Model Parameter Flow (Working)**:
   - ✅ Frontend sends `model` parameter correctly
   - ✅ Backend receives `model` parameter in `enhanced_router_chat`
   - ✅ Model parameter is passed to agents via LLM request manager
   - ✅ Agents attempt to use the selected model

2. **Agent Execution (Failing)**:
   - ❌ Agents call `run_with_consciousness(query, user_id, model=model)`
   - ❌ Base `ConsciousAgent.run_with_consciousness` method signature is `run_with_consciousness(query, user_id, **kwargs)`
   - ❌ The `model` parameter gets passed as `**kwargs` but agents try to pass it as a positional argument
   - ❌ This causes the `AbstractAgent.run()` method to receive unexpected `user_id` parameter

3. **Fallback Behavior**:
   - When agent execution fails, the system falls back to default model
   - This makes it appear that model switching isn't working
   - The selected model is actually being processed but fails during execution

## Investigation Findings

### ✅ What's Working
- **Frontend Model Selector**: Correctly fetches available models and sends selection
- **API Parameter Handling**: Model parameter is correctly received and logged
- **Model Creation Logic**: `create_llm_for_model()` function works correctly
- **LLM Request Manager**: Correctly passes model parameter to agents

### ❌ What's Broken
- **Agent Method Signatures**: Mismatch between expected and actual parameters
- **Parameter Passing**: Model parameter not correctly passed through the execution chain
- **Error Handling**: Agent failures cause fallback to default model without user notification

## Detailed Technical Analysis

### **Agent Execution Chain**
```python
# In enhanced_router_chat (line 900-907)
result = await llm_request_manager.submit_request(
    enhanced_graphmaster_agent.run_with_consciousness,  # Method reference
    RequestPriority.USER_CONVERSATION,
    user_id=user_id,           # ✅ Correct
    timeout=60.0,
    query=query,               # ✅ Correct
    model=model                # ✅ Correct - passed as keyword
)
```

### **Agent Method Signature Issue**
```python
# In base_conscious_agent.py (line 46-51)
async def run_with_consciousness(
    self, 
    query: str, 
    user_id: str = "mainza-user",  # ✅ Expects user_id
    **kwargs                      # ✅ Should receive model via kwargs
):
```

### **Agent Implementation Issue**
```python
# In graphmaster.py (line 140)
result = await dynamic_agent.run(enhanced_query, user_id=user_id, **kwargs)
# ❌ This passes user_id as positional argument to pydantic-ai Agent.run()
# ❌ But pydantic-ai Agent.run() doesn't accept user_id parameter
```

## Impact Assessment

### **User Experience**
- Users select different models but see no difference in responses
- No error messages or feedback about model switching failures
- System appears unresponsive to model selection

### **System Behavior**
- All model selections fall back to default model
- No actual model switching occurs
- Wasted computational resources on failed model attempts

## Recommended Fix Plan

### **Phase 1: Fix Agent Method Signatures**
1. **Update Base Conscious Agent**:
   - Modify `run_with_consciousness` to properly handle model parameter
   - Ensure model parameter is passed correctly to agent execution

2. **Update Agent Implementations**:
   - Fix parameter passing in `execute_with_context` methods
   - Ensure model parameter reaches the actual LLM calls

### **Phase 2: Fix Parameter Passing**
1. **GraphMaster Agent**:
   - Fix `execute_with_context` method to properly handle model parameter
   - Update dynamic agent creation to use correct parameter passing

2. **Simple Chat Agent**:
   - Apply same fixes to ensure consistent behavior

### **Phase 3: Improve Error Handling**
1. **Better Error Messages**:
   - Log specific model switching failures
   - Provide user feedback when model switching fails

2. **Fallback Strategy**:
   - Implement graceful degradation
   - Show which model is actually being used

## Implementation Priority

### **High Priority (Immediate)**
1. Fix agent method signatures and parameter passing
2. Test model switching in Docker environment
3. Verify different models produce different responses

### **Medium Priority (Next)**
1. Improve error handling and user feedback
2. Add model switching status indicators
3. Optimize model loading and switching performance

### **Low Priority (Future)**
1. Add model switching analytics
2. Implement model performance monitoring
3. Add advanced model selection features

## Expected Outcomes

After implementing the fixes:
- ✅ Model selector will work correctly in Docker
- ✅ Different models will produce different responses
- ✅ Users will see clear feedback about model selection
- ✅ System will be more reliable and responsive

## Testing Strategy

1. **Unit Tests**: Test agent method signatures and parameter passing
2. **Integration Tests**: Test model switching through API endpoints
3. **Docker Tests**: Verify model switching works in Docker environment
4. **User Tests**: Confirm different models produce different responses

## Conclusion

The model selector issue is a **parameter passing bug** in the agent execution chain, not a fundamental design problem. The fix requires updating agent method signatures and parameter passing logic. Once implemented, the model selector will work correctly in both local and Docker environments.

**Estimated Fix Time**: 2-3 hours  
**Risk Level**: Low (no breaking changes to existing functionality)  
**Impact**: High (restores core model switching functionality)
