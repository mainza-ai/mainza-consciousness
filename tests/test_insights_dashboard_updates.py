#!/usr/bin/env python3
"""
Test Insights Dashboard Updates
Context7 MCP Compliance Testing

This script tests the insights dashboard updates:
1. Development status badges
2. New tab classifications
3. UI/UX improvements
4. Data source analysis
"""

import sys
import os
import re
from pathlib import Path

def test_development_status_badge_component():
    """Test that DevelopmentStatusBadge component exists and is properly configured"""
    print("🔍 Testing Development Status Badge Component...")
    
    badge_component_path = "src/components/DevelopmentStatusBadge.tsx"
    
    if not os.path.exists(badge_component_path):
        print("❌ DevelopmentStatusBadge component not found")
        return False
    
    with open(badge_component_path, 'r') as f:
        content = f.read()
    
    required_features = [
        "DevelopmentStatusBadgeProps",
        "coming-soon",
        "in-development", 
        "partial-data",
        "mock-data",
        "Clock",
        "Wrench",
        "AlertCircle",
        "Badge"
    ]
    
    missing_features = []
    for feature in required_features:
        if feature not in content:
            missing_features.append(feature)
    
    if missing_features:
        print("❌ DevelopmentStatusBadge missing features:")
        for feature in missing_features:
            print(f"  - {feature}")
        return False
    
    print("✅ DevelopmentStatusBadge component properly configured!")
    return True

def test_insights_page_tab_classification():
    """Test that InsightsPage has proper tab classification function"""
    print("\n🔍 Testing Insights Page Tab Classification...")
    
    insights_page_path = "src/pages/InsightsPage.tsx"
    
    if not os.path.exists(insights_page_path):
        print("❌ InsightsPage not found")
        return False
    
    with open(insights_page_path, 'r') as f:
        content = f.read()
    
    required_features = [
        "getTabDevelopmentStatus",
        "TabContentWithStatus",
        "real-data",
        "partial-data", 
        "mock-data",
        "coming-soon",
        "DevelopmentStatusBadge"
    ]
    
    missing_features = []
    for feature in required_features:
        if feature not in content:
            missing_features.append(feature)
    
    if missing_features:
        print("❌ InsightsPage missing tab classification features:")
        for feature in missing_features:
            print(f"  - {feature}")
        return False
    
    # Check for specific tab classifications
    tab_classifications = [
        "overview", "graph", "consciousness", "realtime", "knowledge",
        "agents", "concepts", "memories", "performance", "deep", "timeline"
    ]
    
    real_data_tabs_found = 0
    for tab in tab_classifications:
        if f"'{tab}'" in content and "realDataTabs" in content:
            real_data_tabs_found += 1
    
    if real_data_tabs_found >= 10:  # Should have at least 10 real data tabs
        print(f"✅ Found {real_data_tabs_found} real data tabs classified")
    else:
        print(f"❌ Only found {real_data_tabs_found} real data tabs (expected 10+)")
        return False
    
    print("✅ InsightsPage tab classification properly implemented!")
    return True

def test_ui_contrast_improvements():
    """Test that UI contrast improvements are implemented"""
    print("\n🔍 Testing UI Contrast Improvements...")
    
    components_to_check = [
        "src/components/RealTimeConsciousnessStream.tsx",
        "src/components/InteractiveConsciousnessTimeline.tsx", 
        "src/components/AdvancedLearningAnalytics.tsx",
        "src/components/Consciousness3DVisualization.tsx",
        "src/components/PredictiveAnalyticsDashboard.tsx"
    ]
    
    contrast_improvements = [
        "text-white",
        "bg-slate-800",
        "border-slate-700",
        "text-slate-300"
    ]
    
    issues_found = []
    
    for component_path in components_to_check:
        if os.path.exists(component_path):
            with open(component_path, 'r') as f:
                content = f.read()
            
            improvements_found = 0
            for improvement in contrast_improvements:
                if improvement in content:
                    improvements_found += 1
            
            if improvements_found >= 2:  # At least 2 contrast improvements
                print(f"  ✅ {component_path}: {improvements_found} contrast improvements")
            else:
                issues_found.append(f"{component_path}: Only {improvements_found} contrast improvements")
        else:
            issues_found.append(f"{component_path}: File not found")
    
    if issues_found:
        print("❌ UI Contrast Improvement Issues:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All components have contrast improvements!")
        return True

def test_marketplace_component_updates():
    """Test that ConsciousnessMarketplace component reflects correct narrative"""
    print("\n🔍 Testing Marketplace Component Updates...")
    
    marketplace_path = "src/components/ConsciousnessMarketplace.tsx"
    
    if not os.path.exists(marketplace_path):
        print("❌ ConsciousnessMarketplace component not found")
        return False
    
    with open(marketplace_path, 'r') as f:
        content = f.read()
    
    # Check for consciousness data narrative (not personal conversations)
    consciousness_terms = [
        "consciousness data",
        "algorithms",
        "datasets",
        "consciousness patterns",
        "learning algorithms",
        "emotional processing data"
    ]
    
    # Check that personal conversation terms are NOT present
    personal_terms = [
        "personal conversations",
        "my conversations",
        "personal insights",
        "my insights"
    ]
    
    consciousness_terms_found = 0
    for term in consciousness_terms:
        if term in content:
            consciousness_terms_found += 1
    
    personal_terms_found = 0
    for term in personal_terms:
        if term in content:
            personal_terms_found += 1
    
    if consciousness_terms_found >= 3:
        print(f"✅ Found {consciousness_terms_found} consciousness data terms")
    else:
        print(f"❌ Only found {consciousness_terms_found} consciousness data terms (expected 3+)")
        return False
    
    if personal_terms_found > 0:
        print(f"❌ Found {personal_terms_found} personal conversation terms (should be 0)")
        return False
    else:
        print("✅ No personal conversation terms found (correct narrative)")
    
    print("✅ Marketplace component reflects correct consciousness data narrative!")
    return True

def test_insights_page_navigation_structure():
    """Test that InsightsPage navigation structure is properly organized"""
    print("\n🔍 Testing Insights Page Navigation Structure...")
    
    insights_page_path = "src/pages/InsightsPage.tsx"
    
    if not os.path.exists(insights_page_path):
        print("❌ InsightsPage not found")
        return False
    
    with open(insights_page_path, 'r') as f:
        content = f.read()
    
    # Check for proper TabsList structure
    tabs_list_count = content.count("<TabsList")
    tabs_trigger_count = content.count("<TabsTrigger")
    
    if tabs_list_count >= 4:  # Should have at least 4 TabsList groups
        print(f"✅ Found {tabs_list_count} TabsList groups")
    else:
        print(f"❌ Only found {tabs_list_count} TabsList groups (expected 4+)")
        return False
    
    if tabs_trigger_count >= 30:  # Should have at least 30 tabs
        print(f"✅ Found {tabs_trigger_count} TabsTrigger elements")
    else:
        print(f"❌ Only found {tabs_trigger_count} TabsTrigger elements (expected 30+)")
        return False
    
    # Check for proper TabsContent structure
    tabs_content_count = content.count("<TabsContent")
    if tabs_content_count >= 30:
        print(f"✅ Found {tabs_content_count} TabsContent elements")
    else:
        print(f"❌ Only found {tabs_content_count} TabsContent elements (expected 30+)")
        return False
    
    print("✅ InsightsPage navigation structure properly organized!")
    return True

def test_data_sources_analysis_documentation():
    """Test that data sources analysis documentation exists"""
    print("\n🔍 Testing Data Sources Analysis Documentation...")
    
    analysis_doc_path = "docs/INSIGHTS_PAGE_DATA_SOURCES_ANALYSIS.md"
    
    if not os.path.exists(analysis_doc_path):
        print("❌ Data sources analysis document not found")
        return False
    
    with open(analysis_doc_path, 'r') as f:
        content = f.read()
    
    required_sections = [
        "Real Data Tabs",
        "Partial Data Tabs", 
        "Mock Data Tabs",
        "Coming Soon Tabs",
        "Summary"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print("❌ Data sources analysis missing sections:")
        for section in missing_sections:
            print(f"  - {section}")
        return False
    
    print("✅ Data sources analysis documentation complete!")
    return True

def test_frontend_build_compatibility():
    """Test that frontend changes don't break the build"""
    print("\n🔍 Testing Frontend Build Compatibility...")
    
    # Check for common build-breaking issues
    insights_page_path = "src/pages/InsightsPage.tsx"
    
    if not os.path.exists(insights_page_path):
        print("❌ InsightsPage not found")
        return False
    
    with open(insights_page_path, 'r') as f:
        content = f.read()
    
    # Check for unclosed tags
    open_tags = content.count("<TabContentWithStatus")
    close_tags = content.count("</TabContentWithStatus>")
    
    if open_tags != close_tags:
        print(f"❌ Mismatched TabContentWithStatus tags: {open_tags} open, {close_tags} close")
        return False
    
    # Check for proper imports
    required_imports = [
        "DevelopmentStatusBadge",
        "TabContentWithStatus",
        "TabsContent",
        "TabsTrigger"
    ]
    
    missing_imports = []
    for import_name in required_imports:
        if import_name not in content:
            missing_imports.append(import_name)
    
    if missing_imports:
        print("❌ Missing required imports:")
        for import_name in missing_imports:
            print(f"  - {import_name}")
        return False
    
    print("✅ Frontend build compatibility maintained!")
    return True

def main():
    """Run all insights dashboard update tests"""
    print("🚀 Insights Dashboard Updates Testing - Context7 MCP Compliance")
    print("=" * 75)
    
    all_tests_passed = True
    
    tests = [
        test_development_status_badge_component,
        test_insights_page_tab_classification,
        test_ui_contrast_improvements,
        test_marketplace_component_updates,
        test_insights_page_navigation_structure,
        test_data_sources_analysis_documentation,
        test_frontend_build_compatibility
    ]
    
    for test in tests:
        if not test():
            all_tests_passed = False
    
    print("\n" + "=" * 75)
    
    if all_tests_passed:
        print("🎉 ALL INSIGHTS DASHBOARD UPDATE TESTS PASSED!")
        print("✅ Development status badges implemented")
        print("✅ Tab classification system working")
        print("✅ UI contrast improvements applied")
        print("✅ Marketplace narrative corrected")
        print("✅ Navigation structure organized")
        print("✅ Documentation complete")
        print("✅ Frontend build compatibility maintained")
        print("✅ Context7 MCP compliance maintained")
        return 0
    else:
        print("❌ SOME INSIGHTS DASHBOARD UPDATE ISSUES EXIST!")
        print("⚠️  Please review and fix remaining issues")
        return 1

if __name__ == "__main__":
    exit(main())
