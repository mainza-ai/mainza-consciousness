"""
Memory Compression and Deduplication System for Mainza AI
Implements advanced memory optimization strategies
"""

import asyncio
import logging
import hashlib
import json
import gzip
import pickle
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from neo4j import GraphDatabase
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class CompressionStrategy(Enum):
    """Compression strategies for different data types"""
    SEMANTIC = "semantic"  # Semantic similarity-based compression
    TEMPORAL = "temporal"  # Time-based compression
    FREQUENCY = "frequency"  # Access frequency-based compression
    SIZE = "size"  # Size-based compression
    HYBRID = "hybrid"  # Combination of strategies

@dataclass
class MemoryChunk:
    """Represents a memory chunk with metadata"""
    id: str
    content: str
    embedding: List[float]
    created_at: datetime
    last_accessed: datetime
    access_count: int
    importance_score: float
    compression_ratio: float
    size_bytes: int
    tags: List[str]
    agent_id: Optional[str] = None

class MemoryCompressionSystem:
    """
    Advanced memory compression and deduplication system
    """
    
    def __init__(self, neo4j_driver, config: Dict[str, Any]):
        self.driver = neo4j_driver
        self.config = config
        self.compression_strategies = {
            CompressionStrategy.SEMANTIC: self._semantic_compression,
            CompressionStrategy.TEMPORAL: self._temporal_compression,
            CompressionStrategy.FREQUENCY: self._frequency_compression,
            CompressionStrategy.SIZE: self._size_compression,
            CompressionStrategy.HYBRID: self._hybrid_compression
        }
        self.compression_stats = {
            "total_compressions": 0,
            "space_saved": 0,
            "deduplications": 0,
            "average_compression_ratio": 0.0,
            "compression_time": 0.0
        }
        self.similarity_threshold = config.get("similarity_threshold", 0.85)
        self.compression_threshold = config.get("compression_threshold", 0.7)
        
    async def compress_memory_system(self, strategy: CompressionStrategy = CompressionStrategy.HYBRID) -> Dict[str, Any]:
        """
        Compress the entire memory system using specified strategy
        """
        try:
            start_time = datetime.now()
            logger.info(f"Starting memory compression with strategy: {strategy.value}")
            
            # Get all memory chunks
            memory_chunks = await self._get_all_memory_chunks()
            logger.info(f"Found {len(memory_chunks)} memory chunks to process")
            
            # Apply compression strategy
            compression_func = self.compression_strategies[strategy]
            compressed_chunks = await compression_func(memory_chunks)
            
            # Update database with compressed chunks
            await self._update_compressed_chunks(compressed_chunks)
            
            # Calculate compression statistics
            compression_time = (datetime.now() - start_time).total_seconds()
            stats = self._calculate_compression_stats(memory_chunks, compressed_chunks, compression_time)
            
            logger.info(f"Memory compression completed: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error compressing memory system: {e}")
            raise
    
    async def _get_all_memory_chunks(self) -> List[MemoryChunk]:
        """Retrieve all memory chunks from the database"""
        try:
            with self.driver.session() as session:
                query = """
                MATCH (m:Memory)
                WHERE m.content IS NOT NULL AND m.embedding IS NOT NULL
                RETURN m.id as id, m.content as content, m.embedding as embedding,
                       m.created_at as created_at, m.last_accessed as last_accessed,
                       m.access_count as access_count, m.importance_score as importance_score,
                       m.size_bytes as size_bytes, m.tags as tags, m.agent_id as agent_id
                ORDER BY m.created_at DESC
                """
                
                result = session.run(query)
                chunks = []
                
                for record in result:
                    chunk = MemoryChunk(
                        id=record["id"],
                        content=record["content"],
                        embedding=record["embedding"],
                        created_at=datetime.fromisoformat(record["created_at"]) if record["created_at"] else datetime.now(),
                        last_accessed=datetime.fromisoformat(record["last_accessed"]) if record["last_accessed"] else datetime.now(),
                        access_count=record["access_count"] or 0,
                        importance_score=record["importance_score"] or 0.5,
                        size_bytes=record["size_bytes"] or len(record["content"]),
                        tags=record["tags"] or [],
                        agent_id=record["agent_id"],
                        compression_ratio=1.0
                    )
                    chunks.append(chunk)
                
                return chunks
                
        except Exception as e:
            logger.error(f"Error retrieving memory chunks: {e}")
            raise
    
    async def _semantic_compression(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress based on semantic similarity"""
        try:
            logger.info("Applying semantic compression...")
            compressed_chunks = []
            processed_chunks = set()
            
            for i, chunk in enumerate(chunks):
                if chunk.id in processed_chunks:
                    continue
                
                # Find semantically similar chunks
                similar_chunks = await self._find_similar_chunks(chunk, chunks[i+1:])
                
                if similar_chunks:
                    # Merge similar chunks
                    merged_chunk = await self._merge_similar_chunks(chunk, similar_chunks)
                    compressed_chunks.append(merged_chunk)
                    
                    # Mark as processed
                    processed_chunks.add(chunk.id)
                    for similar_chunk in similar_chunks:
                        processed_chunks.add(similar_chunk.id)
                else:
                    compressed_chunks.append(chunk)
                    processed_chunks.add(chunk.id)
            
            logger.info(f"Semantic compression: {len(chunks)} -> {len(compressed_chunks)} chunks")
            return compressed_chunks
            
        except Exception as e:
            logger.error(f"Error in semantic compression: {e}")
            raise
    
    async def _temporal_compression(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress based on temporal patterns"""
        try:
            logger.info("Applying temporal compression...")
            
            # Group chunks by time periods
            time_groups = self._group_by_time_periods(chunks)
            compressed_chunks = []
            
            for time_group in time_groups:
                if len(time_group) > 1:
                    # Compress chunks in the same time period
                    compressed_group = await self._compress_time_group(time_group)
                    compressed_chunks.extend(compressed_group)
                else:
                    compressed_chunks.extend(time_group)
            
            logger.info(f"Temporal compression: {len(chunks)} -> {len(compressed_chunks)} chunks")
            return compressed_chunks
            
        except Exception as e:
            logger.error(f"Error in temporal compression: {e}")
            raise
    
    async def _frequency_compression(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress based on access frequency"""
        try:
            logger.info("Applying frequency compression...")
            
            # Sort by access frequency
            chunks_sorted = sorted(chunks, key=lambda x: x.access_count, reverse=True)
            
            # Keep frequently accessed chunks, compress rarely accessed ones
            compressed_chunks = []
            low_frequency_chunks = []
            
            for chunk in chunks_sorted:
                if chunk.access_count > 5:  # Frequently accessed
                    compressed_chunks.append(chunk)
                else:
                    low_frequency_chunks.append(chunk)
            
            # Compress low frequency chunks
            if low_frequency_chunks:
                compressed_low_freq = await self._compress_low_frequency_chunks(low_frequency_chunks)
                compressed_chunks.extend(compressed_low_freq)
            
            logger.info(f"Frequency compression: {len(chunks)} -> {len(compressed_chunks)} chunks")
            return compressed_chunks
            
        except Exception as e:
            logger.error(f"Error in frequency compression: {e}")
            raise
    
    async def _size_compression(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress based on size"""
        try:
            logger.info("Applying size compression...")
            
            # Identify large chunks for compression
            large_chunks = [chunk for chunk in chunks if chunk.size_bytes > 1024]  # > 1KB
            small_chunks = [chunk for chunk in chunks if chunk.size_bytes <= 1024]
            
            compressed_chunks = small_chunks.copy()
            
            if large_chunks:
                # Compress large chunks
                compressed_large = await self._compress_large_chunks(large_chunks)
                compressed_chunks.extend(compressed_large)
            
            logger.info(f"Size compression: {len(chunks)} -> {len(compressed_chunks)} chunks")
            return compressed_chunks
            
        except Exception as e:
            logger.error(f"Error in size compression: {e}")
            raise
    
    async def _hybrid_compression(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Apply hybrid compression strategy"""
        try:
            logger.info("Applying hybrid compression...")
            
            # Step 1: Semantic compression
            semantically_compressed = await self._semantic_compression(chunks)
            
            # Step 2: Temporal compression
            temporally_compressed = await self._temporal_compression(semantically_compressed)
            
            # Step 3: Frequency-based optimization
            frequency_optimized = await self._frequency_compression(temporally_compressed)
            
            # Step 4: Size-based compression
            size_compressed = await self._size_compression(frequency_optimized)
            
            logger.info(f"Hybrid compression: {len(chunks)} -> {len(size_compressed)} chunks")
            return size_compressed
            
        except Exception as e:
            logger.error(f"Error in hybrid compression: {e}")
            raise
    
    async def _find_similar_chunks(self, reference_chunk: MemoryChunk, 
                                 candidate_chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Find chunks similar to the reference chunk"""
        try:
            similar_chunks = []
            
            for candidate in candidate_chunks:
                # Calculate cosine similarity
                similarity = self._calculate_cosine_similarity(
                    reference_chunk.embedding, 
                    candidate.embedding
                )
                
                if similarity >= self.similarity_threshold:
                    similar_chunks.append(candidate)
            
            return similar_chunks
            
        except Exception as e:
            logger.error(f"Error finding similar chunks: {e}")
            return []
    
    def _calculate_cosine_similarity(self, embedding1: List[float], 
                                   embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    async def _merge_similar_chunks(self, reference_chunk: MemoryChunk, 
                                  similar_chunks: List[MemoryChunk]) -> MemoryChunk:
        """Merge similar chunks into a single compressed chunk"""
        try:
            all_chunks = [reference_chunk] + similar_chunks
            
            # Combine content
            combined_content = " ".join([chunk.content for chunk in all_chunks])
            
            # Calculate weighted average embedding
            total_access_count = sum(chunk.access_count for chunk in all_chunks)
            weighted_embedding = []
            
            for i in range(len(reference_chunk.embedding)):
                weighted_value = sum(
                    chunk.embedding[i] * chunk.access_count 
                    for chunk in all_chunks
                ) / total_access_count
                weighted_embedding.append(weighted_value)
            
            # Create merged chunk
            merged_chunk = MemoryChunk(
                id=f"merged_{reference_chunk.id}",
                content=combined_content,
                embedding=weighted_embedding,
                created_at=min(chunk.created_at for chunk in all_chunks),
                last_accessed=max(chunk.last_accessed for chunk in all_chunks),
                access_count=total_access_count,
                importance_score=max(chunk.importance_score for chunk in all_chunks),
                size_bytes=len(combined_content),
                tags=list(set(tag for chunk in all_chunks for tag in chunk.tags)),
                agent_id=reference_chunk.agent_id,
                compression_ratio=len(all_chunks)
            )
            
            return merged_chunk
            
        except Exception as e:
            logger.error(f"Error merging similar chunks: {e}")
            return reference_chunk
    
    def _group_by_time_periods(self, chunks: List[MemoryChunk], 
                              period_hours: int = 24) -> List[List[MemoryChunk]]:
        """Group chunks by time periods"""
        try:
            time_groups = defaultdict(list)
            
            for chunk in chunks:
                # Group by day
                day_key = chunk.created_at.date()
                time_groups[day_key].append(chunk)
            
            return list(time_groups.values())
            
        except Exception as e:
            logger.error(f"Error grouping by time periods: {e}")
            return [chunks]
    
    async def _compress_time_group(self, time_group: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress chunks within the same time group"""
        try:
            if len(time_group) <= 1:
                return time_group
            
            # Find the most important chunk as reference
            reference_chunk = max(time_group, key=lambda x: x.importance_score)
            other_chunks = [chunk for chunk in time_group if chunk.id != reference_chunk.id]
            
            # Merge with reference chunk
            merged_chunk = await self._merge_similar_chunks(reference_chunk, other_chunks)
            return [merged_chunk]
            
        except Exception as e:
            logger.error(f"Error compressing time group: {e}")
            return time_group
    
    async def _compress_low_frequency_chunks(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress chunks with low access frequency"""
        try:
            if len(chunks) <= 1:
                return chunks
            
            # Group by agent if available
            agent_groups = defaultdict(list)
            for chunk in chunks:
                agent_id = chunk.agent_id or "default"
                agent_groups[agent_id].append(chunk)
            
            compressed_chunks = []
            for agent_chunks in agent_groups.values():
                if len(agent_chunks) > 1:
                    # Merge all chunks for this agent
                    reference = agent_chunks[0]
                    others = agent_chunks[1:]
                    merged = await self._merge_similar_chunks(reference, others)
                    compressed_chunks.append(merged)
                else:
                    compressed_chunks.extend(agent_chunks)
            
            return compressed_chunks
            
        except Exception as e:
            logger.error(f"Error compressing low frequency chunks: {e}")
            return chunks
    
    async def _compress_large_chunks(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Compress large chunks by content summarization"""
        try:
            compressed_chunks = []
            
            for chunk in chunks:
                if chunk.size_bytes > 2048:  # > 2KB
                    # Summarize content
                    summarized_content = await self._summarize_content(chunk.content)
                    chunk.content = summarized_content
                    chunk.size_bytes = len(summarized_content)
                    chunk.compression_ratio = len(chunk.content) / len(chunk.content)
                
                compressed_chunks.append(chunk)
            
            return compressed_chunks
            
        except Exception as e:
            logger.error(f"Error compressing large chunks: {e}")
            return chunks
    
    async def _summarize_content(self, content: str) -> str:
        """Summarize content to reduce size"""
        try:
            # Simple summarization - keep first and last parts
            words = content.split()
            if len(words) <= 100:
                return content
            
            # Keep first 50 and last 50 words
            summary = " ".join(words[:50]) + " ... " + " ".join(words[-50:])
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing content: {e}")
            return content
    
    async def _update_compressed_chunks(self, compressed_chunks: List[MemoryChunk]):
        """Update database with compressed chunks"""
        try:
            with self.driver.session() as session:
                # Clear old chunks
                await session.run("MATCH (m:Memory) DELETE m")
                
                # Insert compressed chunks
                for chunk in compressed_chunks:
                    query = """
                    CREATE (m:Memory {
                        id: $id,
                        content: $content,
                        embedding: $embedding,
                        created_at: $created_at,
                        last_accessed: $last_accessed,
                        access_count: $access_count,
                        importance_score: $importance_score,
                        size_bytes: $size_bytes,
                        tags: $tags,
                        agent_id: $agent_id,
                        compression_ratio: $compression_ratio
                    })
                    """
                    
                    await session.run(query, {
                        "id": chunk.id,
                        "content": chunk.content,
                        "embedding": chunk.embedding,
                        "created_at": chunk.created_at.isoformat(),
                        "last_accessed": chunk.last_accessed.isoformat(),
                        "access_count": chunk.access_count,
                        "importance_score": chunk.importance_score,
                        "size_bytes": chunk.size_bytes,
                        "tags": chunk.tags,
                        "agent_id": chunk.agent_id,
                        "compression_ratio": chunk.compression_ratio
                    })
            
            logger.info(f"Updated database with {len(compressed_chunks)} compressed chunks")
            
        except Exception as e:
            logger.error(f"Error updating compressed chunks: {e}")
            raise
    
    def _calculate_compression_stats(self, original_chunks: List[MemoryChunk], 
                                   compressed_chunks: List[MemoryChunk], 
                                   compression_time: float) -> Dict[str, Any]:
        """Calculate compression statistics"""
        try:
            original_size = sum(chunk.size_bytes for chunk in original_chunks)
            compressed_size = sum(chunk.size_bytes for chunk in compressed_chunks)
            
            space_saved = original_size - compressed_size
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            
            stats = {
                "original_chunks": len(original_chunks),
                "compressed_chunks": len(compressed_chunks),
                "compression_ratio": compression_ratio,
                "space_saved_bytes": space_saved,
                "space_saved_percentage": (space_saved / original_size * 100) if original_size > 0 else 0,
                "compression_time_seconds": compression_time,
                "chunks_eliminated": len(original_chunks) - len(compressed_chunks)
            }
            
            # Update global stats
            self.compression_stats.update({
                "total_compressions": self.compression_stats["total_compressions"] + 1,
                "space_saved": self.compression_stats["space_saved"] + space_saved,
                "average_compression_ratio": (
                    (self.compression_stats["average_compression_ratio"] * 
                     (self.compression_stats["total_compressions"] - 1) + compression_ratio) / 
                    self.compression_stats["total_compressions"]
                ),
                "compression_time": self.compression_stats["compression_time"] + compression_time
            })
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating compression stats: {e}")
            return {"error": str(e)}
    
    async def deduplicate_memories(self) -> Dict[str, Any]:
        """Remove duplicate memories from the system"""
        try:
            logger.info("Starting memory deduplication...")
            
            with self.driver.session() as session:
                # Find duplicate memories based on content hash
                duplicate_query = """
                MATCH (m:Memory)
                WHERE m.content IS NOT NULL
                WITH m.content as content, collect(m) as duplicates
                WHERE size(duplicates) > 1
                RETURN content, duplicates
                """
                
                result = session.run(duplicate_query)
                duplicates_found = 0
                memories_removed = 0
                
                for record in result:
                    duplicates = record["duplicates"]
                    duplicates_found += 1
                    
                    # Keep the most recent and important memory
                    keep_memory = max(duplicates, key=lambda x: (
                        x.get("last_accessed", ""),
                        x.get("importance_score", 0)
                    ))
                    
                    # Remove others
                    for memory in duplicates:
                        if memory["id"] != keep_memory["id"]:
                            await session.run(
                                "MATCH (m:Memory {id: $id}) DELETE m",
                                id=memory["id"]
                            )
                            memories_removed += 1
                
                stats = {
                    "duplicate_groups_found": duplicates_found,
                    "memories_removed": memories_removed,
                    "deduplication_successful": True
                }
                
                logger.info(f"Deduplication completed: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"Error in memory deduplication: {e}")
            return {"error": str(e), "deduplication_successful": False}
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression system statistics"""
        return {
            "compression_stats": self.compression_stats,
            "similarity_threshold": self.similarity_threshold,
            "compression_threshold": self.compression_threshold
        }
