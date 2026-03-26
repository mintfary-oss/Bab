from rest_framework import serializers

from .models import Comment, Post, Tag


class TagSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CommentSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta:
        model = Comment
        fields = ["id", "author", "body", "parent", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class PostSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    tags = TagSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "body",
            "visibility",
            "status",
            "tags",
            "pregnancy_week",
            "likes_count",
            "comments_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]
