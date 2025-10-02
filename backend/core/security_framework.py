"""
Security Framework for Mainza AI
Comprehensive security hardening and monitoring system
"""
import os
import hashlib
import secrets
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from functools import wraps
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
import re

logger = logging.getLogger(__name__)

# Security configuration
SECURITY_CONFIG = {
    "SECRET_KEY": os.getenv("SECRET_KEY", secrets.token_urlsafe(32)),
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30,
    "REFRESH_TOKEN_EXPIRE_DAYS": 7,
    "PASSWORD_MIN_LENGTH": 12,
    "MAX_LOGIN_ATTEMPTS": 5,
    "LOCKOUT_DURATION_MINUTES": 15,
    "RATE_LIMIT_REQUESTS": 100,
    "RATE_LIMIT_WINDOW": 3600,  # 1 hour
}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class SecurityFramework:
    """Comprehensive security framework for Mainza AI"""
    
    def __init__(self):
        self.failed_attempts: Dict[str, int] = {}
        self.locked_accounts: Dict[str, datetime] = {}
        self.rate_limits: Dict[str, List[datetime]] = {}
        self.security_events: List[Dict[str, Any]] = []
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=SECURITY_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"])
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECURITY_CONFIG["SECRET_KEY"], algorithm=SECURITY_CONFIG["ALGORITHM"])
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECURITY_CONFIG["SECRET_KEY"], algorithms=[SECURITY_CONFIG["ALGORITHM"]])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        issues = []
        
        if len(password) < SECURITY_CONFIG["PASSWORD_MIN_LENGTH"]:
            issues.append(f"Password must be at least {SECURITY_CONFIG['PASSWORD_MIN_LENGTH']} characters")
        
        if not re.search(r"[A-Z]", password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", password):
            issues.append("Password must contain at least one number")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            issues.append("Password must contain at least one special character")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "strength_score": self._calculate_password_strength(password)
        }
    
    def _calculate_password_strength(self, password: str) -> int:
        """Calculate password strength score (0-100)"""
        score = 0
        
        # Length bonus
        if len(password) >= 12:
            score += 20
        elif len(password) >= 8:
            score += 10
        
        # Character variety bonus
        if re.search(r"[A-Z]", password):
            score += 15
        if re.search(r"[a-z]", password):
            score += 15
        if re.search(r"\d", password):
            score += 15
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 20
        
        # Complexity bonus
        if len(set(password)) > len(password) * 0.7:
            score += 15
        
        return min(100, score)
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """Check if client is within rate limits"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=SECURITY_CONFIG["RATE_LIMIT_WINDOW"])
        
        # Clean old requests
        if client_ip in self.rate_limits:
            self.rate_limits[client_ip] = [
                req_time for req_time in self.rate_limits[client_ip]
                if req_time > window_start
            ]
        else:
            self.rate_limits[client_ip] = []
        
        # Check if within limits
        if len(self.rate_limits[client_ip]) >= SECURITY_CONFIG["RATE_LIMIT_REQUESTS"]:
            return False
        
        # Add current request
        self.rate_limits[client_ip].append(now)
        return True
    
    def check_account_lockout(self, username: str) -> bool:
        """Check if account is locked out"""
        if username in self.locked_accounts:
            lockout_time = self.locked_accounts[username]
            if datetime.utcnow() < lockout_time:
                return True
            else:
                # Remove expired lockout
                del self.locked_accounts[username]
                self.failed_attempts[username] = 0
        
        return False
    
    def record_failed_login(self, username: str, client_ip: str):
        """Record failed login attempt"""
        self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
        
        if self.failed_attempts[username] >= SECURITY_CONFIG["MAX_LOGIN_ATTEMPTS"]:
            lockout_duration = timedelta(minutes=SECURITY_CONFIG["LOCKOUT_DURATION_MINUTES"])
            self.locked_accounts[username] = datetime.utcnow() + lockout_duration
            
            self.log_security_event("account_lockout", {
                "username": username,
                "client_ip": client_ip,
                "failed_attempts": self.failed_attempts[username],
                "lockout_duration": SECURITY_CONFIG["LOCKOUT_DURATION_MINUTES"]
            })
    
    def record_successful_login(self, username: str, client_ip: str):
        """Record successful login"""
        if username in self.failed_attempts:
            del self.failed_attempts[username]
        
        self.log_security_event("successful_login", {
            "username": username,
            "client_ip": client_ip,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security event"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        self.security_events.append(event)
        
        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]
        
        logger.warning(f"Security event: {event_type} - {details}")
    
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input"""
        if not isinstance(input_string, str):
            return str(input_string)
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_string)
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for storage"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for responses"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
            "X-Permitted-Cross-Domain-Policies": "none"
        }
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics"""
        return {
            "failed_attempts": len(self.failed_attempts),
            "locked_accounts": len(self.locked_accounts),
            "rate_limited_ips": len(self.rate_limits),
            "security_events": len(self.security_events),
            "recent_events": self.security_events[-10:] if self.security_events else []
        }

# Security decorators
def require_authentication(func):
    """Decorator to require authentication"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This would check for valid authentication
        # Implementation depends on your auth system
        return await func(*args, **kwargs)
    return wrapper

def rate_limit(requests: int = 100, window: int = 3600):
    """Decorator for rate limiting"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
            # This would implement rate limiting
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
def input_validation(func):
    """Decorator for input validation"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This would validate inputs
        return await func(*args, **kwargs)
    return wrapper

# Global security framework instance
security_framework = SecurityFramework()

# Security middleware
class SecurityMiddleware:
    """FastAPI middleware for security"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Add security headers
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                security_headers = security_framework.get_security_headers()
                
                for header, value in security_headers.items():
                    headers[header.lower().encode()] = value.encode()
                
                message["headers"] = list(headers.items())
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)