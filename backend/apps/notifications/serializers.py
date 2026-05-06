from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "recipient", "actor", "type", "title", "body", "data", "read_at", "created_at")
        read_only_fields = ("recipient",)
