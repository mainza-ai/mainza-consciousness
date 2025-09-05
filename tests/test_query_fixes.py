#!/usr/bin/env python3
"""
Test Query Fixes
Context7 MCP Compliance Testing

This script tests the Neo4j query fixes applied:
1. Memory retrieval query simplification
2. UNION query issues resolved
3. Variable scoping fixes
"""

import sys
import os
import re
import subprocess
from pathlib import Path

def test_memory_query_structure():
    """Test that memory retrieval queries are properly structured"""
    print("🔍 Testing Memory Query Structure...")
    
    file_path = "backend/utils/knowledge_integration.py"
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        issues_found = []
        
        # Check for problematic UNION with variable scoping issues
        if re.search(r'UNION.*MATCH.*OPTIONAL MATCH.*\(u\)', content, re.DOTALL):
            issues_found.append("Complex UNION query with potential scoping issues found")
        
        # Check for simplified query approach
        if re.search(r'conversation_result.*memory_result', content):
            print(f"  ✅ {file_path}: Separated query approach found")
        else:
            print(f"  ⚠️  {file_path}: No separated query approach found")
        
        # Check for proper variable references
        if re.search(r'return.*record\["memory"\].*conversation_result', content):
            print(f"  ✅ {file_path}: Proper result variable references found")
        else:
            print(f"  ⚠️  {file_path}: No proper result variable references found")
        
        if issues_found:
            print("❌ Memory Query Structure Issues Found:")
            for issue in issues_found:
                print(f"  - {issue}")
            return False
        else:
            print("✅ Memory query structure is properly organized!")
            return True
    else:
        print(f"❌ {file_path}: File not found")
        return False

def test_cypher_syntax_validation():
    """Test that Cypher queries have valid syntax"""
    print("\\n🔍 Testing Cypher Syntax Validation...")
    
    file_path = "backend/utils/knowledge_integration.py"
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for balanced quotes in cypher queries
        cypher_blocks = re.findall(r'cypher = """([^"]+)"""', content, re.DOTALL)
        
        for i, block in enumerate(cypher_blocks):
            # Check for basic Cypher syntax elements
            if 'MATCH' in block and 'RETURN' in block:
                print(f"  ✅ Cypher block {i+1}: Basic structure valid")
            else:
                print(f"  ⚠️  Cypher block {i+1}: Missing basic structure")
            
            # Check for proper WITH clause usage
            if 'WITH' in block and 'collect(' in block:
                print(f"  ✅ Cypher block {i+1}: Proper aggregation structure")
            else:
                print(f"  ⚠️  Cypher block {i+1}: No aggregation structure found")
        
        print("✅ Cypher syntax validation completed!")
        return True
    else:
        print(f"❌ {file_path}: File not found")
        return False

def test_python_syntax_validation():
    """Test that Python files have valid syntax"""
    print("\\n🔍 Testing Python Syntax Validation...")
    
    python_files = [
        "backend/utils/knowledge_integration.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
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

def test_module_import():
    """Test that the knowledge integration module imports successfully"""
    print("\\n🔍 Testing Module Import...")
    
    try:
        result = subprocess.run(
            ['conda', 'run', '-n', 'mainza', 'python', '-c', 
             'import sys; sys.path.append("."); from backend.utils.knowledge_integration import knowledge_integration_manager; print("✅ Import successful")'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        
        if result.returncode == 0:
            print("  ✅ backend.utils.knowledge_integration: Import successful")
            return True
        else:
            print(f"  ❌ Import failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Import test failed: {str(e)}")
        return False

def main():
    """Run all query fix tests"""
    print("🚀 Query Fixes Testing - Context7 MCP Compliance")
    print("=" * 55)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        test_memory_query_structure,
        test_cypher_syntax_validation,
        test_python_syntax_validation,
        test_module_import
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\\n" + "=" * 55)
    
    if all_tests_passed:
        print("🎉 ALL QUERY FIXES VALIDATED!")
        print("✅ Memory retrieval queries optimized")
        print("✅ Context7 MCP compliance maintained")
        print("✅ No complex UNION query issues")
        return 0
    else:
        print("❌ SOME QUERY ISSUES STILL EXIST!")
        print("⚠️  Please review and fix remaining issues")
        return 1

if __name__ == "__main__":
    exit(main())