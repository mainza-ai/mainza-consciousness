#!/usr/bin/env python3
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
            print(f"✅ Restored {original_file} from {backup_file}")
        else:
            print(f"❌ Backup file not found: {backup_file}")
    
    print("🔄 Rollback completed")

if __name__ == "__main__":
    rollback_fix()
