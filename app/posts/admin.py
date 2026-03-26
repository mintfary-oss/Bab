from django.contrib import admin
from .models import Comment,Like,Post,Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display=["name","slug"];prepopulated_fields={"slug":("name",)}
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display=["title","author","status","visibility","created_at"];list_filter=["status","visibility"];filter_horizontal=["tags","media_files"]
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display=["author","post","created_at"]
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display=["user","post","created_at"]
