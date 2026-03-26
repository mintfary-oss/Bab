from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):  # type: ignore[type-arg]
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CurrentUserAPIView(generics.RetrieveUpdateAPIView):  # type: ignore[type-arg]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserDetailAPIView(generics.RetrieveAPIView):  # type: ignore[type-arg]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileUpdateAPIView(generics.UpdateAPIView):  # type: ignore[type-arg]
    serializer_class = ProfileSerializer

    def get_object(self):
        p, _ = Profile.objects.get_or_create(user_id=self.kwargs["pk"])
        return p
