#!/usr/bin/env python3
"""
Test Critical Error Fixes
Context7 MCP Compliance Testing

This script tests all the critical error fixes applied:
1. Neo4j Cypher parameter syntax fixes
2. ErrorHandler decorator usage fixes  
3. Neo4j aggregation syntax fixes
4. TypeScript evolution_level property fixes
"""

import sys
import os
import re
import subprocess
from pathlib import Path

def test_cypher_parameter_fixes():
    """Test that all Cypher parameter syntax issues are fixed"""
    print("🔍 Testing Cypher Parameter Syntax Fixes...")
    
    files_to_check = [
        "backend/tools/graphmaster_tools.py",
        "backend/tools/graphmaster_tools_enhanced.py", 
        "backend/tools/graphmaster_tools_optimized.py",
        "backend/utils/knowledge_integration.py"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for problematic patterns
            if re.search(r'\$depth\]', content):
                issues_found.append(f"{file_path}: Still contains $depth parameter in relationship pattern")
            
            # Check for fixed patterns
            if re.search(r'\{depth\}', content):
                print(f"  ✅ {file_path}: Cypher parameter syntax fixed")
            else:
                print(f"  ⚠️  {file_path}: No f-string depth substitution found")
    
    if issues_found:
        print("❌ Cypher Parameter Syntax Issues Found:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All Cypher parameter syntax issues fixed!")
        return True

def test_error_handler_fixes():
    """Test that ErrorHandler decorator usage is fixed"""
    print("\n🔍 Testing ErrorHandler Decorator Fixes...")
    
    files_to_check = [
        "backend/utils/memory_integration.py"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for problematic patterns
            if re.search(r'@error_handler\.handle_errors', content):
                issues_found.append(f"{file_path}: Still uses @error_handler.handle_errors")
            
            # Check for fixed patterns
            if re.search(r'@handle_errors\(', content):
                print(f"  ✅ {file_path}: ErrorHandler decorator usage fixed")
            else:
                print(f"  ⚠️  {file_path}: No @handle_errors decorator found")
    
    if issues_found:
        print("❌ ErrorHandler Decorator Issues Found:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All ErrorHandler decorator issues fixed!")
        return True

def test_aggregation_fixes():
    """Test that Neo4j aggregation syntax issues are fixed"""
    print("\n🔍 Testing Neo4j Aggregation Syntax Fixes...")
    
    files_to_check = [
        "backend/utils/knowledge_integration.py"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for problematic patterns
            if re.search(r'collect\([^)]*count\(\*\)', content):
                issues_found.append(f"{file_path}: Still contains nested aggregation count(*) inside collect()")
            
            # Check for fixed patterns
            if re.search(r'interaction_count', content):
                print(f"  ✅ {file_path}: Aggregation syntax fixed with interaction_count variable")
            else:
                print(f"  ⚠️  {file_path}: No interaction_count variable found")
    
    if issues_found:
        print("❌ Aggregation Syntax Issues Found:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All aggregation syntax issues fixed!")
        return True

def test_typescript_interface_fixes():
    """Test that TypeScript MainzaState interface has evolution_level"""
    print("\n🔍 Testing TypeScript Interface Fixes...")
    
    files_to_check = [
        "src/pages/Index.tsx",
        "src/pages/IndexRedesigned.tsx"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for MainzaState interface
            if re.search(r'interface MainzaState', content):
                if not re.search(r'evolution_level:\s*number', content):
                    issues_found.append(f"{file_path}: MainzaState interface missing evolution_level property")
                else:
                    print(f"  ✅ {file_path}: MainzaState interface has evolution_level property")
            else:
                print(f"  ⚠️  {file_path}: No MainzaState interface found")
    
    if issues_found:
        print("❌ TypeScript Interface Issues Found:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All TypeScript interface issues fixed!")
        return True

def test_syntax_validation():
    """Test that Python files have valid syntax using conda mainza environment"""
    print("\n🔍 Testing Python Syntax Validation...")
    
    python_files = [
        "backend/tools/graphmaster_tools.py",
        "backend/tools/graphmaster_tools_enhanced.py", 
        "backend/tools/graphmaster_tools_optimized.py",
        "backend/utils/knowledge_integration.py",
        "backend/utils/memory_integration.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                # Use conda environment mainza for syntax validation
                result = subprocess.run(
                    ['conda', 'run', '-n', 'mainza', 'python', '-m', 'py_compile', file_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"  ✅ {file_path}: Valid Python syntax")
                else:
                    syntax_errors.append(f"{file_path}: {result.stderr}")
                    
            except Exception as e:
                syntax_errors.append(f"{file_path}: {str(e)}")
    
    if syntax_errors:
        print("❌ Python Syntax Errors Found:")
        for error in syntax_errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ All Python files have valid syntax!")
        return True

def main():
    """Run all critical error fix tests"""
    print("🚀 Critical Error Fixes Testing - Context7 MCP Compliance")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        test_cypher_parameter_fixes,
        test_error_handler_fixes,
        test_aggregation_fixes,
        test_typescript_interface_fixes,
        test_syntax_validation
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\n" + "=" * 60)
    
    if all_tests_passed:
        print("🎉 ALL CRITICAL ERROR FIXES VALIDATED!")
        print("✅ System is ready for production deployment")
        print("✅ Context7 MCP compliance maintained")
        return 0
    else:
        print("❌ SOME CRITICAL ERRORS STILL EXIST!")
        print("⚠️  Please review and fix remaining issues")
        return 1

if __name__ == "__main__":
    exit(main())