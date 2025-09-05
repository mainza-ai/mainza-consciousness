"""
Fix error handler decorator usage across all files
Changes @error_handler.handle_errors to @handle_errors with proper import
"""
import os
import re

# Files that need to be fixed
files_to_fix = [
    "backend/utils/knowledge_integration.py",
    "backend/utils/dynamic_knowledge_manager.py", 
    "backend/utils/consciousness_knowledge_integrator.py",
    "backend/utils/knowledge_graph_evolution.py",
    "backend/utils/consciousness_driven_updates.py",
    "backend/utils/knowledge_graph_maintenance.py",
    "backend/utils/memory_integration.py",
    "backend/utils/enhanced_llm_execution.py",
    "backend/utils/agent_knowledge_integration.py"
]

def fix_file(file_path):
    """Fix error handler decorator usage in a single file"""
    print(f"Fixing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs fixing
        if '@error_handler.handle_errors' not in content:
            print(f"  ✅ {file_path} - No fixes needed")
            return True
        
        # Fix import statement
        if 'from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity' in content:
            content = content.replace(
                'from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity',
                'from backend.core.enhanced_error_handling import ErrorHandler, ErrorSeverity, handle_errors'
            )
        elif 'from backend.core.enhanced_error_handling import' in content and 'handle_errors' not in content:
            # Add handle_errors to existing import
            content = re.sub(
                r'from backend\.core\.enhanced_error_handling import ([^\\n]+)',
                r'from backend.core.enhanced_error_handling import \1, handle_errors',
                content
            )
        
        # Fix decorator usage - convert @error_handler.handle_errors(...) to @handle_errors(...)
        # Pattern to match the decorator with its parameters
        pattern = r'@error_handler\.handle_errors\(\s*severity=ErrorSeverity\.(\w+),\s*fallback_return=([^)]+)\s*\)'
        
        def replacement(match):
            severity = match.group(1)
            fallback_return = match.group(2)
            
            # Map severity to suppress_errors
            suppress_errors = severity.lower() in ['low', 'medium']
            
            return f'@handle_errors(\n        component="{os.path.basename(file_path).replace(".py", "")}",\n        fallback_result={fallback_return},\n        suppress_errors={str(suppress_errors).lower()}\n    )'
        
        content = re.sub(pattern, replacement, content)
        
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {file_path} - Fixed successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ {file_path} - Error: {e}")
        return False

def main():
    """Fix all files"""
    print("🔧 Fixing error handler decorator usage...")
    print("=" * 50)
    
    success_count = 0
    total_count = len(files_to_fix)
    
    for file_path in files_to_fix:
        if fix_file(file_path):
            success_count += 1
    
    print("=" * 50)
    print(f"RESULTS: {success_count}/{total_count} files fixed successfully")
    
    if success_count == total_count:
        print("🎉 All files fixed successfully!")
        print("🚀 System should now start without error handler issues")
    else:
        print("⚠️  Some files failed to fix - please check manually")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)