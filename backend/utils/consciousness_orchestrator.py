"""
FIXED Consciousness Orchestrator for Mainza AI
Central system for managing and coordinating all consciousness processes
CRITICAL FIX: Reduced frequency and impact to prevent throttling user conversations
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
try:
    from backend.agents.self_reflection import self_reflection_agent
except (ImportError, ValueError):
    self_reflection_agent = None

from backend.models.consciousness_models import ConsciousnessState, ConsciousnessCycleResult, EmotionalState
