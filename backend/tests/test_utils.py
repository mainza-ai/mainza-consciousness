import pytest
from backend.utils.embedding import get_embedding, vector_search_chunks
from backend.utils.neo4j import driver

def test_get_embedding_returns_vector():
    vec = get_embedding("test")
    assert isinstance(vec, list)
    assert len(vec) > 0

def test_vector_search_chunks_runs():
    # Should not raise, even if Neo4j is empty
    result = vector_search_chunks("test", top_k=1)
    assert isinstance(result, list)

def test_neo4j_driver_connects():
    session = driver.session()
    assert session is not None
    session.close() 