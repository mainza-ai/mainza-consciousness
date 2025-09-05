from pydantic_ai import RunContext
from backend.models.notification_models import NotificationOutput

def send_notification(ctx: RunContext, message: str, user_id: str = None) -> NotificationOutput:
    # Dummy: In production, integrate with real notification system
    details = {"message": message, "user_id": user_id}
    return NotificationOutput(status="sent", details=details)

def list_notifications(ctx: RunContext, user_id: str = None) -> NotificationOutput:
    # Dummy: In production, fetch from DB or notification service
    notifications = [{"message": "Example notification", "user_id": user_id}]
    return NotificationOutput(status="ok", details=notifications) 