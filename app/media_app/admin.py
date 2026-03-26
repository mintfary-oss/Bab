from django.contrib import admin
from .models import MediaFile
@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display=["id","original_name","media_type","owner","file_size_mb","created_at"]
    list_filter=["media_type"]
