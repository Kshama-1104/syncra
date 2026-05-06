from config.celery import app
from .models import Notification


@app.task
def create_notification(recipient_id, title, body="", actor_id=None, type="system", data=None):
    Notification.objects.create(
        recipient_id=recipient_id,
        actor_id=actor_id,
        type=type,
        title=title,
        body=body,
        data=data or {},
    )
