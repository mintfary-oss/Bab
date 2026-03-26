from django.urls import path

from . import api_views

app_name = "posts_api"
urlpatterns = [
    path("", api_views.PostListCreateAPIView.as_view(), name="list_create"),
    path("<int:pk>/", api_views.PostDetailAPIView.as_view(), name="detail"),
    path("<int:post_id>/comments/", api_views.CommentListCreateAPIView.as_view(), name="comments"),
    path("<int:post_id>/like/", api_views.LikeToggleAPIView.as_view(), name="like"),
]
