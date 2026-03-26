from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, User


class ProfileInline(admin.StackedInline):  # type: ignore[type-arg]
    model = Profile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):  # type: ignore[type-arg]
    inlines = [ProfileInline]
    list_display = [
        "email",
        "username",
        "first_name",
        "expected_due_date",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["email", "username"]
    fieldsets = BaseUserAdmin.fieldsets + (("Дополнительно", {"fields": ("avatar", "birth_date", "expected_due_date", "privacy", "is_email_verified")}),)  # type: ignore[operator]
