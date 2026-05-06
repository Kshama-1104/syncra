from django.db.models import Prefetch
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chat, ChatMember, Message
from .serializers import ChatSerializer, MessageSerializer
from .services import create_chat, create_message


class IsChatMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        chat = obj if isinstance(obj, Chat) else obj.chat
        return chat.memberships.filter(user=request.user).exists()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated, IsChatMember]
    search_fields = ["title", "messages__body"]
    ordering_fields = ["updated_at", "created_at"]

    def get_queryset(self):
        last_messages = Message.objects.order_by("-created_at")
        return (
            Chat.objects.filter(participants=self.request.user)
            .select_related("created_by")
            .prefetch_related("memberships__user", Prefetch("messages", queryset=last_messages, to_attr="prefetched_last_message"))
            .distinct()
        )

    def perform_create(self, serializer):
        participant_ids = self.request.data.get("participant_ids", [])
        chat = create_chat(
            creator=self.request.user,
            chat_type=serializer.validated_data["type"],
            title=serializer.validated_data.get("title", ""),
            participant_ids=participant_ids,
        )
        serializer.instance = chat

    @action(detail=True, methods=["post"])
    def messages(self, request, pk=None):
        chat = self.get_object()
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = create_message(chat=chat, sender=request.user, body=serializer.validated_data.get("body", ""))
        return Response(MessageSerializer(message).data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["chat"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Message.objects.filter(chat__participants=self.request.user).select_related("sender", "chat")
