"""
Security Framework
Context7 MCP Standards Implementation

This module provides comprehensive security controls including:
- Authentication and authorization
- Input validation and sanitization
- Rate limiting and DDoS protection
- Encryption and data protection
- Security monitoring and alerting
- Compliance and audit logging
"""

import asyncio
import logging
import hashlib
import hmac
import secrets
import time
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import re
import json
import ipaddress
from functools import wraps
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different operations"""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    AUTHORIZED = "authorized"
    ADMIN = "admin"
    SYSTEM = "system"

class ThreatLevel(Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityEventType(Enum):
    """Security event types"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_BREACH_ATTEMPT = "data_breach_attempt"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    MALICIOUS_INPUT = "malicious_input"

@dataclass
class SecurityEvent:
    """Security event data structure"""
    event_id: str = field(default_factory=lambda: secrets.token_hex(16))
    event_type: SecurityEventType = SecurityEventType.SUSPICIOUS_ACTIVITY
    threat_level: ThreatLevel = ThreatLevel.MEDIUM
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False

@dataclass
class UserSession:
    """User session information"""
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    permissions: List[str] = field(default_factory=list)
    is_admin: bool = False
    expires_at: Optional[datetime] = None

class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = {}
        self._lock = asyncio.Lock()
    
    async def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed under rate limit"""
        async with self._lock:
            now = time.time()
            
            # Initialize if not exists
            if identifier not in self.requests:
                self.requests[identifier] = []
            
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < self.window_seconds
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # Add current request
            self.requests[identifier].append(now)
            return True
    
    async def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier"""
        async with self._lock:
            if identifier not in self.requests:
                return self.max_requests
            
            now = time.time()
            recent_requests = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < self.window_seconds
            ]
            
            return max(0, self.max_requests - len(recent_requests))

class InputValidator:
    """Input validation and sanitization"""
    
    def __init__(self):
        # Common attack patterns
        self.sql_injection_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
            r"(--|#|/\*|\*/)",
            r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
            r"(\'\s*(OR|AND)\s*\'\w*\'\s*=\s*\'\w*\')"
        ]
        
        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
            r"<object[^>]*>.*?</object>"
        ]
        
        self.command_injection_patterns = [
            r"[;&|`$(){}[\]\\]",
            r"\b(cat|ls|pwd|whoami|id|uname|ps|netstat|ifconfig)\b",
            r"(\.\.\/|\.\.\\\\)"
        ]
    
    def validate_input(self, input_data: Any, input_type: str = "general") -> Dict[str, Any]:
        """Validate input data"""
        result = {
            "is_valid": True,
            "threats_detected": [],
            "sanitized_data": input_data
        }
        
        if isinstance(input_data, str):
            # Check for SQL injection
            if self._check_patterns(input_data, self.sql_injection_patterns):
                result["is_valid"] = False
                result["threats_detected"].append("sql_injection")
            
            # Check for XSS
            if self._check_patterns(input_data, self.xss_patterns):
                result["is_valid"] = False
                result["threats_detected"].append("xss")
            
            # Check for command injection
            if self._check_patterns(input_data, self.command_injection_patterns):
                result["is_valid"] = False
                result["threats_detected"].append("command_injection")
            
            # Sanitize data
            result["sanitized_data"] = self._sanitize_string(input_data)
        
        elif isinstance(input_data, dict):
            # Recursively validate dictionary
            sanitized_dict = {}
            for key, value in input_data.items():
                key_validation = self.validate_input(key, "key")
                value_validation = self.validate_input(value, input_type)
                
                if not key_validation["is_valid"] or not value_validation["is_valid"]:
                    result["is_valid"] = False
                    result["threats_detected"].extend(key_validation["threats_detected"])
                    result["threats_detected"].extend(value_validation["threats_detected"])
                
                sanitized_dict[key_validation["sanitized_data"]] = value_validation["sanitized_data"]
            
            result["sanitized_data"] = sanitized_dict
        
        elif isinstance(input_data, list):
            # Validate list items
            sanitized_list = []
            for item in input_data:
                item_validation = self.validate_input(item, input_type)
                if not item_validation["is_valid"]:
                    result["is_valid"] = False
                    result["threats_detected"].extend(item_validation["threats_detected"])
                sanitized_list.append(item_validation["sanitized_data"])
            
            result["sanitized_data"] = sanitized_list
        
        return result
    
    def _check_patterns(self, text: str, patterns: List[str]) -> bool:
        """Check if text matches any of the threat patterns"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _sanitize_string(self, text: str) -> str:
        """Sanitize string input"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', text)
        
        # Limit length
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000]
        
        return sanitized.strip()

class EncryptionManager:
    """Encryption and decryption management"""
    
    def __init__(self, encryption_key: Optional[bytes] = None):
        if encryption_key:
            self.fernet = Fernet(encryption_key)
        else:
            # Generate key from environment or create new one
            key = os.getenv("ENCRYPTION_KEY")
            if key:
                self.fernet = Fernet(key.encode())
            else:
                self.fernet = Fernet(Fernet.generate_key())
                logger.warning("Using generated encryption key - set ENCRYPTION_KEY environment variable for production")
    
    def encrypt(self, data: Union[str, bytes]) -> str:
        """Encrypt data"""
        if isinstance(data, str):
            data = data.encode()
        
        encrypted = self.fernet.encrypt(data)
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Invalid encrypted data")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            return False
    
    def generate_token(self, payload: Dict[str, Any], expires_hours: int = 24) -> str:
        """Generate JWT token"""
        payload["exp"] = datetime.utcnow() + timedelta(hours=expires_hours)
        payload["iat"] = datetime.utcnow()
        
        # Use a secret key from environment or generate one
        secret_key = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
        
        return jwt.encode(payload, secret_key, algorithm="HS256")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            secret_key = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

class SecurityMonitor:
    """Security monitoring and alerting"""
    
    def __init__(self):
        self.security_events: List[SecurityEvent] = []
        self.blocked_ips: Dict[str, datetime] = {}
        self.suspicious_users: Dict[str, int] = {}
        self.alert_handlers: List[Callable] = []
        self.max_events = 10000
    
    def register_alert_handler(self, handler: Callable):
        """Register security alert handler"""
        self.alert_handlers.append(handler)
    
    async def log_security_event(
        self, 
        event_type: SecurityEventType,
        threat_level: ThreatLevel = ThreatLevel.MEDIUM,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log security event"""
        event = SecurityEvent(
            event_type=event_type,
            threat_level=threat_level,
            user_id=user_id,
            ip_address=ip_address,
            details=details or {}
        )
        
        self.security_events.append(event)
        
        # Maintain event history size
        if len(self.security_events) > self.max_events:
            self.security_events = self.security_events[-self.max_events//2:]
        
        # Check for patterns and trigger alerts
        await self._analyze_security_patterns(event)
        
        # Log event
        logger.warning(f"Security Event [{event.event_type.value}]: {event.details}")
    
    async def _analyze_security_patterns(self, event: SecurityEvent):
        """Analyze security patterns and trigger alerts"""
        # Check for repeated failures from same IP
        if event.ip_address and event.event_type == SecurityEventType.LOGIN_FAILURE:
            recent_failures = [
                e for e in self.security_events[-100:]  # Check last 100 events
                if (e.ip_address == event.ip_address and 
                    e.event_type == SecurityEventType.LOGIN_FAILURE and
                    (datetime.now() - e.timestamp).total_seconds() < 300)  # Last 5 minutes
            ]
            
            if len(recent_failures) >= 5:
                await self._trigger_ip_block(event.ip_address, "Multiple login failures")
        
        # Check for suspicious user activity
        if event.user_id:
            self.suspicious_users[event.user_id] = self.suspicious_users.get(event.user_id, 0) + 1
            
            if self.suspicious_users[event.user_id] >= 10:
                await self._trigger_user_alert(event.user_id, "Suspicious activity pattern")
        
        # Trigger immediate alerts for high/critical threats
        if event.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            await self._trigger_security_alert(event)
    
    async def _trigger_ip_block(self, ip_address: str, reason: str):
        """Block IP address"""
        self.blocked_ips[ip_address] = datetime.now() + timedelta(hours=1)
        
        await self.log_security_event(
            SecurityEventType.SUSPICIOUS_ACTIVITY,
            ThreatLevel.HIGH,
            ip_address=ip_address,
            details={"action": "ip_blocked", "reason": reason}
        )
    
    async def _trigger_user_alert(self, user_id: str, reason: str):
        """Trigger user-specific alert"""
        await self.log_security_event(
            SecurityEventType.SUSPICIOUS_ACTIVITY,
            ThreatLevel.HIGH,
            user_id=user_id,
            details={"action": "user_flagged", "reason": reason}
        )
    
    async def _trigger_security_alert(self, event: SecurityEvent):
        """Trigger security alert to handlers"""
        alert_data = {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "threat_level": event.threat_level.value,
            "timestamp": event.timestamp.isoformat(),
            "user_id": event.user_id,
            "ip_address": event.ip_address,
            "details": event.details
        }
        
        for handler in self.alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(alert_data)
                else:
                    handler(alert_data)
            except Exception as e:
                logger.error(f"Security alert handler failed: {e}")
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP address is blocked"""
        if ip_address in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip_address]:
                return True
            else:
                # Remove expired block
                del self.blocked_ips[ip_address]
        return False
    
    def get_security_report(self) -> Dict[str, Any]:
        """Get security report"""
        recent_events = [
            e for e in self.security_events
            if (datetime.now() - e.timestamp).total_seconds() < 86400  # Last 24 hours
        ]
        
        event_counts = {}
        threat_counts = {}
        
        for event in recent_events:
            event_type = event.event_type.value
            threat_level = event.threat_level.value
            
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            threat_counts[threat_level] = threat_counts.get(threat_level, 0) + 1
        
        return {
            "total_events_24h": len(recent_events),
            "events_by_type": event_counts,
            "events_by_threat_level": threat_counts,
            "blocked_ips": len(self.blocked_ips),
            "suspicious_users": len(self.suspicious_users),
            "unresolved_events": len([e for e in recent_events if not e.resolved])
        }

class SecurityFramework:
    """Main security framework coordinator"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.input_validator = InputValidator()
        self.encryption_manager = EncryptionManager()
        self.security_monitor = SecurityMonitor()
        self.active_sessions: Dict[str, UserSession] = {}
        self.security_policies: Dict[str, Any] = self._load_default_policies()
    
    def _load_default_policies(self) -> Dict[str, Any]:
        """Load default security policies"""
        return {
            "password_policy": {
                "min_length": 8,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special_chars": True
            },
            "session_policy": {
                "max_duration_hours": 24,
                "idle_timeout_minutes": 30,
                "require_2fa": False
            },
            "rate_limiting": {
                "api_requests_per_minute": 100,
                "login_attempts_per_hour": 5,
                "password_reset_per_day": 3
            }
        }
    
    async def authenticate_user(
        self, 
        username: str, 
        password: str, 
        ip_address: str,
        user_agent: str
    ) -> Optional[UserSession]:
        """Authenticate user and create session"""
        
        # Check if IP is blocked
        if self.security_monitor.is_ip_blocked(ip_address):
            await self.security_monitor.log_security_event(
                SecurityEventType.UNAUTHORIZED_ACCESS,
                ThreatLevel.HIGH,
                ip_address=ip_address,
                details={"reason": "blocked_ip", "username": username}
            )
            return None
        
        # Rate limit login attempts
        if not await self.rate_limiter.is_allowed(f"login:{ip_address}"):
            await self.security_monitor.log_security_event(
                SecurityEventType.RATE_LIMIT_EXCEEDED,
                ThreatLevel.MEDIUM,
                ip_address=ip_address,
                details={"endpoint": "login", "username": username}
            )
            return None
        
        # Validate input
        username_validation = self.input_validator.validate_input(username, "username")
        if not username_validation["is_valid"]:
            await self.security_monitor.log_security_event(
                SecurityEventType.MALICIOUS_INPUT,
                ThreatLevel.HIGH,
                ip_address=ip_address,
                details={"threats": username_validation["threats_detected"]}
            )
            return None
        
        # TODO: Implement actual user authentication against database
        # For now, this is a placeholder
        authenticated = self._verify_user_credentials(username, password)
        
        if authenticated:
            # Create session
            session = UserSession(
                session_id=secrets.token_hex(32),
                user_id=username,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=datetime.now() + timedelta(hours=24)
            )
            
            self.active_sessions[session.session_id] = session
            
            await self.security_monitor.log_security_event(
                SecurityEventType.LOGIN_SUCCESS,
                ThreatLevel.LOW,
                user_id=username,
                ip_address=ip_address
            )
            
            return session
        else:
            await self.security_monitor.log_security_event(
                SecurityEventType.LOGIN_FAILURE,
                ThreatLevel.MEDIUM,
                user_id=username,
                ip_address=ip_address
            )
            return None
    
    def _verify_user_credentials(self, username: str, password: str) -> bool:
        """Verify user credentials - placeholder implementation"""
        # TODO: Implement actual credential verification
        return username == "admin" and password == "admin123"
    
    async def validate_session(self, session_id: str, ip_address: str) -> Optional[UserSession]:
        """Validate user session"""
        session = self.active_sessions.get(session_id)
        
        if not session:
            return None
        
        # Check expiration
        if session.expires_at and datetime.now() > session.expires_at:
            del self.active_sessions[session_id]
            return None
        
        # Check IP consistency (optional security measure)
        if session.ip_address != ip_address:
            await self.security_monitor.log_security_event(
                SecurityEventType.SUSPICIOUS_ACTIVITY,
                ThreatLevel.HIGH,
                user_id=session.user_id,
                ip_address=ip_address,
                details={"reason": "ip_mismatch", "original_ip": session.ip_address}
            )
            # Optionally invalidate session
            # del self.active_sessions[session_id]
            # return None
        
        # Update last activity
        session.last_activity = datetime.now()
        return session
    
    def require_security_level(self, required_level: SecurityLevel):
        """Decorator for endpoint security requirements"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Extract request information (this would be adapted for your framework)
                # For now, this is a placeholder implementation
                
                if required_level == SecurityLevel.PUBLIC:
                    return await func(*args, **kwargs)
                
                # TODO: Implement actual security level checking
                # This would involve checking session, permissions, etc.
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    async def validate_and_sanitize_input(self, data: Any) -> Dict[str, Any]:
        """Validate and sanitize input data"""
        return self.input_validator.validate_input(data)
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get overall security status"""
        return {
            "active_sessions": len(self.active_sessions),
            "blocked_ips": len(self.security_monitor.blocked_ips),
            "security_events_24h": len([
                e for e in self.security_monitor.security_events
                if (datetime.now() - e.timestamp).total_seconds() < 86400
            ]),
            "security_report": self.security_monitor.get_security_report()
        }

# Global security framework instance
security_framework = SecurityFramework()

# Convenience decorators
def require_authentication(func):
    """Decorator requiring authentication"""
    return security_framework.require_security_level(SecurityLevel.AUTHENTICATED)(func)

def require_authorization(func):
    """Decorator requiring authorization"""
    return security_framework.require_security_level(SecurityLevel.AUTHORIZED)(func)

def require_admin(func):
    """Decorator requiring admin privileges"""
    return security_framework.require_security_level(SecurityLevel.ADMIN)(func)

# Export key components
__all__ = [
    'SecurityLevel', 'ThreatLevel', 'SecurityEventType', 'SecurityEvent', 'UserSession',
    'RateLimiter', 'InputValidator', 'EncryptionManager', 'SecurityMonitor', 'SecurityFramework',
    'security_framework', 'require_authentication', 'require_authorization', 'require_admin'
]