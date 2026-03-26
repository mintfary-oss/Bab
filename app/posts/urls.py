from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("create/", views.post_create_view, name="create"),
    path("<int:post_id>/", views.post_detail_view, name="detail"),
    path("<int:post_id>/edit/", views.post_edit_view, name="edit"),
    path("<int:post_id>/delete/", views.post_delete_view, name="delete"),
    path("<int:post_id>/comment/", views.comment_create_view, name="comment"),
    path("<int:post_id>/like/", views.like_toggle_view, name="like"),
    path("my/", views.my_posts_view, name="my_posts"),
]
