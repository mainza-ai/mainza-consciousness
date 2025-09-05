from pydantic_ai import RunContext
from backend.models.calendar_models import CalendarOutput

def create_event(ctx: RunContext, title: str, start: str, end: str, user_id: str = None) -> CalendarOutput:
    # Dummy: In production, store in DB or calendar service
    details = {"title": title, "start": start, "end": end, "user_id": user_id}
    return CalendarOutput(status="created", details=details)

def list_events(ctx: RunContext, user_id: str = None) -> CalendarOutput:
    # Dummy: In production, fetch from DB or calendar service
    events = [{"event_id": "1", "title": "Example Event", "start": "2024-07-01T10:00:00", "end": "2024-07-01T11:00:00", "user_id": user_id}]
    return CalendarOutput(status="ok", details=events)

def delete_event(ctx: RunContext, event_id: str) -> CalendarOutput:
    # Dummy: In production, delete from DB or calendar service
    details = {"event_id": event_id}
    return CalendarOutput(status="deleted", details=details) 