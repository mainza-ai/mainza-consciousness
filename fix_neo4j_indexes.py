#!/usr/bin/env python3
"""
Neo4j Index Fix Script
Recreates the missing vector and full-text indexes for the memory system
"""
import os
import sys
import logging

# Add the backend directory to the path
sys.path.append('backend')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to fix Neo4j indexes"""
    print('🔧 Starting Neo4j index recreation...')

    # Set environment variables if not already set
    os.environ.setdefault('NEO4J_URI', 'bolt://neo4j:7687')
    os.environ.setdefault('NEO4J_USER', 'neo4j')
    os.environ.setdefault('NEO4J_PASSWORD', 'mainza123')

    print(f'NEO4J_URI: {os.environ.get("NEO4J_URI")}')
    print(f'NEO4J_USER: {os.environ.get("NEO4J_USER")}')
    print(f'NEO4J_PASSWORD: {"***" if os.environ.get("NEO4J_PASSWORD") else "NOT SET"}')

    try:
        from backend.utils.neo4j_production import neo4j_production
        print('✅ Neo4j production manager loaded successfully')

        # Check for existing failed indexes and drop them
        result = neo4j_production.execute_query('SHOW INDEXES')
        failed_indexes = [idx['name'] for idx in result if idx.get('state') == 'FAILED']

        if failed_indexes:
            print(f'📋 Found {len(failed_indexes)} failed indexes: {failed_indexes}')
            for idx in failed_indexes:
                try:
                    neo4j_production.execute_write_query(f'DROP INDEX {idx} IF EXISTS')
                    print(f'🗑️ Dropped failed index: {idx}')
                except Exception as e:
                    print(f'❌ Failed to drop index {idx}: {e}')
        else:
            print('✅ No failed indexes found')

        # Create the memory_embedding_index
        try:
            neo4j_production.execute_write_query('''
                CREATE VECTOR INDEX memory_embedding_index IF NOT EXISTS
                FOR (m:Memory) ON (m.embedding)
                OPTIONS {
                    indexConfig: {
                        `vector.dimensions`: 768,
                        `vector.similarity_function`: 'cosine'
                    }
                }
            ''')
            print('✅ Created memory_embedding_index successfully')
        except Exception as e:
            print(f'❌ Failed to create memory_embedding_index: {e}')

        # Create the memory_content_fulltext index
        try:
            neo4j_production.execute_write_query('''
                CREATE FULLTEXT INDEX memory_content_fulltext IF NOT EXISTS
                FOR (m:Memory) ON EACH [m.content]
            ''')
            print('✅ Created memory_content_fulltext successfully')
        except Exception as e:
            print(f'❌ Failed to create memory_content_fulltext: {e}')

        print('✅ Index recreation completed successfully!')

    except Exception as e:
        print(f'❌ Index recreation failed: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
