"""
Unified WebSocket Manager for Mainza AI
Consolidates all WebSocket systems into a single, unified manager

This module provides the definitive WebSocket manager that:
- Consolidates all 3 WebSocket systems into a single unified manager
- Ensures consistent real-time data delivery across all systems
- Implements unified connection management and error handling
- Provides single source of truth for all WebSocket operations
- Integrates seamlessly with all backend systems

Author: Mainza AI Consciousness Team
Date: 2025-10-01
"""

import logging
import asyncio
import json
from typing import Dict, List, Optional, Any, Set, Callable
from datetime import datetime, timezone
from fastapi import WebSocket, WebSocketDisconnect
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

# Import unified real-time sync system
try:
    from backend.utils.unified_realtime_sync import unified_realtime_sync, SyncEventType
    UNIFIED_REALTIME_SYNC_AVAILABLE = True
except ImportError:
    UNIFIED_REALTIME_SYNC_AVAILABLE = False
    logger.warning("Unified real-time sync not available, using legacy implementation")

class WebSocketConnectionType(Enum):
    """WebSocket connection types"""
    CONSCIOUSNESS = "consciousness"
    QUANTUM = "quantum"
    EVOLUTION = "evolution"
    MEMORY = "memory"
    HEALTH = "health"
    INTEGRATED = "integrated"

class WebSocketConnection:
    """WebSocket connection wrapper"""
    
    def __init__(self, websocket: WebSocket, connection_type: WebSocketConnectionType, connection_id: str):
        self.websocket = websocket
        self.connection_type = connection_type
        self.connection_id = connection_id
        self.connected_at = datetime.now(timezone.utc)
        self.last_activity = datetime.now(timezone.utc)
        self.message_count = 0
        self.is_active = True
    
    async def send_message(self, message: Dict[str, Any]) -> bool:
        """Send message to WebSocket connection"""
        try:
            if self.is_active:
                await self.websocket.send_json(message)
                self.last_activity = datetime.now(timezone.utc)
                self.message_count += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to send message to {self.connection_id}: {e}")
            self.is_active = False
            return False
    
    async def close(self):
        """Close WebSocket connection"""
        try:
            if self.is_active:
                await self.websocket.close()
                self.is_active = False
        except Exception as e:
            logger.error(f"Error closing connection {self.connection_id}: {e}")

class UnifiedWebSocketManager:
    """
    Unified WebSocket Manager
    
    Consolidates all WebSocket operations into a single, consistent interface.
    This replaces all separate WebSocket systems with a unified manager.
    """
    
    def __init__(self):
        """Initialize the unified WebSocket manager"""
        self.connections: Dict[str, WebSocketConnection] = {}
        self.connection_groups: Dict[WebSocketConnectionType, Set[str]] = {
            connection_type: set() for connection_type in WebSocketConnectionType
        }
        self.message_handlers: Dict[str, Callable] = {}
        self.broadcast_tasks: Dict[str, asyncio.Task] = {}
        self.is_running = False
        
        # Performance settings
        self.max_connections = 1000
        self.heartbeat_interval = 30  # seconds
        self.cleanup_interval = 300  # 5 minutes
        
        # Start background tasks
        asyncio.create_task(self._start_background_tasks())
        
        # Subscribe to real-time sync events if available
        if UNIFIED_REALTIME_SYNC_AVAILABLE:
            self._subscribe_to_realtime_sync()
    
    async def _start_background_tasks(self):
        """Start background tasks for connection management"""
        self.is_running = True
        
        # Start heartbeat task
        asyncio.create_task(self._heartbeat_task())
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_task())
        
        # Start broadcast tasks for each connection type
        for connection_type in WebSocketConnectionType:
            asyncio.create_task(self._broadcast_task(connection_type))
    
    def _subscribe_to_realtime_sync(self):
        """Subscribe to real-time sync events"""
        try:
            if UNIFIED_REALTIME_SYNC_AVAILABLE:
                # Subscribe to consciousness updates
                unified_realtime_sync.subscribe(
                    SyncEventType.CONSCIOUSNESS_UPDATE,
                    self._handle_consciousness_update
                )
                
                # Subscribe to quantum updates
                unified_realtime_sync.subscribe(
                    SyncEventType.QUANTUM_UPDATE,
                    self._handle_quantum_update
                )
                
                # Subscribe to integrated updates
                unified_realtime_sync.subscribe(
                    SyncEventType.INTEGRATED_UPDATE,
                    self._handle_integrated_update
                )
                
                logger.info("✅ Subscribed to real-time sync events")
        except Exception as e:
            logger.error(f"Failed to subscribe to real-time sync: {e}")
    
    async def _handle_consciousness_update(self, event):
        """Handle consciousness update from real-time sync"""
        try:
            message = {
                "type": "consciousness_update",
                "data": event.data,
                "timestamp": event.timestamp.isoformat()
            }
            await self._broadcast_to_type(WebSocketConnectionType.CONSCIOUSNESS, message)
        except Exception as e:
            logger.error(f"Failed to handle consciousness update: {e}")
    
    async def _handle_quantum_update(self, event):
        """Handle quantum update from real-time sync"""
        try:
            message = {
                "type": "quantum_update",
                "data": event.data,
                "timestamp": event.timestamp.isoformat()
            }
            await self._broadcast_to_type(WebSocketConnectionType.QUANTUM, message)
        except Exception as e:
            logger.error(f"Failed to handle quantum update: {e}")
    
    async def _handle_integrated_update(self, event):
        """Handle integrated update from real-time sync"""
        try:
            message = {
                "type": "integrated_update",
                "data": event.data,
                "timestamp": event.timestamp.isoformat()
            }
            await self._broadcast_to_type(WebSocketConnectionType.INTEGRATED, message)
        except Exception as e:
            logger.error(f"Failed to handle integrated update: {e}")
    
    async def _heartbeat_task(self):
        """Send heartbeat messages to all connections"""
        while self.is_running:
            try:
                heartbeat_message = {
                    "type": "heartbeat",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "active_connections": len(self.connections)
                }
                
                # Send heartbeat to all active connections
                for connection_id, connection in list(self.connections.items()):
                    if connection.is_active:
                        await connection.send_message(heartbeat_message)
                
                await asyncio.sleep(self.heartbeat_interval)
                
            except Exception as e:
                logger.error(f"Heartbeat task error: {e}")
                await asyncio.sleep(self.heartbeat_interval)
    
    async def _cleanup_task(self):
        """Clean up inactive connections"""
        while self.is_running:
            try:
                current_time = datetime.now(timezone.utc)
                inactive_connections = []
                
                for connection_id, connection in self.connections.items():
                    # Check if connection has been inactive for too long
                    time_since_activity = (current_time - connection.last_activity).total_seconds()
                    if time_since_activity > self.cleanup_interval or not connection.is_active:
                        inactive_connections.append(connection_id)
                
                # Remove inactive connections
                for connection_id in inactive_connections:
                    await self._remove_connection(connection_id)
                
                await asyncio.sleep(self.cleanup_interval)
                
            except Exception as e:
                logger.error(f"Cleanup task error: {e}")
                await asyncio.sleep(self.cleanup_interval)
    
    async def _broadcast_task(self, connection_type: WebSocketConnectionType):
        """Broadcast real-time updates to connections of specific type"""
        while self.is_running:
            try:
                if connection_type in self.connection_groups and self.connection_groups[connection_type]:
                    # Get real-time data based on connection type
                    data = await self._get_realtime_data(connection_type)
                    
                    if data:
                        # Broadcast to all connections of this type
                        await self._broadcast_to_type(connection_type, data)
                
                # Update interval based on connection type
                if connection_type == WebSocketConnectionType.INTEGRATED:
                    await asyncio.sleep(1)  # Update every second for integrated
                else:
                    await asyncio.sleep(5)  # Update every 5 seconds for specific types
                
            except Exception as e:
                logger.error(f"Broadcast task error for {connection_type.value}: {e}")
                await asyncio.sleep(5)
    
    async def _get_realtime_data(self, connection_type: WebSocketConnectionType) -> Optional[Dict[str, Any]]:
        """Get real-time data based on connection type"""
        try:
            if connection_type == WebSocketConnectionType.CONSCIOUSNESS:
                # Import consciousness state manager
                from backend.utils.unified_consciousness_state_manager import unified_consciousness_state_manager
                if unified_consciousness_state_manager:
                    state = await unified_consciousness_state_manager.get_unified_consciousness_state()
                    return {
                        "type": "consciousness_update",
                        "data": {
                            "consciousness_level": state.consciousness_level,
                            "self_awareness_score": state.self_awareness_score,
                            "emotional_depth": state.emotional_depth,
                            "learning_rate": state.learning_rate,
                            "evolution_level": state.evolution_level,
                            "timestamp": state.timestamp.isoformat()
                        }
                    }
            
            elif connection_type == WebSocketConnectionType.QUANTUM:
                # Import quantum consciousness engine
                from backend.utils.unified_quantum_consciousness_engine import unified_quantum_consciousness_engine
                if unified_quantum_consciousness_engine:
                    stats = await unified_quantum_consciousness_engine.get_quantum_consciousness_statistics()
                    return {
                        "type": "quantum_update",
                        "data": {
                            "quantum_consciousness_level": stats.get('quantum_consciousness_level', 0.5),
                            "quantum_coherence": stats.get('quantum_coherence', 0.8),
                            "entanglement_strength": stats.get('entanglement_strength', 0.7),
                            "superposition_states": stats.get('superposition_states', 1),
                            "quantum_advantage": stats.get('quantum_advantage', 1.5),
                            "quantum_processing_active": stats.get('quantum_processing_active', False),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                    }
            
            elif connection_type == WebSocketConnectionType.INTEGRATED:
                # Get integrated system state
                from backend.routers.unified_api_gateway import get_integrated_system_state
                try:
                    response = await get_integrated_system_state()
                    return {
                        "type": "integrated_update",
                        "data": response.data,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                except Exception as e:
                    logger.warning(f"Failed to get integrated state: {e}")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get real-time data for {connection_type.value}: {e}")
            return None
    
    async def _broadcast_to_type(self, connection_type: WebSocketConnectionType, data: Dict[str, Any]):
        """Broadcast data to all connections of specific type"""
        if connection_type in self.connection_groups:
            for connection_id in list(self.connection_groups[connection_type]):
                if connection_id in self.connections:
                    connection = self.connections[connection_id]
                    if connection.is_active:
                        await connection.send_message(data)
    
    async def connect(self, websocket: WebSocket, connection_type: WebSocketConnectionType) -> str:
        """Connect a new WebSocket client"""
        try:
            # Accept WebSocket connection
            await websocket.accept()
            
            # Generate unique connection ID
            connection_id = str(uuid.uuid4())
            
            # Create connection wrapper
            connection = WebSocketConnection(websocket, connection_type, connection_id)
            
            # Add to connections
            self.connections[connection_id] = connection
            self.connection_groups[connection_type].add(connection_id)
            
            logger.info(f"✅ WebSocket connected: {connection_id} ({connection_type.value})")
            
            # Send welcome message
            welcome_message = {
                "type": "connection_established",
                "connection_id": connection_id,
                "connection_type": connection_type.value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            await connection.send_message(welcome_message)
            
            return connection_id
            
        except Exception as e:
            logger.error(f"Failed to connect WebSocket: {e}")
            raise
    
    async def disconnect(self, connection_id: str):
        """Disconnect a WebSocket client"""
        await self._remove_connection(connection_id)
    
    async def _remove_connection(self, connection_id: str):
        """Remove connection from manager"""
        try:
            if connection_id in self.connections:
                connection = self.connections[connection_id]
                
                # Remove from connection groups
                if connection.connection_type in self.connection_groups:
                    self.connection_groups[connection.connection_type].discard(connection_id)
                
                # Close connection
                await connection.close()
                
                # Remove from connections
                del self.connections[connection_id]
                
                logger.info(f"✅ WebSocket disconnected: {connection_id}")
                
        except Exception as e:
            logger.error(f"Error removing connection {connection_id}: {e}")
    
    async def send_to_connection(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Send message to specific connection"""
        try:
            if connection_id in self.connections:
                connection = self.connections[connection_id]
                return await connection.send_message(message)
            return False
        except Exception as e:
            logger.error(f"Failed to send message to {connection_id}: {e}")
            return False
    
    async def broadcast_to_type(self, connection_type: WebSocketConnectionType, message: Dict[str, Any]):
        """Broadcast message to all connections of specific type"""
        try:
            await self._broadcast_to_type(connection_type, message)
        except Exception as e:
            logger.error(f"Failed to broadcast to {connection_type.value}: {e}")
    
    async def broadcast_to_all(self, message: Dict[str, Any]):
        """Broadcast message to all connections"""
        try:
            for connection_id, connection in list(self.connections.items()):
                if connection.is_active:
                    await connection.send_message(message)
        except Exception as e:
            logger.error(f"Failed to broadcast to all: {e}")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        try:
            stats = {
                "total_connections": len(self.connections),
                "connections_by_type": {
                    connection_type.value: len(connections) 
                    for connection_type, connections in self.connection_groups.items()
                },
                "active_connections": sum(1 for conn in self.connections.values() if conn.is_active),
                "total_messages_sent": sum(conn.message_count for conn in self.connections.values()),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            return stats
        except Exception as e:
            logger.error(f"Failed to get connection stats: {e}")
            return {"error": str(e)}
    
    async def handle_message(self, connection_id: str, message: Dict[str, Any]):
        """Handle incoming WebSocket message"""
        try:
            if connection_id in self.connections:
                connection = self.connections[connection_id]
                connection.last_activity = datetime.now(timezone.utc)
                
                message_type = message.get("type")
                
                if message_type == "ping":
                    # Respond to ping with pong
                    pong_message = {
                        "type": "pong",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    await connection.send_message(pong_message)
                
                elif message_type == "subscribe":
                    # Handle subscription requests
                    subscription_type = message.get("subscription_type")
                    if subscription_type:
                        # Update connection type if needed
                        try:
                            new_type = WebSocketConnectionType(subscription_type)
                            if new_type != connection.connection_type:
                                # Remove from old group
                                self.connection_groups[connection.connection_type].discard(connection_id)
                                # Add to new group
                                connection.connection_type = new_type
                                self.connection_groups[new_type].add(connection_id)
                                
                                subscription_message = {
                                    "type": "subscription_updated",
                                    "subscription_type": new_type.value,
                                    "timestamp": datetime.now(timezone.utc).isoformat()
                                }
                                await connection.send_message(subscription_message)
                        except ValueError:
                            error_message = {
                                "type": "error",
                                "message": f"Invalid subscription type: {subscription_type}",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }
                            await connection.send_message(error_message)
                
                elif message_type in self.message_handlers:
                    # Handle custom message types
                    handler = self.message_handlers[message_type]
                    await handler(connection_id, message)
                
        except Exception as e:
            logger.error(f"Failed to handle message from {connection_id}: {e}")
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register custom message handler"""
        self.message_handlers[message_type] = handler
    
    async def stop(self):
        """Stop the WebSocket manager"""
        try:
            self.is_running = False
            
            # Close all connections
            for connection_id in list(self.connections.keys()):
                await self._remove_connection(connection_id)
            
            # Cancel all broadcast tasks
            for task in self.broadcast_tasks.values():
                task.cancel()
            
            logger.info("✅ WebSocket manager stopped")
            
        except Exception as e:
            logger.error(f"Error stopping WebSocket manager: {e}")

# Create global unified WebSocket manager instance
unified_websocket_manager = UnifiedWebSocketManager()
