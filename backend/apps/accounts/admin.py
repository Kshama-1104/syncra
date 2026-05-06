from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User


@admin.register(User)
class SyncraUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "is_email_verified", "is_active", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("is_email_verified", "is_active", "is_staff")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "display_name", "timezone", "updated_at")
    search_fields = ("user__username", "user__email", "display_name")
