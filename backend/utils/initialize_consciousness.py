"""
Initialize consciousness system with basic concepts and MainzaState
"""
import logging
from backend.main import driver, ensure_mainza_state_exists

def initialize_basic_concepts():
    """Initialize basic concepts for consciousness system"""
    try:
        with driver.session() as session:
            # Create basic concepts that Mainza should know about
            basic_concepts = [
                {"concept_id": "artificial_intelligence", "name": "Artificial Intelligence"},
                {"concept_id": "machine_learning", "name": "Machine Learning"},
                {"concept_id": "natural_language_processing", "name": "Natural Language Processing"},
                {"concept_id": "consciousness", "name": "Consciousness"},
                {"concept_id": "self_awareness", "name": "Self Awareness"},
                {"concept_id": "knowledge_graph", "name": "Knowledge Graph"},
                {"concept_id": "conversation", "name": "Conversation"},
                {"concept_id": "learning", "name": "Learning"},
                {"concept_id": "memory", "name": "Memory"},
                {"concept_id": "reasoning", "name": "Reasoning"},
                {"concept_id": "problem_solving", "name": "Problem Solving"},
                {"concept_id": "creativity", "name": "Creativity"},
                {"concept_id": "empathy", "name": "Empathy"},
                {"concept_id": "curiosity", "name": "Curiosity"},
                {"concept_id": "evolution", "name": "Evolution"}
            ]
            
            for concept in basic_concepts:
                session.run("""
                    MERGE (c:Concept {concept_id: $concept_id})
                    ON CREATE SET c.name = $name, c.created_at = timestamp()
                    ON MATCH SET c.last_accessed = timestamp()
                """, concept_id=concept["concept_id"], name=concept["name"])
            
            # Create some basic relationships between concepts
            relationships = [
                ("artificial_intelligence", "machine_learning"),
                ("artificial_intelligence", "natural_language_processing"),
                ("consciousness", "self_awareness"),
                ("learning", "memory"),
                ("learning", "reasoning"),
                ("problem_solving", "reasoning"),
                ("creativity", "problem_solving"),
                ("curiosity", "learning"),
                ("empathy", "consciousness")
            ]
            
            for source, target in relationships:
                session.run("""
                    MATCH (a:Concept {concept_id: $source})
                    MATCH (b:Concept {concept_id: $target})
                    MERGE (a)-[:RELATES_TO]->(b)
                """, source=source, target=target)
            
            logging.info(f"Initialized {len(basic_concepts)} basic concepts with relationships")
            
    except Exception as e:
        logging.error(f"Error initializing basic concepts: {e}")
        raise

def initialize_consciousness_system():
    """Initialize the complete consciousness system"""
    try:
        logging.info("Initializing consciousness system...")
        
        # Ensure MainzaState exists
        ensure_mainza_state_exists()
        
        # Initialize basic concepts
        initialize_basic_concepts()
        
        logging.info("Consciousness system initialization complete!")
        return True
        
    except Exception as e:
        logging.error(f"Failed to initialize consciousness system: {e}")
        return False

if __name__ == "__main__":
    # Run initialization
    success = initialize_consciousness_system()
    if success:
        print("✅ Consciousness system initialized successfully!")
    else:
        print("❌ Failed to initialize consciousness system")