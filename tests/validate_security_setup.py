#!/usr/bin/env python3
"""
Security Setup Validation Script for Mainza Consciousness System

This script validates that the system is properly configured with secure credentials
and no hardcoded passwords remain in the codebase.
"""

import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_environment_variables():
    """Check that required environment variables are properly configured."""
    print("🔍 Checking Environment Variables...")
    
    # Load environment variables
    load_dotenv()
    
    issues = []
    
    # Check Neo4j password
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    if not neo4j_password:
        issues.append("❌ NEO4J_PASSWORD not set in environment")
    elif len(neo4j_password) < 8:
        issues.append("❌ NEO4J_PASSWORD too short (minimum 8 characters)")
    elif neo4j_password in ["password", "admin", "neo4j", "mainza2024"]:
        issues.append("❌ NEO4J_PASSWORD uses insecure default value")
    else:
        print("✅ NEO4J_PASSWORD properly configured")
    
    # Check LiveKit credentials (optional)
    livekit_key = os.getenv("LIVEKIT_API_KEY")
    livekit_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if livekit_key and livekit_secret:
        if livekit_key in ["devkey", "APIvSeqCu83oLnz"]:
            issues.append("❌ LIVEKIT_API_KEY uses insecure default value")
        elif livekit_secret in ["secret", "jigSXDgPSr6XVcsB0lSjL2ypRO3tTpjTh9AYeb7w2L"]:
            issues.append("❌ LIVEKIT_API_SECRET uses insecure default value")
        else:
            print("✅ LiveKit credentials properly configured")
    else:
        print("ℹ️ LiveKit credentials not configured (voice features will be disabled)")
    
    return issues

def check_hardcoded_credentials():
    """Check for hardcoded credentials in source code."""
    print("\n🔍 Scanning for Hardcoded Credentials...")
    
    # Patterns to search for
    dangerous_patterns = [
        (r'mainza2024', "Default Neo4j password"),
        (r'APIvSeqCu83oLnz', "Default LiveKit API key"),
        (r'jigSXDgPSr6XVcsB0lSjL2ypRO3tTpjTh9AYeb7w2L', "Default LiveKit secret"),
        (r'password.*=.*["\'][^"\']{1,20}["\']', "Potential hardcoded password"),
    ]
    
    # Files to check
    source_files = []
    for pattern in ["**/*.py", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.json"]:
        source_files.extend(Path(".").glob(pattern))
    
    # Exclude certain directories and files
    exclude_patterns = [
        "node_modules/", ".git/", "__pycache__/", ".pytest_cache/",
        "validate_security_setup.py", ".github/workflows/", "test_"
    ]
    
    issues = []
    
    for file_path in source_files:
        # Skip excluded files
        if any(exclude in str(file_path) for exclude in exclude_patterns):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern, description in dangerous_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues.append(f"❌ {file_path}: Found {description}")
                    
        except (UnicodeDecodeError, PermissionError):
            # Skip binary files or files we can't read
            continue
    
    if not issues:
        print("✅ No hardcoded credentials found in source code")
    
    return issues

def check_env_file_security():
    """Check .env file security."""
    print("\n🔍 Checking .env File Security...")
    
    issues = []
    
    # Check if .env exists
    if not os.path.exists(".env"):
        issues.append("⚠️ .env file not found - you'll need to create one")
        return issues
    
    # Check .env file permissions (Unix-like systems)
    if hasattr(os, 'stat'):
        import stat
        env_stat = os.stat(".env")
        mode = stat.filemode(env_stat.st_mode)
        if not (env_stat.st_mode & 0o077 == 0):  # Check if group/other have no permissions
            issues.append("⚠️ .env file has overly permissive permissions (should be 600)")
        else:
            print("✅ .env file permissions are secure")
    
    # Check .gitignore
    if os.path.exists(".gitignore"):
        with open(".gitignore", 'r') as f:
            gitignore_content = f.read()
        if ".env" in gitignore_content:
            print("✅ .env file is properly ignored by git")
        else:
            issues.append("❌ .env file not found in .gitignore")
    else:
        issues.append("❌ .gitignore file not found")
    
    return issues

def check_example_file():
    """Check that .env.example doesn't contain real credentials."""
    print("\n🔍 Checking .env.example File...")
    
    issues = []
    
    if not os.path.exists(".env.example"):
        issues.append("⚠️ .env.example file not found")
        return issues
    
    with open(".env.example", 'r') as f:
        content = f.read()
    
    # Check for insecure defaults
    insecure_patterns = [
        ("mainza2024", "Contains default Neo4j password"),
        ("APIvSeqCu83oLnz", "Contains default LiveKit key"),
        ("jigSXDgPSr6XVcsB0lSjL2ypRO3tTpjTh9AYeb7w2L", "Contains default LiveKit secret"),
    ]
    
    for pattern, description in insecure_patterns:
        if pattern in content:
            issues.append(f"❌ .env.example: {description}")
    
    if not issues:
        print("✅ .env.example uses secure placeholder values")
    
    return issues

def main():
    """Main validation function."""
    print("🔒 Mainza Security Setup Validation")
    print("=" * 50)
    
    all_issues = []
    
    # Run all checks
    all_issues.extend(check_environment_variables())
    all_issues.extend(check_hardcoded_credentials())
    all_issues.extend(check_env_file_security())
    all_issues.extend(check_example_file())
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Security Validation Summary")
    print("=" * 50)
    
    if all_issues:
        print("❌ Security Issues Found:")
        for issue in all_issues:
            print(f"   {issue}")
        print(f"\n🚨 Total Issues: {len(all_issues)}")
        print("\n📖 Please refer to SECURITY_SETUP.md for guidance on fixing these issues.")
        return 1
    else:
        print("✅ All Security Checks Passed!")
        print("🎉 Your Mainza system is properly secured and ready for use.")
        return 0

if __name__ == "__main__":
    sys.exit(main())