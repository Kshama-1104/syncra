from django.contrib import admin

from .models import TypingStatus, UserPresence


@admin.register(UserPresence)
class UserPresenceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_online", "last_seen", "active_chat_id")
    list_filter = ("is_online",)


@admin.register(TypingStatus)
class TypingStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_id", "user", "is_typing", "updated_at")
