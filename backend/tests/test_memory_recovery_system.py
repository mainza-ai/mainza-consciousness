"""
Tests for memory system recovery and repair mechanisms
Tests validation, backup, restore, and recovery functionality.
"""
import pytest
import asyncio
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

# Set environment variables before importing modules that need them
os.environ.setdefault('NEO4J_PASSWORD', 'test_password')
os.environ.setdefault('NEO4J_URI', 'bolt://localhost:7687')
os.environ.setdefault('NEO4J_USER', 'neo4j')

from backend.utils.memory_recovery_system import (
    MemoryRecoverySystem, RecoveryStatus, ValidationIssueType, ValidationIssue,
    RecoveryOperation
)
from backend.utils.memory_error_handling import (
    MemoryConnectionError, MemoryCorruptionError, MemoryValidationError,
    MemoryErrorSeverity
)

class TestMemoryRecoverySystem:
    """Test MemoryRecoverySystem functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.recovery_system = MemoryRecoverySystem()
        
        # Mock Neo4j manager
        self.mock_neo4j = Mock()
        self.recovery_system.neo4j = self.mock_neo4j
    
    @pytest.mark.asyncio
    async def test_retry_with_exponential_backoff_success(self):
        """Test successful operation with retry mechanism"""
        
        async def mock_operation():
            return "success"
        
        result = await self.recovery_system.retry_with_exponential_backoff(
            mock_operation,
            "test_operation"
        )
        
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_with_exponential_backoff_transient_failure(self):
        """Test retry mechanism with transient failures"""
        call_count = 0
        
        async def mock_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:  # Fail first 2 attempts
                raise ConnectionError("Connection failed")
            return "success"
        
        result = await self.recovery_system.retry_with_exponential_backoff(
            mock_operation,
            "test_operation",
            max_attempts=3,
            base_delay=0.01  # Fast for testing
        )
        
        assert result == "success"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_with_exponential_backoff_permanent_failure(self):
        """Test retry mechanism with permanent failure"""
        
        async def mock_operation():
            raise ConnectionError("Permanent connection failure")
        
        with pytest.raises(MemoryConnectionError):
            await self.recovery_system.retry_with_exponential_backoff(
                mock_operation,
                "test_operation",
                max_attempts=2,
                base_delay=0.01
            )
    
    @pytest.mark.asyncio
    async def test_validate_memory_data_success(self):
        """Test memory data validation with valid data"""
        
        # Mock valid memory data
        mock_memories = [
            {
                "m": {
                    "memory_id": "test_memory_1",
                    "content": "Test content",
                    "memory_type": "interaction",
                    "user_id": "test_user",
                    "agent_name": "test_agent",
                    "consciousness_level": 0.7,
                    "emotional_state": "neutral",
                    "importance_score": 0.5,
                    "created_at": datetime.now().isoformat(),
                    "embedding": [0.1, 0.2, 0.3]
                }
            }
        ]
        
        # Make the mock return a coroutine that returns data once then empty
        call_count = 0
        async def mock_execute_query(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_memories
            else:
                return []  # Return empty on subsequent calls to break the loop
        
        self.mock_neo4j.execute_query = mock_execute_query
        
        issues = await self.recovery_system.validate_memory_data(
            memory_ids=["test_memory_1"]
        )
        
        assert isinstance(issues, list)
        # Valid memory should have no issues
        assert len(issues) == 0
    
    @pytest.mark.asyncio
    async def test_validate_memory_data_with_issues(self):
        """Test memory data validation with various issues"""
        
        # Mock memory data with issues
        mock_memories = [
            {
                "m": {
                    "memory_id": "test_memory_1",
                    "content": "",  # Empty content (issue)
                    "memory_type": "invalid_type",  # Invalid type (issue)
                    "user_id": "test_user",
                    "agent_name": "test_agent",
                    "consciousness_level": 1.5,  # Out of range (issue)
                    "emotional_state": "neutral",
                    # Missing importance_score (issue)
                    "created_at": "invalid_date",  # Invalid timestamp (issue)
                    "embedding": []  # Empty embedding (issue)
                }
            }
        ]
        
        # Make the mock return a coroutine that returns data once then empty
        call_count = 0
        async def mock_execute_query(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return mock_memories
            else:
                return []  # Return empty on subsequent calls to break the loop
        
        self.mock_neo4j.execute_query = mock_execute_query
        
        issues = await self.recovery_system.validate_memory_data(
            memory_ids=["test_memory_1"]
        )
        
        assert len(issues) > 0
        
        # Check for specific issue types
        issue_types = [issue.issue_type for issue in issues]
        assert ValidationIssueType.CORRUPTED_DATA in issue_types  # Empty content
        assert ValidationIssueType.INVALID_TYPE in issue_types  # Invalid memory type
        assert ValidationIssueType.MISSING_FIELD in issue_types  # Missing importance_score
    
    def test_validate_single_memory_missing_fields(self):
        """Test validation of memory with missing required fields"""
        
        memory = {
            "memory_id": "test_memory",
            "content": "Test content",
            # Missing required fields
        }
        
        issues = asyncio.run(self.recovery_system._validate_single_memory(memory))
        
        # Should find multiple missing field issues
        missing_field_issues = [
            issue for issue in issues 
            if issue.issue_type == ValidationIssueType.MISSING_FIELD
        ]
        
        assert len(missing_field_issues) > 0
        
        # Check that required fields are flagged
        missing_fields = [issue.field_name for issue in missing_field_issues]
        assert "memory_type" in missing_fields
        assert "user_id" in missing_fields
        assert "agent_name" in missing_fields
    
    def test_validate_single_memory_invalid_types(self):
        """Test validation of memory with invalid data types"""
        
        memory = {
            "memory_id": "test_memory",
            "content": "Test content",
            "memory_type": "invalid_type",
            "user_id": "test_user",
            "agent_name": "test_agent",
            "consciousness_level": "not_a_number",  # Should be float
            "emotional_state": "neutral",
            "importance_score": 2.0,  # Out of range
            "created_at": "invalid_timestamp",
            "embedding": "not_a_list"  # Should be list
        }
        
        issues = asyncio.run(self.recovery_system._validate_single_memory(memory))
        
        # Should find multiple type issues
        type_issues = [
            issue for issue in issues 
            if issue.issue_type in [ValidationIssueType.INVALID_TYPE, ValidationIssueType.CORRUPTED_DATA]
        ]
        
        assert len(type_issues) > 0
    
    @pytest.mark.asyncio
    async def test_repair_memory_issues_success(self):
        """Test successful memory issue repair"""
        
        # Mock issues that can be auto-fixed
        issues = [
            ValidationIssue(
                issue_type=ValidationIssueType.MISSING_FIELD,
                memory_id="test_memory",
                field_name="importance_score",
                description="Missing importance score",
                severity=MemoryErrorSeverity.MEDIUM,
                auto_fixable=True,
                suggested_fix="Set default value"
            ),
            ValidationIssue(
                issue_type=ValidationIssueType.INVALID_TYPE,
                memory_id="test_memory",
                field_name="memory_type",
                description="Invalid memory type",
                severity=MemoryErrorSeverity.MEDIUM,
                auto_fixable=True,
                suggested_fix="Set to interaction"
            )
        ]
        
        # Mock successful repair query
        async def mock_execute_write_query(*args, **kwargs):
            return [{"repaired_id": "test_memory"}]
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        status, fixed_issues = await self.recovery_system.repair_memory_issues(issues)
        
        assert status == RecoveryStatus.SUCCESS
        assert len(fixed_issues) == 2
    
    @pytest.mark.asyncio
    async def test_repair_memory_issues_no_auto_fixable(self):
        """Test repair when no issues are auto-fixable"""
        
        issues = [
            ValidationIssue(
                issue_type=ValidationIssueType.CORRUPTED_DATA,
                memory_id="test_memory",
                field_name="content",
                description="Corrupted content",
                severity=MemoryErrorSeverity.CRITICAL,
                auto_fixable=False
            )
        ]
        
        status, fixed_issues = await self.recovery_system.repair_memory_issues(issues)
        
        assert status == RecoveryStatus.NOT_NEEDED
        assert len(fixed_issues) == 0
    
    @pytest.mark.asyncio
    async def test_create_memory_backup_success(self):
        """Test successful memory backup creation"""
        
        # Mock backup query result
        async def mock_execute_write_query(*args, **kwargs):
            return [{"backed_up_count": 10}]
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        success = await self.recovery_system.create_memory_backup(
            backup_name="test_backup",
            user_id="test_user"
        )
        
        assert success is True
        
        # Since we replaced the mock with a function, we can't use assert_called()
        # The test passes if the function was called successfully (no exceptions)
    
    @pytest.mark.asyncio
    async def test_create_memory_backup_no_memories(self):
        """Test backup creation when no memories match criteria"""
        
        # Mock empty backup result
        async def mock_execute_write_query(*args, **kwargs):
            return [{"backed_up_count": 0}]
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        success = await self.recovery_system.create_memory_backup(
            backup_name="empty_backup"
        )
        
        assert success is False
    
    @pytest.mark.asyncio
    async def test_restore_from_backup_success(self):
        """Test successful memory restore from backup"""
        
        # Mock restore query result
        async def mock_execute_write_query(*args, **kwargs):
            return [{"restored_count": 5}]
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        success = await self.recovery_system.restore_from_backup(
            backup_name="test_backup",
            overwrite_existing=True
        )
        
        assert success is True
        
        # Since we replaced the mock with a function, we can't use assert_called()
        # The test passes if the function was called successfully (no exceptions)
    
    @pytest.mark.asyncio
    async def test_restore_from_backup_no_memories(self):
        """Test restore when no memories are found in backup"""
        
        # Mock empty restore result
        async def mock_execute_write_query(*args, **kwargs):
            return [{"restored_count": 0}]
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        success = await self.recovery_system.restore_from_backup(
            backup_name="nonexistent_backup"
        )
        
        assert success is False
    
    @pytest.mark.asyncio
    async def test_detect_duplicate_memories_success(self):
        """Test duplicate memory detection"""
        
        # Mock duplicate detection result
        mock_duplicates = [
            {
                "memory_id_1": "memory_1",
                "memory_id_2": "memory_2",
                "similarity_score": 0.98
            },
            {
                "memory_id_1": "memory_3",
                "memory_id_2": "memory_4",
                "similarity_score": 0.96
            }
        ]
        
        # Make the mock return a coroutine
        async def mock_execute_query(*args, **kwargs):
            return mock_duplicates
        
        self.mock_neo4j.execute_query = mock_execute_query
        
        duplicates = await self.recovery_system.detect_duplicate_memories(
            user_id="test_user",
            similarity_threshold=0.95
        )
        
        assert len(duplicates) == 2
        assert duplicates[0] == ("memory_1", "memory_2", 0.98)
        assert duplicates[1] == ("memory_3", "memory_4", 0.96)
    
    @pytest.mark.asyncio
    async def test_detect_duplicate_memories_no_duplicates(self):
        """Test duplicate detection when no duplicates exist"""
        
        # Mock empty result
        async def mock_execute_query(*args, **kwargs):
            return []
        
        self.mock_neo4j.execute_query = mock_execute_query
        
        duplicates = await self.recovery_system.detect_duplicate_memories()
        
        assert len(duplicates) == 0
    
    def test_get_recovery_status(self):
        """Test recovery system status retrieval"""
        
        status = asyncio.run(self.recovery_system.get_recovery_status())
        
        assert isinstance(status, dict)
        assert "active_operations" in status
        assert "recovery_history_size" in status
        assert "auto_fix_enabled" in status
        assert "max_retry_attempts" in status
        assert "connection_timeout" in status
        assert "backup_retention_days" in status

class TestValidationIssue:
    """Test ValidationIssue data class"""
    
    def test_validation_issue_creation(self):
        """Test ValidationIssue creation and properties"""
        
        issue = ValidationIssue(
            issue_type=ValidationIssueType.MISSING_FIELD,
            memory_id="test_memory",
            field_name="importance_score",
            description="Missing importance score",
            severity=MemoryErrorSeverity.MEDIUM,
            auto_fixable=True,
            suggested_fix="Set default value",
            context={"additional": "info"}
        )
        
        assert issue.issue_type == ValidationIssueType.MISSING_FIELD
        assert issue.memory_id == "test_memory"
        assert issue.field_name == "importance_score"
        assert issue.description == "Missing importance score"
        assert issue.severity == MemoryErrorSeverity.MEDIUM
        assert issue.auto_fixable is True
        assert issue.suggested_fix == "Set default value"
        assert issue.context == {"additional": "info"}

class TestRecoveryOperation:
    """Test RecoveryOperation data class"""
    
    def test_recovery_operation_creation(self):
        """Test RecoveryOperation creation and properties"""
        
        start_time = datetime.now()
        
        operation = RecoveryOperation(
            operation_id="test_op_123",
            operation_type="validation",
            status=RecoveryStatus.IN_PROGRESS,
            start_time=start_time,
            end_time=None,
            affected_memories=["memory_1", "memory_2"],
            issues_found=[],
            issues_fixed=[],
            metadata={"test": "data"}
        )
        
        assert operation.operation_id == "test_op_123"
        assert operation.operation_type == "validation"
        assert operation.status == RecoveryStatus.IN_PROGRESS
        assert operation.start_time == start_time
        assert operation.end_time is None
        assert operation.affected_memories == ["memory_1", "memory_2"]
        assert operation.issues_found == []
        assert operation.issues_fixed == []
        assert operation.error_message is None
        assert operation.metadata == {"test": "data"}

class TestMemoryRecoveryIntegration:
    """Test memory recovery system integration scenarios"""
    
    def setup_method(self):
        """Setup for each test"""
        self.recovery_system = MemoryRecoverySystem()
        self.mock_neo4j = Mock()
        self.recovery_system.neo4j = self.mock_neo4j
    
    @pytest.mark.asyncio
    async def test_full_validation_and_repair_workflow(self):
        """Test complete validation and repair workflow"""
        
        # Mock memory with issues
        mock_memories = [
            {
                "m": {
                    "memory_id": "test_memory_1",
                    "content": "Test content",
                    "memory_type": "invalid_type",  # Issue to fix
                    "user_id": "test_user",
                    "agent_name": "test_agent",
                    "consciousness_level": 0.7,
                    "emotional_state": "neutral",
                    # Missing importance_score - issue to fix
                    "created_at": datetime.now().isoformat(),
                    "embedding": [0.1, 0.2, 0.3]
                }
            }
        ]
        
        # Mock validation query
        self.mock_neo4j.execute_query.return_value = mock_memories
        
        # Mock repair query
        async def mock_execute_write_query(*args, **kwargs):
            return [{"repaired_id": "test_memory_1"}]
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        # Run validation
        issues = await self.recovery_system.validate_memory_data()
        
        assert len(issues) > 0
        
        # Run repair
        status, fixed_issues = await self.recovery_system.repair_memory_issues(issues)
        
        assert status in [RecoveryStatus.SUCCESS, RecoveryStatus.PARTIAL]
        assert len(fixed_issues) > 0
    
    @pytest.mark.asyncio
    async def test_backup_and_restore_workflow(self):
        """Test complete backup and restore workflow"""
        
        # Mock backup creation
        call_count = 0
        async def mock_execute_write_query(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [{"backed_up_count": 5}]  # Backup creation
            elif call_count == 2:
                return [{"old_backup_count": 2}]  # Cleanup old backups
            else:
                return [{"restored_count": 3}]     # Restore operation
        
        self.mock_neo4j.execute_write_query = mock_execute_write_query
        
        # Create backup
        backup_success = await self.recovery_system.create_memory_backup(
            backup_name="test_workflow_backup"
        )
        
        assert backup_success is True
        
        # Restore from backup
        restore_success = await self.recovery_system.restore_from_backup(
            backup_name="test_workflow_backup",
            overwrite_existing=False
        )
        
        assert restore_success is True
        
        # Since we replaced the mock with a function, we can't use call_count
        # The test passes if both operations completed successfully (no exceptions)

if __name__ == "__main__":
    pytest.main([__file__])