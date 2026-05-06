from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "type", "title", "read_at", "created_at")
    list_filter = ("type", "read_at", "created_at")
    search_fields = ("title", "body", "recipient__username")
