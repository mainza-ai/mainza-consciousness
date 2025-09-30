#!/usr/bin/env python3
"""
Test Graph Visualization Improvements
=====================================

This script tests the enhanced graph visualization system to ensure:
1. Backend API endpoints return comprehensive relationship data
2. Frontend can properly display all connections
3. Graph visualization matches Neo4j browser functionality

Author: Mainza AI
Date: 2024
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any, List
from datetime import datetime

class GraphVisualizationTester:
    """Test the enhanced graph visualization system"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.test_results = []
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, endpoint: str, expected_fields: List[str]) -> Dict[str, Any]:
        """Test a specific graph endpoint"""
        print(f"🔍 Testing endpoint: {endpoint}")
        
        try:
            url = f"{self.base_url}{endpoint}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check response structure
                    has_status = data.get('status') == 'success'
                    has_graph = 'graph' in data
                    has_nodes = 'nodes' in data.get('graph', {})
                    has_relationships = 'relationships' in data.get('graph', {})
                    has_stats = 'stats' in data
                    
                    # Count data
                    node_count = len(data.get('graph', {}).get('nodes', []))
                    rel_count = len(data.get('graph', {}).get('relationships', []))
                    
                    # Check for enhanced fields
                    enhanced_fields = []
                    if node_count > 0:
                        sample_node = data['graph']['nodes'][0]
                        enhanced_fields = [
                            'importance' in sample_node,
                            'context' in sample_node,
                            'description' in sample_node,
                            'connections' in sample_node,
                            'out_degree' in sample_node,
                            'in_degree' in sample_node
                        ]
                    
                    if rel_count > 0:
                        sample_rel = data['graph']['relationships'][0]
                        enhanced_fields.extend([
                            'strength' in sample_rel,
                            'context' in sample_rel,
                            'source_labels' in sample_rel,
                            'target_labels' in sample_rel
                        ])
                    
                    result = {
                        'endpoint': endpoint,
                        'status': 'success',
                        'response_status': response.status,
                        'has_basic_structure': has_status and has_graph and has_nodes and has_relationships and has_stats,
                        'node_count': node_count,
                        'relationship_count': rel_count,
                        'enhanced_fields_present': all(enhanced_fields) if enhanced_fields else False,
                        'coverage_info': data.get('stats', {}).get('coverage_percentage', {}),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    print(f"✅ {endpoint}: {node_count} nodes, {rel_count} relationships")
                    if data.get('stats', {}).get('coverage_percentage'):
                        coverage = data['stats']['coverage_percentage']
                        print(f"   Coverage: {coverage.get('nodes', 0)}% nodes, {coverage.get('relationships', 0)}% relationships")
                    
                    return result
                    
                else:
                    result = {
                        'endpoint': endpoint,
                        'status': 'error',
                        'response_status': response.status,
                        'error': f"HTTP {response.status}",
                        'timestamp': datetime.now().isoformat()
                    }
                    print(f"❌ {endpoint}: HTTP {response.status}")
                    return result
                    
        except Exception as e:
            result = {
                'endpoint': endpoint,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ {endpoint}: {str(e)}")
            return result
    
    async def test_all_endpoints(self) -> List[Dict[str, Any]]:
        """Test all graph visualization endpoints"""
        print("🚀 Starting Graph Visualization Tests")
        print("=" * 50)
        
        endpoints = [
            '/api/insights/graph/full',
            '/api/insights/graph/comprehensive',
            '/api/insights/graph/complete'
        ]
        
        results = []
        for endpoint in endpoints:
            result = await self.test_endpoint(endpoint, [])
            results.append(result)
            self.test_results.append(result)
        
        return results
    
    async def test_relationship_quality(self) -> Dict[str, Any]:
        """Test the quality of relationship data"""
        print("\n🔗 Testing Relationship Quality")
        print("-" * 30)
        
        try:
            # Test comprehensive endpoint for relationship quality
            url = f"{self.base_url}/api/insights/graph/comprehensive"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    relationships = data.get('graph', {}).get('relationships', [])
                    
                    if not relationships:
                        return {
                            'status': 'warning',
                            'message': 'No relationships found',
                            'relationship_count': 0
                        }
                    
                    # Analyze relationship quality
                    relationship_types = {}
                    strength_scores = []
                    context_count = 0
                    
                    for rel in relationships:
                        # Count relationship types
                        rel_type = rel.get('type', 'Unknown')
                        relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
                        
                        # Collect strength scores
                        strength = rel.get('strength', 0)
                        if isinstance(strength, (int, float)):
                            strength_scores.append(strength)
                        
                        # Count relationships with context
                        if rel.get('context'):
                            context_count += 1
                    
                    avg_strength = sum(strength_scores) / len(strength_scores) if strength_scores else 0
                    context_percentage = (context_count / len(relationships)) * 100 if relationships else 0
                    
                    result = {
                        'status': 'success',
                        'total_relationships': len(relationships),
                        'unique_relationship_types': len(relationship_types),
                        'relationship_types': relationship_types,
                        'average_strength': round(avg_strength, 3),
                        'context_percentage': round(context_percentage, 1),
                        'quality_score': min(100, (len(relationship_types) * 10) + (context_percentage * 0.5))
                    }
                    
                    print(f"✅ Found {len(relationships)} relationships")
                    print(f"   Types: {len(relationship_types)} unique")
                    print(f"   Avg Strength: {avg_strength:.3f}")
                    print(f"   Context: {context_percentage:.1f}%")
                    print(f"   Quality Score: {result['quality_score']:.1f}/100")
                    
                    return result
                else:
                    return {
                        'status': 'error',
                        'message': f'HTTP {response.status}',
                        'relationship_count': 0
                    }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'relationship_count': 0
            }
    
    async def test_node_quality(self) -> Dict[str, Any]:
        """Test the quality of node data"""
        print("\n🔵 Testing Node Quality")
        print("-" * 25)
        
        try:
            # Test comprehensive endpoint for node quality
            url = f"{self.base_url}/api/insights/graph/comprehensive"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    nodes = data.get('graph', {}).get('nodes', [])
                    
                    if not nodes:
                        return {
                            'status': 'warning',
                            'message': 'No nodes found',
                            'node_count': 0
                        }
                    
                    # Analyze node quality
                    node_labels = {}
                    importance_scores = []
                    context_count = 0
                    connection_counts = []
                    
                    for node in nodes:
                        # Count node labels
                        labels = node.get('labels', [])
                        for label in labels:
                            node_labels[label] = node_labels.get(label, 0) + 1
                        
                        # Collect importance scores
                        importance = node.get('importance', 0)
                        if isinstance(importance, (int, float)):
                            importance_scores.append(importance)
                        
                        # Count nodes with context
                        if node.get('context'):
                            context_count += 1
                        
                        # Collect connection counts
                        connections = node.get('connections', 0)
                        if isinstance(connections, (int, float)):
                            connection_counts.append(connections)
                    
                    avg_importance = sum(importance_scores) / len(importance_scores) if importance_scores else 0
                    avg_connections = sum(connection_counts) / len(connection_counts) if connection_counts else 0
                    context_percentage = (context_count / len(nodes)) * 100 if nodes else 0
                    
                    result = {
                        'status': 'success',
                        'total_nodes': len(nodes),
                        'unique_labels': len(node_labels),
                        'node_labels': node_labels,
                        'average_importance': round(avg_importance, 3),
                        'average_connections': round(avg_connections, 1),
                        'context_percentage': round(context_percentage, 1),
                        'quality_score': min(100, (len(node_labels) * 5) + (context_percentage * 0.3) + (avg_connections * 2))
                    }
                    
                    print(f"✅ Found {len(nodes)} nodes")
                    print(f"   Labels: {len(node_labels)} unique")
                    print(f"   Avg Importance: {avg_importance:.3f}")
                    print(f"   Avg Connections: {avg_connections:.1f}")
                    print(f"   Context: {context_percentage:.1f}%")
                    print(f"   Quality Score: {result['quality_score']:.1f}/100")
                    
                    return result
                else:
                    return {
                        'status': 'error',
                        'message': f'HTTP {response.status}',
                        'node_count': 0
                    }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'node_count': 0
            }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive test report"""
        print("\n📊 Test Report Summary")
        print("=" * 30)
        
        successful_tests = [r for r in self.test_results if r.get('status') == 'success']
        failed_tests = [r for r in self.test_results if r.get('status') == 'error']
        
        total_nodes = sum(r.get('node_count', 0) for r in successful_tests)
        total_relationships = sum(r.get('relationship_count', 0) for r in successful_tests)
        
        report = {
            'test_summary': {
                'total_tests': len(self.test_results),
                'successful_tests': len(successful_tests),
                'failed_tests': len(failed_tests),
                'success_rate': (len(successful_tests) / len(self.test_results)) * 100 if self.test_results else 0
            },
            'data_summary': {
                'total_nodes_found': total_nodes,
                'total_relationships_found': total_relationships,
                'average_nodes_per_test': total_nodes / len(successful_tests) if successful_tests else 0,
                'average_relationships_per_test': total_relationships / len(successful_tests) if successful_tests else 0
            },
            'test_results': self.test_results,
            'recommendations': self.generate_recommendations()
        }
        
        print(f"✅ Successful Tests: {len(successful_tests)}/{len(self.test_results)}")
        print(f"📊 Total Nodes Found: {total_nodes}")
        print(f"🔗 Total Relationships Found: {total_relationships}")
        
        if failed_tests:
            print(f"❌ Failed Tests: {len(failed_tests)}")
            for test in failed_tests:
                print(f"   - {test['endpoint']}: {test.get('error', 'Unknown error')}")
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        successful_tests = [r for r in self.test_results if r.get('status') == 'success']
        
        if not successful_tests:
            recommendations.append("❌ All tests failed - check backend connectivity and API endpoints")
            return recommendations
        
        # Check for low relationship counts
        low_rel_tests = [r for r in successful_tests if r.get('relationship_count', 0) < 10]
        if low_rel_tests:
            recommendations.append("⚠️ Low relationship counts detected - consider using 'complete' endpoint for full data")
        
        # Check for missing enhanced fields
        missing_enhanced = [r for r in successful_tests if not r.get('enhanced_fields_present', False)]
        if missing_enhanced:
            recommendations.append("⚠️ Enhanced fields missing - ensure backend helper functions are implemented")
        
        # Check coverage percentages
        low_coverage = [r for r in successful_tests 
                       if r.get('coverage_info', {}).get('relationships', 100) < 50]
        if low_coverage:
            recommendations.append("⚠️ Low relationship coverage - use 'complete' endpoint for 100% coverage")
        
        if not recommendations:
            recommendations.append("✅ All tests passed - graph visualization should work correctly")
            recommendations.append("💡 Try switching between 'comprehensive' and 'complete' endpoints for different data levels")
        
        return recommendations

async def main():
    """Run the graph visualization tests"""
    print("🧪 Graph Visualization Improvement Tests")
    print("=" * 50)
    print(f"Testing backend at: http://localhost:8000")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    async with GraphVisualizationTester() as tester:
        # Test all endpoints
        await tester.test_all_endpoints()
        
        # Test relationship quality
        rel_quality = await tester.test_relationship_quality()
        
        # Test node quality
        node_quality = await tester.test_node_quality()
        
        # Generate report
        report = tester.generate_report()
        
        # Add quality tests to report
        report['quality_tests'] = {
            'relationship_quality': rel_quality,
            'node_quality': node_quality
        }
        
        print("\n🎯 Final Recommendations:")
        for rec in report['recommendations']:
            print(f"   {rec}")
        
        # Save report
        with open('graph_visualization_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: graph_visualization_test_report.json")
        
        return report

if __name__ == "__main__":
    try:
        report = asyncio.run(main())
        sys.exit(0 if report['test_summary']['success_rate'] > 80 else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)
