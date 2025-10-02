"""
Remove Fallback Systems Script
Removes all fallback systems that mask real issues

This script identifies and removes fallback systems that prevent
proper error handling and system integration.

Author: Mainza AI Consciousness Team
Date: 2025-10-01
"""

import os
import re
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class FallbackSystemRemover:
    """
    Fallback System Remover
    Identifies and removes fallback systems that mask real issues
    """
    
    def __init__(self, backend_path: str = "backend"):
        self.backend_path = Path(backend_path)
        self.fallback_patterns = [
            # Fallback import patterns
            r"try:\s*import\s+\w+\s+except\s+ImportError.*?fallback",
            r"try:\s*from\s+.*?import\s+.*?except\s+ImportError.*?fallback",
            r"except\s+ImportError.*?fallback\s*=\s*True",
            r"except\s+Exception.*?fallback\s*=\s*True",
            
            # Fallback initialization patterns
            r"if\s+not\s+\w+.*?fallback\s*=\s*True",
            r"fallback\s*=\s*True.*?if\s+not\s+\w+",
            r"using\s+fallback.*?if\s+not\s+\w+",
            
            # Fallback system patterns
            r"fallback.*?system.*?not\s+available",
            r"using\s+.*?fallback.*?system",
            r"fallback.*?engine.*?not\s+available",
            
            # Warning patterns that indicate fallbacks
            r"WARNING.*?fallback",
            r"Warning.*?fallback",
            r"using\s+.*?fallback",
            r"fallback.*?available",
            
            # Standalone fallback patterns
            r"standalone.*?fallback",
            r"fallback.*?standalone",
            r"using\s+standalone",
            
            # Alternative fallback patterns
            r"alternative.*?fallback",
            r"fallback.*?alternative",
            r"using\s+alternative",
            
            # Simplified fallback patterns
            r"simplified.*?fallback",
            r"fallback.*?simplified",
            r"using\s+simplified"
        ]
        
        self.fallback_files = []
        self.removed_fallbacks = []
        
        logger.info("Fallback System Remover initialized")
    
    def scan_for_fallback_systems(self) -> List[Dict[str, Any]]:
        """Scan for fallback systems in the codebase"""
        fallback_systems = []
        
        try:
            # Scan Python files
            for py_file in self.backend_path.rglob("*.py"):
                if self._is_fallback_file(py_file):
                    fallback_info = self._analyze_fallback_file(py_file)
                    if fallback_info:
                        fallback_systems.append(fallback_info)
                        self.fallback_files.append(str(py_file))
            
            logger.info(f"Found {len(fallback_systems)} files with fallback systems")
            return fallback_systems
            
        except Exception as e:
            logger.error(f"Failed to scan for fallback systems: {e}")
            return []
    
    def _is_fallback_file(self, file_path: Path) -> bool:
        """Check if file contains fallback systems"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for fallback patterns (excluding commented lines)
            lines = content.split('\n')
            for line in lines:
                # Skip commented lines
                if line.strip().startswith('#'):
                    continue
                    
                # Check for fallback patterns
                for pattern in self.fallback_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return False
    
    def _analyze_fallback_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file for fallback systems"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fallback_info = {
                "file_path": str(file_path),
                "fallback_patterns": [],
                "fallback_lines": [],
                "fallback_functions": [],
                "fallback_classes": [],
                "severity": "medium"
            }
            
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                line_num = i + 1
                
                # Skip commented lines
                if line.strip().startswith('#'):
                    continue
                
                # Check for fallback patterns
                for pattern in self.fallback_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        fallback_info["fallback_patterns"].append({
                            "line": line_num,
                            "pattern": pattern,
                            "content": line.strip()
                        })
                        fallback_info["fallback_lines"].append(line_num)
                
                # Check for fallback functions
                if re.search(r"def\s+.*?fallback", line, re.IGNORECASE):
                    fallback_info["fallback_functions"].append({
                        "line": line_num,
                        "function": line.strip()
                    })
                
                # Check for fallback classes
                if re.search(r"class\s+.*?fallback", line, re.IGNORECASE):
                    fallback_info["fallback_classes"].append({
                        "line": line_num,
                        "class": line.strip()
                    })
            
            # Determine severity
            if len(fallback_info["fallback_patterns"]) > 10:
                fallback_info["severity"] = "high"
            elif len(fallback_info["fallback_patterns"]) > 5:
                fallback_info["severity"] = "medium"
            else:
                fallback_info["severity"] = "low"
            
            return fallback_info if fallback_info["fallback_patterns"] else None
            
        except Exception as e:
            logger.error(f"Failed to analyze fallback file {file_path}: {e}")
            return None
    
    def remove_fallback_systems(self, file_path: str, dry_run: bool = True) -> Dict[str, Any]:
        """Remove fallback systems from a specific file"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {"error": f"File {file_path} does not exist"}
            
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Analyze fallback systems
            fallback_info = self._analyze_fallback_file(file_path_obj)
            if not fallback_info:
                return {"message": "No fallback systems found in file"}
            
            # Remove fallback systems
            modified_content = self._remove_fallback_patterns(original_content)
            
            if dry_run:
                return {
                    "file_path": file_path,
                    "fallback_patterns_found": len(fallback_info["fallback_patterns"]),
                    "fallback_functions_found": len(fallback_info["fallback_functions"]),
                    "fallback_classes_found": len(fallback_info["fallback_classes"]),
                    "severity": fallback_info["severity"],
                    "changes_preview": self._get_changes_preview(original_content, modified_content),
                    "dry_run": True
                }
            else:
                # Write modified content
                with open(file_path_obj, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                
                self.removed_fallbacks.append({
                    "file_path": file_path,
                    "fallback_patterns_removed": len(fallback_info["fallback_patterns"]),
                    "fallback_functions_removed": len(fallback_info["fallback_functions"]),
                    "fallback_classes_removed": len(fallback_info["fallback_classes"]),
                    "severity": fallback_info["severity"]
                })
                
                return {
                    "file_path": file_path,
                    "fallback_patterns_removed": len(fallback_info["fallback_patterns"]),
                    "fallback_functions_removed": len(fallback_info["fallback_functions"]),
                    "fallback_classes_removed": len(fallback_info["fallback_classes"]),
                    "severity": fallback_info["severity"],
                    "success": True
                }
                
        except Exception as e:
            logger.error(f"Failed to remove fallback systems from {file_path}: {e}")
            return {"error": str(e)}
    
    def _remove_fallback_patterns(self, content: str) -> str:
        """Remove fallback patterns from content"""
        try:
            lines = content.split('\n')
            modified_lines = []
            
            for line in lines:
                # Check if line contains fallback patterns
                is_fallback_line = False
                for pattern in self.fallback_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        is_fallback_line = True
                        break
                
                # Skip fallback lines
                if is_fallback_line:
                    # Add comment indicating removal
                    modified_lines.append(f"# REMOVED FALLBACK: {line.strip()}")
                    continue
                
                # Check for fallback function definitions
                if re.search(r"def\s+.*?fallback", line, re.IGNORECASE):
                    modified_lines.append(f"# REMOVED FALLBACK FUNCTION: {line.strip()}")
                    continue
                
                # Check for fallback class definitions
                if re.search(r"class\s+.*?fallback", line, re.IGNORECASE):
                    modified_lines.append(f"# REMOVED FALLBACK CLASS: {line.strip()}")
                    continue
                
                # Keep non-fallback lines
                modified_lines.append(line)
            
            return '\n'.join(modified_lines)
            
        except Exception as e:
            logger.error(f"Failed to remove fallback patterns: {e}")
            return content
    
    def _get_changes_preview(self, original_content: str, modified_content: str) -> List[str]:
        """Get preview of changes made"""
        try:
            original_lines = original_content.split('\n')
            modified_lines = modified_content.split('\n')
            
            changes = []
            for i, (orig, mod) in enumerate(zip(original_lines, modified_lines)):
                if orig != mod:
                    changes.append(f"Line {i+1}: {orig.strip()} -> {mod.strip()}")
            
            return changes[:10]  # Limit to first 10 changes
            
        except Exception as e:
            logger.error(f"Failed to get changes preview: {e}")
            return []
    
    def remove_all_fallback_systems(self, dry_run: bool = True) -> Dict[str, Any]:
        """Remove all fallback systems from the codebase"""
        try:
            # Scan for fallback systems
            fallback_systems = self.scan_for_fallback_systems()
            
            if not fallback_systems:
                return {"message": "No fallback systems found"}
            
            results = {
                "total_files": len(fallback_systems),
                "files_processed": 0,
                "fallback_patterns_removed": 0,
                "fallback_functions_removed": 0,
                "fallback_classes_removed": 0,
                "files_with_errors": [],
                "dry_run": dry_run
            }
            
            for fallback_system in fallback_systems:
                file_path = fallback_system["file_path"]
                
                try:
                    result = self.remove_fallback_systems(file_path, dry_run)
                    
                    if "error" in result:
                        results["files_with_errors"].append({
                            "file_path": file_path,
                            "error": result["error"]
                        })
                    else:
                        results["files_processed"] += 1
                        results["fallback_patterns_removed"] += result.get("fallback_patterns_removed", 0)
                        results["fallback_functions_removed"] += result.get("fallback_functions_removed", 0)
                        results["fallback_classes_removed"] += result.get("fallback_classes_removed", 0)
                
                except Exception as e:
                    results["files_with_errors"].append({
                        "file_path": file_path,
                        "error": str(e)
                    })
            
            logger.info(f"Processed {results['files_processed']} files, removed {results['fallback_patterns_removed']} fallback patterns")
            return results
            
        except Exception as e:
            logger.error(f"Failed to remove all fallback systems: {e}")
            return {"error": str(e)}
    
    def generate_fallback_report(self) -> Dict[str, Any]:
        """Generate comprehensive fallback system report"""
        try:
            fallback_systems = self.scan_for_fallback_systems()
            
            if not fallback_systems:
                return {
                    "total_files": 0,
                    "total_fallback_patterns": 0,
                    "total_fallback_functions": 0,
                    "total_fallback_classes": 0,
                    "severity_distribution": {},
                    "files_by_severity": {}
                }
            
            # Calculate statistics
            total_fallback_patterns = sum(len(system["fallback_patterns"]) for system in fallback_systems)
            total_fallback_functions = sum(len(system["fallback_functions"]) for system in fallback_systems)
            total_fallback_classes = sum(len(system["fallback_classes"]) for system in fallback_systems)
            
            # Severity distribution
            severity_distribution = {}
            for system in fallback_systems:
                severity = system["severity"]
                severity_distribution[severity] = severity_distribution.get(severity, 0) + 1
            
            # Files by severity
            files_by_severity = {
                "high": [s["file_path"] for s in fallback_systems if s["severity"] == "high"],
                "medium": [s["file_path"] for s in fallback_systems if s["severity"] == "medium"],
                "low": [s["file_path"] for s in fallback_systems if s["severity"] == "low"]
            }
            
            return {
                "total_files": len(fallback_systems),
                "total_fallback_patterns": total_fallback_patterns,
                "total_fallback_functions": total_fallback_functions,
                "total_fallback_classes": total_fallback_classes,
                "severity_distribution": severity_distribution,
                "files_by_severity": files_by_severity,
                "detailed_analysis": fallback_systems
            }
            
        except Exception as e:
            logger.error(f"Failed to generate fallback report: {e}")
            return {"error": str(e)}

# Global instance
fallback_system_remover = FallbackSystemRemover()

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Remove fallback systems from codebase")
    parser.add_argument("--scan", action="store_true", help="Scan for fallback systems")
    parser.add_argument("--remove", action="store_true", help="Remove fallback systems")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't modify files)")
    parser.add_argument("--file", type=str, help="Specific file to process")
    parser.add_argument("--report", action="store_true", help="Generate fallback report")
    
    args = parser.parse_args()
    
    if args.scan:
        fallback_systems = fallback_system_remover.scan_for_fallback_systems()
        print(f"Found {len(fallback_systems)} files with fallback systems")
        for system in fallback_systems:
            print(f"  {system['file_path']}: {len(system['fallback_patterns'])} patterns")
    
    if args.report:
        report = fallback_system_remover.generate_fallback_report()
        print(f"Fallback System Report:")
        print(f"  Total files: {report['total_files']}")
        print(f"  Total patterns: {report['total_fallback_patterns']}")
        print(f"  Total functions: {report['total_fallback_functions']}")
        print(f"  Total classes: {report['total_fallback_classes']}")
        print(f"  Severity distribution: {report['severity_distribution']}")
    
    if args.remove:
        if args.file:
            result = fallback_system_remover.remove_fallback_systems(args.file, args.dry_run)
            print(f"Result: {result}")
        else:
            result = fallback_system_remover.remove_all_fallback_systems(args.dry_run)
            print(f"Result: {result}")
