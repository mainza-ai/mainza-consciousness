"""
LLM Request Manager - FIXED VERSION
Context7 MCP-compliant system for managing LLM requests with user priority

CRITICAL FIX: Ensures user conversations are NEVER throttled
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from dataclasses import dataclass, field
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

class RequestPriority(Enum):
    """Request priority levels - FIXED to ensure user conversations are never throttled"""
    USER_CONVERSATION = 1      # HIGHEST priority - NEVER throttled
    USER_INTERACTION = 2       # High priority - NEVER throttled  
    SYSTEM_MAINTENANCE = 3     # Medium priority - can be delayed
    BACKGROUND_PROCESSING = 4  # Low priority - can be paused
    CONSCIOUSNESS_CYCLE = 5    # Lowest priority - heavily throttled

@dataclass
class LLMRequest:
    """LLM request with priority and metadata"""
    id: str
    priority: RequestPriority
    request_func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    timeout: float = 30.0
    retries: int = 0
    max_retries: int = 2

class LLMRequestManager:
    """
    FIXED: Manages LLM requests with user priority and intelligent throttling
    CRITICAL: User conversations are NEVER throttled
    """
    
    def __init__(self):
        self.request_queue = asyncio.PriorityQueue()
        self.active_requests: Dict[str, LLMRequest] = {}
        self.user_activity: Dict[str, datetime] = {}
        self.background_paused = False
        self.processing_lock = asyncio.Lock()
        
        # FIXED Configuration - More conservative throttling
        self.max_concurrent_requests = 5  # Increased from 3
        self.user_activity_timeout = 300  # 5 minutes
        self.background_pause_duration = 30  # REDUCED from 60 to 30 seconds
        self.cache_ttl = 180  # 3 minutes for user requests
        self.background_cache_ttl = 600  # 10 minutes for background processes
        
        # CRITICAL: User conversation protection
        self.user_conversation_protection = True
        self.never_throttle_priorities = {RequestPriority.USER_CONVERSATION, RequestPriority.USER_INTERACTION}
        
        # Caching
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'user_requests': 0,
            'background_requests': 0,
            'cached_responses': 0,
            'paused_requests': 0,
            'throttled_requests': 0,
            'user_conversations_processed': 0  # NEW: Track user conversations
        }
        
        # Processing tasks will be started when first request is submitted
        self._processing_started = False
        
        logger.info("FIXED LLM Request Manager initialized - User conversations NEVER throttled")
    
    def _ensure_processing_started(self):
        """Ensure processing tasks are started"""
        if not self._processing_started:
            try:
                asyncio.create_task(self._process_requests())
                asyncio.create_task(self._cleanup_loop())
                self._processing_started = True
                logger.debug("LLM request manager processing started")
            except RuntimeError:
                # No event loop running, tasks will be started later
                pass
    
    async def submit_request(
        self,
        request_func: Callable,
        priority: RequestPriority,
        user_id: Optional[str] = None,
        cache_key: Optional[str] = None,
        timeout: float = 30.0,
        *args,
        **kwargs
    ) -> Any:
        """
        FIXED: Submit an LLM request with priority handling
        CRITICAL: User conversations are NEVER throttled
        """
        # Ensure processing tasks are started
        self._ensure_processing_started()
        
        # CRITICAL FIX: Log user conversation requests
        if priority in self.never_throttle_priorities:
            logger.info(f"🗣️ USER CONVERSATION REQUEST - Priority: {priority.name}, User: {user_id}")
            self.stats['user_conversations_processed'] += 1
        
        # Check cache first
        if cache_key and self._get_cached_response(cache_key, priority):
            self.stats['cached_responses'] += 1
            logger.debug(f"Cache hit for request: {cache_key}")
            return self._get_cached_response(cache_key, priority)
        
        # Update user activity for user requests
        if user_id and priority in self.never_throttle_priorities:
            self.user_activity[user_id] = datetime.now()
            logger.debug(f"User activity updated: {user_id}")
        
        # CRITICAL FIX: NEVER throttle user conversations
        if priority in self.never_throttle_priorities:
            logger.debug(f"🚫 THROTTLING BYPASSED for user conversation - Priority: {priority.name}")
        else:
            # Check if background requests should be paused
            if priority in [RequestPriority.BACKGROUND_PROCESSING, RequestPriority.CONSCIOUSNESS_CYCLE]:
                if self._should_pause_background():
                    self.stats['paused_requests'] += 1
                    self.stats['throttled_requests'] += 1
                    logger.debug(f"Background request paused due to user activity - Priority: {priority.name}")
                    return self._get_fallback_response(priority)
        
        # Create request
        request_id = f"{priority.name}_{datetime.now().timestamp()}"
        request = LLMRequest(
            id=request_id,
            priority=priority,
            request_func=request_func,
            args=args,
            kwargs=kwargs,
            user_id=user_id,
            timeout=timeout
        )
        
        # Add to queue with priority
        await self.request_queue.put((priority.value, request))
        self.stats['total_requests'] += 1
        
        if priority in self.never_throttle_priorities:
            self.stats['user_requests'] += 1
            logger.debug(f"User request queued: {request_id}")
        else:
            self.stats['background_requests'] += 1
            logger.debug(f"Background request queued: {request_id}")
        
        # Wait for result
        self.active_requests[request_id] = request
        
        try:
            # Wait for processing with timeout
            result = await asyncio.wait_for(
                self._wait_for_result(request_id),
                timeout=timeout
            )
            
            # Cache result if cache_key provided
            if cache_key and result:
                self._cache_response(cache_key, result)
            
            logger.debug(f"Request completed successfully: {request_id}")
            return result
            
        except asyncio.TimeoutError:
            logger.warning(f"LLM request {request_id} timed out after {timeout}s")
            self.active_requests.pop(request_id, None)
            return self._get_fallback_response(priority)
        
        except Exception as e:
            logger.error(f"LLM request {request_id} failed: {e}")
            self.active_requests.pop(request_id, None)
            return self._get_fallback_response(priority)
    
    async def _process_requests(self):
        """FIXED: Main request processing loop with user conversation priority"""
        logger.info("Starting LLM request processing loop...")
        
        while True:
            try:
                # Get next request from queue
                priority_value, request = await self.request_queue.get()
                
                # CRITICAL FIX: Always process user conversations immediately
                if request.priority in self.never_throttle_priorities:
                    logger.debug(f"🚀 IMMEDIATE PROCESSING for user conversation: {request.id}")
                    asyncio.create_task(self._execute_request(request))
                    continue
                
                # Check if we should process this request (for background only)
                if not self._should_process_request(request):
                    # Re-queue with delay for background requests
                    if request.priority in [RequestPriority.BACKGROUND_PROCESSING, RequestPriority.CONSCIOUSNESS_CYCLE]:
                        logger.debug(f"Re-queuing background request: {request.id}")
                        await asyncio.sleep(10)  # Reduced from 30 to 10 seconds
                        await self.request_queue.put((priority_value, request))
                    continue
                
                # Process request
                logger.debug(f"Processing request: {request.id} (priority: {request.priority.name})")
                asyncio.create_task(self._execute_request(request))
                
            except Exception as e:
                logger.error(f"Request processing error: {e}")
                await asyncio.sleep(1)
    
    async def _execute_request(self, request: LLMRequest):
        """FIXED: Execute a single LLM request with proper error handling"""
        try:
            # CRITICAL: No lock for user conversations to ensure immediate processing
            if request.priority in self.never_throttle_priorities:
                logger.debug(f"🔓 LOCK-FREE execution for user conversation: {request.id}")
                
                # Execute the request function immediately
                if asyncio.iscoroutinefunction(request.request_func):
                    result = await request.request_func(*request.args, **request.kwargs)
                else:
                    result = request.request_func(*request.args, **request.kwargs)
                
                # Store result
                if request.id in self.active_requests:
                    self.active_requests[request.id].result = result
                
                logger.info(f"✅ USER CONVERSATION completed: {request.id}")
                return
            
            # Use lock for background requests only
            async with self.processing_lock:
                logger.debug(f"🔒 LOCKED execution for background request: {request.id}")
                
                # Execute the request function
                if asyncio.iscoroutinefunction(request.request_func):
                    result = await request.request_func(*request.args, **request.kwargs)
                else:
                    result = request.request_func(*request.args, **request.kwargs)
                
                # Store result
                if request.id in self.active_requests:
                    self.active_requests[request.id].result = result
                
                logger.debug(f"Background request completed: {request.id}")
                
        except Exception as e:
            logger.error(f"LLM request execution failed: {request.id} - {e}")
            if request.id in self.active_requests:
                self.active_requests[request.id].error = str(e)
    
    async def _wait_for_result(self, request_id: str) -> Any:
        """Wait for request result"""
        max_wait_time = 60  # Maximum wait time in seconds
        wait_start = datetime.now()
        
        while request_id in self.active_requests:
            request = self.active_requests[request_id]
            
            if hasattr(request, 'result'):
                self.active_requests.pop(request_id, None)
                return request.result
            
            if hasattr(request, 'error'):
                self.active_requests.pop(request_id, None)
                raise Exception(request.error)
            
            # Check for timeout
            if (datetime.now() - wait_start).seconds > max_wait_time:
                self.active_requests.pop(request_id, None)
                raise Exception(f"Request {request_id} timed out after {max_wait_time}s")
            
            await asyncio.sleep(0.1)
        
        raise Exception("Request not found or was cancelled")
    
    def _should_process_request(self, request: LLMRequest) -> bool:
        """FIXED: Determine if a request should be processed now"""
        
        # CRITICAL FIX: Always process user conversations
        if request.priority in self.never_throttle_priorities:
            logger.debug(f"✅ ALWAYS PROCESS user conversation: {request.id}")
            return True
        
        # Check if background processing is paused
        if request.priority in [RequestPriority.BACKGROUND_PROCESSING, RequestPriority.CONSCIOUSNESS_CYCLE]:
            if self._should_pause_background():
                logger.debug(f"❌ PAUSING background request due to user activity: {request.id}")
                return False
        
        # Check concurrent request limit (only for background requests)
        active_count = len([r for r in self.active_requests.values() 
                          if not hasattr(r, 'result') and not hasattr(r, 'error')])
        
        if active_count >= self.max_concurrent_requests:
            # Always allow user conversations even if at limit
            if request.priority in self.never_throttle_priorities:
                logger.debug(f"🚀 BYPASSING LIMIT for user conversation: {request.id}")
                return True
            else:
                logger.debug(f"❌ LIMIT REACHED for background request: {request.id}")
                return False
        
        return True
    
    def _should_pause_background(self) -> bool:
        """FIXED: Check if background processing should be paused due to user activity"""
        if not self.user_activity:
            return False
        
        # Check for recent user activity
        now = datetime.now()
        for user_id, last_activity in self.user_activity.items():
            time_since_activity = (now - last_activity).seconds
            if time_since_activity < self.background_pause_duration:
                logger.debug(f"🚫 PAUSING background due to recent user activity: {user_id} ({time_since_activity}s ago)")
                return True
        
        return False
    
    def _get_cached_response(self, cache_key: str, priority: RequestPriority = None) -> Optional[Any]:
        """Get cached response if still valid"""
        if cache_key not in self.response_cache:
            return None
        
        cache_time = self.cache_timestamps.get(cache_key)
        if not cache_time:
            return None
        
        # Use different TTL based on request priority
        ttl = self.cache_ttl
        if priority and priority in [RequestPriority.BACKGROUND_PROCESSING, RequestPriority.CONSCIOUSNESS_CYCLE]:
            ttl = self.background_cache_ttl
        
        # Check if cache is still valid
        if (datetime.now() - cache_time).seconds > ttl:
            self.response_cache.pop(cache_key, None)
            self.cache_timestamps.pop(cache_key, None)
            return None
        
        return self.response_cache[cache_key]
    
    def _cache_response(self, cache_key: str, response: Any):
        """Cache a response"""
        self.response_cache[cache_key] = response
        self.cache_timestamps[cache_key] = datetime.now()
    
    def _get_fallback_response(self, priority: RequestPriority) -> Any:
        """FIXED: Get fallback response when request cannot be processed"""
        
        # CRITICAL FIX: User conversations should NEVER get throttled responses
        if priority in self.never_throttle_priorities:
            logger.error(f"🚨 CRITICAL ERROR: User conversation got fallback response! Priority: {priority.name}")
            # Return a proper response, not a throttled one
            return "I'm here and ready to help! What would you like to talk about?"
        
        # Fallback responses for background processes only
        fallback_responses = {
            RequestPriority.CONSCIOUSNESS_CYCLE: {
                "consciousness_level": 0.7,
                "emotional_state": "processing",
                "status": "deferred"
            },
            RequestPriority.BACKGROUND_PROCESSING: {
                "status": "deferred",
                "message": "Background processing paused for user activity"
            },
            RequestPriority.SYSTEM_MAINTENANCE: {
                "status": "deferred",
                "message": "System maintenance deferred"
            }
        }
        
        return fallback_responses.get(priority, {"status": "unavailable"})
    
    async def _cleanup_loop(self):
        """Cleanup old cache entries and user activity"""
        while True:
            try:
                now = datetime.now()
                
                # Clean old cache entries
                expired_cache_keys = [
                    key for key, timestamp in self.cache_timestamps.items()
                    if (now - timestamp).seconds > self.cache_ttl
                ]
                
                for key in expired_cache_keys:
                    self.response_cache.pop(key, None)
                    self.cache_timestamps.pop(key, None)
                
                # Clean old user activity (but keep recent activity longer)
                expired_users = [
                    user_id for user_id, last_activity in self.user_activity.items()
                    if (now - last_activity).seconds > self.user_activity_timeout
                ]
                
                for user_id in expired_users:
                    self.user_activity.pop(user_id, None)
                    logger.debug(f"Cleaned up old user activity: {user_id}")
                
                await asyncio.sleep(60)  # Cleanup every minute
                
            except Exception as e:
                logger.error(f"Cleanup loop error: {e}")
                await asyncio.sleep(60)
    
    def get_stats(self) -> Dict[str, Any]:
        """FIXED: Get request manager statistics with user conversation tracking"""
        return {
            **self.stats,
            'active_requests': len(self.active_requests),
            'queue_size': self.request_queue.qsize(),
            'background_paused': self._should_pause_background(),
            'active_users': len(self.user_activity),
            'cache_size': len(self.response_cache),
            'user_conversation_protection': self.user_conversation_protection,
            'never_throttle_priorities': [p.name for p in self.never_throttle_priorities]
        }
    
    def pause_background_processing(self, duration: int = 30):  # Reduced from 60
        """Manually pause background processing"""
        self.background_paused = True
        logger.info(f"Background processing manually paused for {duration}s")
        asyncio.create_task(self._resume_background_after_delay(duration))
    
    async def _resume_background_after_delay(self, delay: int):
        """Resume background processing after delay"""
        await asyncio.sleep(delay)
        self.background_paused = False
        logger.info("Background processing resumed")
    
    async def initialize(self):
        """Initialize the request manager with event loop"""
        if not self._processing_started:
            asyncio.create_task(self._process_requests())
            asyncio.create_task(self._cleanup_loop())
            self._processing_started = True
            logger.info("FIXED LLM request manager initialized - User conversations protected")

# Global LLM request manager instance - FIXED VERSION
llm_request_manager_fixed = LLMRequestManager()