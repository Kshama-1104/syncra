from django.contrib import admin

from .models import Chat, ChatMember, Message, ReadReceipt


class ChatMemberInline(admin.TabularInline):
    model = ChatMember
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "title", "created_by", "updated_at")
    list_filter = ("type",)
    search_fields = ("title",)
    inlines = [ChatMemberInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("body", "sender__username")


@admin.register(ReadReceipt)
class ReadReceiptAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "user", "read_at")
