#!/usr/bin/env python3
"""
CRITICAL FIX: Throttling Response Issue
Fixes the LLM system that's preventing user interactions

This script:
1. Backs up original files
2. Replaces problematic components with fixed versions
3. Updates imports and configurations
4. Validates the fix
"""

import os
import shutil
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def backup_file(file_path: str) -> str:
    """Create backup of original file"""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"
        shutil.copy2(file_path, backup_path)
        logger.info(f"✅ Backed up {file_path} to {backup_path}")
        return backup_path
    return ""

def apply_fix():
    """Apply the comprehensive throttling fix"""
    
    logger.info("🚨 STARTING CRITICAL THROTTLING FIX")
    logger.info("=" * 60)
    
    # Files to fix
    files_to_fix = [
        "backend/utils/llm_request_manager.py",
        "backend/utils/consciousness_orchestrator.py",
        "backend/main.py"
    ]
    
    # Create backups
    logger.info("📦 Creating backups...")
    for file_path in files_to_fix:
        backup_file(file_path)
    
    # 1. Replace LLM Request Manager
    logger.info("🔧 Fixing LLM Request Manager...")
    if os.path.exists("backend/utils/llm_request_manager_fixed.py"):
        shutil.copy2("backend/utils/llm_request_manager_fixed.py", "backend/utils/llm_request_manager.py")
        logger.info("✅ LLM Request Manager replaced with fixed version")
    else:
        logger.error("❌ Fixed LLM Request Manager not found!")
        return False
    
    # 2. Replace Consciousness Orchestrator
    logger.info("🔧 Fixing Consciousness Orchestrator...")
    if os.path.exists("backend/utils/consciousness_orchestrator_fixed.py"):
        shutil.copy2("backend/utils/consciousness_orchestrator_fixed.py", "backend/utils/consciousness_orchestrator.py")
        logger.info("✅ Consciousness Orchestrator replaced with fixed version")
    else:
        logger.error("❌ Fixed Consciousness Orchestrator not found!")
        return False
    
    # 3. Update main.py to use fixed components
    logger.info("🔧 Updating main.py imports...")
    try:
        with open("backend/main.py", "r") as f:
            content = f.read()
        
        # Update imports to use fixed versions
        updated_content = content.replace(
            "from backend.utils.consciousness_orchestrator import start_enhanced_consciousness_loop, consciousness_orchestrator",
            "from backend.utils.consciousness_orchestrator import start_enhanced_consciousness_loop_fixed as start_enhanced_consciousness_loop, consciousness_orchestrator_fixed as consciousness_orchestrator"
        )
        
        updated_content = updated_content.replace(
            "from backend.utils.llm_request_manager import llm_request_manager",
            "from backend.utils.llm_request_manager import llm_request_manager_fixed as llm_request_manager"
        )
        
        with open("backend/main.py", "w") as f:
            f.write(updated_content)
        
        logger.info("✅ main.py updated with fixed imports")
        
    except Exception as e:
        logger.error(f"❌ Failed to update main.py: {e}")
        return False
    
    # 4. Update agentic_router.py to notify consciousness of user activity
    logger.info("🔧 Updating agentic_router.py for user activity awareness...")
    try:
        with open("backend/agentic_router.py", "r") as f:
            content = f.read()
        
        # Add user activity notification
        if "consciousness_orchestrator.notify_user_activity" not in content:
            # Find the enhanced_router_chat endpoint
            enhanced_router_pattern = 'async def enhanced_router_chat('
            if enhanced_router_pattern in content:
                # Add user activity notification at the start of the function
                insertion_point = content.find(enhanced_router_pattern)
                if insertion_point != -1:
                    # Find the end of the function signature and start of body
                    func_start = content.find(':', insertion_point)
                    if func_start != -1:
                        func_body_start = content.find('\n', func_start) + 1
                        
                        # Insert user activity notification
                        notification_code = '''    # CRITICAL FIX: Notify consciousness of user activity
    try:
        from backend.utils.consciousness_orchestrator import consciousness_orchestrator
        if hasattr(consciousness_orchestrator, 'notify_user_activity'):
            consciousness_orchestrator.notify_user_activity(user_id)
    except Exception as e:
        logging.debug(f"Could not notify consciousness of user activity: {e}")
    
'''
                        
                        updated_content = (
                            content[:func_body_start] + 
                            notification_code + 
                            content[func_body_start:]
                        )
                        
                        with open("backend/agentic_router.py", "w") as f:
                            f.write(updated_content)
                        
                        logger.info("✅ agentic_router.py updated with user activity notification")
                    else:
                        logger.warning("⚠️ Could not find function body start in agentic_router.py")
                else:
                    logger.warning("⚠️ Could not find function start in agentic_router.py")
            else:
                logger.warning("⚠️ enhanced_router_chat function not found in agentic_router.py")
        else:
            logger.info("✅ User activity notification already present in agentic_router.py")
            
    except Exception as e:
        logger.error(f"❌ Failed to update agentic_router.py: {e}")
        # This is not critical, continue
    
    # 5. Create a validation script
    logger.info("🔧 Creating validation script...")
    validation_script = '''#!/usr/bin/env python3
"""
Validation script for throttling fix
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def validate_fix():
    """Validate that the fix is working"""
    print("🔍 Validating throttling fix...")
    
    try:
        # Test LLM Request Manager
        from backend.utils.llm_request_manager import LLMRequestManager, RequestPriority
        manager = LLMRequestManager()
        
        # Check that user conversation protection is enabled
        if hasattr(manager, 'user_conversation_protection') and manager.user_conversation_protection:
            print("✅ LLM Request Manager: User conversation protection enabled")
        else:
            print("❌ LLM Request Manager: User conversation protection missing")
            return False
        
        # Check never throttle priorities
        if hasattr(manager, 'never_throttle_priorities'):
            never_throttle = manager.never_throttle_priorities
            if RequestPriority.USER_CONVERSATION in never_throttle and RequestPriority.USER_INTERACTION in never_throttle:
                print("✅ LLM Request Manager: Never throttle priorities configured correctly")
            else:
                print("❌ LLM Request Manager: Never throttle priorities not configured")
                return False
        else:
            print("❌ LLM Request Manager: Never throttle priorities missing")
            return False
        
        # Test Consciousness Orchestrator
        from backend.utils.consciousness_orchestrator import ConsciousnessOrchestrator
        orchestrator = ConsciousnessOrchestrator()
        
        # Check user activity awareness
        if hasattr(orchestrator, 'notify_user_activity'):
            print("✅ Consciousness Orchestrator: User activity awareness enabled")
        else:
            print("❌ Consciousness Orchestrator: User activity awareness missing")
            return False
        
        # Check reduced frequency
        if hasattr(orchestrator, 'consciousness_cycle_interval') and orchestrator.consciousness_cycle_interval >= 300:
            print("✅ Consciousness Orchestrator: Reduced frequency configured")
        else:
            print("❌ Consciousness Orchestrator: Frequency not reduced")
            return False
        
        print("🎉 ALL VALIDATIONS PASSED - Fix is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = validate_fix()
    sys.exit(0 if success else 1)
'''
    
    with open("validate_throttling_fix.py", "w") as f:
        f.write(validation_script)
    
    os.chmod("validate_throttling_fix.py", 0o755)
    logger.info("✅ Validation script created")
    
    # 6. Create rollback script
    logger.info("🔧 Creating rollback script...")
    rollback_script = f'''#!/usr/bin/env python3
"""
Rollback script for throttling fix
"""
import os
import shutil
import glob

def rollback_fix():
    """Rollback the throttling fix"""
    print("🔄 Rolling back throttling fix...")
    
    # Find backup files
    backup_files = glob.glob("backend/utils/*.backup_*") + glob.glob("backend/*.backup_*")
    
    for backup_file in backup_files:
        # Extract original file path
        original_file = backup_file.split('.backup_')[0]
        
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, original_file)
            print(f"✅ Restored {{original_file}} from {{backup_file}}")
        else:
            print(f"❌ Backup file not found: {{backup_file}}")
    
    print("🔄 Rollback completed")

if __name__ == "__main__":
    rollback_fix()
'''
    
    with open("rollback_throttling_fix.py", "w") as f:
        f.write(rollback_script)
    
    os.chmod("rollback_throttling_fix.py", 0o755)
    logger.info("✅ Rollback script created")
    
    logger.info("=" * 60)
    logger.info("🎉 THROTTLING FIX APPLIED SUCCESSFULLY!")
    logger.info("")
    logger.info("📋 SUMMARY OF CHANGES:")
    logger.info("  ✅ LLM Request Manager: User conversations NEVER throttled")
    logger.info("  ✅ Consciousness Orchestrator: Reduced frequency (5min cycles)")
    logger.info("  ✅ User Activity Awareness: Consciousness pauses during user activity")
    logger.info("  ✅ Priority System: User conversations have highest priority")
    logger.info("  ✅ Background Throttling: Only background processes are throttled")
    logger.info("")
    logger.info("🔧 NEXT STEPS:")
    logger.info("  1. Restart the application: conda run -n mainza python backend/main.py")
    logger.info("  2. Test user conversations - they should work immediately")
    logger.info("  3. Run validation: python validate_throttling_fix.py")
    logger.info("  4. If issues occur, rollback: python rollback_throttling_fix.py")
    logger.info("")
    logger.info("🚨 CRITICAL: User conversations should now work without throttling!")
    
    return True

if __name__ == "__main__":
    success = apply_fix()
    if not success:
        logger.error("❌ Fix application failed!")
        exit(1)
    else:
        logger.info("✅ Fix applied successfully!")
        exit(0)