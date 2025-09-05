from pydantic_ai import Agent
from backend.models.calendar_models import CalendarOutput
from backend.tools.calendar_tools import create_event, list_events, delete_event
from backend.agentic_config import local_llm

CALENDAR_PROMPT = "You are the CalendarAgent. You manage events, meetings, and reminders for the user. Use your tools to create, list, or delete calendar events."

tools = [create_event, list_events, delete_event]

calendar_agent = Agent[None, CalendarOutput](
    local_llm,
    system_prompt=CALENDAR_PROMPT,
    tools=[create_event, list_events, delete_event],
) 