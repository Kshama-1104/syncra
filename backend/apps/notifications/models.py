from django.conf import settings
from django.db import models


class Notification(models.Model):
    MESSAGE = "message"
    INVITE = "invite"
    SYSTEM = "system"
    TYPES = [(MESSAGE, "Message"), (INVITE, "Invite"), (SYSTEM, "System")]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=24, choices=TYPES)
    title = models.CharField(max_length=160)
    body = models.CharField(max_length=500, blank=True)
    data = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["recipient", "read_at", "-created_at"])]
