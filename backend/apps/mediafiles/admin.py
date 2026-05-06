from django.contrib import admin

from .models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "content_type", "size", "created_at")
    list_filter = ("content_type", "created_at")
    search_fields = ("owner__username",)
