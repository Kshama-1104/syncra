import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone

from apps.chats.models import Chat, Message, ReadReceipt
from apps.presence.models import UserPresence


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        if not self.user.is_authenticated or not await self.is_member():
            await self.close(code=4401)
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.set_presence(True)
        await self.accept()
        await self.channel_layer.group_send(self.room_group_name, {"type": "presence.event", "user_id": self.user.id, "online": True})

    async def disconnect(self, close_code):
        if getattr(self, "user", None) and self.user.is_authenticated:
            await self.set_presence(False)
            await self.channel_layer.group_send(self.room_group_name, {"type": "presence.event", "user_id": self.user.id, "online": False})
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        event = content.get("type")
        if event == "message.send":
            message = await self.persist_message(content.get("body", ""))
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", "message_id": message["id"], "body": message["body"], "sender_id": self.user.id},
            )
        elif event == "typing":
            await self.channel_layer.group_send(self.room_group_name, {"type": "typing.event", "user_id": self.user.id, "is_typing": bool(content.get("is_typing"))})
        elif event == "message.read":
            await self.mark_read(content.get("message_id"))
            await self.channel_layer.group_send(self.room_group_name, {"type": "read.event", "message_id": content.get("message_id"), "user_id": self.user.id})

    async def chat_message(self, event):
        await self.send_json({"type": "message.created", **event})

    async def typing_event(self, event):
        if event["user_id"] != self.user.id:
            await self.send_json({"type": "typing", **event})

    async def read_event(self, event):
        await self.send_json({"type": "message.read", **event})

    async def presence_event(self, event):
        await self.send_json({"type": "presence", **event})

    @database_sync_to_async
    def is_member(self):
        return Chat.objects.filter(id=self.chat_id, participants=self.user).exists()

    @database_sync_to_async
    def persist_message(self, body):
        message = Message.objects.create(chat_id=self.chat_id, sender=self.user, body=body)
        return {"id": message.id, "body": message.body}

    @database_sync_to_async
    def mark_read(self, message_id):
        if message_id:
            ReadReceipt.objects.get_or_create(message_id=message_id, user=self.user)

    @database_sync_to_async
    def set_presence(self, online):
        UserPresence.objects.update_or_create(user=self.user, defaults={"is_online": online, "last_seen": timezone.now()})
