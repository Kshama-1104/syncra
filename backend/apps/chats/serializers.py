from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from .models import Chat, ChatMember, Message, ReadReceipt


class ChatMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ChatMember
        fields = ("id", "user", "role", "joined_at", "muted_until")


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ("id", "chat", "sender", "body", "status", "reply_to", "created_at", "edited_at", "deleted_at")
        read_only_fields = ("sender", "status")


class ChatSerializer(serializers.ModelSerializer):
    memberships = ChatMemberSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ("id", "type", "title", "created_by", "memberships", "last_message", "created_at", "updated_at")
        read_only_fields = ("created_by",)

    def get_last_message(self, obj):
        message = getattr(obj, "prefetched_last_message", None)
        if message:
            return MessageSerializer(message[0]).data
        last = obj.messages.order_by("-created_at").first()
        return MessageSerializer(last).data if last else None


class ReadReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadReceipt
        fields = ("id", "message", "user", "read_at")
