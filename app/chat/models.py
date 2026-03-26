from django.conf import settings
from django.db import models
from django.utils import timezone


class Friendship(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        ACCEPTED = "accepted", "Принята"
        BLOCKED = "blocked", "Заблокирован"

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friendships_sent"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friendships_received"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("from_user", "to_user")]
        ordering = ["-created_at"]


class Chat(models.Model):
    name = models.CharField(max_length=200, blank=True, default="")
    is_group = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_chats",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or f"Чат #{self.pk}"


class ChatMember(models.Model):
    class Role(models.TextChoices):
        MEMBER = "member", "Участник"
        ADMIN = "admin", "Админ"

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("chat", "user")]


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    body = models.TextField(max_length=5000, blank=True, default="")
    media = models.ForeignKey(
        "media_app.MediaFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]


class Group(models.Model):
    class Privacy(models.TextChoices):
        PUBLIC = "public", "Публичная"
        PRIVATE = "private", "Приватная"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_groups"
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")
    privacy = models.CharField(max_length=10, choices=Privacy.choices, default=Privacy.PUBLIC)
    avatar = models.ImageField(upload_to="images/groups/%Y/%m/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def members_count(self):
        return self.group_members.count()  # type: ignore[attr-defined]


class GroupMember(models.Model):
    class Role(models.TextChoices):
        MEMBER = "member", "Участник"
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Админ"

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_members")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_memberships"
    )
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("group", "user")]


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        FRIEND_REQUEST = "friend_request", "Запрос в друзья"
        NEW_MESSAGE = "new_message", "Сообщение"
        NEW_COMMENT = "new_comment", "Комментарий"
        NEW_LIKE = "new_like", "Лайк"
        GROUP_INVITE = "group_invite", "Приглашение"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=300)
    message = models.TextField(max_length=1000, blank=True, default="")
    payload = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.title}"  # type: ignore[attr-defined]
