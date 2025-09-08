import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_graphmaster_query_endpoint():
    response = client.post("/agent/graphmaster/query", json={"query": "MATCH (n) RETURN n LIMIT 1"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "result" in response.json()

def test_taskmaster_task_endpoint():
    response = client.post("/agent/taskmaster/task", json={"task_command": "create a test task", "user_id": "test_user"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "status" in response.json()

def test_codeweaver_run_endpoint():
    response = client.post("/agent/codeweaver/run", json={"command": "print('hello')"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "result" in response.json()

def test_rag_query_endpoint():
    response = client.post("/agent/rag/query", json={"query": "What is Bayesian inference?"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "answer" in response.json()

def test_notification_send_endpoint():
    response = client.post("/agent/notification/send", json={"message": "Test notification"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "status" in response.json()

def test_calendar_action_endpoint():
    response = client.post("/agent/calendar/action", json={"action": "list_events"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "status" in response.json()

def test_conductor_query_endpoint():
    response = client.post("/agent/conductor/query", json={"request": "Summarize recent activity", "user_id": "test_user"})
    assert response.status_code == 200
    data = response.json()
    assert "final_summary" in data or "reason" in data

def test_build_info_endpoint():
    response = client.get("/build/info")
    assert response.status_code == 200
    data = response.json()
    assert "build_date" in data
    assert "git_commit" in data
    assert "cache_bust" in data
    assert "status" in data

def test_build_health_endpoint():
    response = client.get("/build/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_router_agent_routing():
    # This test assumes router agent is available and cloud LLM is enabled
    response = client.post("/agent/graphmaster/query", json={"query": "What tasks are open?"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "result" in response.json() 