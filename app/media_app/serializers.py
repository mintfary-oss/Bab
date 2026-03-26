from rest_framework import serializers

from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    file_size_mb = serializers.ReadOnlyField()

    class Meta:
        model = MediaFile
        fields = [
            "id",
            "file",
            "thumbnail",
            "media_type",
            "original_name",
            "mime_type",
            "file_size",
            "file_size_mb",
            "width",
            "height",
            "created_at",
        ]


class MediaUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    media_type = serializers.ChoiceField(
        choices=MediaFile.MediaType.choices, default=MediaFile.MediaType.IMAGE
    )
