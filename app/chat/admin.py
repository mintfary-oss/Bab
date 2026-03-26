from django.contrib import admin

from .models import Chat, ChatMember, Friendship, Group, GroupMember, Message, Notification


@admin.register(Friendship)
class FA(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ["from_user", "to_user", "status", "created_at"]


class CMI(admin.TabularInline):  # type: ignore[type-arg]
    model = ChatMember
    extra = 0


@admin.register(Chat)
class CA(admin.ModelAdmin):  # type: ignore[type-arg]
    inlines = [CMI]
    list_display = ["pk", "name", "is_group", "created_at"]


@admin.register(Message)
class MA(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ["sender", "chat", "created_at"]


class GMI(admin.TabularInline):  # type: ignore[type-arg]
    model = GroupMember
    extra = 0


@admin.register(Group)
class GA(admin.ModelAdmin):  # type: ignore[type-arg]
    inlines = [GMI]
    list_display = ["title", "owner", "privacy", "members_count", "created_at"]


@admin.register(Notification)
class NA(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ["user", "notification_type", "title", "is_read", "created_at"]
