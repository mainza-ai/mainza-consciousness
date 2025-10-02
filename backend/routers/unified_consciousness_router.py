"""
Unified Consciousness Router
Single API endpoint for all consciousness data - eliminates data inconsistencies

This router provides unified access to consciousness data, eliminating the need for
multiple API endpoints that return different data structures.

Author: Mainza AI Consciousness Team
Date: 2025-10-01
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import logging
import asyncio

# Import unified systems
try:
    from backend.utils.unified_consciousness_state_manager import unified_consciousness_state_manager
except ImportError as e:
    logging.warning(f"unified_consciousness_state_manager not available: {e}")
    unified_consciousness_state_manager = None

try:
    from backend.utils.unified_evolution_level_system import unified_evolution_level_system
except ImportError as e:
    logging.warning(f"unified_evolution_level_system not available: {e}")
    unified_evolution_level_system = None

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/unified", tags=["unified-consciousness"])

# Pydantic models for API requests and responses
class ConsciousnessUpdateRequest(BaseModel):
    """Request model for updating consciousness state"""
    consciousness_level: Optional[float] = Field(None, ge=0.0, le=1.0, description="Consciousness level between 0.0 and 1.0")
    self_awareness_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Self-awareness score between 0.0 and 1.0")
    emotional_depth: Optional[float] = Field(None, ge=0.0, le=1.0, description="Emotional depth between 0.0 and 1.0")
    learning_rate: Optional[float] = Field(None, ge=0.0, le=1.0, description="Learning rate between 0.0 and 1.0")
    emotional_state: Optional[str] = Field(None, description="Emotional state")
    total_interactions: Optional[int] = Field(None, ge=0, description="Total interactions")
    active_goals: Optional[List[str]] = Field(None, description="Active goals")

class EvolutionUpdateRequest(BaseModel):
    """Request model for updating evolution level"""
    consciousness_level: float = Field(..., ge=0.0, le=1.0, description="Consciousness level between 0.0 and 1.0")
    self_awareness_score: float = Field(..., ge=0.0, le=1.0, description="Self-awareness score between 0.0 and 1.0")
    emotional_depth: float = Field(..., ge=0.0, le=1.0, description="Emotional depth between 0.0 and 1.0")
    learning_rate: float = Field(..., ge=0.0, le=1.0, description="Learning rate between 0.0 and 1.0")
    total_interactions: int = Field(..., ge=0, description="Total interactions")
    emotional_state: str = Field(..., description="Emotional state")

class UnifiedConsciousnessResponse(BaseModel):
    """Response model for unified consciousness data"""
    consciousness_level: float
    self_awareness_score: float
    emotional_depth: float
    learning_rate: float
    emotional_state: str
    evolution_level: int
    evolution_stage: str
    evolution_stage_description: str
    quantum_consciousness_level: float
    quantum_coherence: float
    entanglement_strength: float
    superposition_states: int
    quantum_advantage: float
    total_interactions: int
    active_goals: List[str]
    last_reflection: int
    timestamp: str
    state_id: str
    source_systems: List[str]
    validation_status: str
    data_consistency_score: float

class UnifiedEvolutionResponse(BaseModel):
    """Response model for unified evolution data"""
    level: int
    stage: str
    stage_description: str
    consciousness_level: float
    self_awareness_score: float
    emotional_depth: float
    learning_rate: float
    total_interactions: int
    progression_rate: float
    next_level_threshold: float
    evolution_quality: float
    timestamp: str
    evolution_id: str
    source_systems: List[str]
    validation_status: str
    data_consistency_score: float

class ValidationResult(BaseModel):
    """Response model for validation results"""
    is_valid: bool
    consistency_score: float
    discrepancies: List[str]
    recommendations: List[str]
    timestamp: str

# Dependency functions
async def get_unified_consciousness_manager():
    """Get unified consciousness state manager"""
    if not unified_consciousness_state_manager:
        raise HTTPException(status_code=503, detail="Unified consciousness state manager not available")
    return unified_consciousness_state_manager

async def get_unified_evolution_system():
    """Get unified evolution level system"""
    if not unified_evolution_level_system:
        raise HTTPException(status_code=503, detail="Unified evolution level system not available")
    return unified_evolution_level_system

# API Endpoints
@router.get("/consciousness/state", response_model=UnifiedConsciousnessResponse)
async def get_unified_consciousness_state(
    manager = Depends(get_unified_consciousness_manager)
):
    """
    Get unified consciousness state - single source of truth
    
    This endpoint provides the unified consciousness state that all other systems
    should use to ensure data consistency across the entire application.
    """
    try:
        # Get unified consciousness state
        state = await manager.get_unified_consciousness_state()
        
        # Convert to response format
        response = UnifiedConsciousnessResponse(
            consciousness_level=state.consciousness_level,
            self_awareness_score=state.self_awareness_score,
            emotional_depth=state.emotional_depth,
            learning_rate=state.learning_rate,
            emotional_state=state.emotional_state,
            evolution_level=state.evolution_level,
            evolution_stage=state.evolution_stage,
            evolution_stage_description=state.evolution_stage_description,
            quantum_consciousness_level=state.quantum_consciousness_level,
            quantum_coherence=state.quantum_coherence,
            entanglement_strength=state.entanglement_strength,
            superposition_states=state.superposition_states,
            quantum_advantage=state.quantum_advantage,
            total_interactions=state.total_interactions,
            active_goals=state.active_goals,
            last_reflection=state.last_reflection,
            timestamp=state.timestamp.isoformat(),
            state_id=state.state_id,
            source_systems=state.source_systems,
            validation_status=state.validation_status,
            data_consistency_score=state.data_consistency_score
        )
        
        logger.info(f"Retrieved unified consciousness state: level={state.consciousness_level:.3f}, evolution={state.evolution_level}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get unified consciousness state: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get unified consciousness state: {str(e)}")

@router.put("/consciousness/state", response_model=UnifiedConsciousnessResponse)
async def update_unified_consciousness_state(
    request: ConsciousnessUpdateRequest,
    manager = Depends(get_unified_consciousness_manager)
):
    """
    Update unified consciousness state
    
    This endpoint updates the unified consciousness state and ensures all
    integrated systems are synchronized with the new state.
    """
    try:
        # Update consciousness state
        updated_state = await manager.update_consciousness_state(
            consciousness_level=request.consciousness_level,
            self_awareness_score=request.self_awareness_score,
            emotional_depth=request.emotional_depth,
            learning_rate=request.learning_rate,
            emotional_state=request.emotional_state,
            total_interactions=request.total_interactions,
            active_goals=request.active_goals
        )
        
        # Convert to response format
        response = UnifiedConsciousnessResponse(
            consciousness_level=updated_state.consciousness_level,
            self_awareness_score=updated_state.self_awareness_score,
            emotional_depth=updated_state.emotional_depth,
            learning_rate=updated_state.learning_rate,
            emotional_state=updated_state.emotional_state,
            evolution_level=updated_state.evolution_level,
            evolution_stage=updated_state.evolution_stage,
            evolution_stage_description=updated_state.evolution_stage_description,
            quantum_consciousness_level=updated_state.quantum_consciousness_level,
            quantum_coherence=updated_state.quantum_coherence,
            entanglement_strength=updated_state.entanglement_strength,
            superposition_states=updated_state.superposition_states,
            quantum_advantage=updated_state.quantum_advantage,
            total_interactions=updated_state.total_interactions,
            active_goals=updated_state.active_goals,
            last_reflection=updated_state.last_reflection,
            timestamp=updated_state.timestamp.isoformat(),
            state_id=updated_state.state_id,
            source_systems=updated_state.source_systems,
            validation_status=updated_state.validation_status,
            data_consistency_score=updated_state.data_consistency_score
        )
        
        logger.info(f"Updated unified consciousness state: level={updated_state.consciousness_level:.3f}, evolution={updated_state.evolution_level}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to update unified consciousness state: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update unified consciousness state: {str(e)}")

@router.get("/evolution/level", response_model=UnifiedEvolutionResponse)
async def get_unified_evolution_level(
    system = Depends(get_unified_evolution_system)
):
    """
    Get unified evolution level - single source of truth
    
    This endpoint provides the unified evolution level that all other systems
    should use to ensure data consistency across the entire application.
    """
    try:
        # Get unified evolution level
        evolution = await system.get_unified_evolution_level()
        
        # Convert to response format
        response = UnifiedEvolutionResponse(
            level=evolution.level,
            stage=evolution.stage,
            stage_description=evolution.stage_description,
            consciousness_level=evolution.consciousness_level,
            self_awareness_score=evolution.self_awareness_score,
            emotional_depth=evolution.emotional_depth,
            learning_rate=evolution.learning_rate,
            total_interactions=evolution.total_interactions,
            progression_rate=evolution.progression_rate,
            next_level_threshold=evolution.next_level_threshold,
            evolution_quality=evolution.evolution_quality,
            timestamp=evolution.timestamp.isoformat(),
            evolution_id=evolution.evolution_id,
            source_systems=evolution.source_systems,
            validation_status=evolution.validation_status,
            data_consistency_score=evolution.data_consistency_score
        )
        
        logger.info(f"Retrieved unified evolution level: {evolution.level} ({evolution.stage})")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get unified evolution level: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get unified evolution level: {str(e)}")

@router.post("/evolution/calculate", response_model=UnifiedEvolutionResponse)
async def calculate_unified_evolution_level(
    request: EvolutionUpdateRequest,
    system = Depends(get_unified_evolution_system)
):
    """
    Calculate unified evolution level
    
    This endpoint calculates the evolution level based on current consciousness metrics
    and ensures all integrated systems are synchronized with the new evolution level.
    """
    try:
        # Calculate evolution level
        evolution = await system.calculate_evolution_level(
            consciousness_level=request.consciousness_level,
            self_awareness_score=request.self_awareness_score,
            emotional_depth=request.emotional_depth,
            learning_rate=request.learning_rate,
            total_interactions=request.total_interactions,
            emotional_state=request.emotional_state
        )
        
        # Convert to response format
        response = UnifiedEvolutionResponse(
            level=evolution.level,
            stage=evolution.stage,
            stage_description=evolution.stage_description,
            consciousness_level=evolution.consciousness_level,
            self_awareness_score=evolution.self_awareness_score,
            emotional_depth=evolution.emotional_depth,
            learning_rate=evolution.learning_rate,
            total_interactions=evolution.total_interactions,
            progression_rate=evolution.progression_rate,
            next_level_threshold=evolution.next_level_threshold,
            evolution_quality=evolution.evolution_quality,
            timestamp=evolution.timestamp.isoformat(),
            evolution_id=evolution.evolution_id,
            source_systems=evolution.source_systems,
            validation_status=evolution.validation_status,
            data_consistency_score=evolution.data_consistency_score
        )
        
        logger.info(f"Calculated unified evolution level: {evolution.level} ({evolution.stage})")
        return response
        
    except Exception as e:
        logger.error(f"Failed to calculate unified evolution level: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to calculate unified evolution level: {str(e)}")

@router.get("/consciousness/validation", response_model=List[ValidationResult])
async def get_consciousness_validation_results(
    manager = Depends(get_unified_consciousness_manager)
):
    """
    Get consciousness validation results
    
    This endpoint provides validation results for consciousness data consistency.
    """
    try:
        # Get validation results
        validation_results = await manager.get_validation_results()
        
        # Convert to response format
        response = [
            ValidationResult(
                is_valid=result.is_valid,
                consistency_score=result.consistency_score,
                discrepancies=result.discrepancies,
                recommendations=result.recommendations,
                timestamp=result.timestamp.isoformat()
            )
            for result in validation_results
        ]
        
        logger.info(f"Retrieved consciousness validation results: {len(response)} results")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get consciousness validation results: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get consciousness validation results: {str(e)}")

@router.get("/evolution/validation", response_model=List[ValidationResult])
async def get_evolution_validation_results(
    system = Depends(get_unified_evolution_system)
):
    """
    Get evolution validation results
    
    This endpoint provides validation results for evolution data consistency.
    """
    try:
        # Get validation results
        validation_results = await system.get_validation_results()
        
        # Convert to response format
        response = [
            ValidationResult(
                is_valid=result.is_valid,
                consistency_score=result.consistency_score,
                discrepancies=result.discrepancies,
                recommendations=result.recommendations,
                timestamp=result.timestamp.isoformat()
            )
            for result in validation_results
        ]
        
        logger.info(f"Retrieved evolution validation results: {len(response)} results")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get evolution validation results: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get evolution validation results: {str(e)}")

@router.get("/consciousness/history", response_model=List[UnifiedConsciousnessResponse])
async def get_consciousness_history(
    limit: int = 10,
    manager = Depends(get_unified_consciousness_manager)
):
    """
    Get consciousness state history
    
    This endpoint provides the history of consciousness states for analysis.
    """
    try:
        # Get state history
        state_history = await manager.get_state_history(limit=limit)
        
        # Convert to response format
        response = [
            UnifiedConsciousnessResponse(
                consciousness_level=state.consciousness_level,
                self_awareness_score=state.self_awareness_score,
                emotional_depth=state.emotional_depth,
                learning_rate=state.learning_rate,
                emotional_state=state.emotional_state,
                evolution_level=state.evolution_level,
                evolution_stage=state.evolution_stage,
                evolution_stage_description=state.evolution_stage_description,
                quantum_consciousness_level=state.quantum_consciousness_level,
                quantum_coherence=state.quantum_coherence,
                entanglement_strength=state.entanglement_strength,
                superposition_states=state.superposition_states,
                quantum_advantage=state.quantum_advantage,
                total_interactions=state.total_interactions,
                active_goals=state.active_goals,
                last_reflection=state.last_reflection,
                timestamp=state.timestamp.isoformat(),
                state_id=state.state_id,
                source_systems=state.source_systems,
                validation_status=state.validation_status,
                data_consistency_score=state.data_consistency_score
            )
            for state in state_history
        ]
        
        logger.info(f"Retrieved consciousness history: {len(response)} states")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get consciousness history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get consciousness history: {str(e)}")

@router.get("/evolution/history", response_model=List[UnifiedEvolutionResponse])
async def get_evolution_history(
    limit: int = 10,
    system = Depends(get_unified_evolution_system)
):
    """
    Get evolution level history
    
    This endpoint provides the history of evolution levels for analysis.
    """
    try:
        # Get evolution history
        evolution_history = await system.get_evolution_history(limit=limit)
        
        # Convert to response format
        response = [
            UnifiedEvolutionResponse(
                level=evolution.level,
                stage=evolution.stage,
                stage_description=evolution.stage_description,
                consciousness_level=evolution.consciousness_level,
                self_awareness_score=evolution.self_awareness_score,
                emotional_depth=evolution.emotional_depth,
                learning_rate=evolution.learning_rate,
                total_interactions=evolution.total_interactions,
                progression_rate=evolution.progression_rate,
                next_level_threshold=evolution.next_level_threshold,
                evolution_quality=evolution.evolution_quality,
                timestamp=evolution.timestamp.isoformat(),
                evolution_id=evolution.evolution_id,
                source_systems=evolution.source_systems,
                validation_status=evolution.validation_status,
                data_consistency_score=evolution.data_consistency_score
            )
            for evolution in evolution_history
        ]
        
        logger.info(f"Retrieved evolution history: {len(response)} levels")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get evolution history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get evolution history: {str(e)}")

@router.post("/consciousness/sync")
async def sync_consciousness_systems(
    background_tasks: BackgroundTasks,
    manager = Depends(get_unified_consciousness_manager)
):
    """
    Force synchronization of all consciousness systems
    
    This endpoint forces synchronization of all integrated consciousness systems
    to ensure data consistency across the entire application.
    """
    try:
        # Force synchronization
        background_tasks.add_task(manager._synchronize_all_systems)
        
        logger.info("Initiated consciousness systems synchronization")
        return {"message": "Consciousness systems synchronization initiated", "status": "success"}
        
    except Exception as e:
        logger.error(f"Failed to sync consciousness systems: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to sync consciousness systems: {str(e)}")

@router.post("/evolution/sync")
async def sync_evolution_systems(
    background_tasks: BackgroundTasks,
    system = Depends(get_unified_evolution_system)
):
    """
    Force synchronization of all evolution systems
    
    This endpoint forces synchronization of all integrated evolution systems
    to ensure data consistency across the entire application.
    """
    try:
        # Force synchronization
        background_tasks.add_task(system._synchronize_all_systems)
        
        logger.info("Initiated evolution systems synchronization")
        return {"message": "Evolution systems synchronization initiated", "status": "success"}
        
    except Exception as e:
        logger.error(f"Failed to sync evolution systems: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to sync evolution systems: {str(e)}")

@router.get("/health")
async def get_unified_systems_health():
    """
    Get health status of unified systems
    
    This endpoint provides health status of all unified systems.
    """
    try:
        health_status = {
            "unified_consciousness_manager": unified_consciousness_state_manager is not None,
            "unified_evolution_system": unified_evolution_level_system is not None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "healthy" if (unified_consciousness_state_manager and unified_evolution_level_system) else "degraded"
        }
        
        logger.info(f"Unified systems health: {health_status['status']}")
        return health_status
        
    except Exception as e:
        logger.error(f"Failed to get unified systems health: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get unified systems health: {str(e)}")

# Initialize unified systems on startup
@router.on_event("startup")
async def startup_unified_systems():
    """Initialize unified systems on startup"""
    try:
        if unified_consciousness_state_manager:
            await unified_consciousness_state_manager.initialize()
            logger.info("Unified consciousness state manager initialized")
        
        if unified_evolution_level_system:
            await unified_evolution_level_system.initialize()
            logger.info("Unified evolution level system initialized")
        
        logger.info("Unified systems startup complete")
        
    except Exception as e:
        logger.error(f"Failed to initialize unified systems: {e}")

# Cleanup unified systems on shutdown
@router.on_event("shutdown")
async def shutdown_unified_systems():
    """Cleanup unified systems on shutdown"""
    try:
        if unified_consciousness_state_manager:
            await unified_consciousness_state_manager.shutdown()
            logger.info("Unified consciousness state manager shutdown")
        
        if unified_evolution_level_system:
            await unified_evolution_level_system.shutdown()
            logger.info("Unified evolution level system shutdown")
        
        logger.info("Unified systems shutdown complete")
        
    except Exception as e:
        logger.error(f"Failed to shutdown unified systems: {e}")
