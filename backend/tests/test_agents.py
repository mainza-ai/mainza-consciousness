from backend.agents.graphmaster import graphmaster_agent
from backend.agents.taskmaster import taskmaster_agent
from backend.agents.codeweaver import codeweaver_agent
from backend.agents.rag import rag_agent
from backend.agents.notification import notification_agent
from backend.agents.calendar import calendar_agent
from backend.agents.conductor import conductor_agent
from backend.agents.router import router_agent

def test_graphmaster_agent_tools():
    assert hasattr(graphmaster_agent, 'tools')
    assert len(graphmaster_agent.tools) > 0

def test_taskmaster_agent_tools():
    assert hasattr(taskmaster_agent, 'tools')
    assert len(taskmaster_agent.tools) > 0

def test_codeweaver_agent_tools():
    assert hasattr(codeweaver_agent, 'tools')
    assert len(codeweaver_agent.tools) > 0

def test_rag_agent_tools():
    assert hasattr(rag_agent, 'tools')
    assert len(rag_agent.tools) > 0

def test_notification_agent_tools():
    assert hasattr(notification_agent, 'tools')
    assert len(notification_agent.tools) > 0

def test_calendar_agent_tools():
    assert hasattr(calendar_agent, 'tools')
    assert len(calendar_agent.tools) > 0

def test_conductor_agent_tools():
    assert hasattr(conductor_agent, 'tools')
    assert len(conductor_agent.tools) > 0

def test_router_agent_tools():
    assert hasattr(router_agent, 'tools')
    assert len(router_agent.tools) > 0 