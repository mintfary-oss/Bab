from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField("Аватар", upload_to="images/avatars/%Y/%m/", blank=True, null=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    expected_due_date = models.DateField("ПДР", blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class PrivacyChoice(models.TextChoices):
        PUBLIC = "public", "Публичный"
        FRIENDS = "friends", "Друзья"
        PRIVATE = "private", "Приватный"

    privacy = models.CharField(
        max_length=10, choices=PrivacyChoice.choices, default=PrivacyChoice.PUBLIC
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_full_name() or self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=1000, blank=True, default="")
    location = models.CharField(max_length=200, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    social_links = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль: {self.user}"
