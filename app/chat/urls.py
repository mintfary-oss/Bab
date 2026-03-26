from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("friends/", views.friends_list_view, name="friends"),
    path("friends/request/<int:user_id>/", views.friend_request_view, name="friend_request"),
    path("friends/accept/<int:friendship_id>/", views.friend_accept_view, name="friend_accept"),
    path("friends/reject/<int:friendship_id>/", views.friend_reject_view, name="friend_reject"),
    path("", views.chat_list_view, name="list"),
    path("<int:chat_id>/", views.chat_detail_view, name="detail"),
    path("<int:chat_id>/send/", views.send_message_view, name="send"),
    path("start/<int:user_id>/", views.start_chat_view, name="start"),
    path("groups/", views.group_list_view, name="groups"),
    path("groups/create/", views.group_create_view, name="group_create"),
    path("groups/<int:group_id>/", views.group_detail_view, name="group_detail"),
    path("groups/<int:group_id>/join/", views.group_join_view, name="group_join"),
    path("groups/<int:group_id>/leave/", views.group_leave_view, name="group_leave"),
    path("notifications/", views.notifications_view, name="notifications"),
    path(
        "notifications/<int:notification_id>/read/",
        views.notification_read_view,
        name="notification_read",
    ),
    path(
        "notifications/read-all/", views.notifications_read_all_view, name="notifications_read_all"
    ),
]
