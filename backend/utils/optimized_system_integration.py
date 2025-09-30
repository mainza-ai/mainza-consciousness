"""
Optimized System Integration for Mainza AI
Integrates all optimization systems into a unified, high-performance architecture
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Import all optimization systems
from .optimized_vector_embeddings import OptimizedVectorEmbeddings
from .enhanced_redis_caching import EnhancedRedisCache, CacheManager
from .memory_compression_system import MemoryCompressionSystem, CompressionStrategy
from .optimized_agent_memory_system import OptimizedAgentMemorySystem, MemoryType, MemoryImportance
from .performance_monitoring_system import PerformanceMonitoringSystem, MetricType

logger = logging.getLogger(__name__)

class OptimizedMainzaSystem:
    """
    Unified optimized system integrating all performance improvements
    """
    
    def __init__(self, neo4j_driver, redis_url: str, config: Dict[str, Any]):
        self.driver = neo4j_driver
        self.redis_url = redis_url
        self.config = config
        
        # Initialize optimization systems
        self.vector_embeddings = None
        self.redis_cache = None
        self.memory_compression = None
        self.agent_memory = None
        self.performance_monitoring = None
        
        # System status
        self.initialized = False
        self.optimization_stats = {
            "vector_optimizations": 0,
            "cache_optimizations": 0,
            "memory_compressions": 0,
            "agent_optimizations": 0,
            "performance_improvements": 0
        }
        
    async def initialize(self):
        """Initialize all optimization systems"""
        try:
            logger.info("Initializing optimized Mainza system...")
            
            # Initialize vector embeddings system
            self.vector_embeddings = OptimizedVectorEmbeddings(
                self.driver, 
                self.config.get("vector_embeddings", {})
            )
            await self.vector_embeddings.create_optimized_vector_indexes()
            logger.info("Vector embeddings system initialized")
            
            # Initialize enhanced Redis caching
            cache_config = self.config.get("redis_cache", {
                "compression_enabled": True,
                "serialization_method": "json",
                "default_ttl": 3600,
                "max_memory_usage": "512mb"
            })
            self.redis_cache = EnhancedRedisCache(self.redis_url, cache_config)
            await self.redis_cache.initialize()
            logger.info("Enhanced Redis caching initialized")
            
            # Initialize memory compression system
            compression_config = self.config.get("memory_compression", {
                "similarity_threshold": 0.85,
                "compression_threshold": 0.7
            })
            self.memory_compression = MemoryCompressionSystem(
                self.driver, 
                compression_config
            )
            logger.info("Memory compression system initialized")
            
            # Initialize optimized agent memory system
            agent_config = self.config.get("agent_memory", {
                "consolidation_threshold": 0.8,
                "learning_threshold": 0.7,
                "memory_decay_rate": 0.1,
                "cross_agent_similarity_threshold": 0.75
            })
            self.agent_memory = OptimizedAgentMemorySystem(
                self.driver, 
                agent_config
            )
            logger.info("Optimized agent memory system initialized")
            
            # Initialize performance monitoring
            monitoring_config = self.config.get("performance_monitoring", {
                "monitoring_interval": 30,
                "alert_thresholds": {
                    "cpu_usage": 80.0,
                    "memory_usage": 85.0,
                    "disk_usage": 90.0,
                    "response_time": 5.0,
                    "error_rate": 5.0,
                    "cache_hit_rate": 70.0
                }
            })
            self.performance_monitoring = PerformanceMonitoringSystem(
                self.driver, 
                self.redis_cache.redis_client, 
                monitoring_config
            )
            await self.performance_monitoring.start_monitoring()
            logger.info("Performance monitoring system initialized")
            
            self.initialized = True
            logger.info("Optimized Mainza system initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Error initializing optimized system: {e}")
            raise
    
    async def optimize_system_performance(self) -> Dict[str, Any]:
        """
        Run comprehensive system optimization
        """
        try:
            if not self.initialized:
                await self.initialize()
            
            logger.info("Starting comprehensive system optimization...")
            optimization_results = {}
            
            # 1. Vector Embeddings Optimization
            logger.info("Running vector embeddings optimization...")
            try:
                # Optimize memory storage
                vector_optimization = await self.vector_embeddings.optimize_memory_storage()
                optimization_results["vector_embeddings"] = vector_optimization
                self.optimization_stats["vector_optimizations"] += 1
                logger.info("Vector embeddings optimization completed")
            except Exception as e:
                logger.error(f"Vector embeddings optimization failed: {e}")
                optimization_results["vector_embeddings"] = {"error": str(e)}
            
            # 2. Memory Compression
            logger.info("Running memory compression...")
            try:
                compression_result = await self.memory_compression.compress_memory_system(
                    CompressionStrategy.HYBRID
                )
                optimization_results["memory_compression"] = compression_result
                self.optimization_stats["memory_compressions"] += 1
                logger.info("Memory compression completed")
            except Exception as e:
                logger.error(f"Memory compression failed: {e}")
                optimization_results["memory_compression"] = {"error": str(e)}
            
            # 3. Agent Memory Optimization
            logger.info("Running agent memory optimization...")
            try:
                # Get all agent IDs (this would be from your agent system)
                agent_ids = await self._get_all_agent_ids()
                
                agent_optimization_results = {}
                for agent_id in agent_ids:
                    # Consolidate agent memories
                    consolidation_result = await self.agent_memory.consolidate_agent_memories(agent_id)
                    
                    # Optimize memory retrieval
                    retrieval_optimization = await self.agent_memory.optimize_memory_retrieval(agent_id)
                    
                    agent_optimization_results[agent_id] = {
                        "consolidation": consolidation_result,
                        "retrieval_optimization": retrieval_optimization
                    }
                
                optimization_results["agent_memory"] = agent_optimization_results
                self.optimization_stats["agent_optimizations"] += 1
                logger.info("Agent memory optimization completed")
            except Exception as e:
                logger.error(f"Agent memory optimization failed: {e}")
                optimization_results["agent_memory"] = {"error": str(e)}
            
            # 4. Cache Optimization
            logger.info("Running cache optimization...")
            try:
                # Clean up expired keys
                await self.redis_cache.cleanup_expired_keys()
                
                # Get cache statistics
                cache_stats = await self.redis_cache.get_cache_stats()
                optimization_results["cache_optimization"] = cache_stats
                self.optimization_stats["cache_optimizations"] += 1
                logger.info("Cache optimization completed")
            except Exception as e:
                logger.error(f"Cache optimization failed: {e}")
                optimization_results["cache_optimization"] = {"error": str(e)}
            
            # 5. Cross-Agent Learning Analysis
            logger.info("Analyzing cross-agent learning patterns...")
            try:
                learning_analysis = await self.agent_memory.learn_from_cross_agent_interactions()
                optimization_results["cross_agent_learning"] = learning_analysis
                logger.info("Cross-agent learning analysis completed")
            except Exception as e:
                logger.error(f"Cross-agent learning analysis failed: {e}")
                optimization_results["cross_agent_learning"] = {"error": str(e)}
            
            # 6. Performance Analysis
            logger.info("Analyzing system performance...")
            try:
                performance_summary = self.performance_monitoring.get_performance_summary()
                optimization_recommendations = self.performance_monitoring.get_optimization_recommendations()
                
                optimization_results["performance_analysis"] = {
                    "summary": performance_summary,
                    "recommendations": optimization_recommendations
                }
                self.optimization_stats["performance_improvements"] += 1
                logger.info("Performance analysis completed")
            except Exception as e:
                logger.error(f"Performance analysis failed: {e}")
                optimization_results["performance_analysis"] = {"error": str(e)}
            
            # Generate overall optimization report
            optimization_results["overall_stats"] = self.optimization_stats
            optimization_results["optimization_timestamp"] = datetime.now().isoformat()
            
            logger.info("Comprehensive system optimization completed")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Error in system optimization: {e}")
            return {"error": str(e)}
    
    async def get_system_health_report(self) -> Dict[str, Any]:
        """
        Get comprehensive system health report
        """
        try:
            if not self.initialized:
                return {"error": "System not initialized"}
            
            health_report = {
                "timestamp": datetime.now().isoformat(),
                "system_status": "operational" if self.initialized else "not_initialized",
                "optimization_stats": self.optimization_stats
            }
            
            # Vector embeddings health
            try:
                vector_metrics = self.vector_embeddings.get_performance_metrics()
                health_report["vector_embeddings"] = {
                    "status": "healthy",
                    "metrics": vector_metrics
                }
            except Exception as e:
                health_report["vector_embeddings"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Redis cache health
            try:
                cache_stats = await self.redis_cache.get_cache_stats()
                health_report["redis_cache"] = {
                    "status": "healthy",
                    "metrics": cache_stats
                }
            except Exception as e:
                health_report["redis_cache"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Memory compression health
            try:
                compression_stats = self.memory_compression.get_compression_stats()
                health_report["memory_compression"] = {
                    "status": "healthy",
                    "metrics": compression_stats
                }
            except Exception as e:
                health_report["memory_compression"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Agent memory health
            try:
                agent_metrics = self.agent_memory.get_performance_metrics()
                health_report["agent_memory"] = {
                    "status": "healthy",
                    "metrics": agent_metrics
                }
            except Exception as e:
                health_report["agent_memory"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Performance monitoring health
            try:
                performance_summary = self.performance_monitoring.get_performance_summary()
                health_report["performance_monitoring"] = {
                    "status": "healthy",
                    "metrics": performance_summary
                }
            except Exception as e:
                health_report["performance_monitoring"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Overall health score
            healthy_components = sum(1 for component in health_report.values() 
                                   if isinstance(component, dict) and component.get("status") == "healthy")
            total_components = len([k for k in health_report.keys() 
                                  if k not in ["timestamp", "system_status", "optimization_stats"]])
            
            health_score = (healthy_components / total_components * 100) if total_components > 0 else 0
            health_report["overall_health_score"] = health_score
            
            return health_report
            
        except Exception as e:
            logger.error(f"Error generating system health report: {e}")
            return {"error": str(e)}
    
    async def _get_all_agent_ids(self) -> List[str]:
        """Get all agent IDs from the system"""
        try:
            with self.driver.session() as session:
                query = """
                MATCH (a:Agent)
                RETURN DISTINCT a.id as agent_id
                """
                result = session.run(query)
                return [record["agent_id"] for record in result]
        except Exception as e:
            logger.error(f"Error getting agent IDs: {e}")
            return []
    
    async def store_optimized_memory(self, agent_id: str, content: str, 
                                   memory_type: MemoryType, importance: MemoryImportance,
                                   emotional_context: Dict[str, float] = None) -> str:
        """
        Store memory with full optimization pipeline
        """
        try:
            if not self.initialized:
                await self.initialize()
            
            # Generate optimized embedding
            embedding = await self.vector_embeddings.generate_optimized_embedding(
                content, memory_type.value
            )
            
            # Store in agent memory system
            memory_id = await self.agent_memory.store_agent_memory(
                agent_id, content, memory_type, importance, embedding, emotional_context
            )
            
            # Cache the memory for fast retrieval
            cache_key = f"memory:{agent_id}:{memory_id}"
            await self.redis_cache.set(cache_key, {
                "content": content,
                "embedding": embedding,
                "memory_type": memory_type.value,
                "importance": importance.value
            }, ttl=7200)  # 2 hours
            
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing optimized memory: {e}")
            raise
    
    async def retrieve_optimized_memories(self, agent_id: str, query: str, 
                                         memory_types: List[MemoryType] = None,
                                         limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve memories with full optimization pipeline
        """
        try:
            if not self.initialized:
                await self.initialize()
            
            # Try cache first
            cache_key = f"retrieval:{agent_id}:{hash(query)}"
            cached_result = await self.redis_cache.get(cache_key)
            if cached_result:
                return cached_result
            
            # Retrieve from agent memory system
            memories = await self.agent_memory.retrieve_agent_memories(
                agent_id, query, memory_types, limit
            )
            
            # Convert to dictionary format
            result = []
            for memory in memories:
                result.append({
                    "id": memory.id,
                    "content": memory.content,
                    "memory_type": memory.memory_type.value,
                    "importance": memory.importance.value,
                    "created_at": memory.created_at.isoformat(),
                    "access_count": memory.access_count,
                    "retrieval_strength": memory.retrieval_strength
                })
            
            # Cache the result
            await self.redis_cache.set(cache_key, result, ttl=1800)  # 30 minutes
            
            return result
            
        except Exception as e:
            logger.error(f"Error retrieving optimized memories: {e}")
            return []
    
    async def cross_agent_knowledge_transfer(self, source_agent: str, target_agent: str, 
                                           knowledge: str, transfer_type: str = "semantic") -> bool:
        """
        Transfer knowledge between agents with optimization
        """
        try:
            if not self.initialized:
                await self.initialize()
            
            # Use agent memory system for transfer
            success = await self.agent_memory.cross_agent_knowledge_transfer(
                source_agent, target_agent, knowledge, transfer_type
            )
            
            if success:
                # Update performance metrics
                self.performance_monitoring.record_request(True, 0.1)  # Fast operation
            
            return success
            
        except Exception as e:
            logger.error(f"Error in cross-agent knowledge transfer: {e}")
            return False
    
    async def run_periodic_optimization(self):
        """
        Run periodic optimization tasks
        """
        try:
            logger.info("Running periodic optimization tasks...")
            
            # Memory compression
            await self.memory_compression.compress_memory_system(CompressionStrategy.HYBRID)
            
            # Cache cleanup
            await self.redis_cache.cleanup_expired_keys()
            
            # Agent memory consolidation for all agents
            agent_ids = await self._get_all_agent_ids()
            for agent_id in agent_ids:
                await self.agent_memory.consolidate_agent_memories(agent_id)
            
            # Cross-agent learning analysis
            await self.agent_memory.learn_from_cross_agent_interactions()
            
            logger.info("Periodic optimization tasks completed")
            
        except Exception as e:
            logger.error(f"Error in periodic optimization: {e}")

    async def optimize_memory_storage(self) -> Dict[str, Any]:
        """Optimize memory storage system"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Run memory storage optimization
            result = await self.memory_compression.optimize_storage()
            self.optimization_stats["memory_compressions"] += 1
            
            return {
                "status": "success",
                "optimization_type": "memory_storage",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing memory storage: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_memory_retrieval(self) -> Dict[str, Any]:
        """Optimize memory retrieval system"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Run memory retrieval optimization
            result = await self.vector_embeddings.optimize_retrieval()
            self.optimization_stats["vector_optimizations"] += 1
            
            return {
                "status": "success",
                "optimization_type": "memory_retrieval",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing memory retrieval: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_vector_embeddings(self) -> Dict[str, Any]:
        """Optimize vector embeddings system"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Run vector embeddings optimization
            result = await self.vector_embeddings.optimize_embeddings()
            self.optimization_stats["vector_optimizations"] += 1
            
            return {
                "status": "success",
                "optimization_type": "vector_embeddings",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing vector embeddings: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_cross_agent_learning(self) -> Dict[str, Any]:
        """Optimize cross-agent learning system"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Run cross-agent learning optimization
            result = await self.agent_memory.optimize_cross_agent_learning()
            self.optimization_stats["agent_optimizations"] += 1
            
            return {
                "status": "success",
                "optimization_type": "cross_agent_learning",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing cross-agent learning: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_memory_compression(self) -> Dict[str, Any]:
        """Optimize memory compression system"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Run memory compression optimization
            result = await self.memory_compression.optimize_compression()
            self.optimization_stats["memory_compressions"] += 1
            
            return {
                "status": "success",
                "optimization_type": "memory_compression",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing memory compression: {e}")
            return {"status": "error", "message": str(e)}

    async def optimize_agent_memory(self) -> Dict[str, Any]:
        """Optimize agent memory system"""
        try:
            if not self.initialized:
                await self.initialize()
            
            # Run agent memory optimization
            result = await self.agent_memory.optimize_agent_memory()
            self.optimization_stats["agent_optimizations"] += 1
            
            return {
                "status": "success",
                "optimization_type": "agent_memory",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error optimizing agent memory: {e}")
            return {"status": "error", "message": str(e)}
    
    async def shutdown(self):
        """Shutdown all optimization systems"""
        try:
            logger.info("Shutting down optimized system...")
            
            if self.performance_monitoring:
                await self.performance_monitoring.stop_monitoring()
            
            if self.redis_cache:
                await self.redis_cache.close()
            
            self.initialized = False
            logger.info("Optimized system shutdown completed")
            
        except Exception as e:
            logger.error(f"Error shutting down optimized system: {e}")


# Global system instance
_optimized_system = None

async def get_optimized_system(neo4j_driver=None, redis_url: str = None, config: Dict[str, Any] = None) -> OptimizedMainzaSystem:
    """
    Get or create the global optimized system instance
    """
    global _optimized_system
    
    if _optimized_system is None:
        if neo4j_driver is None or redis_url is None:
            raise ValueError("neo4j_driver and redis_url are required for initialization")
        
        _optimized_system = OptimizedMainzaSystem(neo4j_driver, redis_url, config or {})
        await _optimized_system.initialize()
    
    return _optimized_system

async def optimize_system_performance(neo4j_driver=None, redis_url: str = None, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run system optimization using the global instance
    """
    system = await get_optimized_system(neo4j_driver, redis_url, config)
    return await system.optimize_system_performance()

async def get_system_health(neo4j_driver=None, redis_url: str = None, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get system health using the global instance
    """
    system = await get_optimized_system(neo4j_driver, redis_url, config)
    return await system.get_system_health_report()
