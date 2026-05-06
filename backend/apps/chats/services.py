from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Chat, ChatMember, Message


def create_chat(*, creator, chat_type, participant_ids, title=""):
    chat = Chat.objects.create(type=chat_type, title=title, created_by=creator)
    member_ids = set(participant_ids) | {creator.id}
    ChatMember.objects.bulk_create([ChatMember(chat=chat, user_id=user_id) for user_id in member_ids], ignore_conflicts=True)
    return chat


def create_message(*, chat, sender, body):
    message = Message.objects.create(chat=chat, sender=sender, body=body)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{chat.id}",
        {"type": "chat.message", "message_id": message.id, "body": message.body, "sender_id": sender.id},
    )
    return message
