from django.urls import path
from . import api_views
app_name="chat_api"
urlpatterns=[path("",api_views.ChatListAPIView.as_view(),name="list"),path("<int:chat_id>/messages/",api_views.MessageListCreateAPIView.as_view(),name="messages"),path("friends/",api_views.FriendListAPIView.as_view(),name="friends"),path("friends/request/",api_views.FriendRequestAPIView.as_view(),name="friend_request"),path("groups/",api_views.GroupListAPIView.as_view(),name="groups"),path("notifications/",api_views.NotificationListAPIView.as_view(),name="notifications")]
