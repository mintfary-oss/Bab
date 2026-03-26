import os
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


def media_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    td = {"image": "images", "video": "videos", "gif": "images", "doc": "documents"}.get(
        instance.media_type, "other"
    )
    return f"{td}/{timezone.now().strftime('%Y/%m')}/{uuid.uuid4().hex}{ext}"


class MediaFile(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Изображение"
        VIDEO = "video", "Видео"
        GIF = "gif", "GIF"
        DOCUMENT = "doc", "Документ"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_files"
    )
    file = models.FileField(upload_to=media_upload_path)
    thumbnail = models.ImageField(upload_to="thumbnails/%Y/%m/", blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.IMAGE)
    original_name = models.CharField(max_length=255, default="")
    mime_type = models.CharField(max_length=100, default="")
    file_size = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Медиа-файл"
        verbose_name_plural = "Медиа-файлы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.media_type}: {self.original_name}"

    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)
