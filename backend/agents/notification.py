from pydantic_ai import Agent
from backend.models.notification_models import NotificationOutput
from backend.tools.notification_tools import send_notification, list_notifications
from backend.agentic_config import local_llm

NOTIFICATION_PROMPT = "You are the NotificationAgent. You send reminders and alerts to the user. Use your tools to send or list notifications."

notification_agent = Agent[None, NotificationOutput](
    local_llm,
    system_prompt=NOTIFICATION_PROMPT,
    tools=[send_notification, list_notifications],
) 