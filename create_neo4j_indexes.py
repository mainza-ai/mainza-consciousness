#!/usr/bin/env python3
"""
Create Missing Neo4j Indexes - Direct Backend Connection
"""
import sys
import os
sys.path.insert(0, '/app')

# Set environment variables for Neo4j connection
os.environ['NEO4J_URI'] = 'bolt://mainza-neo4j:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'mainza123'

try:
    from neo4j import GraphDatabase, basic_auth
    
    # Create driver
    driver = GraphDatabase.driver(
        os.environ['NEO4J_URI'], 
        auth=basic_auth(os.environ['NEO4J_USER'], os.environ['NEO4J_PASSWORD'])
    )
    
    with driver.session() as session:
        # Create vector index
        try:
            result = session.run("""
                CREATE VECTOR INDEX memory_embedding_index IF NOT EXISTS
                FOR (m:Memory) ON (m.embedding)
                OPTIONS {
                    indexConfig: {
                        `vector.dimensions`: 768,
                        `vector.similarity_function`: 'cosine'
                    }
                }
            """)
            print("✅ memory_embedding_index created/promoted")
        except Exception as e:
            print(f"⚠️  memory_embedding_index creation: {e}")
        
        # Create full-text index
        try:
            session.run("""
                CREATE FULLTEXT INDEX memory_content_fulltext IF NOT EXISTS
                FOR (m:Memory) ON EACH [m.content]
            """)
            print("✅ memory_content_fulltext created/promoted")
        except Exception as e:
            print(f"⚠️  memory_content_fulltext creation: {e}")
        
        # Verify indexes
        try:
            indexes = session.run("SHOW INDEXES")
            index_names = [idx['name'] for idx in indexes if 'memory' in idx.get('name', '').lower()]
            print(f"✅ Verified indexes: {index_names}")
        except Exception as e:
            print(f"⚠️  Index verification failed: {e}")
    
    driver.close()
    print("✅ Neo4j indexes creation process completed")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Neo4j index creation failed: {e}")
    sys.exit(1)
