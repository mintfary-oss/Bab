from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile
User=get_user_model()
class ProfileSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    class Meta:
        model=Profile;fields=["bio","location","phone","social_links"]
class UserSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model=User;fields=["id","username","email","first_name","last_name","avatar","birth_date","expected_due_date","privacy","created_at","profile"]
        read_only_fields=["id","email","created_at"]
class RegisterSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    password=serializers.CharField(write_only=True,min_length=8)
    password_confirm=serializers.CharField(write_only=True)
    class Meta:
        model=User;fields=["username","email","password","password_confirm","expected_due_date"]
    def validate(self,attrs):  # type: ignore[override]
        if attrs["password"]!=attrs.pop("password_confirm"): raise serializers.ValidationError({"password_confirm":"Пароли не совпадают."})
        return attrs
    def create(self,validated_data):
        pw=validated_data.pop("password");u=User(**validated_data);u.set_password(pw);u.save();Profile.objects.create(user=u);return u
