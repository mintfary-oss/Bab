from rest_framework import serializers

from .models import Hospital, HospitalReview


class HospitalSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta:
        model = Hospital
        fields = [
            "id",
            "name",
            "region",
            "city",
            "address",
            "phone",
            "email",
            "website",
            "hospital_type",
            "description",
            "rating_avg",
            "reviews_count",
        ]


class HospitalReviewSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta:
        model = HospitalReview
        fields = ["id", "author", "rating", "body", "is_recommended", "visited", "created_at"]
        read_only_fields = ["id", "author", "created_at"]
