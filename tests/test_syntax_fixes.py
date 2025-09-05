"""
Test syntax fixes for Ollama-native environment
Validates that all syntax errors are resolved
"""
import sys
import ast
import traceback

def test_python_syntax(file_path):
    """Test if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(source_code)
        print(f"✅ {file_path} - Syntax OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax Error: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"⚠️  {file_path} - Other Error: {e}")
        return False

def test_import_syntax():
    """Test that critical modules can be imported without syntax errors"""
    
    modules_to_test = [
        "backend.core.enhanced_error_handling",
        "backend.core.performance_optimization", 
        "backend.config.llm_optimization",
        "backend.agentic_config"
    ]
    
    results = []
    
    for module_name in modules_to_test:
        try:
            print(f"Testing import: {module_name}")
            __import__(module_name)
            print(f"✅ {module_name} - Import OK")
            results.append(True)
        except SyntaxError as e:
            print(f"❌ {module_name} - Syntax Error: {e}")
            results.append(False)
        except ImportError as e:
            print(f"⚠️  {module_name} - Import Error (dependencies): {e}")
            results.append(True)  # Import errors are OK, syntax errors are not
        except Exception as e:
            print(f"❌ {module_name} - Other Error: {e}")
            results.append(False)
    
    return results

def main():
    """Run syntax validation tests"""
    print("🔍 Testing Python syntax fixes...")
    print("=" * 50)
    
    # Test specific files that had syntax issues
    files_to_test = [
        "backend/core/enhanced_error_handling.py",
        "backend/core/performance_optimization.py"
    ]
    
    syntax_results = []
    for file_path in files_to_test:
        result = test_python_syntax(file_path)
        syntax_results.append(result)
    
    print("\n🔍 Testing module imports...")
    print("=" * 50)
    
    import_results = test_import_syntax()
    
    print("\n" + "=" * 50)
    print("SYNTAX TEST RESULTS")
    print("=" * 50)
    
    print(f"✅ File Syntax Tests: {sum(syntax_results)}/{len(syntax_results)} passed")
    print(f"✅ Import Tests: {sum(import_results)}/{len(import_results)} passed")
    
    all_passed = all(syntax_results) and all(import_results)
    
    if all_passed:
        print("\n🎉 ALL SYNTAX TESTS PASSED")
        print("🚀 System ready for startup")
    else:
        print("\n⚠️  SOME SYNTAX TESTS FAILED")
        print("🔧 Please fix syntax errors before startup")
    
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)