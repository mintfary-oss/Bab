from django.db.models import Q
from rest_framework import generics,permissions,status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Chat,ChatMember,Friendship,Group,Message,Notification
from .serializers import ChatSerializer,FriendshipSerializer,GroupSerializer,MessageSerializer,NotificationSerializer
class FriendListAPIView(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class=FriendshipSerializer
    def get_queryset(self):  # type: ignore[override]
        return Friendship.objects.filter(Q(from_user=self.request.user)|Q(to_user=self.request.user),status=Friendship.Status.ACCEPTED)
class FriendRequestAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request:Request)->Response:
        tid=request.data.get("to_user_id")  # type: ignore[union-attr]
        if not tid: return Response({"error":"to_user_id required"},status=status.HTTP_400_BAD_REQUEST)
        f,c=Friendship.objects.get_or_create(from_user=request.user,to_user_id=tid)
        return Response(FriendshipSerializer(f).data,status=status.HTTP_201_CREATED if c else status.HTTP_200_OK)
class ChatListAPIView(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class=ChatSerializer
    def get_queryset(self):  # type: ignore[override]
        return Chat.objects.filter(pk__in=ChatMember.objects.filter(user=self.request.user).values_list("chat_id",flat=True))
class MessageListCreateAPIView(generics.ListCreateAPIView):  # type: ignore[type-arg]
    serializer_class=MessageSerializer
    def get_queryset(self):  # type: ignore[override]
        return Message.objects.filter(chat_id=self.kwargs["chat_id"])
    def perform_create(self,s): s.save(sender=self.request.user,chat_id=self.kwargs["chat_id"])
class GroupListAPIView(generics.ListCreateAPIView):  # type: ignore[type-arg]
    serializer_class=GroupSerializer
    def get_queryset(self):  # type: ignore[override]
        return Group.objects.filter(privacy=Group.Privacy.PUBLIC)
    def perform_create(self,s): s.save(owner=self.request.user)
class NotificationListAPIView(generics.ListAPIView):  # type: ignore[type-arg]
    serializer_class=NotificationSerializer
    def get_queryset(self):  # type: ignore[override]
        return Notification.objects.filter(user=self.request.user)
