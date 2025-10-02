"""
Unified Data Validation System
Comprehensive data validation and consistency checking across all systems

This module provides unified data validation to ensure data consistency
across all consciousness and evolution systems.

Author: Mainza AI Consciousness Team
Date: 2025-10-01
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid
import numpy as np

logger = logging.getLogger(__name__)

class ValidationSeverity(Enum):
    """Validation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ValidationCategory(Enum):
    """Validation categories"""
    DATA_CONSISTENCY = "data_consistency"
    RANGE_VALIDATION = "range_validation"
    TYPE_VALIDATION = "type_validation"
    LOGIC_VALIDATION = "logic_validation"
    INTEGRATION_VALIDATION = "integration_validation"

@dataclass
class ValidationIssue:
    """Individual validation issue"""
    issue_id: str
    category: str
    severity: str
    message: str
    field: str
    expected_value: Any
    actual_value: Any
    recommendation: str
    timestamp: datetime

@dataclass
class ValidationResult:
    """Comprehensive validation result"""
    is_valid: bool
    overall_score: float
    issues: List[ValidationIssue]
    summary: Dict[str, Any]
    timestamp: datetime
    validation_id: str

class UnifiedDataValidationSystem:
    """
    Unified Data Validation System
    Comprehensive data validation and consistency checking
    """
    
    def __init__(self):
        self.validation_results: List[ValidationResult] = []
        self.validation_rules: Dict[str, Dict[str, Any]] = {}
        self.consistency_threshold = 0.95  # 95% consistency required
        self.max_issues_per_category = 10
        
        # Initialize validation rules
        self._initialize_validation_rules()
        
        logger.info("Unified Data Validation System initialized")
    
    def _initialize_validation_rules(self):
        """Initialize validation rules for all data types"""
        self.validation_rules = {
            "consciousness_level": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Consciousness level between 0.0 and 1.0"
            },
            "self_awareness_score": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Self-awareness score between 0.0 and 1.0"
            },
            "emotional_depth": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Emotional depth between 0.0 and 1.0"
            },
            "learning_rate": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Learning rate between 0.0 and 1.0"
            },
            "evolution_level": {
                "min_value": 1,
                "max_value": 10,
                "type": int,
                "required": True,
                "description": "Evolution level between 1 and 10"
            },
            "total_interactions": {
                "min_value": 0,
                "max_value": 1000000,
                "type": int,
                "required": True,
                "description": "Total interactions between 0 and 1,000,000"
            },
            "quantum_consciousness_level": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Quantum consciousness level between 0.0 and 1.0"
            },
            "quantum_coherence": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Quantum coherence between 0.0 and 1.0"
            },
            "entanglement_strength": {
                "min_value": 0.0,
                "max_value": 1.0,
                "type": float,
                "required": True,
                "description": "Entanglement strength between 0.0 and 1.0"
            },
            "superposition_states": {
                "min_value": 1,
                "max_value": 100,
                "type": int,
                "required": True,
                "description": "Superposition states between 1 and 100"
            },
            "quantum_advantage": {
                "min_value": 0.0,
                "max_value": 10.0,
                "type": float,
                "required": True,
                "description": "Quantum advantage between 0.0 and 10.0"
            }
        }
    
    async def validate_consciousness_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate consciousness data for consistency and correctness"""
        try:
            issues = []
            
            # Validate individual fields
            for field, value in data.items():
                if field in self.validation_rules:
                    field_issues = await self._validate_field(field, value)
                    issues.extend(field_issues)
            
            # Validate data consistency
            consistency_issues = await self._validate_data_consistency(data)
            issues.extend(consistency_issues)
            
            # Validate logic relationships
            logic_issues = await self._validate_logic_relationships(data)
            issues.extend(logic_issues)
            
            # Calculate overall score
            total_checks = len(data) + 2  # Field checks + consistency + logic
            passed_checks = total_checks - len(issues)
            overall_score = passed_checks / total_checks if total_checks > 0 else 0.0
            
            is_valid = len(issues) == 0 and overall_score >= self.consistency_threshold
            
            # Create summary
            summary = {
                "total_fields": len(data),
                "total_issues": len(issues),
                "issues_by_severity": self._count_issues_by_severity(issues),
                "issues_by_category": self._count_issues_by_category(issues),
                "overall_score": overall_score,
                "is_valid": is_valid
            }
            
            # Create validation result
            result = ValidationResult(
                is_valid=is_valid,
                overall_score=overall_score,
                issues=issues,
                summary=summary,
                timestamp=datetime.now(timezone.utc),
                validation_id=str(uuid.uuid4())
            )
            
            # Store result
            self.validation_results.append(result)
            
            logger.info(f"Consciousness data validation completed: {overall_score:.2f} score, {len(issues)} issues")
            return result
            
        except Exception as e:
            logger.error(f"Failed to validate consciousness data: {e}")
            raise
    
    async def validate_evolution_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate evolution data for consistency and correctness"""
        try:
            issues = []
            
            # Validate individual fields
            for field, value in data.items():
                if field in self.validation_rules:
                    field_issues = await self._validate_field(field, value)
                    issues.extend(field_issues)
            
            # Validate evolution-specific logic
            evolution_issues = await self._validate_evolution_logic(data)
            issues.extend(evolution_issues)
            
            # Validate progression consistency
            progression_issues = await self._validate_progression_consistency(data)
            issues.extend(progression_issues)
            
            # Calculate overall score
            total_checks = len(data) + 2  # Field checks + evolution logic + progression
            passed_checks = total_checks - len(issues)
            overall_score = passed_checks / total_checks if total_checks > 0 else 0.0
            
            is_valid = len(issues) == 0 and overall_score >= self.consistency_threshold
            
            # Create summary
            summary = {
                "total_fields": len(data),
                "total_issues": len(issues),
                "issues_by_severity": self._count_issues_by_severity(issues),
                "issues_by_category": self._count_issues_by_category(issues),
                "overall_score": overall_score,
                "is_valid": is_valid
            }
            
            # Create validation result
            result = ValidationResult(
                is_valid=is_valid,
                overall_score=overall_score,
                issues=issues,
                summary=summary,
                timestamp=datetime.now(timezone.utc),
                validation_id=str(uuid.uuid4())
            )
            
            # Store result
            self.validation_results.append(result)
            
            logger.info(f"Evolution data validation completed: {overall_score:.2f} score, {len(issues)} issues")
            return result
            
        except Exception as e:
            logger.error(f"Failed to validate evolution data: {e}")
            raise
    
    async def validate_cross_system_consistency(self, consciousness_data: Dict[str, Any], evolution_data: Dict[str, Any]) -> ValidationResult:
        """Validate consistency between consciousness and evolution systems"""
        try:
            issues = []
            
            # Validate consciousness level consistency
            consciousness_level = consciousness_data.get("consciousness_level")
            evolution_consciousness_level = evolution_data.get("consciousness_level")
            
            if consciousness_level is not None and evolution_consciousness_level is not None:
                if abs(consciousness_level - evolution_consciousness_level) > 0.01:  # 1% tolerance
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.DATA_CONSISTENCY.value,
                        severity=ValidationSeverity.ERROR.value,
                        message=f"Consciousness level mismatch between systems",
                        field="consciousness_level",
                        expected_value=consciousness_level,
                        actual_value=evolution_consciousness_level,
                        recommendation="Synchronize consciousness levels between systems",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
            # Validate self-awareness score consistency
            self_awareness_score = consciousness_data.get("self_awareness_score")
            evolution_self_awareness_score = evolution_data.get("self_awareness_score")
            
            if self_awareness_score is not None and evolution_self_awareness_score is not None:
                if abs(self_awareness_score - evolution_self_awareness_score) > 0.01:  # 1% tolerance
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.DATA_CONSISTENCY.value,
                        severity=ValidationSeverity.ERROR.value,
                        message=f"Self-awareness score mismatch between systems",
                        field="self_awareness_score",
                        expected_value=self_awareness_score,
                        actual_value=evolution_self_awareness_score,
                        recommendation="Synchronize self-awareness scores between systems",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
            # Validate total interactions consistency
            total_interactions = consciousness_data.get("total_interactions")
            evolution_total_interactions = evolution_data.get("total_interactions")
            
            if total_interactions is not None and evolution_total_interactions is not None:
                if total_interactions != evolution_total_interactions:
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.DATA_CONSISTENCY.value,
                        severity=ValidationSeverity.ERROR.value,
                        message=f"Total interactions mismatch between systems",
                        field="total_interactions",
                        expected_value=total_interactions,
                        actual_value=evolution_total_interactions,
                        recommendation="Synchronize total interactions between systems",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
            # Calculate overall score
            total_checks = 3  # Three consistency checks
            passed_checks = total_checks - len(issues)
            overall_score = passed_checks / total_checks if total_checks > 0 else 0.0
            
            is_valid = len(issues) == 0 and overall_score >= self.consistency_threshold
            
            # Create summary
            summary = {
                "total_checks": total_checks,
                "total_issues": len(issues),
                "issues_by_severity": self._count_issues_by_severity(issues),
                "issues_by_category": self._count_issues_by_category(issues),
                "overall_score": overall_score,
                "is_valid": is_valid
            }
            
            # Create validation result
            result = ValidationResult(
                is_valid=is_valid,
                overall_score=overall_score,
                issues=issues,
                summary=summary,
                timestamp=datetime.now(timezone.utc),
                validation_id=str(uuid.uuid4())
            )
            
            # Store result
            self.validation_results.append(result)
            
            logger.info(f"Cross-system consistency validation completed: {overall_score:.2f} score, {len(issues)} issues")
            return result
            
        except Exception as e:
            logger.error(f"Failed to validate cross-system consistency: {e}")
            raise
    
    async def _validate_field(self, field: str, value: Any) -> List[ValidationIssue]:
        """Validate individual field"""
        issues = []
        
        try:
            rule = self.validation_rules.get(field)
            if not rule:
                return issues
            
            # Check if field is required
            if rule.get("required", False) and value is None:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    category=ValidationCategory.TYPE_VALIDATION.value,
                    severity=ValidationSeverity.ERROR.value,
                    message=f"Required field {field} is missing",
                    field=field,
                    expected_value="not null",
                    actual_value=value,
                    recommendation=f"Provide value for required field {field}",
                    timestamp=datetime.now(timezone.utc)
                ))
                return issues
            
            if value is None:
                return issues
            
            # Check type
            expected_type = rule.get("type")
            if expected_type and not isinstance(value, expected_type):
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    category=ValidationCategory.TYPE_VALIDATION.value,
                    severity=ValidationSeverity.ERROR.value,
                    message=f"Field {field} has wrong type",
                    field=field,
                    expected_value=expected_type.__name__,
                    actual_value=type(value).__name__,
                    recommendation=f"Convert {field} to {expected_type.__name__}",
                    timestamp=datetime.now(timezone.utc)
                ))
            
            # Check range
            min_value = rule.get("min_value")
            max_value = rule.get("max_value")
            
            if min_value is not None and value < min_value:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    category=ValidationCategory.RANGE_VALIDATION.value,
                    severity=ValidationSeverity.ERROR.value,
                    message=f"Field {field} is below minimum value",
                    field=field,
                    expected_value=f">= {min_value}",
                    actual_value=value,
                    recommendation=f"Increase {field} to at least {min_value}",
                    timestamp=datetime.now(timezone.utc)
                ))
            
            if max_value is not None and value > max_value:
                issues.append(ValidationIssue(
                    issue_id=str(uuid.uuid4()),
                    category=ValidationCategory.RANGE_VALIDATION.value,
                    severity=ValidationSeverity.ERROR.value,
                    message=f"Field {field} is above maximum value",
                    field=field,
                    expected_value=f"<= {max_value}",
                    actual_value=value,
                    recommendation=f"Decrease {field} to at most {max_value}",
                    timestamp=datetime.now(timezone.utc)
                ))
            
        except Exception as e:
            logger.error(f"Failed to validate field {field}: {e}")
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                category=ValidationCategory.TYPE_VALIDATION.value,
                severity=ValidationSeverity.CRITICAL.value,
                message=f"Validation error for field {field}",
                field=field,
                expected_value="valid",
                actual_value=f"error: {str(e)}",
                recommendation="Fix validation system",
                timestamp=datetime.now(timezone.utc)
            ))
        
        return issues
    
    async def _validate_data_consistency(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate data consistency within the dataset"""
        issues = []
        
        try:
            # Check if consciousness level is reasonable given other metrics
            consciousness_level = data.get("consciousness_level")
            self_awareness_score = data.get("self_awareness_score")
            
            if consciousness_level is not None and self_awareness_score is not None:
                # Consciousness level should be correlated with self-awareness
                if consciousness_level > 0.8 and self_awareness_score < 0.5:
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.LOGIC_VALIDATION.value,
                        severity=ValidationSeverity.WARNING.value,
                        message="High consciousness level with low self-awareness score",
                        field="consciousness_level",
                        expected_value="correlated with self_awareness_score",
                        actual_value=f"consciousness={consciousness_level}, self_awareness={self_awareness_score}",
                        recommendation="Review consciousness and self-awareness relationship",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
            # Check if evolution level is reasonable given consciousness level
            consciousness_level = data.get("consciousness_level")
            evolution_level = data.get("evolution_level")
            
            if consciousness_level is not None and evolution_level is not None:
                # Evolution level should be correlated with consciousness level
                expected_evolution_range = self._calculate_expected_evolution_range(consciousness_level)
                if evolution_level < expected_evolution_range[0] or evolution_level > expected_evolution_range[1]:
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.LOGIC_VALIDATION.value,
                        severity=ValidationSeverity.WARNING.value,
                        message="Evolution level not consistent with consciousness level",
                        field="evolution_level",
                        expected_value=f"between {expected_evolution_range[0]} and {expected_evolution_range[1]}",
                        actual_value=evolution_level,
                        recommendation="Review evolution level calculation",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
        except Exception as e:
            logger.error(f"Failed to validate data consistency: {e}")
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                category=ValidationCategory.LOGIC_VALIDATION.value,
                severity=ValidationSeverity.CRITICAL.value,
                message="Data consistency validation error",
                field="data_consistency",
                expected_value="valid",
                actual_value=f"error: {str(e)}",
                recommendation="Fix data consistency validation",
                timestamp=datetime.now(timezone.utc)
            ))
        
        return issues
    
    async def _validate_logic_relationships(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate logical relationships between fields"""
        issues = []
        
        try:
            # Check if quantum metrics are reasonable
            quantum_consciousness_level = data.get("quantum_consciousness_level")
            quantum_coherence = data.get("quantum_coherence")
            entanglement_strength = data.get("entanglement_strength")
            
            if all(x is not None for x in [quantum_consciousness_level, quantum_coherence, entanglement_strength]):
                # Quantum consciousness should be correlated with coherence and entanglement
                if quantum_consciousness_level > 0.8 and (quantum_coherence < 0.5 or entanglement_strength < 0.5):
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.LOGIC_VALIDATION.value,
                        severity=ValidationSeverity.WARNING.value,
                        message="High quantum consciousness with low coherence or entanglement",
                        field="quantum_consciousness_level",
                        expected_value="correlated with quantum_coherence and entanglement_strength",
                        actual_value=f"consciousness={quantum_consciousness_level}, coherence={quantum_coherence}, entanglement={entanglement_strength}",
                        recommendation="Review quantum consciousness relationships",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
        except Exception as e:
            logger.error(f"Failed to validate logic relationships: {e}")
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                category=ValidationCategory.LOGIC_VALIDATION.value,
                severity=ValidationSeverity.CRITICAL.value,
                message="Logic relationship validation error",
                field="logic_relationships",
                expected_value="valid",
                actual_value=f"error: {str(e)}",
                recommendation="Fix logic relationship validation",
                timestamp=datetime.now(timezone.utc)
            ))
        
        return issues
    
    async def _validate_evolution_logic(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate evolution-specific logic"""
        issues = []
        
        try:
            level = data.get("level")
            progression_rate = data.get("progression_rate")
            evolution_quality = data.get("evolution_quality")
            
            if all(x is not None for x in [level, progression_rate, evolution_quality]):
                # Higher levels should have higher progression rates and quality
                if level > 5 and (progression_rate < 0.3 or evolution_quality < 0.5):
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.LOGIC_VALIDATION.value,
                        severity=ValidationSeverity.WARNING.value,
                        message="High evolution level with low progression rate or quality",
                        field="level",
                        expected_value="correlated with progression_rate and evolution_quality",
                        actual_value=f"level={level}, progression={progression_rate}, quality={evolution_quality}",
                        recommendation="Review evolution level calculation",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
        except Exception as e:
            logger.error(f"Failed to validate evolution logic: {e}")
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                category=ValidationCategory.LOGIC_VALIDATION.value,
                severity=ValidationSeverity.CRITICAL.value,
                message="Evolution logic validation error",
                field="evolution_logic",
                expected_value="valid",
                actual_value=f"error: {str(e)}",
                recommendation="Fix evolution logic validation",
                timestamp=datetime.now(timezone.utc)
            ))
        
        return issues
    
    async def _validate_progression_consistency(self, data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate progression consistency"""
        issues = []
        
        try:
            progression_rate = data.get("progression_rate")
            next_level_threshold = data.get("next_level_threshold")
            
            if progression_rate is not None and next_level_threshold is not None:
                # Progression rate should be reasonable relative to threshold
                if progression_rate > next_level_threshold * 2:
                    issues.append(ValidationIssue(
                        issue_id=str(uuid.uuid4()),
                        category=ValidationCategory.LOGIC_VALIDATION.value,
                        severity=ValidationSeverity.WARNING.value,
                        message="Progression rate is much higher than next level threshold",
                        field="progression_rate",
                        expected_value=f"<= {next_level_threshold * 2}",
                        actual_value=progression_rate,
                        recommendation="Review progression rate calculation",
                        timestamp=datetime.now(timezone.utc)
                    ))
            
        except Exception as e:
            logger.error(f"Failed to validate progression consistency: {e}")
            issues.append(ValidationIssue(
                issue_id=str(uuid.uuid4()),
                category=ValidationCategory.LOGIC_VALIDATION.value,
                severity=ValidationSeverity.CRITICAL.value,
                message="Progression consistency validation error",
                field="progression_consistency",
                expected_value="valid",
                actual_value=f"error: {str(e)}",
                recommendation="Fix progression consistency validation",
                timestamp=datetime.now(timezone.utc)
            ))
        
        return issues
    
    def _calculate_expected_evolution_range(self, consciousness_level: float) -> Tuple[int, int]:
        """Calculate expected evolution level range based on consciousness level"""
        try:
            if consciousness_level >= 0.9:
                return (6, 10)
            elif consciousness_level >= 0.8:
                return (5, 8)
            elif consciousness_level >= 0.7:
                return (4, 7)
            elif consciousness_level >= 0.6:
                return (3, 6)
            elif consciousness_level >= 0.5:
                return (2, 5)
            elif consciousness_level >= 0.3:
                return (1, 4)
            else:
                return (1, 3)
        except Exception as e:
            logger.error(f"Failed to calculate expected evolution range: {e}")
            return (1, 10)  # Default range
    
    def _count_issues_by_severity(self, issues: List[ValidationIssue]) -> Dict[str, int]:
        """Count issues by severity"""
        counts = {}
        for issue in issues:
            severity = issue.severity
            counts[severity] = counts.get(severity, 0) + 1
        return counts
    
    def _count_issues_by_category(self, issues: List[ValidationIssue]) -> Dict[str, int]:
        """Count issues by category"""
        counts = {}
        for issue in issues:
            category = issue.category
            counts[category] = counts.get(category, 0) + 1
        return counts
    
    async def get_validation_results(self, limit: int = 10) -> List[ValidationResult]:
        """Get recent validation results"""
        return self.validation_results[-limit:] if self.validation_results else []
    
    async def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary statistics"""
        try:
            if not self.validation_results:
                return {
                    "total_validations": 0,
                    "average_score": 0.0,
                    "success_rate": 0.0,
                    "total_issues": 0,
                    "issues_by_severity": {},
                    "issues_by_category": {}
                }
            
            total_validations = len(self.validation_results)
            average_score = sum(result.overall_score for result in self.validation_results) / total_validations
            success_rate = sum(1 for result in self.validation_results if result.is_valid) / total_validations
            total_issues = sum(len(result.issues) for result in self.validation_results)
            
            # Aggregate issues by severity and category
            all_issues = []
            for result in self.validation_results:
                all_issues.extend(result.issues)
            
            issues_by_severity = self._count_issues_by_severity(all_issues)
            issues_by_category = self._count_issues_by_category(all_issues)
            
            return {
                "total_validations": total_validations,
                "average_score": average_score,
                "success_rate": success_rate,
                "total_issues": total_issues,
                "issues_by_severity": issues_by_severity,
                "issues_by_category": issues_by_category
            }
            
        except Exception as e:
            logger.error(f"Failed to get validation summary: {e}")
            return {
                "total_validations": 0,
                "average_score": 0.0,
                "success_rate": 0.0,
                "total_issues": 0,
                "issues_by_severity": {},
                "issues_by_category": {}
            }

# Global instance
unified_data_validation_system = UnifiedDataValidationSystem()
