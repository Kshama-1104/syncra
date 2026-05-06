from django.conf import settings
from django.db import models


class Chat(models.Model):
    DIRECT = "direct"
    GROUP = "group"
    CHAT_TYPES = [(DIRECT, "Direct"), (GROUP, "Group")]

    type = models.CharField(max_length=16, choices=CHAT_TYPES)
    title = models.CharField(max_length=160, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_chats")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ChatMember", related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["type", "-updated_at"])]

    def __str__(self):
        return self.title or f"{self.type}:{self.pk}"


class ChatMember(models.Model):
    MEMBER = "member"
    ADMIN = "admin"
    ROLES = [(MEMBER, "Member"), (ADMIN, "Admin")]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_memberships")
    role = models.CharField(max_length=16, choices=ROLES, default=MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)
    muted_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["chat", "user"], name="unique_chat_member")]
        indexes = [models.Index(fields=["user", "chat"])]


class Message(models.Model):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    STATUS_CHOICES = [(SENT, "Sent"), (DELIVERED, "Delivered"), (READ, "Read")]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=SENT)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["chat", "-created_at"]),
            models.Index(fields=["sender", "-created_at"]),
        ]


class ReadReceipt(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="read_receipts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="read_receipts")
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["message", "user"], name="unique_message_reader")]
