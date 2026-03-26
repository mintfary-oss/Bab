from rest_framework import serializers
from .models import Chat,Friendship,Group,Message,Notification
class FriendshipSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta: model=Friendship;fields=["id","from_user","to_user","status","created_at"]
class MessageSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta: model=Message;fields=["id","chat","sender","body","media","created_at"];read_only_fields=["id","sender","created_at"]
class ChatSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta: model=Chat;fields=["id","name","is_group","owner","created_at"]
class GroupSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    members_count=serializers.ReadOnlyField()
    class Meta: model=Group;fields=["id","title","description","privacy","owner","members_count","created_at"]
class NotificationSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta: model=Notification;fields=["id","notification_type","title","message","is_read","created_at"]
