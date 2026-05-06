from django.conf import settings
from django.db import models


class UserPresence(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="presence")
    is_online = models.BooleanField(default=False, db_index=True)
    last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    active_chat_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_id}:{self.is_online}"


class TypingStatus(models.Model):
    chat_id = models.BigIntegerField(db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_typing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["chat_id", "user"], name="unique_typing_status")]
