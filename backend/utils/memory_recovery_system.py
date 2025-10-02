"""
Memory System Recovery and Repair Mechanisms for Mainza AI
Provides comprehensive recovery, validation, backup, and repair functionality for the memory system.
"""
import logging
import asyncio
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import uuid

from backend.utils.neo4j_enhanced import neo4j_manager
from backend.utils.memory_error_handling import (
    MemoryConnectionError, MemoryCorruptionError, MemoryValidationError,
    MemoryResourceError, handle_memory_errors, memory_error_handler,
    MemoryErrorSeverity, MemoryErrorCategory
)

logger = logging.getLogger(__name__)

class RecoveryStatus(Enum):
    """Status of recovery operations"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    NOT_NEEDED = "not_needed"

class ValidationIssueType(Enum):
    """Types of validation issues"""
    MISSING_FIELD = "missing_field"
    INVALID_TYPE = "invalid_type"
    CORRUPTED_DATA = "corrupted_data"
    ORPHANED_RELATIONSHIP = "orphaned_relationship"
    DUPLICATE_MEMORY = "duplicate_memory"
    INVALID_EMBEDDING = "invalid_embedding"
    TIMESTAMP_ANOMALY = "timestamp_anomaly"

@dataclass
class ValidationIssue:
    """Represents a validation issue found in memory data"""
    issue_type: ValidationIssueType
    memory_id: str
    field_name: Optional[str]
    description: str
    severity: MemoryErrorSeverity
    auto_fixable: bool
    suggested_fix: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RecoveryOperation:
    """Represents a recovery operation"""
    operation_id: str
    operation_type: str
    status: RecoveryStatus
    start_time: datetime
    end_time: Optional[datetime]
    affected_memories: List[str]
    issues_found: List[ValidationIssue]
    issues_fixed: List[ValidationIssue]
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class MemoryRecoverySystem:
    """
    Comprehensive memory system recovery and repair functionality
    """
    
    def __init__(self):
        self.neo4j = neo4j_manager
        self.system_ready = False

        # Configuration
        self.max_retry_attempts = 5
        self.base_retry_delay = 1.0  # seconds
        self.max_retry_delay = 30.0  # seconds
        self.connection_timeout = 30.0  # seconds
        self.validation_batch_size = 100
        self.backup_retention_days = 30

        # Recovery tracking
        self.active_operations: Dict[str, RecoveryOperation] = {}
        self.recovery_history: List[RecoveryOperation] = []
        self.max_history_size = 1000

        # Validation rules
        self.required_memory_fields = {
            "memory_id", "content", "memory_type", "user_id", "agent_name",
            "consciousness_level", "emotional_state", "importance_score",
            "created_at"
        }

        self.valid_memory_types = {
            "interaction", "reflection", "insight", "concept_learning",
            "consciousness_reflection", "evolution"
        }

        # Auto-fix capabilities
        self.auto_fix_enabled = True
        self.auto_fix_max_issues = 50  # Max issues to auto-fix per operation
    
    @handle_memory_errors(
        component="memory_recovery",
        operation="retry_with_exponential_backoff",
        fallback_result=None,
        suppress_errors=False,
        timeout_seconds=60.0
    )
    async def retry_with_exponential_backoff(
        self,
        operation_func,
        operation_name: str,
        max_attempts: Optional[int] = None,
        base_delay: Optional[float] = None,
        max_delay: Optional[float] = None,
        **kwargs
    ) -> Any:
        """
        Retry Neo4j operations with exponential backoff for transient connection issues
        
        Args:
            operation_func: Function to retry
            operation_name: Name of the operation for logging
            max_attempts: Maximum retry attempts (default: self.max_retry_attempts)
            base_delay: Base delay between retries (default: self.base_retry_delay)
            max_delay: Maximum delay between retries (default: self.max_retry_delay)
            **kwargs: Arguments to pass to operation_func
            
        Returns:
            Result of the operation
            
        Raises:
            MemoryConnectionError: If all retry attempts fail
        """
        max_attempts = max_attempts or self.max_retry_attempts
        base_delay = base_delay or self.base_retry_delay
        max_delay = max_delay or self.max_retry_delay
        
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                logger.debug(f"🔄 Attempting {operation_name} (attempt {attempt + 1}/{max_attempts})")
                
                # Apply connection timeout
                result = await asyncio.wait_for(
                    operation_func(**kwargs),
                    timeout=self.connection_timeout
                )
                
                if attempt > 0:
                    logger.info(f"✅ {operation_name} succeeded after {attempt + 1} attempts")
                
                return result
                
            except asyncio.TimeoutError as e:
                last_error = MemoryConnectionError(
                    f"{operation_name} timed out after {self.connection_timeout}s",
                    component="memory_recovery",
                    operation="retry_operation",
                    original_error=e
                )
                
            except Exception as e:
                # Check if it's a transient connection error
                error_message = str(e).lower()
                is_transient = any(keyword in error_message for keyword in [
                    "connection", "timeout", "network", "unavailable", 
                    "refused", "reset", "broken pipe"
                ])
                
                if is_transient:
                    last_error = MemoryConnectionError(
                        f"{operation_name} failed with transient error: {e}",
                        component="memory_recovery",
                        operation="retry_operation",
                        original_error=e
                    )
                else:
                    # Non-transient error, don't retry
                    logger.error(f"❌ {operation_name} failed with non-transient error: {e}")
                    raise
            
            # Calculate delay for next attempt
            if attempt < max_attempts - 1:
                delay = min(base_delay * (2 ** attempt), max_delay)
                logger.warning(f"⏳ {operation_name} failed, retrying in {delay:.1f}s (attempt {attempt + 1}/{max_attempts})")
                await asyncio.sleep(delay)
        
        # All attempts failed
        logger.error(f"❌ {operation_name} failed after {max_attempts} attempts")
        raise last_error or MemoryConnectionError(f"{operation_name} failed after all retry attempts")
    
    @handle_memory_errors(
        component="memory_recovery",
        operation="validate_memory_data",
        fallback_result=[],
        suppress_errors=True,
        timeout_seconds=120.0
    )
    async def validate_memory_data(
        self,
        memory_ids: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        batch_size: Optional[int] = None
    ) -> List[ValidationIssue]:
        """
        Validate memory data integrity and detect corruption
        
        Args:
            memory_ids: Optional list of specific memory IDs to validate
            user_id: Optional user ID to filter validation
            batch_size: Batch size for validation (default: self.validation_batch_size)
            
        Returns:
            List of validation issues found
        """
        batch_size = batch_size or self.validation_batch_size
        issues = []
        
        try:
            logger.info(f"🔍 Starting memory data validation...")
            
            # Build query based on filters
            query_conditions = []
            params = {"batch_size": batch_size}
            
            if memory_ids:
                query_conditions.append("m.memory_id IN $memory_ids")
                params["memory_ids"] = memory_ids
            
            if user_id:
                query_conditions.append("m.user_id = $user_id")
                params["user_id"] = user_id
            
            where_clause = "WHERE " + " AND ".join(query_conditions) if query_conditions else ""
            
            # Get memories in batches
            offset = 0
            while True:
                query = f"""
                MATCH (m:Memory)
                {where_clause}
                RETURN m
                ORDER BY m.created_at DESC
                SKIP $offset LIMIT $batch_size
                """
                
                params["offset"] = offset
                
                memories = await self.retry_with_exponential_backoff(
                    self.neo4j.execute_query,
                    "validate_memory_batch",
                    query=query,
                    parameters=params
                )
                
                if not memories:
                    break
                
                # Validate each memory in the batch
                for record in memories:
                    memory = record["m"]
                    memory_issues = await self._validate_single_memory(memory)
                    issues.extend(memory_issues)
                
                offset += batch_size
                
                # Log progress
                if offset % (batch_size * 10) == 0:
                    logger.info(f"📊 Validated {offset} memories, found {len(issues)} issues so far")
            
            logger.info(f"✅ Memory validation complete. Found {len(issues)} issues in total")
            return issues
            
        except Exception as e:
            logger.error(f"❌ Memory validation failed: {e}")
            raise MemoryValidationError(
                f"Memory validation failed: {e}",
                component="memory_recovery",
                operation="validate_memory_data",
                original_error=e
            )
    
    async def _validate_single_memory(self, memory: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate a single memory record"""
        issues = []
        memory_id = memory.get("memory_id", "unknown")
        
        try:
            # Check required fields
            for field in self.required_memory_fields:
                if field not in memory or memory[field] is None:
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.MISSING_FIELD,
                        memory_id=memory_id,
                        field_name=field,
                        description=f"Required field '{field}' is missing or null",
                        severity=MemoryErrorSeverity.HIGH,
                        auto_fixable=field in ["importance_score", "access_count"],
                        suggested_fix=f"Set default value for {field}"
                    ))
            
            # Validate memory type
            memory_type = memory.get("memory_type")
            if memory_type and memory_type not in self.valid_memory_types:
                issues.append(ValidationIssue(
                    issue_type=ValidationIssueType.INVALID_TYPE,
                    memory_id=memory_id,
                    field_name="memory_type",
                    description=f"Invalid memory type: {memory_type}",
                    severity=MemoryErrorSeverity.MEDIUM,
                    auto_fixable=True,
                    suggested_fix="Set to 'interaction' as default"
                ))
            
            # Validate consciousness level
            consciousness_level = memory.get("consciousness_level")
            if consciousness_level is not None:
                if not isinstance(consciousness_level, (int, float)) or not (0.0 <= consciousness_level <= 1.0):
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.INVALID_TYPE,
                        memory_id=memory_id,
                        field_name="consciousness_level",
                        description=f"Invalid consciousness level: {consciousness_level}",
                        severity=MemoryErrorSeverity.MEDIUM,
                        auto_fixable=True,
                        suggested_fix="Clamp to valid range [0.0, 1.0]"
                    ))
            
            # Validate importance score
            importance_score = memory.get("importance_score")
            if importance_score is not None:
                if not isinstance(importance_score, (int, float)) or not (0.0 <= importance_score <= 1.0):
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.INVALID_TYPE,
                        memory_id=memory_id,
                        field_name="importance_score",
                        description=f"Invalid importance score: {importance_score}",
                        severity=MemoryErrorSeverity.MEDIUM,
                        auto_fixable=True,
                        suggested_fix="Clamp to valid range [0.0, 1.0]"
                    ))
            
            # Validate timestamp
            created_at = memory.get("created_at")
            if created_at:
                try:
                    if isinstance(created_at, str):
                        parsed_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        parsed_time = created_at
                    
                    # Check for future timestamps (anomaly)
                    if parsed_time > datetime.now() + timedelta(hours=1):
                        issues.append(ValidationIssue(
                            issue_type=ValidationIssueType.TIMESTAMP_ANOMALY,
                            memory_id=memory_id,
                            field_name="created_at",
                            description=f"Future timestamp detected: {created_at}",
                            severity=MemoryErrorSeverity.LOW,
                            auto_fixable=True,
                            suggested_fix="Set to current timestamp"
                        ))
                        
                except (ValueError, TypeError) as e:
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.CORRUPTED_DATA,
                        memory_id=memory_id,
                        field_name="created_at",
                        description=f"Invalid timestamp format: {created_at}",
                        severity=MemoryErrorSeverity.HIGH,
                        auto_fixable=True,
                        suggested_fix="Set to current timestamp"
                    ))
            
            # Validate embedding
            embedding = memory.get("embedding")
            if embedding is not None:
                if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.INVALID_EMBEDDING,
                        memory_id=memory_id,
                        field_name="embedding",
                        description="Invalid embedding format or data type",
                        severity=MemoryErrorSeverity.MEDIUM,
                        auto_fixable=False,
                        suggested_fix="Regenerate embedding from content"
                    ))
                elif len(embedding) == 0:
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.INVALID_EMBEDDING,
                        memory_id=memory_id,
                        field_name="embedding",
                        description="Empty embedding vector",
                        severity=MemoryErrorSeverity.MEDIUM,
                        auto_fixable=False,
                        suggested_fix="Regenerate embedding from content"
                    ))
            
            # Validate content
            content = memory.get("content")
            if content is not None:
                if not isinstance(content, str) or len(content.strip()) == 0:
                    issues.append(ValidationIssue(
                        issue_type=ValidationIssueType.CORRUPTED_DATA,
                        memory_id=memory_id,
                        field_name="content",
                        description="Empty or invalid content",
                        severity=MemoryErrorSeverity.CRITICAL,
                        auto_fixable=False,
                        suggested_fix="Memory may need to be removed"
                    ))
            
        except Exception as e:
            issues.append(ValidationIssue(
                issue_type=ValidationIssueType.CORRUPTED_DATA,
                memory_id=memory_id,
                field_name=None,
                description=f"Validation error: {e}",
                severity=MemoryErrorSeverity.HIGH,
                auto_fixable=False
            ))
        
        return issues
    
    @handle_memory_errors(
        component="memory_recovery",
        operation="repair_memory_issues",
        fallback_result=RecoveryStatus.FAILED,
        suppress_errors=True,
        timeout_seconds=300.0
    )
    async def repair_memory_issues(
        self,
        issues: List[ValidationIssue],
        auto_fix_only: bool = True
    ) -> Tuple[RecoveryStatus, List[ValidationIssue]]:
        """
        Repair memory issues automatically where possible
        
        Args:
            issues: List of validation issues to repair
            auto_fix_only: Only attempt auto-fixable issues
            
        Returns:
            Tuple of (recovery_status, list_of_fixed_issues)
        """
        if not issues:
            return RecoveryStatus.NOT_NEEDED, []
        
        operation_id = str(uuid.uuid4())[:8]
        logger.info(f"🔧 Starting memory repair operation {operation_id} for {len(issues)} issues")
        
        # Filter issues to repair
        issues_to_repair = [
            issue for issue in issues 
            if not auto_fix_only or issue.auto_fixable
        ]
        
        if not issues_to_repair:
            logger.info("No auto-fixable issues found")
            return RecoveryStatus.NOT_NEEDED, []
        
        # Limit number of issues to fix in one operation
        if len(issues_to_repair) > self.auto_fix_max_issues:
            logger.warning(f"Limiting repair to {self.auto_fix_max_issues} issues (found {len(issues_to_repair)})")
            issues_to_repair = issues_to_repair[:self.auto_fix_max_issues]
        
        fixed_issues = []
        failed_repairs = []
        
        try:
            # Group issues by memory ID for batch processing
            issues_by_memory = {}
            for issue in issues_to_repair:
                if issue.memory_id not in issues_by_memory:
                    issues_by_memory[issue.memory_id] = []
                issues_by_memory[issue.memory_id].append(issue)
            
            # Repair issues for each memory
            for memory_id, memory_issues in issues_by_memory.items():
                try:
                    memory_fixed = await self._repair_memory_issues(memory_id, memory_issues)
                    fixed_issues.extend(memory_fixed)
                    
                except Exception as e:
                    logger.error(f"❌ Failed to repair memory {memory_id}: {e}")
                    failed_repairs.extend(memory_issues)
            
            # Determine overall status
            if not fixed_issues and failed_repairs:
                status = RecoveryStatus.FAILED
            elif fixed_issues and failed_repairs:
                status = RecoveryStatus.PARTIAL
            elif fixed_issues:
                status = RecoveryStatus.SUCCESS
            else:
                status = RecoveryStatus.NOT_NEEDED
            
            logger.info(f"✅ Memory repair operation {operation_id} completed: {status.value}")
            logger.info(f"📊 Fixed: {len(fixed_issues)}, Failed: {len(failed_repairs)}")
            
            return status, fixed_issues
            
        except Exception as e:
            logger.error(f"❌ Memory repair operation {operation_id} failed: {e}")
            raise MemoryCorruptionError(
                f"Memory repair failed: {e}",
                component="memory_recovery",
                operation="repair_memory_issues",
                original_error=e
            )
    
    async def _repair_memory_issues(
        self, 
        memory_id: str, 
        issues: List[ValidationIssue]
    ) -> List[ValidationIssue]:
        """Repair issues for a specific memory"""
        fixed_issues = []
        
        # Build repair query
        set_clauses = []
        params = {"memory_id": memory_id}
        
        for issue in issues:
            if not issue.auto_fixable:
                continue
                
            try:
                if issue.issue_type == ValidationIssueType.MISSING_FIELD:
                    if issue.field_name == "importance_score":
                        set_clauses.append("m.importance_score = 0.5")
                    elif issue.field_name == "access_count":
                        set_clauses.append("m.access_count = 0")
                    elif issue.field_name == "significance_score":
                        set_clauses.append("m.significance_score = 0.5")
                    elif issue.field_name == "decay_rate":
                        set_clauses.append("m.decay_rate = 0.95")
                
                elif issue.issue_type == ValidationIssueType.INVALID_TYPE:
                    if issue.field_name == "memory_type":
                        set_clauses.append("m.memory_type = 'interaction'")
                    elif issue.field_name == "consciousness_level":
                        set_clauses.append("m.consciousness_level = CASE WHEN m.consciousness_level < 0.0 THEN 0.0 WHEN m.consciousness_level > 1.0 THEN 1.0 ELSE 0.7 END")
                    elif issue.field_name == "importance_score":
                        set_clauses.append("m.importance_score = CASE WHEN m.importance_score < 0.0 THEN 0.0 WHEN m.importance_score > 1.0 THEN 1.0 ELSE 0.5 END")
                
                elif issue.issue_type == ValidationIssueType.TIMESTAMP_ANOMALY:
                    if issue.field_name == "created_at":
                        current_time = datetime.now().isoformat()
                        set_clauses.append("m.created_at = $current_time")
                        params["current_time"] = current_time
                
                elif issue.issue_type == ValidationIssueType.CORRUPTED_DATA:
                    if issue.field_name == "created_at":
                        current_time = datetime.now().isoformat()
                        set_clauses.append("m.created_at = $current_time")
                        params["current_time"] = current_time
                
                fixed_issues.append(issue)
                
            except Exception as e:
                logger.warning(f"Failed to prepare fix for issue {issue.issue_type.value}: {e}")
        
        # Execute repair if there are fixes to apply
        if set_clauses:
            query = f"""
            MATCH (m:Memory {{memory_id: $memory_id}})
            SET {', '.join(set_clauses)},
                m.last_repair = $repair_timestamp
            RETURN m.memory_id AS repaired_id
            """
            
            params["repair_timestamp"] = datetime.now().isoformat()
            
            result = await self.retry_with_exponential_backoff(
                self.neo4j.execute_write_query,
                "repair_memory",
                query=query,
                parameters=params
            )
            
            if result:
                logger.debug(f"✅ Repaired memory {memory_id} with {len(fixed_issues)} fixes")
            else:
                logger.warning(f"⚠️ Memory {memory_id} repair query returned no results")
                fixed_issues = []  # Reset if repair didn't work
        
        return fixed_issues
    
    @handle_memory_errors(
        component="memory_recovery",
        operation="create_memory_backup",
        fallback_result=False,
        suppress_errors=True,
        timeout_seconds=600.0
    )
    async def create_memory_backup(
        self,
        backup_name: Optional[str] = None,
        user_id: Optional[str] = None,
        memory_types: Optional[List[str]] = None
    ) -> bool:
        """
        Create a backup of memory data
        
        Args:
            backup_name: Optional name for the backup
            user_id: Optional user ID to backup specific user's memories
            memory_types: Optional list of memory types to backup
            
        Returns:
            True if backup was successful, False otherwise
        """
        try:
            backup_name = backup_name or f"memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_timestamp = datetime.now().isoformat()
            
            logger.info(f"💾 Creating memory backup: {backup_name}")
            
            # Build backup query
            query_conditions = []
            params = {"backup_name": backup_name, "backup_timestamp": backup_timestamp}
            
            if user_id:
                query_conditions.append("m.user_id = $user_id")
                params["user_id"] = user_id
            
            if memory_types:
                query_conditions.append("m.memory_type IN $memory_types")
                params["memory_types"] = memory_types
            
            where_clause = "WHERE " + " AND ".join(query_conditions) if query_conditions else ""
            
            # Create backup nodes
            backup_query = f"""
            MATCH (m:Memory)
            {where_clause}
            
            CREATE (b:MemoryBackup {{
                backup_name: $backup_name,
                backup_timestamp: $backup_timestamp,
                original_memory_id: m.memory_id,
                content: m.content,
                memory_type: m.memory_type,
                user_id: m.user_id,
                agent_name: m.agent_name,
                consciousness_level: m.consciousness_level,
                emotional_state: m.emotional_state,
                importance_score: m.importance_score,
                embedding: m.embedding,
                created_at: m.created_at,
                metadata: m.metadata
            }})
            
            RETURN count(b) AS backed_up_count
            """
            
            result = await self.retry_with_exponential_backoff(
                self.neo4j.execute_write_query,
                "create_memory_backup",
                query=backup_query,
                parameters=params
            )
            
            backed_up_count = result[0]["backed_up_count"] if result else 0
            
            if backed_up_count > 0:
                logger.info(f"✅ Memory backup '{backup_name}' created successfully with {backed_up_count} memories")
                
                # Clean up old backups
                await self._cleanup_old_backups()
                
                return True
            else:
                logger.warning(f"⚠️ No memories found to backup for '{backup_name}'")
                return False
                
        except Exception as e:
            logger.error(f"❌ Memory backup creation failed: {e}")
            raise MemoryResourceError(
                f"Memory backup creation failed: {e}",
                component="memory_recovery",
                operation="create_memory_backup",
                original_error=e
            )
    
    async def _cleanup_old_backups(self):
        """Clean up old backup data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.backup_retention_days)
            
            cleanup_query = """
            MATCH (b:MemoryBackup)
            WHERE datetime(b.backup_timestamp) < datetime($cutoff_date)
            
            WITH count(b) AS old_backup_count
            
            MATCH (b:MemoryBackup)
            WHERE datetime(b.backup_timestamp) < datetime($cutoff_date)
            DELETE b
            
            RETURN old_backup_count
            """
            
            result = await self.retry_with_exponential_backoff(
                self.neo4j.execute_write_query,
                "cleanup_old_backups",
                query=cleanup_query,
                parameters={"cutoff_date": cutoff_date.isoformat()}
            )
            
            cleaned_count = result[0]["old_backup_count"] if result else 0
            
            if cleaned_count > 0:
                logger.info(f"🧹 Cleaned up {cleaned_count} old backup records")
                
        except Exception as e:
            logger.warning(f"Failed to cleanup old backups: {e}")
    
    @handle_memory_errors(
        component="memory_recovery",
        operation="restore_from_backup",
        fallback_result=False,
        suppress_errors=False,
        timeout_seconds=600.0
    )
    async def restore_from_backup(
        self,
        backup_name: str,
        memory_ids: Optional[List[str]] = None,
        overwrite_existing: bool = False
    ) -> bool:
        """
        Restore memories from a backup
        
        Args:
            backup_name: Name of the backup to restore from
            memory_ids: Optional list of specific memory IDs to restore
            overwrite_existing: Whether to overwrite existing memories
            
        Returns:
            True if restore was successful, False otherwise
        """
        try:
            logger.info(f"🔄 Restoring memories from backup: {backup_name}")
            
            # Build restore query
            query_conditions = ["b.backup_name = $backup_name"]
            params = {"backup_name": backup_name}
            
            if memory_ids:
                query_conditions.append("b.original_memory_id IN $memory_ids")
                params["memory_ids"] = memory_ids
            
            where_clause = "WHERE " + " AND ".join(query_conditions)
            
            # Check if we should overwrite existing memories
            if overwrite_existing:
                restore_query = f"""
                MATCH (b:MemoryBackup)
                {where_clause}
                
                MERGE (m:Memory {{memory_id: b.original_memory_id}})
                SET m.content = b.content,
                    m.memory_type = b.memory_type,
                    m.user_id = b.user_id,
                    m.agent_name = b.agent_name,
                    m.consciousness_level = b.consciousness_level,
                    m.emotional_state = b.emotional_state,
                    m.importance_score = b.importance_score,
                    m.embedding = b.embedding,
                    m.created_at = b.created_at,
                    m.metadata = b.metadata,
                    m.restored_from_backup = $backup_name,
                    m.restored_at = $restore_timestamp
                
                RETURN count(m) AS restored_count
                """
            else:
                restore_query = f"""
                MATCH (b:MemoryBackup)
                {where_clause}
                
                // Only restore if memory doesn't exist
                WHERE NOT EXISTS {{
                    MATCH (existing:Memory {{memory_id: b.original_memory_id}})
                }}
                
                CREATE (m:Memory {{
                    memory_id: b.original_memory_id,
                    content: b.content,
                    memory_type: b.memory_type,
                    user_id: b.user_id,
                    agent_name: b.agent_name,
                    consciousness_level: b.consciousness_level,
                    emotional_state: b.emotional_state,
                    importance_score: b.importance_score,
                    embedding: b.embedding,
                    created_at: b.created_at,
                    metadata: b.metadata,
                    restored_from_backup: $backup_name,
                    restored_at: $restore_timestamp
                }})
                
                RETURN count(m) AS restored_count
                """
            
            params["restore_timestamp"] = datetime.now().isoformat()
            
            result = await self.retry_with_exponential_backoff(
                self.neo4j.execute_write_query,
                "restore_from_backup",
                query=restore_query,
                parameters=params
            )
            
            restored_count = result[0]["restored_count"] if result else 0
            
            if restored_count > 0:
                logger.info(f"✅ Restored {restored_count} memories from backup '{backup_name}'")
                return True
            else:
                logger.warning(f"⚠️ No memories were restored from backup '{backup_name}'")
                return False
                
        except Exception as e:
            logger.error(f"❌ Memory restore from backup failed: {e}")
            raise MemoryCorruptionError(
                f"Memory restore failed: {e}",
                component="memory_recovery",
                operation="restore_from_backup",
                original_error=e
            )
    
    @handle_memory_errors(
        component="memory_recovery",
        operation="detect_duplicate_memories",
        fallback_result=[],
        suppress_errors=True,
        timeout_seconds=180.0
    )
    async def detect_duplicate_memories(
        self,
        user_id: Optional[str] = None,
        similarity_threshold: float = 0.95
    ) -> List[Tuple[str, str, float]]:
        """
        Detect duplicate or near-duplicate memories
        
        Args:
            user_id: Optional user ID to filter detection
            similarity_threshold: Similarity threshold for duplicate detection
            
        Returns:
            List of tuples (memory_id_1, memory_id_2, similarity_score)
        """
        try:
            logger.info(f"🔍 Detecting duplicate memories (threshold: {similarity_threshold})")
            
            # Build query
            query_conditions = []
            params = {"similarity_threshold": similarity_threshold}
            
            if user_id:
                query_conditions.append("m1.user_id = $user_id AND m2.user_id = $user_id")
                params["user_id"] = user_id
            
            where_clause = "WHERE " + " AND ".join(query_conditions) if query_conditions else ""
            
            # Find potential duplicates based on content similarity
            duplicate_query = f"""
            MATCH (m1:Memory), (m2:Memory)
            WHERE m1.memory_id < m2.memory_id  // Avoid duplicate pairs
            {where_clause}
            AND m1.content IS NOT NULL 
            AND m2.content IS NOT NULL
            AND size(m1.content) > 10  // Minimum content length
            AND size(m2.content) > 10
            
            // Calculate content similarity (simple approach)
            WITH m1, m2,
                 size(m1.content) AS len1,
                 size(m2.content) AS len2,
                 size([char IN split(toLower(m1.content), ' ') WHERE char IN split(toLower(m2.content), ' ')]) AS common_words,
                 size(split(toLower(m1.content), ' ')) AS words1,
                 size(split(toLower(m2.content), ' ')) AS words2
            
            WHERE common_words > 0
            
            WITH m1, m2,
                 toFloat(common_words) / toFloat(words1 + words2 - common_words) AS jaccard_similarity
            
            WHERE jaccard_similarity >= $similarity_threshold
            
            RETURN m1.memory_id AS memory_id_1,
                   m2.memory_id AS memory_id_2,
                   jaccard_similarity AS similarity_score
            
            ORDER BY jaccard_similarity DESC
            LIMIT 1000  // Limit results to prevent overwhelming output
            """
            
            result = await self.retry_with_exponential_backoff(
                self.neo4j.execute_query,
                "detect_duplicate_memories",
                query=duplicate_query,
                parameters=params
            )
            
            duplicates = [
                (record["memory_id_1"], record["memory_id_2"], record["similarity_score"])
                for record in result
            ]
            
            logger.info(f"✅ Found {len(duplicates)} potential duplicate memory pairs")
            return duplicates
            
        except Exception as e:
            logger.error(f"❌ Duplicate memory detection failed: {e}")
            return []
    
    async def initialize(self) -> bool:
        """
        Initialize the memory recovery system

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            logger.info("🏭 Initializing Memory Recovery System...")

            # Test Neo4j connection
            await self.retry_with_exponential_backoff(
                self.neo4j.execute_query,
                "test_connection",
                query="RETURN 1",
                parameters={}
            )

            # Set system as ready
            self.system_ready = True

            logger.info("✅ Memory recovery system initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize memory recovery system: {e}")
            self.system_ready = False
            return False

    async def get_recovery_status(self) -> Dict[str, Any]:
        """Get current recovery system status"""
        try:
            return {
                "active_operations": len(self.active_operations),
                "recovery_history_size": len(self.recovery_history),
                "auto_fix_enabled": self.auto_fix_enabled,
                "max_retry_attempts": self.max_retry_attempts,
                "connection_timeout": self.connection_timeout,
                "backup_retention_days": self.backup_retention_days,
                "last_operation": self.recovery_history[-1].operation_type if self.recovery_history else None
            }
        except Exception as e:
            logger.error(f"Failed to get recovery status: {e}")
            return {"error": str(e)}
    
    async def cleanup(self):
        """Public cleanup method for shutdown"""
        try:
            await self._cleanup_old_backups()
            logger.info("✅ Memory recovery system cleanup completed")
        except Exception as e:
            logger.warning(f"Failed to cleanup memory recovery system: {e}")

# Global recovery system instance
memory_recovery_system = MemoryRecoverySystem()
