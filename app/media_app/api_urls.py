from django.urls import path

from . import api_views

app_name = "media_api"
urlpatterns = [
    path("upload/", api_views.MediaUploadAPIView.as_view(), name="upload"),
    path("my/", api_views.MyMediaListAPIView.as_view(), name="my_list"),
    path("<int:pk>/delete/", api_views.MediaDeleteAPIView.as_view(), name="delete"),
]
